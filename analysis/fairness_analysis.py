"""Fairness and explainability evaluation for SecureFinance Africa module M3 (Task 4).

Run:  python analysis/generate_data.py && python analysis/fairness_analysis.py
Outputs (evidence/): metrics tables (CSV), charts (PNG), decision-review sheet (CSV), summary.txt
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parent.parent
EVID = ROOT / "evidence"
EVID.mkdir(exist_ok=True)
SEED = 42
THRESH_TARGET_APPROVAL = 0.62   # operating point: approve about 62% overall (assumption)

df = pd.read_csv(ROOT / "data" / "synthetic_customers.csv")
ALL_FEATS = ["income_stability", "txn_regularity", "months_history",
             "device_basic", "location_changes_90d"]
PROXY_FEATS = ["device_basic", "location_changes_90d"]
NO_PROXY = [f for f in ALL_FEATS if f not in PROXY_FEATS]

train, test = train_test_split(df, test_size=0.4, random_state=SEED, stratify=df["location_type"])
test = test.reset_index(drop=True)


def fit(feats, label):
    sc = StandardScaler().fit(train[feats])
    m = LogisticRegression(max_iter=1000).fit(sc.transform(train[feats]), train[label])
    return sc, m


def decide(sc, m, feats, data):
    p = m.predict_proba(sc.transform(data[feats]))[:, 1]
    return p


VARIANTS = {
    "V0 baseline (all features, historical decisions)": (ALL_FEATS, "hist_approved"),
    "V1 proxy features removed (historical decisions)": (NO_PROXY, "hist_approved"),
    "V2 outcome labels (all features, repayment outcomes)": (ALL_FEATS, "repaid_true"),
}

models, scores, approvals = {}, {}, {}
for name, (feats, label) in VARIANTS.items():
    sc, m = fit(feats, label)
    p = decide(sc, m, feats, test)
    thr = np.quantile(p, 1 - THRESH_TARGET_APPROVAL)   # same overall approval rate for comparability
    models[name] = (sc, m, feats)
    scores[name] = p
    approvals[name] = (p >= thr).astype(int)


def group_metrics(data, approved, mask):
    d = data[mask]; a = approved[mask]
    y = d["repaid_true"].values
    return {
        "n": int(mask.sum()),
        "approval_rate": a.mean(),
        "approval_rate_among_creditworthy (TPR)": a[y == 1].mean(),
        "approval_rate_among_defaulters (FPR)": a[y == 0].mean(),
        "repay_rate_among_approved (precision)": y[a == 1].mean() if (a == 1).any() else np.nan,
    }


def groups(data):
    return {
        "urban": (data["location_type"] == "urban").values,
        "rural": (data["location_type"] == "rural").values,
        "male": (data["gender"] == "male").values,
        "female": (data["gender"] == "female").values,
        "rural women": ((data["location_type"] == "rural") & (data["gender"] == "female")).values,
        "urban men": ((data["location_type"] == "urban") & (data["gender"] == "male")).values,
    }

G = groups(test)
rows = []
for vname, a in approvals.items():
    for gname, mask in G.items():
        r = group_metrics(test, a, mask)
        r.update({"variant": vname, "group": gname})
        rows.append(r)
metrics = pd.DataFrame(rows)[["variant", "group", "n", "approval_rate",
                              "approval_rate_among_creditworthy (TPR)",
                              "approval_rate_among_defaulters (FPR)",
                              "repay_rate_among_approved (precision)"]]
metrics.round(3).to_csv(EVID / "group_metrics.csv", index=False)

# --- Gap summary: reference group vs comparison group ---
PAIRS = [("rural", "urban"), ("female", "male"), ("rural women", "urban men")]


def gap_row(vname, a, data, comp, ref, G):
    rc = group_metrics(data, a, G[comp]); rr = group_metrics(data, a, G[ref])
    return {
        "variant": vname, "comparison": f"{comp} vs {ref}",
        "impact_ratio (approval)": rc["approval_rate"] / rr["approval_rate"],
        "equal_opportunity_gap (TPR)": rc["approval_rate_among_creditworthy (TPR)"] - rr["approval_rate_among_creditworthy (TPR)"],
        "FPR_gap": rc["approval_rate_among_defaulters (FPR)"] - rr["approval_rate_among_defaulters (FPR)"],
        "precision_gap": rc["repay_rate_among_approved (precision)"] - rr["repay_rate_among_approved (precision)"],
    }

gaps = pd.DataFrame([gap_row(v, a, test, c, r, G) for v, a in approvals.items() for c, r in PAIRS])

# bootstrap 95% CI for the baseline rural-vs-urban gaps
rng = np.random.default_rng(SEED)
base = list(approvals)[0]
boot = {"impact_ratio (approval)": [], "equal_opportunity_gap (TPR)": []}
for _ in range(1000):
    idx = rng.integers(0, len(test), len(test))
    bt = test.iloc[idx].reset_index(drop=True); ba = approvals[base][idx]
    g = groups(bt)
    row = gap_row(base, ba, bt, "rural", "urban", g)
    for k in boot:
        boot[k].append(row[k])
ci = {k: (np.percentile(v, 2.5), np.percentile(v, 97.5)) for k, v in boot.items()}
gaps.round(3).to_csv(EVID / "gap_summary.csv", index=False)

auc = {v: roc_auc_score(test["repaid_true"], s) for v, s in scores.items()}

# --- Explainability 1: permutation importance (baseline) on AUC against true outcomes ---
sc, m, feats = models[base]
def perm_importance(feats_list, sc, m, data, y, reps=20):
    X = data[feats_list].copy()
    baseline = roc_auc_score(y, m.predict_proba(sc.transform(X))[:, 1])
    out = {}
    r = np.random.default_rng(SEED)
    for f in feats_list:
        drops = []
        for _ in range(reps):
            Xp = X.copy(); Xp[f] = r.permutation(Xp[f].values)
            drops.append(baseline - roc_auc_score(y, m.predict_proba(sc.transform(Xp))[:, 1]))
        out[f] = np.mean(drops)
    return pd.Series(out)

pi = perm_importance(feats, sc, m, test, test["hist_approved"])   # importance for the decision the model mimics
coefs = pd.Series(m.coef_[0], index=feats)
imp = pd.DataFrame({"standardised_coefficient": coefs, "permutation_importance_AUC_drop": pi}).round(3)
imp.to_csv(EVID / "explainability_importance.csv")

# --- Explainability 2: decision review of wrongly declined creditworthy rural customers ---
p0 = scores[base]
thr0 = np.quantile(p0, 1 - THRESH_TARGET_APPROVAL)
wrong = test[(approvals[base] == 0) & (test["repaid_true"] == 1)]
wrong_rural = wrong[wrong["location_type"] == "rural"]
cf = wrong_rural.copy(); cf["device_basic"] = 0
flip_device = (m.predict_proba(sc.transform(cf[feats]))[:, 1] >= thr0).mean()

contrib = pd.DataFrame(sc.transform(wrong_rural[feats]) * coefs.values, columns=feats, index=wrong_rural.index)
sheet = wrong_rural[["customer_id", "location_type", "gender"] + feats].copy()
sheet["model_score"] = p0[wrong_rural.index].round(3)
sheet["decision"] = "declined"
sheet["top_negative_driver"] = contrib.idxmin(axis=1)
sheet["top_negative_contribution"] = contrib.min(axis=1).round(2)
sheet["flips_if_device_basic_0"] = (m.predict_proba(sc.transform(cf[feats]))[:, 1] >= thr0)
sheet.head(10).to_csv(EVID / "decision_review_sheet.csv", index=False)

# --- Charts ---
variants = list(approvals)
short = ["V0 baseline", "V1 no proxies", "V2 outcome labels"]
def bar_chart(metric, title, fname, ylabel):
    fig, ax = plt.subplots(figsize=(7, 4))
    w = 0.25
    for i, (v, s) in enumerate(zip(variants, short)):
        vals = [metrics[(metrics.variant == v) & (metrics.group == g)][metric].values[0] for g in ["urban", "rural", "male", "female"]]
        ax.bar(np.arange(4) + (i - 1) * w, vals, w, label=s)
    ax.set_xticks(range(4)); ax.set_xticklabels(["urban", "rural", "male", "female"])
    ax.set_title(title); ax.set_ylabel(ylabel); ax.set_ylim(0, 1); ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(EVID / fname, dpi=150); plt.close(fig)

bar_chart("approval_rate", "Approval rate by group (same overall approval rate)", "chart_approval_rate.png", "approval rate")
bar_chart("approval_rate_among_creditworthy (TPR)", "Approval rate among customers who would repay", "chart_equal_opportunity.png", "approval rate (equal opportunity)")

fig, ax = plt.subplots(figsize=(6, 3.5))
imp["permutation_importance_AUC_drop"].sort_values().plot.barh(ax=ax)
ax.set_title("Baseline model: permutation importance"); ax.set_xlabel("AUC drop when feature is shuffled")
fig.tight_layout(); fig.savefig(EVID / "chart_permutation_importance.png", dpi=150); plt.close(fig)

# --- Text summary ---
with open(EVID / "summary.txt", "w") as f:
    f.write(f"Test set n={len(test)}; overall approval rate target={THRESH_TARGET_APPROVAL}\n")
    f.write("AUC against true repayment: " + "; ".join(f"{k.split(' (')[0]}={v:.3f}" for k, v in auc.items()) + "\n\n")
    f.write(gaps.round(3).to_string(index=False) + "\n\n")
    f.write(f"Baseline bootstrap 95% CI, rural vs urban: impact ratio {ci['impact_ratio (approval)'][0]:.3f} to {ci['impact_ratio (approval)'][1]:.3f}; "
            f"equal opportunity gap {ci['equal_opportunity_gap (TPR)'][0]:.3f} to {ci['equal_opportunity_gap (TPR)'][1]:.3f}\n\n")
    f.write(imp.to_string() + "\n\n")
    f.write(f"Wrongly declined creditworthy rural customers (baseline): {len(wrong_rural)}\n")
    f.write(f"Share approved if only device_basic is set to 0: {flip_device:.3f}\n")
print(open(EVID / "summary.txt").read())
