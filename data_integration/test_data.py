import pandas as pd
import json
import joblib
import numpy as np

data = pd.read_csv('data_test.csv',index_col=0)
fraud = pd.read_csv('fraud.csv')
fraud_input = fraud[['signup_time','purchase_time']]
idx_tt = data.index
X = data.drop('is_fraud',axis=1)
y = data.is_fraud

nn = len(y)

def rand_vals(lim):
    val, i = [], 0
    while i < lim: 
        val.append(np.random.randint(0,nn))
        i += 1
    return val    

nvals = 10
idx = rand_vals(nvals)
yy = y.iloc[idx]
xx = X.iloc[idx]
indices = idx_tt[idx]

knn = joblib.load('knn_classifier.joblib')
logreg = joblib.load('logreg_classifier.joblib')
pred_knn = knn.predict(xx)
pred_logreg = logreg.predict(xx)
fraud = fraud_input.iloc[indices].reset_index(drop=True)

output_knn = xx.copy()
output_knn["is_fraud"] = yy
output_knn["prediction.csv"] = pred_knn
output_knn = pd.concat([output_knn.reset_index(drop=True),fraud],axis=1)

output_logreg = xx.copy()
output_logreg["is_fraud"] = yy
output_logreg["prediction"] = pred_logreg
output_logreg = pd.concat([output_logreg.reset_index(drop=True),fraud],axis=1)

output_knn.to_json('output_knn.json')
output_logreg.to_json('output_logreg.json')