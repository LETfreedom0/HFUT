import pandas as pd
import numpy as np
from numpy.random import RandomState
from sklearn.naive_bayes import GaussianNB,BernoulliNB
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

names = ["make", "address", "all", "3d", "our", "over", "remove", "internet",
                "order", "mail", "receive", "will", "people", "report", "addresses",
                "free", "business", "email", "you", "credit", "your", "font", "000",
                "money", "hp", "hpl", "george", "650", "lab", "labs", "telnet", "857",
                "data", "415", "85", "technology", "1999", "parts", "pm", "direct", "cs",
                "meeting", "original", "project", "re", "edu", "table", "conference",
                ";","(","[","!","$","#","average","longest","total","spam"]


def init_data1():
    data = pd.read_csv("train.txt",names=names)
    d1=data
    
    for ind in d1.index:
        if d1.loc[ind]['spam'] == 'unknown':
            d1.drop(ind,axis=0,inplace=True)
    d1.reset_index()
    d1.to_csv("to_train.csv")

def init_data2():
    data = pd.read_csv("train.txt",names=names)
    d2=data
    
    for inde in d2.index:
        if d2.loc[inde]['spam'] != 'unknown':
            d2.drop(inde,axis=0,inplace=True)
    del d2['spam']
    d2.reset_index(drop=True)
    d2.to_csv("to_predict.csv")
    
def init_data3():
    data = pd.read_csv("test.txt",names=names)
    data.to_csv("test.csv")
        
if __name__ == '__main__':
    #init_data1()
    #init_data2()
    init_data3()
    

#return train_test_split(X, y, test_size=0.3, random_state=RandomState())

