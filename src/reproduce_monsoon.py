"""Audit the preserved ERA5 NetCDF4/HDF5 snapshot; never overwrite source data."""
from pathlib import Path
import argparse, hashlib, json, platform, importlib.metadata
import h5py
import numpy as np
import pandas as pd
from scipy.stats import linregress
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

YEARS=list(range(2016,2026))
def text_attr(value):
    return value.decode() if isinstance(value,bytes) else str(value)

def read_inputs(folder):
    frames=[];manifest=[];grid=None
    for year in YEARS:
        name=f'multan_{year}.nc' if year!=2022 else 'multan_2022_full.nc'
        path=folder/name
        with h5py.File(path,'r') as f:
            assert text_attr(f['valid_time'].attrs['units'])=='seconds since 1970-01-01'
            assert text_attr(f['valid_time'].attrs['calendar'])=='proleptic_gregorian'
            assert text_attr(f['tp'].attrs['units'])=='m'
            assert text_attr(f['tp'].attrs['GRIB_stepType'])=='accum'
            assert text_attr(f['t2m'].attrs['units'])=='K'
            assert text_attr(f['t2m'].attrs['GRIB_stepType'])=='instant'
            for var in ['tp','t2m']:
                assert 'scale_factor' not in f[var].attrs and 'add_offset' not in f[var].attrs
            lat=f['latitude'][:];lon=f['longitude'][:]
            if grid is None:grid=(lat,lon)
            else:assert np.array_equal(lat,grid[0]) and np.array_equal(lon,grid[1])
            time=pd.DatetimeIndex(pd.to_datetime(f['valid_time'][:],unit='s'))
            start=f'{year}-01-01' if year==2022 else f'{year}-06-01'
            end=f'{year}-12-31 23:00' if year==2022 else f'{year}-09-30 23:00'
            assert time.equals(pd.date_range(start,end,freq='h')),f'{name}: timestamps incomplete'
            tp=f['tp'][:];t2m=f['t2m'][:]
            assert tp.shape==t2m.shape==(len(time),3,3)
            assert np.isfinite(tp).all() and np.isfinite(t2m).all()
            assert tp.min()>=0 and (t2m>150).all() and (t2m<350).all()
            # Match historical float32 reduction before independent aggregation.
            rain=tp.mean(axis=(1,2))*1000;temp=t2m.mean(axis=(1,2))-273.15
            frames.append(pd.DataFrame({'utc':time,'precip_mm':rain,'temp_c':temp}))
            manifest.append(dict(file=name,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),bytes=path.stat().st_size,hours=len(time),first_utc=str(time[0]),last_utc=str(time[-1]),latitude=lat.tolist(),longitude=lon.tolist(),missing_tp=0,missing_t2m=0,tp_units='m',t2m_units='K',expver=np.unique(f['expver'][:]).astype(str).tolist()))
    hourly=pd.concat(frames,ignore_index=True).sort_values('utc')
    assert not hourly.utc.duplicated().any()
    return hourly,manifest

def aggregate_days(hourly,offset_hours=5,interval_corrected=True):
    """Rain belongs to [end-1h,end); instantaneous temperature keeps its timestamp."""
    end=hourly.utc+pd.Timedelta(hours=offset_hours)
    rain_date=(end-pd.Timedelta(hours=1) if interval_corrected else end).dt.floor('D')
    rain=hourly.groupby(rain_date).precip_mm.agg(observed_rain_mm='sum',rain_hours='count')
    temp=hourly.groupby(end.dt.floor('D')).temp_c.agg(observed_temp_c='mean',temp_hours='count')
    out=rain.join(temp,how='outer').sort_index();out.index.name='date'
    out['precip_mm']=out.observed_rain_mm.where(out.rain_hours==24)
    out['temp_c']=out.observed_temp_c.where(out.temp_hours==24)
    return out

def longest_dry(values):
    best=run=0
    for v in values:
        if pd.notna(v) and v<1:run+=1;best=max(best,run)
        else:run=0
    return best

def summarize(days,strict=True):
    rows=[]
    for year in YEARS:
        expected=pd.date_range(f'{year}-06-01',f'{year}-09-30',freq='D')
        d=days.reindex(expected);v=d.precip_mm if strict else d.observed_rain_mm
        complete=bool((d.rain_hours==24).all())
        valid=v.dropna();peak=valid.idxmax()
        row=dict(year=year,observed_total_mm=float(d.observed_rain_mm.sum(min_count=1)),complete_days=int((d.rain_hours==24).sum()),missing_rain_hours=int(2928-d.rain_hours.fillna(0).sum()),full_season_total_mm=float(v.sum()) if (complete or not strict) else np.nan,complete_day_total_mm=float(valid.sum()),wettest_day_date=str(peak.date()),wettest_day_mm=float(valid.max()),heavy_rain_days_count=int((valid>10).sum()),longest_observed_dry_spell_days=longest_dry(v),mean_complete_day_temp_c=float(d.temp_c.mean()))
        rows.append(row)
    return pd.DataFrame(rows)

def run(input_dir,baseline_dir,output_dir):
    output_dir.mkdir(parents=True,exist_ok=True)
    hourly,manifest=read_inputs(input_dir)
    (output_dir/'input_manifest.json').write_text(json.dumps(manifest,indent=2))
    legacy=aggregate_days(hourly,interval_corrected=False)
    old=pd.read_csv(baseline_dir/'daily_data.csv',parse_dates=['date_pkt']).set_index('date_pkt')
    assert old.index.equals(legacy.index)
    checks=[]
    for col,new,tol in [('precip_mm','observed_rain_mm',1e-4),('temp_c','observed_temp_c',1e-4)]:
        delta=np.abs(old[col]-legacy[new]);checks.append(dict(check='daily_'+col,max_abs_difference=float(delta.max()),tolerance=tol,passed=bool((delta<=tol).all())))
    legacy_summary=summarize(legacy,strict=False)
    published=pd.read_csv(baseline_dir/'yearly_summary.csv')
    for oldcol,newcol,tol in [('monsoon_total_mm','full_season_total_mm',1e-3),('wettest_day_mm','wettest_day_mm',1e-4),('heavy_rain_days_count','heavy_rain_days_count',0),('longest_dry_spell_days','longest_observed_dry_spell_days',0)]:
        delta=np.abs(published[oldcol]-legacy_summary[newcol]);checks.append(dict(check='annual_'+oldcol,max_abs_difference=float(delta.max()),tolerance=tol,passed=bool((delta<=tol).all())))
    checks.append(dict(check='wettest_dates',max_abs_difference=0,tolerance=0,passed=bool((published.wettest_day_date==legacy_summary.wettest_day_date).all())))
    pd.DataFrame(checks).to_csv(output_dir/'legacy_reconciliation.csv',index=False)
    assert all(x['passed'] for x in checks),checks
    corrected=aggregate_days(hourly);utc=aggregate_days(hourly,offset_hours=0)
    corrected.to_csv(output_dir/'daily_pkt_interval_corrected.csv')
    annual=summarize(corrected);annual.to_csv(output_dir/'annual_coverage_qualified.csv',index=False)
    comparison=[]
    for year in YEARS:
        for name,days,col in [('legacy_PKT',legacy,'observed_rain_mm'),('corrected_PKT',corrected,'precip_mm'),('legacy_UTC',aggregate_days(hourly,0,False),'observed_rain_mm'),('corrected_UTC',utc,'precip_mm')]:
            d=days.loc[f'{year}-06-01':f'{year}-09-30',col].dropna()
            comparison.append(dict(year=year,convention=name,wettest_day=str(d.idxmax().date()),wettest_mm=float(d.max())))
    pd.DataFrame(comparison).to_csv(output_dir/'day_boundary_comparison.csv',index=False)
    # Fixed dates common to all years; do not compare 121 days with 122 days.
    common=[]
    for year in YEARS:
        d=corrected.reindex(pd.date_range(f'{year}-06-02',f'{year}-09-30',freq='D'))
        assert (d.rain_hours==24).all() and (d.temp_hours==24).all()
        common.append(dict(year=year,days=len(d),rainfall_mm=float(d.precip_mm.sum()),temperature_c=float(d.temp_c.mean())))
    common=pd.DataFrame(common);common.to_csv(output_dir/'common_window_jun02_sep30.csv',index=False)
    lr=linregress(published.year,published.monsoon_total_mm);cr=linregress(common.year,common.rainfall_mm)
    # Quantify historical resampling across years: absent dates were represented as zero rain.
    mons=hourly[hourly.utc.dt.month.isin([6,7,8,9])].set_index('utc').precip_mm
    bad=mons.resample('D').sum();count=mons.resample('D').count()
    legacy_utc_valid=mons.groupby(mons.index.floor('D')).sum()
    metrics=dict(legacy_trend_slope=float(lr.slope),legacy_trend_p=float(lr.pvalue),common_window_trend_slope=float(cr.slope),common_window_trend_p=float(cr.pvalue),common_window_days=121,empty_days_created_by_legacy_resample=int((count==0).sum()),legacy_resampled_95th=float(bad.quantile(.95)),legacy_observed_utc_95th=float(legacy_utc_valid.quantile(.95)),corrected_complete_pkt_95th=float(corrected.loc[corrected.index.month.isin([6,7,8,9]),'precip_mm'].quantile(.95)),schema='Preserved NetCDF4/HDF5 snapshot only; unscaled float32 variables on a fixed 3x3 grid')
    (output_dir/'audit_metrics.json').write_text(json.dumps(metrics,indent=2))
    packages={x:importlib.metadata.version(x) for x in ['h5py','numpy','pandas','scipy','matplotlib']}
    (output_dir/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),platform=platform.system(),packages=packages),indent=2))
    fig,axs=plt.subplots(1,2,figsize=(12,4.5))
    axs[0].plot(common.year,common.rainfall_mm,'o-',color='#287c70');axs[0].set(title='Common complete window: 2 June-30 September',ylabel='Rainfall (mm)',xlabel='Year');axs[0].text(.03,.95,f'Slope {cr.slope:.2f} mm/year; p={cr.pvalue:.3f}',transform=axs[0].transAxes,va='top')
    daily2020=pd.DataFrame({'Legacy PKT date':legacy.observed_rain_mm,'Correct interval PKT date':corrected.precip_mm}).loc['2020-08-29':'2020-09-02']
    daily2020.index=daily2020.index.strftime('%d %b');daily2020.plot.bar(ax=axs[1],color=['#b28a64','#287c70'],rot=0);axs[1].set(title='2020 event: daily assignment matters',ylabel='Rainfall (mm)',xlabel='Date')
    fig.tight_layout();fig.savefig(output_dir/'timing_and_common_window.png',dpi=160);plt.close(fig)
    print(json.dumps(metrics,indent=2));print(annual.to_string(index=False))
    return metrics

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--input-dir',type=Path,required=True);a.add_argument('--baseline-dir',type=Path,default=Path('data/processed'));a.add_argument('--output-dir',type=Path,default=Path('results/reproducibility'));args=a.parse_args();run(args.input_dir,args.baseline_dir,args.output_dir)
