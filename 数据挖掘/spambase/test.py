import pandas as pd
import numpy as np
from numpy.random import RandomState
from sklearn.naive_bayes import GaussianNB,BernoulliNB,MultinomialNB
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import  AdaBoostClassifier
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

def load_data(url,train):
    data = pd.read_csv(url)
    d1 = data.iloc[:,1:58]
    d2 = data.iloc[:,58:]
    if train:
        return d1,d2
    else:
        data = data.iloc[:,1:]
        return data

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2.-0.2, 1.03*height, '%s' % float(height))
        
def get_res(x_train,y_train,x_test,y_test):
    
    knn = KNeighborsClassifier()
    knn.fit(x_train,y_train)
    
    lg = LogisticRegression(penalty='l2')
    lg.fit(x_train,y_train)
    
    dtc = DecisionTreeClassifier()
    dtc.fit(x_train,y_train)
    
    gb = GradientBoostingClassifier(n_estimators=200)
    gb.fit(x_train,y_train)
    
    ab = AdaBoostClassifier()
    ab.fit(x_train,y_train)
    
    gnb = GaussianNB()
    gnb.fit(x_train,y_train)
    
    svm = SVC()
    svm.fit(x_train,y_train)
    
    mnb = MultinomialNB(alpha=0.01)
    mnb.fit(x_train,y_train)
    
    bnb = BernoulliNB(alpha=1.0, binarize=0.31, fit_prior=True, class_prior=None)
    bnb.fit(x_train,y_train)
    
    rtc = RandomForestClassifier(n_estimators=10,max_depth=20, random_state=47)
    rtc.fit(x_train,y_train)

    num_list=[knn.score(x_test,y_test),lg.score(x_test,y_test),
              dtc.score(x_test,y_test),gb.score(x_test,y_test),
              ab.score(x_test,y_test),gnb.score(x_test,y_test),
              svm.score(x_test,y_test),mnb.score(x_test,y_test),
              bnb.score(x_test,y_test),rtc.score(x_test,y_test)]
    name_list = ['KNN','Logistic','DecisionTree','GradientBoosting',
                'AdaBoost','GaussianNB','SVC','MultinomialNB',
                'BernoulliNB','RandomForest']
    plt.title('title')
    num_list=np.around(num_list,decimals=3)
    autolabel(plt.bar(range(len(num_list)),
                      num_list,color='rb',tick_label=name_list,width=0.4))
    plt.show()

if __name__ == '__main__':
    x_train,y_train = load_data(url="to_train.csv",train=True)
    x_test,y_test = load_data(url="test.csv",train=True)
    get_res(x_train,y_train,x_test,y_test)
