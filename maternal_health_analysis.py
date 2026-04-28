"""
Maternal Health Risk Analysis
==============================
Author  : [Your Name]
Dataset : Maternal_Health_Risk_Data_Set.xlsx  |  1,014 patients
Purpose : Exploratory data analysis and visualization of maternal health
          risk classification, vital signs patterns, and prediction model
          accuracy comparison across high, mid, and low risk patients.

Usage:
    python maternal_health_analysis.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ── Theme ──────────────────────────────────────────────────────────────
DARK_BG    = "#0D1117"
CARD_BG    = "#161B22"
HIGH_RED   = "#E74C3C"
MID_AMBER  = "#F39C12"
LOW_GREEN  = "#27AE60"
PINK       = "#E91E8C"
BLUE       = "#2E86AB"
TEAL       = "#00BFA5"
WHITE      = "#FFFFFF"
LIGHT_GREY = "#8B949E"
PALETTE    = [HIGH_RED, MID_AMBER, LOW_GREEN, PINK, BLUE, TEAL]

plt.rcParams.update({
    "figure.facecolor": DARK_BG,
    "axes.facecolor":   CARD_BG,
    "axes.edgecolor":   "#21262D",
    "axes.labelcolor":  LIGHT_GREY,
    "axes.titlecolor":  WHITE,
    "text.color":       WHITE,
    "xtick.color":      LIGHT_GREY,
    "ytick.color":      LIGHT_GREY,
    "grid.color":       "#21262D",
    "grid.linestyle":   "--",
    "grid.alpha":       0.4,
    "font.family":      "DejaVu Sans",
})

# ── Load Data ──────────────────────────────────────────────────────────
print("Loading data...")
xl   = pd.read_excel('/mnt/user-data/uploads/Maternal_Health_Risk_Data_Set.xlsx', sheet_name=None)
df   = xl['Maternal Health Risk Data Set'].copy()
pred = xl['IF Prediction'].copy()
scr  = xl['ScorePrediction'].copy()

def age_group(a):
    if a < 20:   return 'Teen (10-19)'
    elif a < 30: return 'Young Adult (20-29)'
    elif a < 40: return 'Adult (30-39)'
    else:        return 'Older Adult (40+)'

df['AgeGroup'] = df['Age'].apply(age_group)

total          = len(df)
risk_counts    = df['RiskLevel'].value_counts()
vitals_by_risk = df.groupby('RiskLevel')[
    ['SystolicBP','DiastolicBP','Blood Sugar','BodyTemp','HeartRate']].mean()
age_risk       = df.groupby(['AgeGroup','RiskLevel']).size().unstack(fill_value=0)
if_acc         = round(pred['CorrectPrediction'].eq('Correct').mean()*100,1)
sc_acc         = round(scr['CorrectPrediction'].eq('Correct').mean()*100,1)
if_by_risk     = pred.groupby(['RiskLevel','CorrectPrediction']).size().unstack(fill_value=0)
sc_by_risk     = scr.groupby(['RiskLevel','CorrectPrediction']).size().unstack(fill_value=0)

print(f"  ✓ {total:,} patients | High: {risk_counts.get('high risk',0)} | "
      f"Mid: {risk_counts.get('mid risk',0)} | Low: {risk_counts.get('low risk',0)}")

# ══════════════════════════════════════════════════════════════════════
# FIGURE 1 — RISK DISTRIBUTION & DEMOGRAPHICS
# ══════════════════════════════════════════════════════════════════════
print("Generating Figure 1: Risk Distribution & Demographics...")
fig1 = plt.figure(figsize=(20, 14), facecolor=DARK_BG)
fig1.suptitle("MATERNAL HEALTH RISK ANALYTICS  •  Risk Distribution & Demographics",
              fontsize=16, fontweight='bold', color=PINK, y=0.98)
gs = gridspec.GridSpec(2, 3, figure=fig1, hspace=0.45, wspace=0.38)

# 1A — Risk level donut
ax1 = fig1.add_subplot(gs[0, 0])
r_vals  = [risk_counts.get('high risk',0), risk_counts.get('mid risk',0), risk_counts.get('low risk',0)]
r_colors= [HIGH_RED, MID_AMBER, LOW_GREEN]
ax1.pie(r_vals, colors=r_colors,
        wedgeprops=dict(width=0.55, edgecolor=DARK_BG, linewidth=2), startangle=90)
ax1.text(0, 0.1, f'{total:,}', ha='center', va='center',
         fontsize=14, fontweight='bold', color=WHITE)
ax1.text(0, -0.2, 'patients', ha='center', va='center', fontsize=9, color=LIGHT_GREY)
ax1.set_title("Risk Level Distribution", fontsize=12, fontweight='bold', pad=10)
patches = [mpatches.Patch(color=c, label=f'{l}  {v:,}  ({round(v/total*100,1)}%)')
           for c,l,v in zip(r_colors,['High Risk','Mid Risk','Low Risk'],r_vals)]
ax1.legend(handles=patches, loc='lower center', fontsize=8,
           framealpha=0, labelcolor=LIGHT_GREY, ncol=1, bbox_to_anchor=(0.5,-0.18))

# 1B — Age distribution by risk (stacked bar)
ax2 = fig1.add_subplot(gs[0, 1:])
age_order = ['Teen (10-19)','Young Adult (20-29)','Adult (30-39)','Older Adult (40+)']
x = range(len(age_order))
h_vals = [int(age_risk.loc[ag,'high risk']) if ag in age_risk.index and 'high risk' in age_risk.columns else 0 for ag in age_order]
m_vals = [int(age_risk.loc[ag,'mid risk'])  if ag in age_risk.index and 'mid risk'  in age_risk.columns else 0 for ag in age_order]
l_vals = [int(age_risk.loc[ag,'low risk'])  if ag in age_risk.index and 'low risk'  in age_risk.columns else 0 for ag in age_order]
b1 = ax2.bar(x, h_vals, label='High Risk', color=HIGH_RED, alpha=0.9, width=0.55)
b2 = ax2.bar(x, m_vals, label='Mid Risk',  color=MID_AMBER, alpha=0.9, width=0.55, bottom=h_vals)
b3 = ax2.bar(x, l_vals, label='Low Risk',  color=LOW_GREEN, alpha=0.9, width=0.55,
             bottom=[h+m for h,m in zip(h_vals,m_vals)])
for bars in [b1,b2,b3]:
    for bar in bars:
        h = bar.get_height()
        if h > 15:
            ax2.text(bar.get_x()+bar.get_width()/2,
                     bar.get_y()+h/2, str(int(h)),
                     ha='center', va='center', fontsize=8, color=WHITE, fontweight='bold')
ax2.set_xticks(x); ax2.set_xticklabels(age_order, fontsize=9)
ax2.set_ylabel("Patient Count", fontsize=9)
ax2.set_title("Patient Count by Age Group & Risk Level", fontsize=12, fontweight='bold', pad=10)
ax2.legend(fontsize=9, framealpha=0, labelcolor=LIGHT_GREY, loc='upper right')
ax2.grid(axis='y'); ax2.spines['top'].set_visible(False); ax2.spines['right'].set_visible(False)

# 1C — Age box plot by risk
ax3 = fig1.add_subplot(gs[1, 0])
risk_order = ['low risk','mid risk','high risk']
risk_labels= ['Low Risk','Mid Risk','High Risk']
data_bp    = [df[df['RiskLevel']==r]['Age'].values for r in risk_order]
bp = ax3.boxplot(data_bp, patch_artist=True, notch=False,
                 medianprops=dict(color=WHITE, linewidth=2),
                 whiskerprops=dict(color=LIGHT_GREY),
                 capprops=dict(color=LIGHT_GREY),
                 flierprops=dict(marker='o', color=LIGHT_GREY, alpha=0.4, markersize=3))
for patch, color in zip(bp['boxes'], [LOW_GREEN, MID_AMBER, HIGH_RED]):
    patch.set_facecolor(color); patch.set_alpha(0.7)
ax3.set_xticklabels(risk_labels, fontsize=9)
ax3.set_ylabel("Age (years)", fontsize=9)
ax3.set_title("Age Distribution by Risk Level", fontsize=12, fontweight='bold', pad=10)
ax3.grid(axis='y'); ax3.spines['top'].set_visible(False); ax3.spines['right'].set_visible(False)

# 1D — Age histogram overlay
ax4 = fig1.add_subplot(gs[1, 1:])
for risk, color, label in zip(risk_order, [LOW_GREEN, MID_AMBER, HIGH_RED], risk_labels):
    data = df[df['RiskLevel']==risk]['Age']
    ax4.hist(data, bins=20, alpha=0.5, color=color, label=label, edgecolor='none')
ax4.axvline(df['Age'].mean(), color=WHITE, linestyle='--', alpha=0.6, linewidth=1.5)
ax4.text(df['Age'].mean()+0.5, ax4.get_ylim()[1]*0.85 if ax4.get_ylim()[1]>0 else 10,
         f'avg {df["Age"].mean():.1f}y', fontsize=8, color=WHITE, alpha=0.7)
ax4.set_xlabel("Age (years)", fontsize=9); ax4.set_ylabel("Frequency", fontsize=9)
ax4.set_title("Age Distribution Histogram by Risk Level", fontsize=12, fontweight='bold', pad=10)
ax4.legend(fontsize=9, framealpha=0, labelcolor=LIGHT_GREY)
ax4.grid(axis='y'); ax4.spines['top'].set_visible(False); ax4.spines['right'].set_visible(False)

plt.savefig('/home/claude/fig1_risk_demographics.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
plt.close()
print("  ✓ Figure 1 saved")

# ══════════════════════════════════════════════════════════════════════
# FIGURE 2 — VITAL SIGNS ANALYSIS
# ══════════════════════════════════════════════════════════════════════
print("Generating Figure 2: Vital Signs Analysis...")
fig2 = plt.figure(figsize=(20, 14), facecolor=DARK_BG)
fig2.suptitle("MATERNAL HEALTH RISK ANALYTICS  •  Vital Signs Analysis",
              fontsize=16, fontweight='bold', color=TEAL, y=0.98)
gs2 = gridspec.GridSpec(2, 3, figure=fig2, hspace=0.45, wspace=0.38)

vitals = ['SystolicBP','DiastolicBP','Blood Sugar','BodyTemp','HeartRate']
vital_labels = ['Systolic BP\n(mmHg)','Diastolic BP\n(mmHg)','Blood Sugar\n(mmol/L)','Body Temp\n(°F)','Heart Rate\n(bpm)']

# 2A — Grouped bar: average vitals by risk
ax5 = fig2.add_subplot(gs2[0, :2])
x = range(len(vitals))
w = 0.25
for i,(risk,color,label) in enumerate(zip(risk_order,[LOW_GREEN,MID_AMBER,HIGH_RED],risk_labels)):
    vals = [vitals_by_risk.loc[risk,v] for v in vitals]
    # Normalize for display — use percentage of max
    bars = ax5.bar([xi + i*w for xi in x], vals, w, label=label, color=color, alpha=0.85)
ax5.set_xticks([xi+w for xi in x]); ax5.set_xticklabels(vital_labels, fontsize=9)
ax5.set_title("Average Vital Signs by Risk Level", fontsize=12, fontweight='bold', pad=10)
ax5.legend(fontsize=9, framealpha=0, labelcolor=LIGHT_GREY)
ax5.grid(axis='y'); ax5.spines['top'].set_visible(False); ax5.spines['right'].set_visible(False)

# 2B — Blood sugar violin plot
ax6 = fig2.add_subplot(gs2[0, 2])
bs_data = [df[df['RiskLevel']==r]['Blood Sugar'].values for r in risk_order]
parts = ax6.violinplot(bs_data, positions=[1,2,3], showmeans=True, showmedians=False)
for i,(pc,color) in enumerate(zip(parts['bodies'],[LOW_GREEN,MID_AMBER,HIGH_RED])):
    pc.set_facecolor(color); pc.set_alpha(0.6)
for part in ['cbars','cmins','cmaxes','cmeans']:
    if part in parts: parts[part].set_color(WHITE)
ax6.set_xticks([1,2,3]); ax6.set_xticklabels(['Low','Mid','High'], fontsize=9)
ax6.set_ylabel("Blood Sugar (mmol/L)", fontsize=9)
ax6.set_title("Blood Sugar Distribution\nby Risk Level", fontsize=11, fontweight='bold', pad=10)
ax6.grid(axis='y'); ax6.spines['top'].set_visible(False); ax6.spines['right'].set_visible(False)

# 2C — Systolic vs Diastolic BP scatter
ax7 = fig2.add_subplot(gs2[1, :2])
for risk, color, label in zip(risk_order,[LOW_GREEN,MID_AMBER,HIGH_RED],risk_labels):
    sub = df[df['RiskLevel']==risk]
    ax7.scatter(sub['DiastolicBP'], sub['SystolicBP'],
                c=color, alpha=0.35, s=18, label=label, edgecolors='none')
ax7.axhline(120, color=WHITE, linestyle='--', alpha=0.4, linewidth=1)
ax7.axvline(80,  color=WHITE, linestyle='--', alpha=0.4, linewidth=1)
ax7.text(81, 121, 'Normal threshold', fontsize=7.5, color=WHITE, alpha=0.5)
ax7.set_xlabel("Diastolic BP (mmHg)", fontsize=9)
ax7.set_ylabel("Systolic BP (mmHg)", fontsize=9)
ax7.set_title("Systolic vs Diastolic Blood Pressure by Risk Level", fontsize=12, fontweight='bold', pad=10)
ax7.legend(fontsize=9, framealpha=0, labelcolor=LIGHT_GREY)
ax7.grid(); ax7.spines['top'].set_visible(False); ax7.spines['right'].set_visible(False)

# 2D — Heart rate by risk box plot
ax8 = fig2.add_subplot(gs2[1, 2])
hr_data = [df[df['RiskLevel']==r]['HeartRate'].values for r in risk_order]
bp2 = ax8.boxplot(hr_data, patch_artist=True,
                  medianprops=dict(color=WHITE, linewidth=2),
                  whiskerprops=dict(color=LIGHT_GREY),
                  capprops=dict(color=LIGHT_GREY),
                  flierprops=dict(marker='o', color=LIGHT_GREY, alpha=0.4, markersize=3))
for patch,color in zip(bp2['boxes'],[LOW_GREEN,MID_AMBER,HIGH_RED]):
    patch.set_facecolor(color); patch.set_alpha(0.7)
ax8.set_xticklabels(['Low','Mid','High'], fontsize=9)
ax8.set_ylabel("Heart Rate (bpm)", fontsize=9)
ax8.set_title("Heart Rate Distribution\nby Risk Level", fontsize=11, fontweight='bold', pad=10)
ax8.grid(axis='y'); ax8.spines['top'].set_visible(False); ax8.spines['right'].set_visible(False)

plt.savefig('/home/claude/fig2_vital_signs.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
plt.close()
print("  ✓ Figure 2 saved")

# ══════════════════════════════════════════════════════════════════════
# FIGURE 3 — PREDICTION MODEL ACCURACY
# ══════════════════════════════════════════════════════════════════════
print("Generating Figure 3: Prediction Model Accuracy...")
fig3 = plt.figure(figsize=(20, 14), facecolor=DARK_BG)
fig3.suptitle("MATERNAL HEALTH RISK ANALYTICS  •  Prediction Model Accuracy",
              fontsize=16, fontweight='bold', color=BLUE, y=0.98)
gs3 = gridspec.GridSpec(2, 3, figure=fig3, hspace=0.45, wspace=0.38)

# 3A — Overall accuracy comparison (donut side by side)
for ax_idx, (model_name, correct, incorrect, acc, color) in enumerate([
    ("IF Model",    pred['CorrectPrediction'].eq('Correct').sum(),
                    pred['CorrectPrediction'].eq('Incorrect').sum(), if_acc, BLUE),
    ("Score Model", scr['CorrectPrediction'].eq('Correct').sum(),
                    scr['CorrectPrediction'].eq('Incorrect').sum(), sc_acc, TEAL),
]):
    ax = fig3.add_subplot(gs3[0, ax_idx])
    ax.pie([correct, incorrect], colors=[color, HIGH_RED],
           wedgeprops=dict(width=0.55, edgecolor=DARK_BG, linewidth=2), startangle=90)
    ax.text(0, 0.1,  f'{acc}%',   ha='center', va='center',
            fontsize=16, fontweight='bold', color=color)
    ax.text(0, -0.2, 'accurate', ha='center', va='center', fontsize=9, color=LIGHT_GREY)
    ax.set_title(f"{model_name}\nOverall Accuracy", fontsize=11, fontweight='bold', pad=10)
    patches = [mpatches.Patch(color=color, label=f'Correct  {correct:,}'),
               mpatches.Patch(color=HIGH_RED, label=f'Incorrect  {incorrect:,}')]
    ax.legend(handles=patches, loc='lower center', fontsize=8,
              framealpha=0, labelcolor=LIGHT_GREY, ncol=1, bbox_to_anchor=(0.5,-0.18))

# 3C — Accuracy by risk level comparison
ax_cmp = fig3.add_subplot(gs3[0, 2])
risk_labels_short = ['High Risk','Mid Risk','Low Risk']
risks_ordered = ['high risk','mid risk','low risk']
if_acc_by_risk, sc_acc_by_risk = [], []
for risk in risks_ordered:
    ic = int(if_by_risk.loc[risk,'Correct'])   if risk in if_by_risk.index and 'Correct'   in if_by_risk.columns else 0
    ii = int(if_by_risk.loc[risk,'Incorrect']) if risk in if_by_risk.index and 'Incorrect' in if_by_risk.columns else 0
    sc = int(sc_by_risk.loc[risk,'Correct'])   if risk in sc_by_risk.index and 'Correct'   in sc_by_risk.columns else 0
    si = int(sc_by_risk.loc[risk,'Incorrect']) if risk in sc_by_risk.index and 'Incorrect' in sc_by_risk.columns else 0
    if_acc_by_risk.append(round(ic/(ic+ii)*100,1) if (ic+ii)>0 else 0)
    sc_acc_by_risk.append(round(sc/(sc+si)*100,1) if (sc+si)>0 else 0)
x3 = range(len(risk_labels_short))
ax_cmp.bar([xi-0.2 for xi in x3], if_acc_by_risk, 0.35, label='IF Model',    color=BLUE,  alpha=0.85)
ax_cmp.bar([xi+0.2 for xi in x3], sc_acc_by_risk, 0.35, label='Score Model', color=TEAL,  alpha=0.85)
for xi,(iv,sv) in enumerate(zip(if_acc_by_risk,sc_acc_by_risk)):
    ax_cmp.text(xi-0.2, iv+0.5, f'{iv}%', ha='center', fontsize=8, color=WHITE)
    ax_cmp.text(xi+0.2, sv+0.5, f'{sv}%', ha='center', fontsize=8, color=WHITE)
ax_cmp.set_xticks(x3); ax_cmp.set_xticklabels(risk_labels_short, fontsize=9)
ax_cmp.set_ylabel("Accuracy (%)", fontsize=9); ax_cmp.set_ylim(0,115)
ax_cmp.set_title("Accuracy by Risk\nLevel Comparison", fontsize=11, fontweight='bold', pad=10)
ax_cmp.legend(fontsize=8, framealpha=0, labelcolor=LIGHT_GREY)
ax_cmp.grid(axis='y'); ax_cmp.spines['top'].set_visible(False); ax_cmp.spines['right'].set_visible(False)

# 3D — Heatmap: IF model confusion
ax_hm1 = fig3.add_subplot(gs3[1, 0])
if_confusion = pred.groupby(['RiskLevel','PredictedLevel']).size().unstack(fill_value=0)
if_confusion.index = [i.title() for i in if_confusion.index]
if_confusion.columns = [c.title() for c in if_confusion.columns]
sns.heatmap(if_confusion, ax=ax_hm1, cmap='Blues', annot=True, fmt='d',
            linewidths=0.5, linecolor=DARK_BG, annot_kws={'size':10,'color':'white'})
ax_hm1.set_title("IF Model — Confusion Matrix", fontsize=11, fontweight='bold', pad=10)
ax_hm1.set_xlabel("Predicted", fontsize=9); ax_hm1.set_ylabel("Actual", fontsize=9)
ax_hm1.tick_params(axis='both', labelsize=8)

# 3E — Heatmap: Score model confusion
ax_hm2 = fig3.add_subplot(gs3[1, 1])
sc_confusion = scr.groupby(['RiskLevel','ScorePerPatient']).size().unstack(fill_value=0)
sc_confusion.index = [i.title() for i in sc_confusion.index]
sc_confusion.columns = [c.title() for c in sc_confusion.columns]
sns.heatmap(sc_confusion, ax=ax_hm2, cmap='Greens', annot=True, fmt='d',
            linewidths=0.5, linecolor=DARK_BG, annot_kws={'size':10,'color':'white'})
ax_hm2.set_title("Score Model — Confusion Matrix", fontsize=11, fontweight='bold', pad=10)
ax_hm2.set_xlabel("Predicted", fontsize=9); ax_hm2.set_ylabel("Actual", fontsize=9)
ax_hm2.tick_params(axis='both', labelsize=8)

# 3F — Model comparison summary bar
ax_sum = fig3.add_subplot(gs3[1, 2])
metrics = ['Overall\nAccuracy','High Risk\nDetection','Mid Risk\nDetection','Low Risk\nDetection']
if_vals_sum = [if_acc] + if_acc_by_risk
sc_vals_sum = [sc_acc] + sc_acc_by_risk
x4 = range(len(metrics))
ax_sum.bar([xi-0.2 for xi in x4], if_vals_sum, 0.35, label='IF Model',    color=BLUE, alpha=0.85)
ax_sum.bar([xi+0.2 for xi in x4], sc_vals_sum, 0.35, label='Score Model', color=TEAL, alpha=0.85)
ax_sum.set_xticks(x4); ax_sum.set_xticklabels(metrics, fontsize=8)
ax_sum.set_ylabel("Accuracy (%)", fontsize=9); ax_sum.set_ylim(0,120)
ax_sum.set_title("Full Model Comparison", fontsize=11, fontweight='bold', pad=10)
ax_sum.legend(fontsize=8, framealpha=0, labelcolor=LIGHT_GREY)
ax_sum.grid(axis='y'); ax_sum.spines['top'].set_visible(False); ax_sum.spines['right'].set_visible(False)

plt.savefig('/home/claude/fig3_prediction_accuracy.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
plt.close()
print("  ✓ Figure 3 saved")

# ══════════════════════════════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("  MATERNAL HEALTH ANALYTICS — SUMMARY STATISTICS")
print("="*60)
print(f"  Total Patients      : {total:,}")
print(f"  High Risk           : {risk_counts.get('high risk',0):,}  ({round(risk_counts.get('high risk',0)/total*100,1)}%)")
print(f"  Mid Risk            : {risk_counts.get('mid risk',0):,}  ({round(risk_counts.get('mid risk',0)/total*100,1)}%)")
print(f"  Low Risk            : {risk_counts.get('low risk',0):,}  ({round(risk_counts.get('low risk',0)/total*100,1)}%)")
print(f"  Avg Age (High Risk) : {round(df[df['RiskLevel']=='high risk']['Age'].mean(),1)} years")
print(f"  Avg Age (Low Risk)  : {round(df[df['RiskLevel']=='low risk']['Age'].mean(),1)} years")
print(f"  IF Model Accuracy   : {if_acc}%")
print(f"  Score Model Accuracy: {sc_acc}%")
print(f"  Best for High Risk  : IF Model ({if_acc_by_risk[0]}% vs {sc_acc_by_risk[0]}%)")
print("="*60)
print("\n✅ All 3 figures saved to /home/claude/")
