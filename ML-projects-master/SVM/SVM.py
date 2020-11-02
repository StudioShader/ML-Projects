import os
import time
import warnings  
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import skimage.color as color
import Pre_processing
from skimage import io
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
warnings.filterwarnings('ignore')

# data loading
g = os.listdir('./good_data')
b = os.listdir('./bad_data')

g = ['./good_data/'+x for x in g]
b = ['./bad_data/'+x for x in b]

temp = np.ones(len(g))
test_ans = np.concatenate((temp , np.zeros(len(b))), axis=0)

# loading processing data (features matrix) from CSV file
data = pd.read_csv("./processed data/data4Nall.csv")

# data normalization
scaler = StandardScaler()
scaler.fit(data)
data = scaler.transform(data)

# preprocessing pure data and loading features matrix to CSV file
#data = Pre_processing.get_average_colors(g+b, 4)
#df = pd.DataFrame(data)
#df.to_csv (r'./data4Nsq30.csv', index = None, header=True) 

X_train, X_test, y_train, y_test = train_test_split(data, test_ans, random_state=0)

st_time = time.time()
# SVM train and predict
svc = LinearSVC(max_iter=3000)
svc.fit(X_train, y_train)
y_pred = svc.predict(X_test)
print(confusion_matrix(y_test, y_pred))
print('Prediction accuracy is {}%'.format(accuracy_score(y_test, y_pred) * 100))
end_time = time.time()
print('Train and test time: {}%'.format(end_time - st_time))