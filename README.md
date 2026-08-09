# 🚨 RedFlag — Real-Time Credit Card Fraud Detection Platform

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![ML](https://img.shields.io/badge/ML-Scikit--learn-orange)
![XGBoost](https://img.shields.io/badge/Model-XGBoost-green)
![Streamlit](https://img.shields.io/badge/Deploy-Streamlit-red)

## 📌 Problem Statement
Credit card fraud causes billions in losses annually. 
This project builds a real-time fraud detection system 
trained on 283K transactions with 99.5% class imbalance.

## 🎯 Results
| Model | ROC-AUC | Recall | Precision |
|-------|---------|--------|-----------|
| Random Forest | 0.978 | 83% | 46% |
| XGBoost | 0.972 | 83% | 29% |
| **Winner** | **Random Forest** | | |

## 🛠️ Tech Stack
- Python, Pandas, NumPy
- Scikit-learn, XGBoost
- SMOTE (imbalanced-learn)
- Streamlit (deployment)

## 📊 Key Steps
1. EDA on 283K transactions
2. SMOTE to fix 99.5% class imbalance
3. Random Forest + XGBoost comparison
4. ROC-AUC evaluation
5. Live Streamlit deployment

## 🚀 Run Locally
pip install -r requirements.txt
streamlit run app.py

## 👩‍💻 Author
Vaishnavi Parashar — B.Tech AI/ML, ITM University
