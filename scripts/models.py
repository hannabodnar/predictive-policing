import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split, cross_val_score, RandomizedSearchCV, learning_curve
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report, ConfusionMatrixDisplay, roc_curve, auc
import matplotlib.pyplot as plt

# load data
data = pd.read_csv('aggragated_data.csv')
df = pd.DataFrame(data[['Date Rptd', 'TIME OCC', 'DATE OCC', 'Area Code', 'Rpt Dist No', 'Crime Code', 'Vict Age', 'Vict Sex', 'Vict Descent', 'Premise Code', 'Weapon Used Cd', 'Status Desc', 'LAT', 'LON']])


date_cols = ['Date Rptd', 'DATE OCC']
df[date_cols] = df[date_cols].apply(pd.to_datetime)
df['TIME OCC'] = pd.to_datetime(df['TIME OCC'], format='%H:%M:%S')
df['Date Rptd Year'] = df['Date Rptd'].dt.year
df['Date Rptd Month'] = df['Date Rptd'].dt.month
df['Date Rptd Day'] = df['Date Rptd'].dt.day
df['DATE OCC Year'] = df['DATE OCC'].dt.year
df['DATE OCC Month'] = df['DATE OCC'].dt.month
df['DATE OCC Day'] = df['DATE OCC'].dt.day
df['TIME OCC (hour)'] = df['TIME OCC'].dt.hour
df = df.drop(columns=['DATE OCC', 'Date Rptd', 'TIME OCC'])

# Encode categorical features
encoder = LabelEncoder()
df['Vict Sex Encoded'] = encoder.fit_transform(df['Vict Sex'])
df['Vict Descent Encoded'] = encoder.fit_transform(df['Vict Descent'])
df['Status Desc Encoded'] = encoder.fit_transform(df['Status Desc'])
status_labels = list(zip(df['Status Desc Encoded'], df['Status Desc']))
descent_labels = list(zip(df['Vict Descent Encoded'], df['Vict Descent']))
sex_labels = list(zip(df['Vict Sex Encoded'], df['Vict Sex']))
df = df.drop(columns=['Status Desc', 'Vict Descent', 'Vict Sex'])



cols = [col for col in df.columns.values if (col != 'Crime Code') & (col != 'DR_NO')]
features = df[cols]
predictor = df['Crime Code']

# split data
x_train, x_test, y_train, y_test = train_test_split(features, predictor, test_size=0.3, random_state=42)
scaler = MinMaxScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# Random Forest Classifier
rf_classifier = RandomForestClassifier(class_weight='balanced', random_state=10)


param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [10, 20, 50],
    'min_samples_split': [10, 100, 1000],
    'min_samples_leaf': [10, 100, 1000]
}
random_search = RandomizedSearchCV(estimator=rf_classifier, param_distributions=param_grid, n_iter=3, cv=5, random_state=10)
random_search.fit(x_train, y_train)
best_params = random_search.best_params_
best_rf_classifier = RandomForestClassifier(**best_params, class_weight='balanced')
best_rf_classifier.fit(x_train, y_train)
test_scores = best_rf_classifier.score(x_test, y_test)
print(test_scores)
#y_pred = rf_classifier.predict(x_test)
#print(classification_report(y_test, y_pred))

# Plot Feature Importance
feature_importance = best_rf_classifier.feature_importances_
feature_names = features.columns.values
plt.figure(figsize=(10, 6))
plt.bar(range(len(feature_importance)), feature_importance, color='blue', alpha=0.7)
plt.xlabel('Feature')
plt.ylabel('Importance')
plt.title('Feature Importance')
plt.xticks(ticks=np.arange(len(feature_names)), labels=feature_names, rotation=45)
plt.tight_layout()
#plt.savefig('area_features.png')
plt.savefig('rf_feature_crime.png')
plt.show()

# Plot Confusion Matrix
#ConfusionMatrixDisplay.from_estimator(best_rf_classifier, x_test, y_test)
#plt.show()


# Support Vector Machine (SVM)
svm_classifier = SVC(random_state=10)
svm_classifier.fit(x_train, y_train)
y_pred = svm_classifier.predict(x_test)
print(svm_classifier.score(x_test, y_test))