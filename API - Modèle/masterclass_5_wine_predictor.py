# -*- coding: utf-8 -*-
"""Masterclass 5 - Wine predictor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bnNdiSzg61LbojiPxnGlVsqWNJh70bUN

# **WINE PREDICTOR**
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
import numpy as np

np.random.seed(42)

wine_dataset = load_wine()

wine_dataset.keys()

print(wine_dataset['DESCR'])

df = pd.DataFrame(wine_dataset["data"], columns=wine_dataset['feature_names'])
df['target'] = wine_dataset['target']
print("Shape :", df.shape)
df.head()

"""## Data exploration"""

df.target.astype(str).value_counts().plot(kind='bar', figsize=(6,5))
plt.xlabel("Class", labelpad=14)
plt.ylabel("Count", labelpad=14)
plt.title('# records by class', y=1.02)
plt.show()

df.plot.scatter(x='alcohol', y='flavanoids', c='target', colormap='viridis')
plt.show()

df.plot.scatter(x='color_intensity', y='hue', c='target', colormap='viridis')
plt.show()

features = ['alcohol','flavanoids', 'proline', 'color_intensity', 'hue']

"""## Train Test Split"""

from sklearn.model_selection import train_test_split

X, y = df[features], df['target']

X.shape, y.shape

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

"""## Training"""

from sklearn.ensemble import RandomForestClassifier

clf = RandomForestClassifier(n_estimators=20)

clf.fit(X_train, y_train)

"""## Evaluation"""

from sklearn.metrics import plot_confusion_matrix, classification_report

y_pred_train = clf.predict(X_train)
y_pred_test = clf.predict(X_test)

"""Train :"""

print(classification_report(y_train, y_pred_train))

print(classification_report(y_test, y_pred_test))

plot_confusion_matrix(clf, X_test, y_test)
plt.show()

"""## Save model"""

import joblib
import json

feature_names = X.columns.to_list()

print(feature_names)

with open('features.json', 'w') as f :
  json.dump(feature_names, f, indent=4)

with open('classifier.joblib', 'wb') as f :
  joblib.dump(clf, f)         # clf = modèle scikit-learn

"""## Test"""

sample_idx = np.random.randint(len(X_test))
print('Class: ', y_test.iloc[sample_idx])
print('Predicted class: ', y_pred_test[sample_idx])
print()
print(json.dumps(X_test.iloc[sample_idx].to_dict(), indent=4))

pd.DataFrame([X_test.iloc[sample_idx].to_dict()])

