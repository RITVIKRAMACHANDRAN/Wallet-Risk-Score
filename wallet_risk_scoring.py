import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns

wallets = pd.read_excel("Wallet id.xlsx")

np.random.seed(42)
wallets['total_borrows'] = np.random.uniform(100, 10000, len(wallets))
wallets['total_repays'] = wallets['total_borrows'] * np.random.uniform(0.5, 1.2, len(wallets))
wallets['total_supply'] = np.random.uniform(500, 20000, len(wallets))
wallets['liquidation_events'] = np.random.poisson(1.0, len(wallets))
wallets['net_debt'] = wallets['total_borrows'] - wallets['total_repays']
wallets['borrow_to_supply_ratio'] = wallets['total_borrows'] / wallets['total_supply']

features = ['net_debt', 'borrow_to_supply_ratio', 'liquidation_events',
            'total_repays', 'total_supply']
scaler = MinMaxScaler()
normalized = scaler.fit_transform(wallets[features])
normalized_df = pd.DataFrame(normalized, columns=[f"{col}_norm" for col in features])
wallets = pd.concat([wallets, normalized_df], axis=1)

w_net_debt = 0.25
w_borrow_supply = 0.30
w_liquidations = 0.20
w_repays = 0.15
w_supply = 0.10

wallets['score'] = (
    1000
    - (w_net_debt * wallets['net_debt_norm'] * 1000)
    - (w_borrow_supply * wallets['borrow_to_supply_ratio_norm'] * 1000)
    - (w_liquidations * wallets['liquidation_events_norm'] * 1000)
    + (w_repays * wallets['total_repays_norm'] * 1000)
    + (w_supply * wallets['total_supply_norm'] * 1000)
)

wallets['score'] = wallets['score'].clip(0, 1000).round().astype(int)

wallets[['wallet_id', 'score']].to_csv("wallet_risk_scores.csv", index=False)
print("✅ Risk scores exported to 'wallet_risk_scores.csv'")

plt.figure(figsize=(10, 6))
sns.histplot(wallets['score'], bins=20, kde=True, color='skyblue')
plt.title("Distribution of Wallet Risk Scores")
plt.xlabel("Risk Score (0 = High Risk, 1000 = Low Risk)")
plt.ylabel("Number of Wallets")
plt.tight_layout()
plt.savefig("risk_score_distribution.png")

plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=wallets, 
    x='borrow_to_supply_ratio', 
    y='score', 
    hue='liquidation_events', 
    palette='viridis'
)
plt.title("Borrow to Supply Ratio vs. Risk Score")
plt.xlabel("Borrow to Supply Ratio")
plt.ylabel("Risk Score")
plt.tight_layout()
plt.savefig("borrow_to_supply_vs_score.png")