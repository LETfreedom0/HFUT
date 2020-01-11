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

import warnings

warnings.filterwarnings("ignore")

def load_data(url,train):
    data = pd.read_csv(url)
    d1 = data.iloc[:,1:58]
    d2 = data.iloc[:,58:]
    if train:
        return d1,d2,data
    else:
        data = data.iloc[:,1:]
        return data
        
def get_res(x_train,y_train,x_pre,flag):
    """
    knn = KNeighborsClassifier()
    knn.fit(x_train,y_train)
    knn_pre = knn.predict(x_pre)
    #knn_pre = pd.DataFrame(knn_pre)
    """
    lg = LogisticRegression(penalty='l2')
    lg.fit(x_train,y_train)
    lg_pre = lg.predict(x_pre)
    #lg_pre = pd.DataFrame(lg_pre)
    
    dtc = DecisionTreeClassifier()
    dtc.fit(x_train,y_train)
    dtc_pre = dtc.predict(x_pre)
    #dtc_pre = pd.DataFrame(dtc_pre)
    
    gb = GradientBoostingClassifier(n_estimators=200)
    gb.fit(x_train,y_train)
    gb_pre = gb.predict(x_pre)
    #gb_pre = pd.DataFrame(gb_pre)
    
    ab = AdaBoostClassifier(algorithm="SAMME.R", learning_rate=1.0,n_estimators=16)
    ab.fit(x_train,y_train)
    ab_pre = ab.predict(x_pre)
    #ab_pre = pd.DataFrame(ab_pre)
    """
    gnb = GaussianNB()
    gnb.fit(x_train,y_train)
    gnb_pre = gnb.predict(x_pre)
    #gnb_pre = pd.DataFrame(gnb_pre)
    
    svm = SVC(kernel='rbf', probability=True)
    svm.fit(x_train,y_train)
    svm_pre = svm.predict(x_pre)
    #svm_pre = pd.DataFrame(svm_pre)
    
    mnb = MultinomialNB(alpha=0.01)
    mnb.fit(x_train,y_train)
    mnb_pre = mnb.predict(x_pre)
    #mnb_pre = pd.DataFrame(mnb_pre)
    """
    """
    bnb = BernoulliNB()
    bnb.fit(x_train,y_train)
    bnb_pre = bnb.predict(x_pre)
    #bnb_pre = pd.DataFrame(bnb_pre)
    """
    rtc = RandomForestClassifier(n_estimators=10,max_depth=20, random_state=47)
    rtc.fit(x_train,y_train)
    rtc_pre = rtc.predict(x_pre)
    #rtc_pre = pd.DataFrame(rtc_pre)

    size = rtc_pre.size

    res = []
    for i in range(0,size):
        """
        arr=[knn_pre[i],lg_pre[i],dtc_pre[i],gb_pre[i],ab_pre[i],gnb_pre[i],
             svm_pre[i],mnb_pre[i],bnb_pre[i],rtc_pre[i]]
        """
        arr=[lg_pre[i]*0.15,dtc_pre[i]*0.1,gb_pre[i]*0.2,ab_pre[i]*0.3,rtc_pre[i]*0.25]
        #print(arr)#输出数据用4，训练预测用4
        if np.sum(arr)>=flag:
            res.append(1)
        else:
            res.append(0)
    return res
def get_full_data_csv(flag):
#if __name__ == '__main__':
    x_train,y_train,data_train = load_data(url="to_train.csv",train=True)
    x_pre = load_data(url="to_predict.csv",train=False)
    #print(x_train)

    res = get_res(x_train,y_train,x_pre,flag)
    res = pd.DataFrame(res,columns = ['spam'])
    #print(res)
    dataset = pd.concat([x_pre,res],axis=1)
    #dataset = dataset.iloc[:,1:]
    #print(dataset)
    data_train = data_train.iloc[:,1:]
    #print(data_train)
    data_train = data_train.append(dataset,ignore_index=False)
    data_train.to_csv("full_data_t.csv")
