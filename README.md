# Multan Monsoon Rainfall & Temperature Analysis Using ERA5 (2016–2025)

**Collaborative climate-data analysis of monsoon variability near Multan, Pakistan, with a focused 2022 case study.**

**Contributors:** Musab Shahid · Alishba Ehsan · Mudassir Mujahid · Bareera  
**Dataset:** ECMWF ERA5 hourly single-level atmospheric reanalysis via the Copernicus Climate Data Store  
**Area:** 30.0–30.5°N, 71.2–71.8°E (~3×3 ERA5 grid)  
**Study period:** June–September 2016–2025; full-year 2022 also analyzed.

## Research questions

How did recent monsoon rainfall fluctuate, was a statistically meaningful linear trend detectable, and how did the 2022 season differ in total rainfall, heavy-rain events, and temperature? The study also examines diurnal and spatial differences.

**This is atmospheric reanalysis, not direct ground-station rainfall, satellite imagery classification, or a hydrological flood simulation.**

## Selected results

| Indicator | Result |
|---|---|
| 2022 June–September rainfall | **374.2 mm**, highest during 2016–2025 |
| 2021 monsoon rainfall | **53.4 mm**, lowest |
| Linear rainfall trend | **+5.96 mm/year**, **p = 0.591** (not statistically significant) |
| 2022 monsoon mean temperature | **33.0°C** vs about **33.9°C** in the other nine years |
| Wettest Pakistan-calendar-day (daily table) | **104.29 mm**, 31 August 2020 |
| Wettest UTC day (separate extremes analysis) | **110.91 mm**, 31 August 2020 |

**Why the two 2020 rainfall values differ:** The main daily series sums precipitation by Pakistan local date after a UTC+5 conversion. A separate gridded extreme-day calculation aggregates on UTC dates. The windows are different, so the numbers should not be compared as though they measure exactly the same day. See [methodology reconciliation](docs/METHODOLOGY_AND_RESULT_RECONCILIATION.md).

## Figures

![Annual rainfall trend](figures/annual_rainfall_trend.png)

![Annual precipitation anomalies](figures/annual_rainfall_anomalies.png)

![Diurnal rainfall](figures/rainfall_diurnal_pattern.png)

![Monsoon temperatures](figures/monsoon_temperature_by_year.png)

![2022 full year temperature and precipitation](figures/full_year_2022_timeseries_ARCHIVED.png)

See [all figures](figures/).

## Files

- [Analysis-only notebook](notebooks/Multan_ERA5_Analysis_ONLY_NO_DOWNLOAD.ipynb)
- [Derived CSV files](data/processed/) and [data provenance](data/README.md)
- [Original report](docs/original_analysis_report.pdf) and [final poster](docs/final_poster.pdf)
- [Execution instructions](docs/RUNNING.md)
- [Complete research archive](https://drive.google.com/drive/folders/1-VWthMW-y28WWE5xLciciaOSFqXTT3I_)

## Reproducibility

The analysis notebook reuses existing NetCDF data under `/content/drive/MyDrive/ERA5_Multan/`; it is configured **not to redownload** data. Raw ERA5 GRIB and NetCDF files remain in Drive instead of the GitHub repository. The original report remains unchanged and should be read with the methodological note.

## Limitations

The 10-year study period is too short to establish a long-term climate trend. ERA5 grid values are not station observations. This analysis does not model inundation, flood routing, or flood attribution. All four contributors are credited; individual contributions should not be assumed. The full-year 2022 figure was recovered from an older saved notebook output.

## Data source

Copernicus Climate Change Service, ECMWF ERA5 hourly data on single levels, accessed via the [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/). Upstream data redistribution remains subject to its terms.

## Related research portfolio

- [South Punjab Drought Event Analysis (2001–2025)](https://github.com/musab-shahid/south-punjab-drought-analysis) — separate independent drought research; see its methodological limitations.
- [Multan Urban Heat Island Analysis (2013–2023)](https://github.com/musab-shahid/multan-uhi-analysis) — undergraduate Landsat and Google Earth Engine analysis.

**Attribution reminder:** This ERA5 project is collaborative and credits Musab Shahid, Alishba Ehsan, Mudassir Mujahid, and Bareera; this cross-link does not assign unverified individual contributions.
