# Export scripts

These scripts rebuild the long-form CSVs and `data.mat` files from original source files. They are not needed if you are only analyzing the files already in `datasets/`.

CSV columns and MATLAB fields use **camelCase**. Each dataset folder has a `data.mat` whose only variable is a struct `d`.

```bash
python scripts/export_to_csv.py
python scripts/export_bart.py
python scripts/export_stark_mst.py
python scripts/export_amyloid_ravlt.py
python scripts/export_osf_additions.py
```

Requires `numpy`, `pandas`, and `scipy`. `xlsx_sheets.py` is a small xlsx reader used for ranking workbooks and QuestionPro exports (no openpyxl required).
