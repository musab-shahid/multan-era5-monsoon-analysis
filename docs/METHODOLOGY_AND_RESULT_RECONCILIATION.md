# Reconciliation of the 2020 daily rainfall maximum

Two code paths used the same ERA5 regional time series but **different day boundaries**.

| Code path | Procedure | 31 August 2020 |
|---|---|---:|
| Main daily table | Shift hourly timestamps to Pakistan Standard Time (UTC+5), then group by local calendar date | **104.288370 mm** |
| Extreme-event visualization | Resample on the original UTC coordinate, then spatially average | **110.912804 mm** |

The difference is **6.624434 mm**. Different five-hour-shifted daily windows can produce different precipitation totals. These should not be described as two measurements of an identical 24-hour period.

The main annual daily table and this repository's headline figures use **104.29 mm (PKT day)**. The 95th-percentile extremes plot uses **110.91 mm (UTC day)** and must be labeled as such. The original report records both without enough explanation; the report remains an unchanged historical artifact.

## Additional caveats

- The extreme-event 95th percentile (approximately 9.01 mm/day) was computed using UTC-day values, not the local daily-data CSV.
- The first/last local day of a converted time series may be incomplete without padding in the original UTC data.
- This is an observational climate-reanalysis description, not a model of inundation, drainage, flood routing or causation.
- Figures were recovered from saved notebook outputs, not independently regenerated for publication.

## Supporting files

- [Derived local-day CSVs](../data/processed/)
- [Notebook with saved analysis output](../notebooks/Multan_ERA5_Analysis_ONLY_NO_DOWNLOAD.ipynb)
- [Original analysis report](original_analysis_report.pdf), sections 4.3 and 4.7
