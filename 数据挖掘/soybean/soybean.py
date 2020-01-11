#from __future__ import print_function
import pandas as pd
import numpy as np
#from sklearn import model_selection
#from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
#from sklearn.neighbors import KNeighborsClassifier
#from sklearn.svm import SVC
#from sklearn.naive_bayes import GaussianNB
#from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
#import pickle
from sklearn.preprocessing import Imputer
#from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

import warnings

warnings.filterwarnings("ignore")

def load_data(url):
    names = ['Class', 'date', 'plant-stand', 'precip', 'temp', 'hail', 'crop-hist', 'area-damaged',
             'severity', 'seed-tmt', 'germination', 'plant-growth',
             'leaves', 'leafspots-halo', 'leafspots-marg', 'leafspot-size', 'leaf-shread', 'leaf-malf',
             'leaf-mild', 'stem', 'lodging', 'stem-cankers', 'canker-lesion', 'fruiting-bodies',
             'external decay', 'mycelium', 'int-discolor', 'sclerotia', 'fruit-pods', 'fruit spots',
             'seed', 'mold-growth', 'seed-discolor', 'seed-size', 'shriveling', 'roots']
    dataset = pd.read_csv(url, names=names)
    dataset = dataset.replace({'?':np.nan})
    df1=dataset.iloc[:, 1:]
    df2=dataset.iloc[:, :1]
    imr= Imputer(missing_values = 'NaN', strategy = 'most_frequent', axis = 0 )
    imr = imr.fit(df1)
    imputed_data = imr.transform(df1.values)
    df = pd.DataFrame(imputed_data)
    dataset=pd.concat([df2,df],axis=1)
    array = dataset.values
    x = array[:, 1:]
    y = array[:, 0]
    return x,y,dataset

def DecisionTree(x_train,y_train,x_test,y_test,depth,features):
    dtc = DecisionTreeClassifier(max_depth=depth,max_features=features) #7-9, 31-33
    dtc.fit(x_train, y_train)
    return dtc.score(x_test,y_test)
    #print(dtc.score(x_test,y_test))

   
def RandomForest(x_train,y_train,x_test,y_test,estimators,depth,samples_split,samples_leaf,state):
    rfc = RandomForestClassifier(n_estimators= estimators, max_depth=depth, min_samples_split=samples_split,
                                                   min_samples_leaf=samples_leaf, random_state=state)
    rfc.fit(x_train,y_train)
    return rfc.score(x_test,y_test)
    #print(rfc.score(x_test,y_test))

    
def DrawDTC(x_train,y_train,x_test,y_test):
    depth=[i for i in range(4,16)]
    feature=[i for i in range(20,34)]
    res_depth=[]
    res_feature=[]
    for i in depth:
        sum=0
        for w in range(0,10):
            sum = sum + DecisionTree(x_train,y_train,x_test,y_test,i,32)
        res_depth.append(sum/10)

    for i in feature:
        sum=0
        for w in range(0,10):
            sum = sum + DecisionTree(x_train,y_train,x_test,y_test,8,i)
        res_feature.append(sum/10)

    max_indx1 = np.argmax(res_depth)
    plt.title('max_depth of DecisionTree')
    plt.xlabel('max_depth')
    plt.ylabel('score')
    plt.plot(max_indx1+4,res_depth[max_indx1],'rs')
    plt.plot(depth,res_depth)
    plt.grid(True)
    res_depth=np.around(res_depth,decimals=3)
    for a,b in zip(depth,res_depth):
        plt.text(a,b,b,ha='center',va='bottom')
    plt.show()
    
    max_indx2 = np.argmax(res_feature)
    plt.title('max_features of DecisionTree')
    plt.xlabel('max_features')
    plt.ylabel('score')
    plt.plot(max_indx2+20,res_feature[max_indx2],'ks')
    plt.plot(feature,res_feature)
    plt.grid(True)
    res_feature=np.around(res_feature,decimals=3)
    for a,b in zip(feature,res_feature):
        plt.text(a,b,b,ha='center',va='bottom')
    plt.show()
    
def DrawRTC(x_train,y_train,x_test,y_test):
    estimators=[i for i in range(5,15)]
    depth=[i for i in range(10,20)]
    state=[i for i in range(15,25)]
    res_depth=[]
    res_state=[]
    res_estimators=[]
    for i in estimators:
        sum=0
        for w in range(0,10):
            sum = sum + RandomForest(x_train,y_train,x_test,y_test,i,15,4,1,19)
        res_estimators.append(sum/10)

    for i in depth:
        sum=0
        for w in range(0,10):
            sum = sum + RandomForest(x_train,y_train,x_test,y_test,10,i,4,1,19)
        res_depth.append(sum/10)

    for i in state:
        sum=0
        for w in range(0,10):
            sum = sum + RandomForest(x_train,y_train,x_test,y_test,10,15,4,1,i)
        res_state.append(sum/10)
        
    max_indx1 = np.argmax(res_estimators)
    plt.title('n_estimators of RandomForest')
    plt.xlabel('n_estimators')
    plt.ylabel('score')
    plt.plot(max_indx1+5,res_estimators[max_indx1],'rs')
    plt.plot(estimators,res_estimators)
    plt.grid(True)
    res_estimators=np.around(res_estimators,decimals=3)
    for a,b in zip(estimators,res_estimators):
        plt.text(a,b,b,ha='center',va='bottom')
    plt.show()
    
    max_indx2 = np.argmax(res_depth)
    plt.title('max_depth of RandomForest')
    plt.xlabel('max_depth')
    plt.ylabel('score')
    plt.plot(max_indx2+10,res_depth[max_indx2],'ks')
    plt.plot(depth,res_depth)
    plt.grid(True)
    res_depth=np.around(res_depth,decimals=3)
    for a,b in zip(depth,res_depth):
        plt.text(a,b,b,ha='center',va='bottom')
    plt.show()

    max_indx3 = np.argmax(res_state)
    plt.title('random_state of RandomForest')
    plt.xlabel('random_state')
    plt.ylabel('score')
    plt.plot(max_indx3+15,res_state[max_indx3],'bs')
    plt.plot(state,res_state)
    plt.grid(True)
    res_state=np.around(res_state,decimals=3)
    for a,b in zip(state,res_state):
        plt.text(a,b,b,ha='center',va='bottom')
    plt.show() 

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2.-0.2, 1.03*height, '%s' % float(height))

def DrawBar(x_train,y_train,x_test,y_test):
    name_list = ['DecisionTree','RandomForest']
    num_list = []
    sum=0
    for w in range(0,10):
        sum = sum + DecisionTree(x_train,y_train,x_test,y_test,8,32)
    num_list.append(sum/10)
    sum=0
    for w in range(0,10):
        sum = sum + RandomForest(x_train,y_train,x_test,y_test,10,15,4,1,19)
    num_list.append(sum/10)
    num_list=np.around(num_list,decimals=3)
    plt.title('DecisionTree and RandomForest')
    autolabel(plt.bar(range(len(num_list)), num_list,color='rb',tick_label=name_list,width=0.4))
    plt.show()

 
def Draw(x_train,y_train,x_test,y_test):
    #the best is max_depth=8 ,max_features= 32
    DrawDTC(x_train,y_train,x_test,y_test)
    
    #the best is n_estimators= 10, max_depth=15, min_samples_split=4, min_samples_leaf=1, random_state=19
    DrawRTC(x_train,y_train,x_test,y_test)

    DrawBar(x_train,y_train,x_test,y_test)
    
if __name__ == '__main__':
    name1="soybean-large.data"
    name2="soybean-large.test"
    x_train,y_train,train_data = load_data(name1)
    x_test,y_test,test_data = load_data(name2)

    Draw(x_train,y_train,x_test,y_test)
    #DrawDTC(x_train,y_train,x_test,y_test) #the best is max_depth=8 ,max_features= 32
    #DrawRTC(x_train,y_train,x_test,y_test) #the best is n_estimators= 10, max_depth=15, min_samples_split=4, min_samples_leaf=1, random_state=19
    #DrawBar(x_train,y_train,x_test,y_test)
    


    
    
    
    
