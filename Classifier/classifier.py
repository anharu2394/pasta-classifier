from sklearn import svm
from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from PIL import Image
import numpy as np
from skimage import data
import os
import pickle
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt  
def load_data():
    bolog_imgs = np.array([data.imread('./../images/bolognese/' + path) for path in os.listdir('./../images/bolognese')])
    carbo_imgs = np.array([data.imread('./../images/carbonara/' + path) for path in os.listdir('./../images/carbonara')])
    bolog_imgs = bolog_imgs.reshape(len(bolog_imgs), -1).astype(np.float64)
    carbo_imgs = carbo_imgs.reshape(len(carbo_imgs), -1).astype(np.float64)
    bolog_vc = np.array([0 for i in range(len(bolog_imgs))])
    carbo_vc = np.array([1 for i in range(len(carbo_imgs))])
    bolog_f = np.concatenate([bolog_imgs, carbo_imgs], axis=0)
    np.random.seed(1)
    np.random.shuffle(bolog_f)
    carbo_f = np.concatenate([bolog_vc, carbo_vc], axis=0)
    np.random.seed(1)
    np.random.shuffle(carbo_f)
    return bolog_f, carbo_f

clf = svm.SVC(gamma=0.001, C=100.)
feature, target = load_data()
feature = feature.reshape((len(feature), -1))
X_train, X_test, y_train, y_test = train_test_split(
    feature, target, test_size=0.5, random_state=0)

clf = MLPClassifier(solver="lbfgs",random_state=0,activation='relu',hidden_layer_sizes=[100,100],alpha=0.0001)
clf.fit(X_train, y_train)
pred_x = np.array(X_test[:3])
print(pred_x)
print(clf.predict(pred_x))
print ("predict:", clf.score(X_test, y_test))
filename = 'pasta_model.sav'
pickle.dump(clf, open(filename, 'wb'))
