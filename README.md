# Maternal Health Risk Analytics Dashboard
### Risk Classification & Prediction Model Analysis | Excel · Python · Data Visualization

---

## 📋 PROJECT OVERVIEW

An end-to-end data analysis project exploring **1,014 maternal health patient records**, focusing on risk classification (high, mid, low), vital signs patterns, demographic breakdowns, and the accuracy of two prediction models — an IF-based model and a Score-based model.

The project demonstrates the full analytics workflow: raw data → exploration → multi-sheet Excel dashboard → Python visualizations → written insights.

---

## 🎯 BUSINESS QUESTIONS ANSWERED

1. What proportion of patients fall into each risk category, and who is most affected?
2. Which vital signs most strongly distinguish high-risk from low-risk patients?
3. How does age relate to maternal health risk level?
4. Which prediction model — IF-based or Score-based — is more accurate overall?
5. Does prediction accuracy vary across the three risk categories?

---

## 📁 PROJECT STRUCTURE

```
maternal-health-analytics/
│
├── data/
│   └── Maternal_Health_Risk_Data_Set.xlsx     # Source data (1,014 records)
│
├── excel/
│   └── Maternal_Health_Dashboard.xlsx         # Full Excel dashboard (5 sheets)
│
├── python/
│   └── maternal_health_analysis.py            # Analysis & visualizations
│
├── visuals/
│   ├── fig1_risk_demographics.png             # Risk distribution & age breakdown
│   ├── fig2_vital_signs.png                   # Vital signs analysis
│   └── fig3_prediction_accuracy.png           # Model accuracy comparison
│
└── README.md
```

---

## 🔍 KEY FINDINGS

| Metric | Value |
|---|---|
| Total Patients | 1,014 |
| High Risk | **272 (26.8%)** |
| Mid Risk | 336 (33.1%) |
| Low Risk | 406 (40.0%) |
| Avg Age — High Risk | 36.2 years |
| Avg Age — Low Risk | 26.9 years |
| Avg Systolic BP — High Risk | 124.2 mmHg |
| Avg Blood Sugar — High Risk | 12.1 mmol/L |
| IF Model Overall Accuracy | **53.9%** |
| Score Model Overall Accuracy | 53.1% |
| IF Model — High Risk Detection | **81.2%** |
| Score Model — High Risk Detection | 43.8% |

**Highlighted Insights:**
- High risk patients are on average **9 years older** than low risk patients (36.2 vs 26.9 years)
- Blood sugar is the strongest risk differentiator — high risk avg 12.1 vs low risk 7.2 mmol/L, a 68% difference
- Systolic BP gap of 18.3 mmHg between high and low risk patients is clinically significant
- The IF model is dramatically better at detecting high risk patients (81.2% vs 43.8%)
- The Score model performs better for low risk detection (46.8% vs 21.4%)
- Older Adults (40+) have the highest concentration of high risk cases (120 patients)
- Teens (10–19) are predominantly low risk (139 patients) — the safest demographic

---

## 🛠️ TOOLS & SKILLS DEMONSTRATED

**Microsoft Excel**
- Multi-sheet dashboard architecture with dark professional theme
- KPI summary cards, clinical reference tables, model comparison matrices
- Conditional colour coding by risk level (red / amber / green)
- Pivot-style aggregation tables across risk, age group, and hospital metrics

**Python**
- `pandas` — data loading, groupby analysis, age group engineering, aggregation
- `matplotlib` — multi-panel figures, box plots, histograms, scatter plots, bar charts, donut charts
- `seaborn` — confusion matrix heatmaps for model evaluation
- Custom dark-theme styling via `rcParams`
- Clean, documented, reusable code

**Analytical Skills**
- Risk stratification and clinical threshold analysis
- Demographic segmentation by age group
- Vital signs interpretation against clinical normal ranges
- Prediction model evaluation — confusion matrices, accuracy by class
- Data storytelling — connecting numbers to clinical meaning

---

## ▶️ HOW TO RUN

```bash
# Clone the repository
git clone https://github.com/laurel-anangwe/maternal-health-analytics.git
cd maternal-health-analytics

# Install dependencies
pip install pandas matplotlib seaborn openpyxl

# Run the analysis
python python/maternal_health_analysis.py
```

Output: 3 high-resolution visualization figures saved to `/visuals/`

---

## 📸 Dashboard Preview

**Overview & KPIs**
![Dashboard Overview](dashboard-overview.png)

**Risk Analysis**
![Risk Analysis](dashboard-risk.png)

**Vital Signs**
![Vital Signs](dashboard-vitals.png)

---

## 🔮 POTENTIAL EXTENSIONS

- **Logistic Regression model** in Python to improve prediction accuracy beyond 53.9%
- **Power BI / Tableau** interactive dashboard version
- **Feature importance analysis** — quantify which vital sign contributes most to risk
- **Age-stratified analysis** — separate models for teens vs adults vs older adults

---
---

*Maternal Health Risk Analytics — built with Excel & Python | Dataset: Maternal_Health_Risk_Data_Set.xlsx*
