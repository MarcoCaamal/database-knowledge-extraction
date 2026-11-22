"""Quality assurance for the Superstore final-project deliverables."""
from pathlib import Path
from zipfile import is_zipfile, ZipFile
import json
import subprocess
from lxml import etree
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
  "dashboard/Superstore_Executive_Dashboard.twb",
  "dashboard/Superstore_Executive_Dashboard.twbx",
  "dashboard/sales_orders.csv",
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

pptx=ROOT/"presentation/Superstore_Executive_Story.pptx"
assert is_zipfile(pptx) and len(Presentation(pptx).slides)==10
pdf=ROOT/"presentation/Superstore_Executive_Story.pdf"
assert pdf.read_bytes().startswith(b"%PDF")
pdfinfo=subprocess.run(["pdfinfo",str(pdf)],capture_output=True,text=True,check=False)
if pdfinfo.returncode==0:
    pages=[line for line in pdfinfo.stdout.splitlines() if line.startswith("Pages:")]
    assert pages and pages[0].split()[-1]=="10",f"Unexpected page count: {pages}"

# Check Tableau workbook XML package integrity. Opening in Tableau Desktop
# is a separate visual/semantic check and cannot be claimed here.
twbx=ROOT/"dashboard/Superstore_Executive_Dashboard.twbx"
twb=ROOT/"dashboard/Superstore_Executive_Dashboard.twb"
assert is_zipfile(twbx)
with ZipFile(twbx) as f:
    assert f.testzip() is None
    assert set(f.namelist())=={twb.name,"sales_orders.csv"}
    root=etree.fromstring(f.read(twb.name))
    assert len(root.xpath("./worksheets/worksheet"))==4
    assert len(root.xpath("./dashboards/dashboard"))==1
    assert len(root.xpath("./actions/action"))==1
    assert f.read(twb.name)==twb.read_bytes()
    with f.open("sales_orders.csv") as csv_file:
        packaged=pd.read_csv(csv_file)
    assert len(packaged)==9994
    assert abs(packaged.revenue.sum()-2297200.86)<0.02
    assert abs(packaged.profit.sum()-286397.02)<0.02
    assert {"state","discount_band","revenue","profit","order_date"}.issubset(packaged.columns)

subprocess.run([str(ROOT/".venv/bin/python"),"-m","py_compile",
                str(ROOT/"dashboard/app.py"),
                str(ROOT/"scripts/build_tableau_workbook.py")],check=True)
slide_text="\n".join(s.text for slide in Presentation(pptx).slides for s in slide.shapes if s.has_text_frame)
assert all(name in slide_text for name in [
    "Juan Manuel Sánchez Hernández", "Seir Mendoza Vidal",
    "José Rodrigo de la Cruz Chim", "Marco Antonio Caamal Chi",
])
assert "Fifth member" in slide_text
print(f"PASS: {len(df):,} records, {len(codes)} executed code cells, {len(figures)} figures, {len(tables)} tables")
print("PASS: Tableau TWBX ZIP/XML structure, 4 sheets, 1 dashboard, 1 selection action, original 9,994 records")
print("PASS: 10-slide PowerPoint and PDF, 4 named participants, placeholder for fifth person")
print("NOTE: Validate workbook opening/interactivity in Tableau Desktop before the final submission.")
