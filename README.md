# Monsoon Rainfall & Flood-Risk Analysis for Multan

*Using ERA5 Reanalysis Data*

A completed descriptive study of rainfall and temperature variability over a nine-point ERA5 grid around Multan, with a focused examination of 2022.

**Project lead and primary analyst:** Musab Shahid. **Original team:** Musab Shahid, Alishba Ehsan, Mudassir Mujahid and Bareera. [Contributions](docs/CONTRIBUTIONS.md).

## Read the research

- **[Final research report (PDF)](docs/FINAL_REPORT.pdf)** · [Readable report](docs/FINAL_REPORT.md)
- **[Final results and figures](results/final/)** · [Public case study](https://musab-shahid-earth-observation.brinycourt4.chatgpt.site/projects/multan-era5-monsoon-analysis)

## Main findings

All cross-year findings use the same complete **2 June-30 September** window: 121 Pakistan-calendar days per year, 2016-2025.

| Finding | Result |
| --- | --- |
| Wettest window | 2022: **374.2 mm** |
| Driest window | 2021: **53.4 mm** |
| Mean rainfall across ten windows | **200.2 mm** |
| Rainfall slope | **+5.91 mm/year; p = 0.594**, not statistically significant |
| Coolest window | 2022: **32.99 C** mean 2 m temperature |
| Largest daily rainfall | **106.50 mm on 31 August 2020** |

![Rainfall by year](results/final/rainfall_by_year.png)

![Temperature and 2022 accumulation](results/final/temperature_and_2022.png)

## Approach and scope

Hourly precipitation and 2 m temperature are averaged equally across the 3x3 grid, converted to mm and Celsius, and aggregated to Pakistan calendar days. Rainfall uses its preceding-hour accumulation interval. Final tables include only complete 24-hour days. Excluding 1 June consistently avoids the UTC/local-date boundary gap in nine seasonal source files. The complete full-year 2022 source is subset to the same comparison window.

This is a regional reanalysis case study. It does not estimate ward-level conditions, model flooding, or establish a long-term climate trend. Station comparisons and an extended climate record are outside this completed project's scope.

## Reproduce the results

Use Python 3.12 and the ten preserved NetCDF inputs listed in the [input manifest](results/reproducibility/input_manifest.json). Original inputs are in the [Drive data archive](https://drive.google.com/drive/folders/1ED2SPbPAN9K2-oaKn_uFI0RqNxntEr04).

```sh
pip install -r requirements-reproducibility.txt
python src/reproduce_monsoon.py --input-dir /path/to/ERA5_Multan
python src/build_research_release.py
python -m unittest discover -s tests -v
```

[Executed notebook](notebooks/ERA5_Reproducibility_Audit.ipynb) · [Running guide](docs/RUNNING.md) · [Environment](results/reproducibility/environment.json).

## Supporting methods and archive

The [technical audit](docs/REPRODUCIBILITY_AUDIT.md) records source checks, historical reconciliation and timing corrections. Use **docs/FINAL_REPORT.pdf** and **results/final/** for current results. These replace historical numerical summaries for presentation purposes; original artifacts are retained for provenance.

- [Original report](docs/original_analysis_report.pdf), [historical poster](docs/final_poster.pdf), [historical figures](figures/) and [historical CSVs](data/processed/)
- [Original analysis notebook](notebooks/Multan_ERA5_Analysis_ONLY_NO_DOWNLOAD.ipynb)
- [Original presentation](https://docs.google.com/presentation/d/1gorhCmLKybStK6BY5sCedjADk4B45ZSu/edit)

Data credit: Copernicus Climate Change Service / ECMWF ERA5, accessed through the Climate Data Store. November 2026 release preparation used AI assistance; see the contribution statement. This repository is a research portfolio release, not a claim of peer-reviewed publication.
