# 10-Minute Team Presentation — Speaker Notes

**Topic:** The Cost of Discounting: Why Strong Retail Revenue Does Not Guarantee Profitability  
**Language:** English (adjust to your instructor's preference)  
**Format:** Exactly 5 students × approximately 2 minutes each.  
**Dataset:** Sample Superstore, 2015–2018. Historical educational retail sample.  

Four participants have been identified. The fifth name and student ID are still pending because the assignment requires exactly five participants.

| Participant | Slides | Approx. time | Responsibility |
|---|---:|---:|---|
| **Juan Manuel Sánchez Hernández (2302084) — Story Lead** | 1–2 | 0:00–2:00 | Setup, business question |
| **Seir Mendoza Vidal (2302072) — Data Architect** | 3–4 | 2:00–4:00 | Data preparation, trend |
| **José Rodrigo de la Cruz Chim (2302089) — Python Specialist** | 5–6 | 4:00–6:00 | Categories, distribution/line profitability |
| **Marco Antonio Caamal Chi (2302075) — BI Lead** | 7–8 | 6:00–8:00 | Discount effect, geographic drill-down and dashboard demonstration |
| **[Fifth member: name and ID pending] — QA & Integration** | 9–10 | 8:00–10:00 | Recommendations, limitations, close |

## Juan Manuel Sánchez Hernández (2302084) — Opening and Business Challenge (slides 1–2)

"Good morning. Our final project is called **The Cost of Discounting**. Our goal is not only to visualize sales, but to use data to support business decisions. We used the Sample Superstore educational dataset to explore retail activity over four years, from 2015 to 2018.

Imagine that you manage a retail company and you see increasing sales. That sounds like excellent news. But does selling more necessarily mean earning more? High revenue could hide unprofitable product lines, discounts, or regional operations.

Our central question is: **Why do some categories and regions sell a lot without producing healthy profit?** We will answer that using business intelligence tools, Python visualizations, and a clear narrative. First, we establish the business context. Next, we uncover the most important patterns. Finally, we make recommendations that a management team could test.

The key performance measures are total sales, total profit, profit margin, and unique orders. We will compare these across categories, discount levels, dates, and states. With that context established, my teammate will explain how the dataset was prepared and what the overall trends show."

**Transition:** “Now let's see the data behind the analysis.”

## Seir Mendoza Vidal (2302072) — Dataset and Time Trend (slides 3–4)

"We worked with **9,994 order lines**, representing **5,009 distinct orders** and **793 customers**. One important detail is that a single order can contain several product lines. Therefore, we count unique order IDs instead of treating every row as a separate order.

The dataset includes continuous measures such as sales and profit, categorical fields such as category and region, dates, and geographic fields such as state and city. This makes it a good choice for the assignment.

Our technical workflow followed five stages: acquiring the public CSV, checking data quality, transforming fields with Pandas, visualizing patterns in Python and BI software, and making recommendations. We found **11 missing postal codes**. We did not invent values for them, because that would make geographic analysis less trustworthy.

Looking at the year-by-year chart, revenue increased from approximately **$484,000 in 2015** to **$733,000 in 2018**. Total profit also grew, but the business still shows uneven margins. In 2018, sales grew about **20.4%** compared with 2017, while the overall profit margin for 2018 was about **12.74%**.

These findings are useful, but an aggregate trend is not enough. To understand performance, we need to break the numbers down by product categories and subcategories."

**Transition:** “The next section explains where the margin problem is concentrated.”

## José Rodrigo de la Cruz Chim (2302089) — Category and Product-Line Profitability (slides 5–6)

"We calculated **weighted profit margins** as total profit divided by total sales for each group. This is different from simply averaging the profit margin of every row, which can produce misleading results.

Our first major insight is that **Technology** and **Office Supplies** generate profit margins of about **17%**, while **Furniture** generates only **2.49%**. Furniture sells roughly **$742,000**, but produces only about **$18,451** in profit. That is a strong example of why revenue alone cannot tell the entire business story.

To investigate further, we looked at individual subcategories. **Tables** generated around **$207,000** in sales but lost approximately **$17,725**. **Bookcases** lost another **$3,473** on approximately **$115,000** in sales.

In our Python notebook, we also use histograms, density plots, box plots and confidence intervals to study the distribution and uncertainty of profitability. Averages can hide extreme values, so it is important to inspect variation and outliers. We use correlation analysis carefully, because association does not prove cause and effect.

Based on these results, we would recommend reviewing supplier costs, prices and discount practices for specific furniture lines, rather than applying the same policy to every product."

**Transition:** “Now we'll connect profitability to discounts and geography.”

## Marco Antonio Caamal Chi (2302075) — Discounts, Geography and BI Interaction (slides 7–8)

"We divided order lines into four discount groups: no discount, discounts up to 20%, discounts between 20 and 40%, and discounts above 40%.

The results show an important pattern: the groups with discounts **above 20%** produce a combined negative profit of approximately **$135,000**. Orders with no discount are highly profitable in aggregate. This makes discount policy a strong candidate for further investigation.

However, we must make a distinction. The dataset shows a **relationship**, but it does not prove that discounts caused the losses. Certain products may be discounted because they are already difficult to sell, or because they have different cost structures.

The geographic analysis highlights additional concerns. **Texas** loses about **$25,700** in profit despite producing about **$170,000** in sales. Ohio, Pennsylvania and Illinois also show meaningful losses.

[**Optional 15–20-second demo:** Open the Streamlit dashboard or the native BI file, apply a category filter, then select a region and show how the other charts update. If the live dashboard is not ready, point to the charts on slides 7 and 8 instead.]

These patterns demonstrate why interactive filtering and drill-down matter: managers need to identify which combinations of products, promotions and locations require attention."

**Transition:** “We will finish with practical recommendations and limitations.”

## [Fifth member: name and ID pending] — Recommendations, Quality Checks and Closing (slides 9–10)

"Our team proposes three concrete actions.

First, introduce a controlled pilot for discounts over **20%**. We would not simply ban every larger discount. Instead, we would test a manager-approval process, compare similar customer groups and measure both margin and conversion rates.

Second, review the **Tables** and **Bookcases** product lines. Their negative profits suggest a need to examine purchase costs, pricing, logistics and product-level promotions.

Third, perform a focused regional review of **Texas, Ohio, Pennsylvania and Illinois**. We should look at local product mix and discount patterns rather than assuming that geography alone explains losses.

For data quality, we verified totals against the original CSV, preserved missing postal-code values instead of inventing them, and used zero-based bar charts and readable colors. Our notebook includes commented statistical transformations and reproducible visualizations.

There are also important limitations. This is an **educational sample**, not a live company's financial data. The results are descriptive; they do not estimate the future effects of any proposed intervention.

Our final message is simple: **optimize profit, not revenue alone**. Business intelligence becomes useful when we connect reliable data, appropriate charts and clear decisions. Thank you."

## Final checks before class

- Rehearse with a timer: 120 seconds per speaker including slide changes; reduce text if needed.
- Add each member's real name to slide 1, the repository README and this script.
- Execute the notebook with **Restart & Run All**, and verify generated PNG, SVG and HTML files.
- Run the interactive dashboard and verify selections and filtering.
- Prefer delivering the native `.pbix` or `.twbx` named in the assignment in addition to the Streamlit source.
- Make the GitHub repository accessible to the professor. A private GitHub repository does **not** permit “anyone with the link” without explicit access.
- Confirm that all five students speak, that the slides match the actual data, and that the presentation lasts exactly around 10 minutes.