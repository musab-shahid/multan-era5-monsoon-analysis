# Running without re-downloading ERA5 data

You do **not** need to run the notebook to view the saved figures and report.

To reproduce its computations:

1. Open [the analysis-only notebook](../notebooks/Multan_ERA5_Analysis_ONLY_NO_DOWNLOAD.ipynb) in Google Colab.
2. Mount the Google Drive holding `ERA5_Multan`.
3. Confirm files exist in `/content/drive/MyDrive/ERA5_Multan/`: `multan_2016.nc` through `multan_2021.nc`, `multan_2022_full.nc`, and `multan_2023.nc` through `multan_2025.nc`.
4. Run only if reproduction is required. The analysis-only notebook checks inputs and does not issue CDS download requests; it stops when an input is missing.
5. Outputs, including `daily_data.csv` and `yearly_summary.csv`, may be overwritten. Keep a backup.

Python libraries include `xarray`, `numpy`, `pandas`, `scipy`, `matplotlib`, and a NetCDF reader. Versions are not pinned; clean-environment execution has not been independently verified.

**Security:** Older, unredacted notebooks and the historical code PDF contain a CDS API credential. They are deliberately excluded here. Rotate or revoke that credential in your CDS account. This analysis-only notebook requires no CDS credential.
