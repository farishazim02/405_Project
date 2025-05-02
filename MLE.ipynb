import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt

use_cols = ['genre', 'mean_duration_sec', 'n_track', 'num_artists', 'num_extra_artists', 'release_year']
df = pd.read_csv('merged_summary.csv', usecols=use_cols)

df['genre'] = df['genre'].fillna('Unknown')
num_cols = ['mean_duration_sec', 'n_track', 'num_artists', 'num_extra_artists', 'release_year']
imp_num = SimpleImputer(strategy='median')
df[num_cols] = imp_num.fit_transform(df[num_cols])
median_val = df['mean_duration_sec'].median()
df['long_mean'] = (df['mean_duration_sec'] > median_val).astype(int)

df_enc = pd.get_dummies(df, columns=['genre'], drop_first=True)
y = df_enc['long_mean']
X = df_enc.drop(columns=['long_mean', 'mean_duration_sec'], errors='ignore')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

log_model = LogisticRegression(max_iter=1000)
log_model.fit(X_train, y_train)
log_probs = log_model.predict_proba(X_test)[:, 1]

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_probs = rf_model.predict_proba(X_test)[:, 1]

auc_log = roc_auc_score(y_test, log_probs)
auc_rf = roc_auc_score(y_test, rf_probs)
print(f'Logistic Regression AUC = {auc_log:.3f}')
print(f'Random Forest AUC = {auc_rf:.3f}')

fpr_l, tpr_l, _ = roc_curve(y_test, log_probs)
plt.figure()
plt.plot(fpr_l, tpr_l)
plt.plot([0, 1], [0, 1], '--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title(f'Logistic ROC (AUC = {auc_log:.3f})')
plt.show()

fpr_rf, tpr_rf, _ = roc_curve(y_test, rf_probs)
plt.figure()
plt.plot(fpr_rf, tpr_rf)
plt.plot([0, 1], [0, 1], '--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title(f'Random Forest ROC (AUC = {auc_rf:.3f})')
plt.show()

probs_df = pd.DataFrame({
    'true_label': y_test.values,
    'logistic_prob': log_probs,
    'rf_prob': rf_probs
})
