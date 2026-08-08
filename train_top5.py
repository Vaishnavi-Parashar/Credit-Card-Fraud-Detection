import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix


# ==========================================
# STEP 1 - LOAD DATA
# ==========================================

df = pd.read_csv("creditcard.csv")

print("Dataset Shape:", df.shape)


# ==========================================
# STEP 2 - REMOVE DUPLICATES
# ==========================================

df = df.drop_duplicates()

print("Shape After Removing Duplicates:", df.shape)


# ==========================================
# STEP 3 - SEPARATE FEATURES AND TARGET
# ==========================================

X = df.drop("Class", axis=1)
y = df["Class"]

print("\nTotal Features:", X.shape[1])


# ==========================================
# STEP 4 - TRAIN RANDOM FOREST
#         USING ALL FEATURES
#         TO FIND FEATURE IMPORTANCE
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

rf_all = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)

rf_all.fit(X_train, y_train)


# ==========================================
# STEP 5 - FIND TOP 5 FEATURES
# ==========================================

feature_importance = pd.Series(
    rf_all.feature_importances_,
    index=X.columns
).sort_values(ascending=False)

top_5_features = feature_importance.head(5).index.tolist()

print("\n===================================")
print("TOP 5 FEATURES")
print("===================================")

for feature in top_5_features:
    print(feature)

print("\nFeature Importance:")
print(feature_importance.head(5))


# ==========================================
# STEP 6 - CREATE DATASET WITH ONLY TOP 5
# ==========================================

X_top5 = X[top_5_features]

print("\nTop 5 Dataset Shape:", X_top5.shape)


# ==========================================
# STEP 7 - TRAIN/TEST SPLIT FOR TOP 5
# ==========================================

X_train_top5, X_test_top5, y_train_top5, y_test_top5 = train_test_split(
    X_top5,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ==========================================
# STEP 8 - TRAIN FINAL RANDOM FOREST
#         USING ONLY TOP 5 FEATURES
# ==========================================

rf_top5 = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)

rf_top5.fit(X_train_top5, y_train_top5)


# ==========================================
# STEP 9 - EVALUATE FINAL MODEL
# ==========================================

y_pred = rf_top5.predict(X_test_top5)

print("\n===================================")
print("FINAL MODEL - TOP 5 FEATURES")
print("===================================")

print(classification_report(y_test_top5, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test_top5, y_pred))


# ==========================================
# STEP 10 - SAVE FINAL MODEL
# ==========================================

joblib.dump(rf_top5, "fraud_model_top5.pkl")

joblib.dump(top_5_features, "top5_features.pkl")


print("\n===================================")
print("FILES SAVED SUCCESSFULLY")
print("===================================")

print("fraud_model_top5.pkl")
print("top5_features.pkl")

print("\nFinal Top 5 Features:")
print(top_5_features)