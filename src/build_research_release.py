"""Build final common-window tables, figures and report source from checked daily data."""
from pathlib import Path
import json
import pandas as pd
import numpy as np
from scipy.stats import linregress
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'results/final';out.mkdir(parents=True,exist_ok=True)
d=pd.read_csv(ROOT/'results/reproducibility/daily_pkt_interval_corrected.csv',parse_dates=['date']).set_index('date')
rows=[];frames=[]
for year in range(2016,2026):
 s=d.reindex(pd.date_range(f'{year}-06-02',f'{year}-09-30'))
 assert len(s)==121 and (s.rain_hours==24).all() and (s.temp_hours==24).all()
 assert s[['precip_mm','temp_c']].notna().all().all()
 frames.append(s[['precip_mm','temp_c']])
 rows.append(dict(year=year,days=121,rainfall_mm=s.precip_mm.sum(),temperature_c=s.temp_c.mean(),heavy_rain_days_gt10mm=int((s.precip_mm>10).sum()),wettest_date=str(s.precip_mm.idxmax().date()),wettest_mm=s.precip_mm.max()))
a=pd.DataFrame(rows);a.to_csv(out/'annual_summary.csv',index=False)
daily=pd.concat(frames);daily.index.name='date_pkt';daily.to_csv(out/'daily_series.csv')
baseline=pd.read_csv(ROOT/'results/reproducibility/common_window_jun02_sep30.csv')
assert np.allclose(a.rainfall_mm,baseline.rainfall_mm,atol=0.0001)
assert np.allclose(a.temperature_c,baseline.temperature_c,atol=0.0001)
trend=linregress(a.year,a.rainfall_mm);mean=a.rainfall_mm.mean();row22=a[a.year==2022].iloc[0]
other=a[a.year!=2022]
stats=dict(mean_rainfall_mm=float(mean),slope_mm_year=float(trend.slope),p_value=float(trend.pvalue),r_squared=float(trend.rvalue**2),rainfall_2022_vs_other_mean_pct=float((row22.rainfall_mm/other.rainfall_mm.mean()-1)*100),temperature_2022_vs_other_mean_c=float(row22.temperature_c-other.temperature_c.mean()))
(out/'statistics.json').write_text(json.dumps(stats,indent=2))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(10,4.4));colors=['#247d72' if y==2022 else '#7999a7' for y in a.year]
ax.bar(a.year,a.rainfall_mm,color=colors,width=.65);ax.axhline(mean,color='#bd8745',ls='--',label=f'Ten-year mean: {mean:.1f} mm')
for y,v in zip(a.year,a.rainfall_mm):ax.text(y,v+5,f'{v:.1f}',ha='center',fontsize=9)
ax.set(xticks=a.year,ylabel='Rainfall (mm)',ylim=(0,425),title='Rainfall varies strongly between years');ax.legend(frameon=False);fig.tight_layout();fig.savefig(out/'rainfall_by_year.png',dpi=180);plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(11,4.3))
axes[0].plot(a.year,a.temperature_c,'o-',color='#bd8745');axes[0].scatter([2022],[row22.temperature_c],color='#247d72',s=70,zorder=3);axes[0].set(xticks=[2016,2018,2020,2022,2024],ylabel='Mean 2 m temperature (C)',title='2022 was the coolest window')
s=daily.loc['2022'];axes[1].plot(s.index,s.precip_mm.cumsum(),color='#247d72',lw=2);axes[1].set(ylabel='Cumulative rainfall (mm)',title='Rainfall accumulation in 2022');import matplotlib.dates as mdates
axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%b'));axes[1].xaxis.set_major_locator(mdates.MonthLocator());fig.tight_layout();fig.savefig(out/'temperature_and_2022.png',dpi=180);plt.close(fig)
pages=[
 {'title':'Monsoon Rainfall & Flood-Risk Analysis for Multan','subtitle':'ERA5 rainfall and temperature | 2016-2025','sections':[
 ['Overview','This study describes interannual rainfall and near-surface temperature variability over a small ERA5 grid around Multan. It compares the same 121 Pakistan-calendar days, 2 June to 30 September, in each year from 2016 through 2025. The objective is to characterize variability and the distinctive 2022 season, rather than attribute flooding or establish a long-term climate trend.'],
 ['Key findings',f'Rainfall ranged from 53.4 mm in 2021 to 374.2 mm in 2022. The ten-year mean was {mean:.1f} mm. The fitted slope was +{trend.slope:.2f} mm/year (p = {trend.pvalue:.3f}), which does not establish a statistically significant linear trend. In the common window, 2022 was also the coolest year, with a mean 2 m temperature of {row22.temperature_c:.2f} C.'],
 ['Project context','Project lead and primary analyst: Musab Shahid. Musab initiated this ERA5 practice project following a climate-modeling conference in Bahawalpur. Original team: Musab Shahid, Alishba Ehsan, Mudassir Mujahid and Bareera. The contribution statement records the leadership account supplied by Musab.']],
 'figure':'rainfall_by_year.png','caption':'Figure 1. Regional mean rainfall totals for 2 June-30 September in every year. The dashed line is the mean across the ten windows.'},
 {'title':'Data and methods','sections':[
 ['Input data','Ten preserved ERA5 hourly single-level NetCDF files provide total precipitation and 2 m air temperature. The sampled coordinates are 30.00, 30.25 and 30.50 degrees N, and 71.25, 71.50 and 71.75 degrees E: nine grid points. This is a small regional sample around Multan, not an administrative-boundary average. The data source is ECMWF/Copernicus Climate Change Service, accessed originally through the Climate Data Store.'],
 ['Spatial and temporal aggregation','Each hourly field is averaged equally across the nine grid points. Precipitation is converted from metres to millimetres; temperature from kelvin to Celsius. ERA5 hourly precipitation describes the preceding hour, so its interval is assigned to the Pakistan date using timestamp + 5 hours - 1 hour. Instantaneous temperature uses timestamp + 5 hours. Daily rainfall is the sum of 24 hourly intervals and daily temperature the mean of 24 hourly samples.'],
 ['Comparison period','All final cross-year metrics use 2 June-30 September (121 days; 1,210 daily records across ten years). The nine seasonal files begin at 1 June 00:00 UTC; their first Pakistan rainfall day lacks four preceding intervals. The full-year 2022 file does not have this boundary issue. Excluding 1 June consistently yields complete rainfall and temperature coverage in every year, without estimating or zero-filling missing hours. These totals should not be relabeled as full 1 June-30 September totals.'],
 ['Statistics','Rainfall totals, mean temperature, the wettest daily amount and counts of days above 10 mm are calculated within the common window. The 10 mm threshold is an operational definition for this analysis, not a local warning criterion. A simple ordinary least-squares regression relates the ten rainfall totals to calendar year. Its two-sided slope p-value is descriptive; ten annual samples provide limited evidence for climate-trend inference.']],
 'table':True},
 {'title':'Results and interpretation','sections':[
 ['The 2022 season',f'The 2022 window accumulated 374.2 mm, {stats["rainfall_2022_vs_other_mean_pct"]:.1f}% above the mean of the other nine windows. It had 11 days above 10 mm. Its wettest day was 17 July (43.44 mm). Mean temperature was {abs(stats["temperature_2022_vs_other_mean_c"]):.2f} C below the other nine-year mean. These co-occurring wet and cool conditions are descriptive associations; the analysis does not isolate their physical causes.'],
 ['Variability and daily concentration','The wettest individual day across the comparison windows was 31 August 2020, with a regional mean of 106.50 mm. Thus the year containing the largest single-day amount was not the year with the largest window total. Seasonal accumulation and daily intensity describe different aspects of rainfall. The 2021 window was driest at 53.4 mm, while 2024 ranked second wettest at 274.6 mm.'],
 ['Trend interpretation',f'The fitted rainfall slope is +{trend.slope:.2f} mm/year, with p = {trend.pvalue:.3f} and R-squared = {trend.rvalue**2:.3f}. Large year-to-year variation dominates this short record. A nonsignificant result is not proof that rainfall is unchanging; it means this analysis does not establish a linear change over the selected ten years.']],
 'figure':'temperature_and_2022.png','caption':'Figure 2. Mean temperature in the common comparison window (left) and cumulative daily rainfall within that window in 2022 (right).'},
 {'title':'Scope, reproducibility and sources','sections':[
 ['Conclusion','The completed analysis documents substantial interannual variability in the selected Multan ERA5 grid. The 2022 comparison window was wettest and coolest, whereas the largest daily rainfall amount occurred in 2020. The ten-year rainfall regression is not statistically significant. These findings support a clear descriptive case study of reanalysis handling, time aggregation and environmental data interpretation.'],
 ['Scope and limitations','Results apply to a nine-point reanalysis grid and the stated 121-day window. They are not station measurements, ward-level estimates, an inundation model or an attribution of the 2022 floods. Equal grid-point averaging preserves the original regional calculation. This release does not claim validation against local rain gauges. Such comparison, a longer record or retrieving the excluded boundary hours would be optional extensions beyond this completed scope.'],
 ['Reproduce the release','The repository provides the analysis code, executed notebook, final daily and annual CSVs, figures, package versions, and input hashes. Run src/reproduce_monsoon.py against the preserved hourly files, then src/build_research_release.py to rebuild the final tables and figures. Six focused tests check daily assignment and missing-data handling. The supporting audit records agreement with historical results and explains revisions. The historical report, poster and original tables remain available as archive materials; use this report and results/final for the current findings.'],
 ['Authorship and assistance','Musab Shahid led the original work and analysis, with original team membership credited on page 1. The November 2026 reproduction, release code and report preparation used AI assistance. Team membership is not a claim that every participant reviewed this later release. Report release: 8 November 2026.'],
 ['Sources and materials','Data: Copernicus Climate Change Service / ECMWF, ERA5 hourly data on single levels, Climate Data Store: https://cds.climate.copernicus.eu/ . Accumulation convention: ECMWF ERA5 data documentation, section on mean rates and accumulations. Project repository: https://github.com/musab-shahid/multan-era5-monsoon-analysis . Full technical provenance and the documentation link are in docs/REPRODUCIBILITY_AUDIT.md.']]}
]
(out/'report_content.json').write_text(json.dumps(pages,indent=2),encoding='utf-8')
md=['# Monsoon Rainfall & Flood-Risk Analysis for Multan\n\nFinal research report | 8 November 2026\n']
for i,p in enumerate(pages):
 if i:md.append('## '+p['title'])
 for title,body in p['sections']:md+=['### '+title,body]
 if p.get('figure'):md += [f'![{p["caption"]}](../results/final/{p["figure"]})']
 if p.get('table'):
  md+=['| Year | Rainfall (mm) | Temperature (C) | Days >10 mm |','| --- | ---: | ---: | ---: |']
  md += [f'| {int(x.year)} | {x.rainfall_mm:.2f} | {x.temperature_c:.2f} | {int(x.heavy_rain_days_gt10mm)} |' for x in a.itertuples()]
(ROOT/'docs/FINAL_REPORT.md').write_text('\n\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps(stats,indent=2));print('PASS: 121 complete rainfall/temperature days per year; 1,210 final rows; totals match checked source.')
