# Wallet Risk Scoring – Compound Protocol 

## Overview

This project implements a wallet risk scoring model using wallet activity similar to the Compound lending protocol. Wallets are evaluated based on borrowing, repaying, supply, and liquidation behavior.


## Input

- `Wallet id.xlsx`: Contains a list of wallet addresses to be evaluated.


## 📈 Features

- `total_borrows` – Total amount borrowed by the wallet  
- `total_repays` – Total amount repaid  
- `total_supply` – Total collateral or supplied assets  
- `liquidation_events` – Count of liquidations  
- `net_debt` – Calculated as borrows minus repays  
- `borrow_to_supply_ratio` – Debt-to-collateral ratio  


## 🧠 Feature Engineering & Scoring Logic

1. **Normalization**: All key features are scaled between 0 and 1 using Min-Max Scaler.  
2. **Scoring Formula**: Wallets are scored out of 1000 using a weighted formula:

score = 1000
- (0.25 * net_debt)
- (0.30 * borrow_to_supply_ratio)
- (0.20 * liquidation_events)
+ (0.15 * repays)
+ (0.10 * supply)


Lower risk wallets will have higher scores.

##  Output

- `wallet_risk_scores.csv` – Contains final scores with format:

| wallet_id | score |
|-----------|-------|
| 0xabc...  | 832   |

- `risk_score_distribution.png` – Histogram of risk scores  
- `borrow_to_supply_vs_score.png` – Scatter plot of borrow/supply ratio vs score  

## 📊 Visualizations

### 1. Risk Score Distribution  
Displays how scores are distributed across all wallets.

### 2. Borrow-to-Supply vs Score  
Reveals how the borrow/supply ratio affects risk scoring, color-coded by liquidation events.

## 🛠️ Tools & Libraries

- Python 3.x  
- `pandas`, `numpy` – data processing  
- `scikit-learn` – normalization  
- `matplotlib`, `seaborn` – plotting  

## ✅ How to Run

1. Place `Wallet id.xlsx` in the same folder.  
2. Run the script:

```bash
python wallet_risk_scoring.py
