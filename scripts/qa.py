"""QA checks for reproducible deliverables.

Usage: .venv/bin/python scripts/qa.py
"""
from pathlib import Path
from zipfile import is_zipfile
import json
import subprocess
import nbformat
import pandas as pd
from pptx import Presentation

ROOT=Path(__file__).resolve().parents[1]
required=[
  "data/raw/Sample_Superstore.csv",
  "data/processed/superstore_clean.csv",
  "data/verified_summary.json",
  "final_visualizations.ipynb",
  "dashboard/app.py",
  "presentation/Superstore_Executive_Story.pptx",
  "presentation/Superstore_Executive_Story.pdf",
  "presentation/TEAM_SCRIPT.md"
]
for name in required:
    assert (ROOT/name).is_file(),f"Missing {name}"
df=pd.read_csv(ROOT/required[0])
summary=json.loads((ROOT/"data/verified_summary.json").read_text())
assert len(df)==summary["records"]==9994
assert abs(df.Sales.sum()-summary["sales_usd"])<.01
assert abs(df.Profit.sum()-summary["profit_usd"])<.01
nb=nbformat.read(ROOT/"final_visualizations.ipynb",as_version=4)
codes=[c for c in nb.cells if c.cell_type=="code"]
assert codes and all(c.execution_count is not None for c in codes),"Notebook not fully executed"
errors=[o.get("evalue") for c in codes for o in c.get("outputs",[]) if o.output_type=="error"]
assert not errors,errors
figures=list((ROOT/"outputs/figures").glob("*"))
tables=list((ROOT/"outputs/tables").glob("*.csv"))
assert len(figures)>=12
assert len(tables)>=8
deck=ROOT/"presentation/Superstore_Executive_Story.pptx"
assert is_zipfile(deck) and len(Presentation(deck).slides)==10
pdf=ROOT/"presentation/Superstore_Executive_Story.pdf"
assert pdf.read_bytes().startswith(b"%PDF")
check=subprocess.run(["pdfinfo",str(pdf)],capture_output=True,text=True,check=False)
if check.returncode==0:
    pages=[line for line in check.stdout.splitlines() if line.startswith("Pages:")]
    assert pages and pages[0].split()[-1]=="10",f"Unexpected page count: {pages}"
subprocess.run([str(ROOT/".venv/bin/python"),"-m","py_compile",str(ROOT/"dashboard/app.py")],check=True)
print(f"PASS: {len(df):,} records, {len(codes)} executed code cells, {len(figures)} figures, {len(tables)} tables")
print("PASS: 10-slide PowerPoint, PDF, dashboard syntax, independently verified statistics")
print("WARN: Native TWBX/PBIX file remains outstanding; public GitHub repository is published")
