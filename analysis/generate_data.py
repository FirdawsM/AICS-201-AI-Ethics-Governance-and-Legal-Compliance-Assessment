"""Generate the synthetic SecureFinance Africa dataset (Task 4).

All records are artificial. No real person, customer or identifier is used.
Run:  python analysis/generate_data.py
Output: data/synthetic_customers.csv
"""
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 42
N = 8000
rng = np.random.default_rng(SEED)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# --- Groups (assumed shares are illustrative) ---
rural = rng.random(N) < 0.35          # 1 = rural / peri-urban, 0 = urban
female = rng.random(N) < 0.50         # 1 = female, 0 = male

# --- Latent creditworthiness z: same distribution in every group (assumption) ---
z = rng.normal(0, 1, N)

# --- Features ---
income_stability = np.clip(55 + 14 * z + rng.normal(0, 8, N), 0, 100)
txn_regularity = np.clip(60 + 12 * z + rng.normal(0, 10, N), 0, 100)

# Credit history length: shorter for rural customers and for women (thin files),
# only weakly related to true creditworthiness.
months_base = 44 - 14 * rural - 5 * female
months_history = np.clip(months_base + 4 * z + rng.gamma(2.0, 6.0, N) - 12, 0, None).round()

# Proxy features: related to group, NOT to true creditworthiness.
device_basic = (rng.random(N) < np.where(rural, 0.55, 0.15)).astype(int)   # 1 = basic phone
location_changes_90d = rng.poisson(np.where(rural, 2.6, 1.0))

# --- Ground truth: would the customer repay? Depends on z only (not on group). ---
p_repay = sigmoid(1.4 * z + 1.1)
repaid_true = (rng.random(N) < p_repay).astype(int)

# --- Historical analyst decision (training label). Encodes past exclusion:
#     basic-phone and thin-file customers were approved less often than their
#     true creditworthiness justified. This is the planted label bias. ---
thin_file = (months_history < 24).astype(int)
p_hist = sigmoid(1.4 * z + 1.1 - 0.9 * device_basic - 0.6 * thin_file)
hist_approved = (rng.random(N) < p_hist).astype(int)

df = pd.DataFrame({
    "customer_id": [f"SYN{i:05d}" for i in range(N)],
    "location_type": np.where(rural, "rural", "urban"),
    "gender": np.where(female, "female", "male"),
    "income_stability": income_stability.round(1),
    "txn_regularity": txn_regularity.round(1),
    "months_history": months_history.astype(int),
    "device_basic": device_basic,
    "location_changes_90d": location_changes_90d,
    "hist_approved": hist_approved,
    "repaid_true": repaid_true,
})

out = Path(__file__).resolve().parent.parent / "data" / "synthetic_customers.csv"
out.parent.mkdir(exist_ok=True)
df.to_csv(out, index=False)
print(f"Wrote {len(df)} rows to {out}")
