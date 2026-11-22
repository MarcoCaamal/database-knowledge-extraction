"""Interactive Superstore BI dashboard (open-source alternative to Power BI/Tableau).

Run from repository root:
    streamlit run dashboard/app.py

Charts use raw, historical educational data. Revenue and profit are USD.
Cross-filter categories via Plotly point selection; sidebar filters affect all panels.
"""
from pathlib import Path
import re
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data/raw/Sample_Superstore.csv"

st.set_page_config(page_title="Superstore — Executive BI", page_icon="📊", layout="wide")

@st.cache_data
def load_data() -> pd.DataFrame:
    if not CSV.is_file():
        raise FileNotFoundError(f"Missing {CSV}; run python scripts/download_data.py")
    df = pd.read_csv(CSV, encoding="utf-8-sig", dtype={"Postal Code": "string"})
    df.columns = [re.sub(r"[^a-z0-9]+", "_", col.lower()).strip("_") for col in df.columns]
    for col in ("order_date", "ship_date"):
        df[col] = pd.to_datetime(df[col], format="%Y-%m-%d")
    for col in ("sales", "profit", "discount", "quantity"):
        df[col] = pd.to_numeric(df[col], errors="raise")
    df["year"] = df["order_date"].dt.year
    df["month"] = df["order_date"].dt.strftime("%Y-%m")
    return df

try:
    all_data = load_data()
except Exception as exc:
    st.error("Unable to load dataset. Run: python scripts/download_data.py")
    st.exception(exc)
    st.stop()

st.title("Superstore | Executive Retail Performance")
st.caption("Historical educational sample · 2015–2018 · USD · each record is an order line")

with st.sidebar:
    st.header("Filters")
    selected_years = st.multiselect("Year", sorted(all_data.year.unique()), default=sorted(all_data.year.unique()))
    selected_regions = st.multiselect("Region", sorted(all_data.region.unique()), default=sorted(all_data.region.unique()))
    selected_cats = st.multiselect("Category", sorted(all_data.category.unique()), default=sorted(all_data.category.unique()))
    selected_segments = st.multiselect("Segment", sorted(all_data.segment.unique()), default=sorted(all_data.segment.unique()))
    selected_states = st.multiselect("State", sorted(all_data.state.unique()), default=sorted(all_data.state.unique()))
    st.caption("Click a category bar for additional cross-filtering. Select states and years here for drill-down.")

df = all_data.loc[
    all_data.year.isin(selected_years)
    & all_data.region.isin(selected_regions)
    & all_data.category.isin(selected_cats)
    & all_data.segment.isin(selected_segments)
    & all_data.state.isin(selected_states)
].copy()
if df.empty:
    st.warning("No rows match your filters.")
    st.stop()

sales, profit = float(df.sales.sum()), float(df.profit.sum())
c1, c2, c3, c4 = st.columns(4)
c1.metric("Sales", f"${sales:,.0f}")
c2.metric("Profit", f"${profit:,.0f}")
c3.metric("Margin", f"{profit / sales:.1%}" if sales else "N/A")
c4.metric("Orders", f"{df.order_id.nunique():,}")

a,b=st.columns(2)
with a:
    cats = df.groupby("category", as_index=False).agg(sales=("sales","sum"), profit=("profit","sum"))
    cats["margin"] = 100*cats.profit/cats.sales
    fig=px.bar(cats,x="category",y="profit",color="margin",color_continuous_scale="Viridis",
               title="Category profit — click a bar to filter",labels={"profit":"Profit (USD)","category":"Category"})
    fig.update_yaxes(rangemode="tozero")
    result=st.plotly_chart(fig,on_select="rerun",selection_mode="points",use_container_width=True,key="category_selection")
    chosen={p.get("x") for p in result.selection.points} if result and result.selection else set()
    drilled=df.loc[df.category.isin(chosen)].copy() if chosen else df.copy()
with b:
    monthly=drilled.groupby("month",as_index=False).agg(sales=("sales","sum"),profit=("profit","sum"))
    fig=px.line(monthly,x="month",y="sales",markers=True,title="Monthly sales",labels={"sales":"Sales (USD)"})
    st.plotly_chart(fig,use_container_width=True)

a,b=st.columns(2)
with a:
    sub=drilled.groupby("sub_category",as_index=False).agg(sales=("sales","sum"),profit=("profit","sum"))
    sub=sub.sort_values("profit")
    fig=px.bar(sub,x="profit",y="sub_category",orientation="h",color="profit",
               color_continuous_scale="RdBu",color_continuous_midpoint=0,title="Profit by product subcategory")
    fig.update_xaxes(zeroline=True)
    st.plotly_chart(fig,use_container_width=True)
with b:
    region=drilled.groupby("region",as_index=False).agg(sales=("sales","sum"),profit=("profit","sum"))
    fig=px.bar(region,x="region",y="profit",color="profit",title="Regional profitability",
               color_continuous_scale="RdBu",color_continuous_midpoint=0)
    fig.update_yaxes(rangemode="tozero")
    st.plotly_chart(fig,use_container_width=True)

a,b=st.columns(2)
with a:
    labels=["0%",">0–20%",">20–40%",">40%"]
    drilled["discount_group"]=pd.cut(drilled.discount,[-0.001,0,0.2,0.4,1],labels=labels,include_lowest=True)
    discounts=drilled.groupby("discount_group",observed=True,as_index=False).agg(sales=("sales","sum"),profit=("profit","sum"))
    discounts["margin_pct"]=100*discounts.profit/discounts.sales
    fig=px.bar(discounts,x="discount_group",y="margin_pct",color="margin_pct",title="Profit margin vs. discount")
    fig.update_yaxes(zeroline=True)
    st.plotly_chart(fig,use_container_width=True)
with b:
    sample=drilled.sample(n=min(len(drilled),2500),random_state=42)
    fig=px.scatter(sample,x="discount",y="profit",size="sales",color="category",
                   hover_data=["state","sub_category","sales"],title="Discount × profit (sample of lines)")
    st.plotly_chart(fig,use_container_width=True)

st.subheader("Geographic profitability — US states")
states=drilled.groupby("state",as_index=False).agg(sales=("sales","sum"),profit=("profit","sum"))
abbr={"Alabama":"AL","Arizona":"AZ","Arkansas":"AR","California":"CA","Colorado":"CO",
      "Connecticut":"CT","Delaware":"DE","District of Columbia":"DC","Florida":"FL",
      "Georgia":"GA","Idaho":"ID","Illinois":"IL","Indiana":"IN","Iowa":"IA","Kansas":"KS",
      "Kentucky":"KY","Louisiana":"LA","Maine":"ME","Maryland":"MD","Massachusetts":"MA",
      "Michigan":"MI","Minnesota":"MN","Mississippi":"MS","Missouri":"MO","Montana":"MT",
      "Nebraska":"NE","Nevada":"NV","New Hampshire":"NH","New Jersey":"NJ","New Mexico":"NM",
      "New York":"NY","North Carolina":"NC","North Dakota":"ND","Ohio":"OH","Oklahoma":"OK",
      "Oregon":"OR","Pennsylvania":"PA","Rhode Island":"RI","South Carolina":"SC",
      "South Dakota":"SD","Tennessee":"TN","Texas":"TX","Utah":"UT","Vermont":"VT",
      "Virginia":"VA","Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY"}
states["state_code"]=states.state.map(abbr)
fig=px.choropleth(states.dropna(subset=["state_code"]),locations="state_code",locationmode="USA-states",
                  color="profit",scope="usa",color_continuous_scale="RdBu",
                  color_continuous_midpoint=0,hover_name="state",hover_data=["sales","profit"],
                  title="State total profit, USD")
st.plotly_chart(fig,use_container_width=True)

st.subheader("Audit / export")
st.dataframe(drilled[["order_id","order_date","region","state","category","sub_category","sales","quantity","discount","profit"]],
             hide_index=True,use_container_width=True,height=320)
st.download_button("Download filtered CSV",drilled.to_csv(index=False).encode("utf-8"),"filtered_superstore.csv","text/csv")
st.caption("Profit margin = SUM(profit)/SUM(sales). Descriptive association does not prove causation.")
