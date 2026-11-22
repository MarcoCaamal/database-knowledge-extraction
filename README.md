# Enterprise Multi-Modal Data Visualization & Storytelling

**Course:** Database Knowledge Extraction  |  **Deadline:** November 24, 2026 at 23:59  |  **Team:** exactly 5 students

## Executive question

**Why can revenue growth coexist with weak profitability?**

We investigate a historical educational retail dataset (Sample Superstore, 2015–2018), using Python statistical analyses, an interactive open-source BI dashboard, and an executive presentation. This is a classroom dataset, not an audited real business.

## Data

Original (public CSV): https://raw.githubusercontent.com/mikemooreviz/superstore/master/superstore.csv

- **9,994** order lines; **5,009** orders; **793** customers.
- **$2,297,200.86** total revenue; **$286,397.02** total profit; **12.47%** weighted margin.
- **Furniture**: $741,999.80 sales and only **2.49%** margin.
- **Tables**: −$17,725.48; **Bookcases**: −$3,472.56 profit.
- Groups with discounts **above 20%** have negative aggregate profit. This is an **association**, not proof that discounts cause losses.
- 11 postal codes are missing; they are treated as unknown (not invented).

Recompute aggregate verification: `python scripts/verify_data.py`.

## Current deliverables (created directly in this workspace)

| Deliverable | Location | Status |
| --- | --- | --- |
| Python notebook | `final_visualizations.ipynb` | **Executed successfully** against real CSV |
| Notebook charts | `outputs/figures/` | PNG, SVG and interactive HTML generated |
| Analytical tables | `outputs/tables/` | Generated |
| Clean dataset | `data/processed/superstore_clean.csv` | Generated |
| Interactive open-source BI dashboard | `dashboard/app.py` | **Starts and responds over HTTP**; interactive cross-filtering needs live demonstration |
| Executive presentation (PowerPoint) | `presentation/Superstore_Executive_Story.pptx` | **10 editable slides**; team name placeholders pending |
| Executive presentation (PDF) | `presentation/Superstore_Executive_Story.pdf` | **10 pages** |
| Team presentation script | `presentation/TEAM_SCRIPT.md` | Ten-minute plan split into five parts |
| Native Tableau/Power BI | `dashboard/Superstore_Executive_Dashboard.twbx` | **Generated** with four worksheets, one dashboard and packaged CSV; XML/schema validated, Tableau Desktop visual test pending |
| GitHub repository URL | https://github.com/MarcoCaamal/database-knowledge-extraction | **Published publicly** |

The assignment's final deliverables request `.twbx` or `.pbix`. **A packaged Tableau `.twbx` is now included**, alongside the open-source Streamlit alternative. It passed the official Tableau 2026.1 XSD and eight additional XML checks, but must still be opened in Tableau Desktop/Public on a supported Windows/macOS computer before final submission.

## Project layout

```text
database-knowledge-extraction/
├── final_visualizations.ipynb
├── data/
│   ├── raw/Sample_Superstore.csv
│   ├── processed/superstore_clean.csv
│   └── verified_summary.json
├── dashboard/
│   ├── app.py                   # tested open-source Streamlit dashboard
│   ├── Superstore_Executive_Dashboard.twbx  # packaged native Tableau workbook
│   ├── Superstore_Executive_Dashboard.twb   # XML source
│   └── sales_orders.csv         # packaged 9,994-line CSV
├── outputs/
│   ├── figures/             # PNG, SVG, interactive Plotly HTML
│   └── tables/              # CSV aggregations and bootstrap CI
├── presentation/
│   ├── Superstore_Executive_Story.pptx
│   ├── Superstore_Executive_Story.pdf
│   ├── TEAM_SCRIPT.md
│   └── assets/              # figures used by slides
├── scripts/
│   ├── download_data.py
│   ├── verify_data.py
│   ├── build_presentation.py
│   ├── qa.py
│   └── build_tableau_workbook.py
├── POWER_BI_GUIDE.md
├── INSTRUCCIONES_PARA_ENTREGA.md
└── requirements.txt
```

## Run locally (Linux/macOS)

The workspace already has a tested Python environment at `.venv/` and downloaded source data. If a new machine is needed:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/download_data.py
```

To inspect or rerun the reproducible analyses:

```bash
.venv/bin/jupyter lab final_visualizations.ipynb
.venv/bin/python scripts/verify_data.py
.venv/bin/python scripts/build_presentation.py
.venv/bin/streamlit run dashboard/app.py
.venv/bin/python scripts/qa.py
```

To rerun the notebook noninteractively:

```bash
.venv/bin/jupyter nbconvert --to notebook --execute final_visualizations.ipynb --output final_visualizations.ipynb
```

## BI interaction demonstration

Use the left sidebar to filter by **year, region, category, segment and state**; select a category bar for cross-filtering. Show category profitability, monthly sales, product-level losses, discounts, the US state choropleth and exportable records.

## Storytelling & team presentation

Our arc: **Setup → Conflict/Insight → Resolution**. All five students should speak for ~2 minutes each. Replace the five placeholders in the cover slide and script. Follow `presentation/TEAM_SCRIPT.md`.

## GitHub publishing and access

The project is already published in a public GitHub repository: **https://github.com/MarcoCaamal/database-knowledge-extraction**. Validate that the repository opens without signing in. Public repositories are viewable by everyone with the URL.

```bash
git push origin main
```

This repository already has an `origin` remote, so do **not** create it a second time. Use `git push` for updates. The source video from the latest class was not attached; the team still needs to watch it.

## Limitations

Data are historical and educational; no causal or predictive conclusion is established. Confidence intervals in the notebook are bootstrap estimates, not guarantees. Revenue is not profit. Bars begin at zero; signed profit uses a diverging color treatment.
