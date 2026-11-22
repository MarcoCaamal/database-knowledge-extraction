# Power BI Native Deliverable — `.pbix`

**IMPORTANT:** `dashboard/app.py` is a functional open-source alternative, but the final requirements explicitly ask for a `.pbix` or `.twbx`. This guide explains how the team can produce a native Power BI deliverable on Windows.

1. Open **Power BI Desktop** on Windows.
2. Click **Get Data → Text/CSV** and import `data/processed/superstore_clean.csv` (after running the notebook).
3. Under **Transform data**, set `order_date` and `ship_date` as dates, `sales`/`profit` as decimal numbers, `discount` as decimal, `row_id` as whole number. IDs/postal codes must remain text.
4. Name the table `OrderLines`. Create these DAX measures (Modeling → New measure):

```dax
Total Sales = SUM(OrderLines[sales])
Total Profit = SUM(OrderLines[profit])
Profit Margin % = DIVIDE([Total Profit], [Total Sales], 0)
Distinct Orders = DISTINCTCOUNT(OrderLines[order_id])
Order Lines = COUNTROWS(OrderLines)
Loss-Making Lines = CALCULATE([Order Lines], OrderLines[profit] < 0)
Avg Discount % = AVERAGE(OrderLines[discount])
```

5. Build a **16:9 executive dashboard** with four cards at the top for sales, profit, profit margin and distinct orders.
6. Add visuals:
   - Line chart: `order_date` (month/year) → `[Total Sales]`.
   - Clustered bar chart: `category` → `[Total Profit]`; color negative values differently.
   - Bar chart: `discount_band` → `[Profit Margin %]`.
   - Map / filled map: `state` → `[Total Profit]` (set data category to State or Province, country = United States).
   - Matrix / table: `region`, `category` → Sales, Profit, Profit Margin.
7. Add **slicers** for `year`, `region`, `category` and `segment`.
8. Use **Format → Edit interactions** to make charts cross-filter others rather than ignore filters. Add a drill-down hierarchy: `category` → `sub_category` → `product_name`.
9. Apply accessible sequential colors for magnitudes and a diverging palette for negative vs positive values; bars must start at zero. Test selections and compare headline numbers with `data/verified_summary.json`.
10. Save as `dashboard/Superstore_Executive_Dashboard.pbix`. Commit the file and link the public-access GitHub repository.

**Sanity checks (all years selected):** $2,297,200.86 sales, $286,397.02 profit, 5,009 distinct orders, weighted margin approximately 12.47%.

**Presentation justification if using Streamlit instead:** The assignment's setup section explicitly accepts an open-source BI option with explanation; Streamlit + Plotly enables filters, selection-based chart filtering and data drill-down without proprietary desktop software. **Still request approval** if the instructor grades strictly by file extension.