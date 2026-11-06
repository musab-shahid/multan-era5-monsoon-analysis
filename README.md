# Multan Monsoon Rainfall & Temperature Analysis (ERA5, 2016–2025)

**ERA5 reanalysis · Python/xarray · Monsoon variability · Descriptive statistics · 2022 case study**

A **collaborative** analysis of monsoon rainfall and temperature in the Multan region, with a closer look at the 2022 season.

**Contributors:** Musab Shahid · Alishba Ehsan · Mudassir Mujahid · Bareera  
**Data:** ECMWF ERA5 hourly single-level reanalysis via the Copernicus Climate Data Store  
**Study region:** 30.0–30.5°N, 71.2–71.8°E (approximately 3×3 ERA5 grid points)  
**Period:** June–September 2016–2025, plus full-year 2022 context

> **Research scope:** Reanalysis-derived rainfall and temperature, **not** direct rain-gauge observations or a hydrological flood-routing simulation. A 10-year record is insufficient to establish a long-term climate trend.

## Explore the project

| Start here | What it contains |
| --- | --- |
| [Research figures](figures/) | Published seasonal rainfall, anomaly, temperature and hourly-pattern charts |
| [Analysis-only Colab notebook](notebooks/Multan_ERA5_Analysis_ONLY_NO_DOWNLOAD.ipynb) | Reusable calculations using existing NetCDF files; **no CDS re-download** |
| [Daily and annual CSVs](data/processed/) | Regional daily time series and 10-year seasonal summary |
| [Reproduction guide](docs/RUNNING.md) | Expected Drive inputs and environment notes |
| [Original research report](docs/original_analysis_report.pdf) | Preserved research narrative |
| [Final poster](docs/final_poster.pdf) | Poster-format visual summary |
| [2020 UTC/PKT reconciliation](docs/METHODOLOGY_AND_RESULT_RECONCILIATION.md) | Why the two reported August 2020 daily maxima differ |
| [Original presentation (Drive)](https://docs.google.com/presentation/d/1gorhCmLKybStK6BY5sCedjADk4B45ZSu/edit) | Archived classroom presentation; source material, not the primary reproducibility artifact |

## Research questions

How variable were monsoon rainfall totals over 2016–2025? Is the fitted trend statistically meaningful? How did 2022 differ in seasonal total, daily intensity, heavy-rain frequency and temperature?

## Key findings

| Indicator | Result | Interpretation |
| --- | ---: | --- |
| Highest monsoon total | **374.2 mm — 2022** | Wettest selected season |
| Lowest monsoon total | **53.4 mm — 2021** | Driest selected season |
| Linear rainfall trend | **+5.96 mm/year; p = 0.591** | **Not statistically significant** |
| Mean 2022 monsoon temperature | **33.0°C** | About 0.9°C cooler than the other nine-year mean |
| Wettest day by Pakistan calendar | **104.29 mm — 31 Aug 2020** | Local-date daily aggregation |
| Wettest day in separate UTC analysis | **110.91 mm — 31 Aug 2020** | Different 24-hour boundary; not the same statistic |

![Annual rainfall and fitted line (nonsignificant)](figures/annual_rainfall_trend.png)

## Evidence in figures

| Rainfall anomalies | Diurnal pattern |
| --- | --- |
| ![Monsoon rainfall anomalies](figures/annual_rainfall_anomalies.png) | ![Average precipitation by month and hour](figures/rainfall_diurnal_pattern.png) |

| Monsoon temperature | Full-year 2022 context |
| --- | --- |
| ![Monsoon temperatures](figures/monsoon_temperature_by_year.png) | ![Archived full-year 2022 time series](figures/full_year_2022_timeseries_ARCHIVED.png) |

See the [full figures gallery](figures/).

## Analysis and reproducibility

The notebook reads the original hourly **NetCDF** files kept in Google Drive, averages the small ERA5 spatial grid, converts precipitation from metres to millimetres and temperature from Kelvin to Celsius, and aggregates by calendar date after a UTC→Pakistan-time conversion. It computes seasonal totals, wettest days, >10 mm daily rainfall counts, dry spells, regression and visualizations.

**Important timing qualification:** ERA5 hourly precipitation is accumulated over the preceding hour. A day boundary based on the hour-ending timestamp can shift an accumulation at midnight to the next calendar day. This affects interpretation of daily extremes and requires an hourly-source check before any revised historical values are published. The local/UTC window difference is separately explained in the [methodology note](docs/METHODOLOGY_AND_RESULT_RECONCILIATION.md).

- Daily and annual processed summaries were rechecked against the published CSVs: totals, wettest-day records, heavy-rain counts and longest dry spells match to reported precision.
- The repository has **not** established a fresh independent execution from clean NetCDF inputs. Package versions are not pinned.
- Raw GRIB/NetCDF data are in the [research archive on Drive](https://drive.google.com/drive/folders/1-VWthMW-y28WWE5xLciciaOSFqXTT3I_), not GitHub. [Data provenance](data/README.md) documents the outputs.
- 2022 rainfall extremes do not establish causation of observed flooding; there is no terrain, streamflow, drainage or inundation model here.
- All four contributors are credited. Specific individual contributions are **not** asserted without evidence.

## Research portfolio

| Project | Focus | Research context |
| --- | --- | --- |
| [Multan Urban Heat Analysis](https://github.com/musab-shahid/multan-uhi-analysis) | Landsat thermal remote sensing and spatial grouping | Undergraduate final-year project |
| **This project — ERA5 Monsoon** | Reanalysis time series, seasonal rainfall and statistical inference | **Collaborative**, four contributors |
| [South Punjab Drought Analysis](https://github.com/musab-shahid/south-punjab-drought-analysis) | Multi-sensor drought monitoring and environmental response | **Independent** research-application report |

**Data credit:** Copernicus Climate Change Service, ECMWF ERA5, accessed through the [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/). Respect upstream data licensing and attribution.
