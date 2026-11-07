# Independent numerical reproduction and timing audit

8 November 2026. This audit reads all ten preserved hourly NetCDF files independently of the historical notebook's saved outputs. The original report, notebook and processed CSVs remain historical artifacts.

## Results

All published daily rainfall/temperature values and annual summary metrics were reproduced within declared tolerances. Maximum daily discrepancies were below 0.000002 mm and 0.000002 C; annual rainfall discrepancies were below 0.000033 mm. Wettest dates, heavy-rain counts and longest dry spells match exactly under the historical convention. See [reconciliation](../results/reproducibility/legacy_reconciliation.csv).

The input checks confirm hourly timestamp continuity within each file, consistent 3x3 coordinates, expected units, finite values, nonnegative precipitation and unique timestamps. Nine files cover June-September UTC; 2022 covers the entire year. SHA-256 hashes and coverage are recorded in [the manifest](../results/reproducibility/input_manifest.json). This verifies the supplied snapshot, not an independent CDS acquisition or ground validation.

## Corrections

ERA5 hourly precipitation is accumulated over the preceding hour. Assign rainfall to the local interval start (UTC timestamp + 5 hours - 1 hour); instantaneous temperature retains UTC timestamp + 5 hours. This follows [ECMWF's accumulation documentation](https://confluence.ecmwf.int/spaces/CKB/pages/76414402/ERA5%2Bdata%2Bdocumentation).

| 31 August 2020 | Rainfall, mm |
| --- | ---: |
| Historical PKT timestamp grouping | 104.28837 |
| Corrected PKT interval grouping | 106.50100 |
| Historical UTC timestamp grouping | 110.91280 |
| Corrected UTC interval grouping | 111.00308 |

Daily assignment changes other metrics too: the corrected 2022 PKT maximum is 43.43796 mm on 17 July, replacing the historical 46.69767 mm on 21 June. Corrected complete-day heavy-rain counts in 2022 are 11 rather than 10. These are changes in aggregation, not new observations.

Nine seasonal files lack four rainfall intervals at the start of 1 June PKT. Full-season totals are therefore left blank for those years; observed sums are explicitly partial. Missing hours are not assumed dry. The common comparison window is **2 June-30 September: 121 complete days in every year**. Its rainfall slope is 5.91154 mm/year with p=0.59404, compared with the historical 5.95784 and p=0.59090. Neither establishes a statistically significant trend.

The historical notebook source resamples concatenated seasonal data across intervening calendar dates. Its default sum creates **2,189 empty days as zero rainfall**. That source path gives a 95th percentile of 2.74319 mm/day; using only observed UTC dates gives 9.01036. The latter matches the earlier reported threshold, so the saved result and current source path should not be treated as interchangeable. Corrected complete PKT days give 9.03042 mm/day, using a different day convention. The revised script never inserts interseason dry days.

## Run and test

Install `requirements-reproducibility.txt` using Python 3.12. Supply the existing files listed in the manifest; no CDS credential is needed.

```sh
python src/reproduce_monsoon.py --input-dir /path/to/ERA5_Multan
python -m unittest discover -s tests -v
```

The reader uses h5py for the exact validated NetCDF4/HDF5 schema and rejects incompatible layouts or units. It is not a general CF reader. Regional averaging remains the historical equal-grid-point mean; no new area weighting is introduced. New outputs go to `results/reproducibility/` and never overwrite the original data/processed tables. The audit notebook uses `ERA5_INPUT_DIR` or `data/raw` for local inputs.

Six synthetic tests cover midnight assignment, complete 24-hour days, missing hours, interseason gaps, missing-day dry-spell breaks and UTC/PKT differences. Environment versions are recorded. This is an independent numerical reproduction using available packages, not a newly provisioned clean-environment certification or a rerun of every historical plotting cell.

## Release scope

The completed research release uses 2 June-30 September in all ten years. See [the final report](FINAL_REPORT.pdf) and [final tables and figures](../results/final/); these supersede historical numerical summaries for presentation. Retrieving boundary hours would enable full 1 June-30 September totals. Station comparisons and a longer record would be optional extensions, not requirements for this descriptive project's completion.
