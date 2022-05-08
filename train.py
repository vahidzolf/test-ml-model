from sklearn.linear_model import LogisticRegression
import pickle
import pandas as pd
import numpy as np

iris = pd.read_csv("iris.csv")

X = []
y = []
for row in iris.itertuples(index=True, name='Pandas'):
    X.append([row.petallength, row.petalwidth, row.sepallength, row.sepalwidth])
    if row[5] == 'Iris-setosa':
        y.append(0)
    elif row[5] == 'Iris-versicolor':
        y.append(1)
    elif row[5] == 'Iris-virginica':
        y.append(2)

X = np.array(X)
y = np.array(y)

# shuffle arrays since y values are in order
from sklearn.utils import shuffle

X_new, y_new = shuffle(X, y, random_state=0)

n_samples_train = 120  # number of samples for training (--> #samples for testing = len(y_new) - 120 = 30)
X_train = X_new[:n_samples_train, :]
y_train = y_new[:n_samples_train]

X_test = X_new[n_samples_train:, :]
y_test = y_new[n_samples_train:]

clf = LogisticRegression(solver='lbfgs', max_iter=1000)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

with open('iris_trained_model.pkl', 'wb') as f:
    pickle.dump(clf, f)
