import pandas as pd
import json
import joblib
import numpy as np

data = pd.read_csv('data_test.csv',index_col=0)
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

knn = joblib.load('knn_classifier.joblib')
pred_knn = knn.predict(xx)
output_knn = xx.copy()
output_knn["is_fraud"] = yy
output_knn["prediction.csv"] = pred_knn


logreg = joblib.load('logreg_classifier.joblib')
pred_logreg = logreg.predict(xx)
output_logreg = xx.copy()
output_logreg["is_fraud"] = yy
output_logreg["prediction"] = pred_logreg

output_knn.to_csv('output_knn.csv')
output_logreg.to_csv('output_logreg.csv')

