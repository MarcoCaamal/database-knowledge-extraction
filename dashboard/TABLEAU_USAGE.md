# Tableau native dashboard — delivered artifact

**File to submit:** `dashboard/Superstore_Executive_Dashboard.twbx`  
**Workbook source (for version control):** `dashboard/Superstore_Executive_Dashboard.twb`  
**Packaged data:** `dashboard/sales_orders.csv` (9,994 rows)

## Open it

1. Use Tableau Desktop or Tableau Public on a supported Windows/macOS computer.
2. Open `Superstore_Executive_Dashboard.twbx`.
3. Select the **Superstore Executive BI** dashboard.
4. Inspect the four worksheets:
   - **Category Profit** — SUM(Profit) by category.
   - **Monthly Sales** — SUM(Sales) by month.
   - **US State Profit** — geographic profit by state.
   - **Discount Band Profit** — SUM(Profit) by discount grouping.
5. Click a category in **Category Profit** and inspect other views for cross-filtering; deselect to reset.
6. Confirm values match `data/verified_summary.json`: sales ~**$2,297,201**, profit ~**$286,397**.
7. Save from Tableau after any layout adjustments before submitting.

## Verification performed

- Generated using a real Tableau workbook XML template adapted for the Superstore dataset.
- All 9,994 original line items are embedded as CSV inside the TWBX ZIP package.
- Source workbook passes **official 2026.1 Tableau workbook XSD** syntax validation.
- Workbook passes **8/8 additional cross-reference and worksheet/window checks**.
- No stale external Windows Hyper extract path remains.
- No stale thumbnails from the reference workbook remain.
- Bundle ZIP integrity and embedded totals were verified in `scripts/qa.py`.

**Important limitation:** This Linux workspace does not have Tableau Desktop/Public installed. No actual Tableau renderer or semantic loading test was possible. The structural checks are comprehensive but **do not guarantee it will open and display correctly**. Open it in Tableau before final submission.

## Regeneration

```bash
cd ~/projects/database-knowledge-extraction
.venv/bin/python scripts/build_tableau_workbook.py
.venv/bin/python scripts/qa.py
```

Regeneration needs internet to retrieve the public Tableau reference XML template. The delivered `.twbx` is self-contained and does not need that source template.

**Reference template:** [Kilo-Org Tableau dashboard creator](https://github.com/Kilo-Org/kilo-marketplace/tree/main/skills/tableau-dashboard-creator/references/snippets/dashboard) and the [Tableau workbook XML schema](https://github.com/tableau/tableau-document-schemas).

## Project team

| Student | ID |
|---|---|
| Juan Manuel Sánchez Hernández | 2302084 |
| Seir Mendoza Vidal | 2302072 |
| José Rodrigo de la Cruz Chim | 2302089 |
| Marco Antonio Caamal Chi | 2302075 |
| **Fifth member pending** | **Pending** |

The assignment requires **exactly five students**. Do not submit with only four names without confirming the missing participant.
