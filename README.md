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
| Native Tableau/Power BI | `*.twbx` or `*.pbix` | **NOT CREATED**; see `POWER_BI_GUIDE.md` |
| GitHub repository URL | — | **Not yet published** |

The assignment allows an open-source tool in Step 1 option C, but **its final deliverables explicitly request .twbx or .pbix**. We therefore must not claim that Streamlit is guaranteed to satisfy the native dashboard-file rubric. Confirm with the instructor or create the native deliverable.

## Project layout

```text
database-knowledge-extraction/
├── final_visualizations.ipynb
├── data/
│   ├── raw/Sample_Superstore.csv
│   ├── processed/superstore_clean.csv
│   └── verified_summary.json
├── dashboard/app.py
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
│   └── qa.py
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

Repository has been initialized locally, but no GitHub remote was created. Before the deadline, publish the project to a **public** repository or grant explicit access to the evaluator. Private GitHub repository URLs are *not* accessible merely through an unlisted URL.

```bash
gh repo create database-knowledge-extraction --public --source=. --remote=origin --push
```

Only run that command with the team's authorization, and verify the URL in a private browser window. The source video from the latest class was not attached; the team still needs to watch it.

## Limitations

Data are historical and educational; no causal or predictive conclusion is established. Confidence intervals in the notebook are bootstrap estimates, not guarantees. Revenue is not profit. Bars begin at zero; signed profit uses a diverging color treatment.
