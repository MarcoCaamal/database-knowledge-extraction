"""Recompute independently verified summary values from the real sample CSV."""
from pathlib import Path
import json
import pandas as pd

root = Path(__file__).resolve().parents[1]
data = pd.read_csv(root/"data/raw/Sample_Superstore.csv",encoding="utf-8-sig",dtype={"Postal Code":"string"})
data["Order Date"] = pd.to_datetime(data["Order Date"],format="%Y-%m-%d")
data["year"]=data["Order Date"].dt.year
data["discount_band"]=pd.cut(data["Discount"],[-.001,0,.2,.4,1],labels=["0%",">0–20%",">20–40%",">40%"],include_lowest=True)
def agg(col):
    tab=data.groupby(col,observed=True).agg(sales=("Sales","sum"),profit=("Profit","sum"),records=("Row ID","size"))
    tab["margin_pct"]=100*tab.profit/tab.sales
    return tab.reset_index()
def clean(row,col,rename="name",include_count=False):
    d={rename: row[col], "sales":round(float(row["sales"]),2),
       "profit":round(float(row["profit"]),2), "margin_pct":round(float(row["margin_pct"]),2)}
    if include_count:d["records"]=int(row["records"])
    return d
summary={
    "source_url":"https://raw.githubusercontent.com/mikemooreviz/superstore/master/superstore.csv",
    "dataset_name":"Sample Superstore (educational retail dataset)",
    "date_min":data["Order Date"].min().strftime("%Y-%m-%d"),
    "date_max":data["Order Date"].max().strftime("%Y-%m-%d"),
    "records":len(data),
    "orders":data["Order ID"].nunique(),
    "customers":data["Customer ID"].nunique(),
    "sales_usd":round(float(data["Sales"].sum()),2),
    "profit_usd":round(float(data["Profit"].sum()),2),
    "negative_profit_lines":int((data["Profit"]<0).sum()),
    "average_discount":round(float(data["Discount"].mean()),4),
    "postal_code_nulls":int(data["Postal Code"].isna().sum())
}
summary["categories"]=[clean(r,"Category") for _,r in agg("Category").sort_values("margin_pct",ascending=False).iterrows()]
summary["regions"]=[clean(r,"Region") for _,r in agg("Region").sort_values("profit",ascending=False).iterrows()]
summary["years"]=[clean(r,"year","year") for _,r in agg("year").sort_values("year").iterrows()]
summary["discount_bands"]=[clean(r,"discount_band","band",True) for _,r in agg("discount_band").iterrows()]
summary["losing_states"]=[clean(r,"State","state") for _,r in agg("State").query("profit < 0").sort_values("profit").iterrows()]
summary["subcategories"]=[clean(r,"Sub-Category") for _,r in agg("Sub-Category").sort_values("profit").iterrows()]
assert summary["records"]==9994
assert summary["orders"]==5009
assert summary["postal_code_nulls"]==11
assert abs(summary["sales_usd"]-2297200.86)<.01
root.joinpath("data/verified_summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2,default=str)+"\n",encoding="utf-8")
print("Verified values saved into data/verified_summary.json")
