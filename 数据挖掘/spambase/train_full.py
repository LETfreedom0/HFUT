#-- coding: utf-8 --
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
from sklearn.linear_model import LogisticRegression
import warnings
from predict import get_res
from predict import get_full_data_csv
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")

def load_data(url):
    data = pd.read_csv(url)
    d1 = data.iloc[:,1:58]
    d2 = data.iloc[:,58:]
    return d1,d2

def showScore(flag,acc_score,rec_score):
    plt.title('Prediction Accuracy(number of votes='+str(flag)+')', fontsize=10)
    plt.xlabel('Number of votes', fontsize=10)
    plt.ylabel('Accuracy', fontsize=10)
    xline = np.mgrid[0.6:1.0:20j]
    yline = acc_score
    y = rec_score
    #max_indx=np.argmax(dt_score)
    plt.scatter(xline, yline, c=yline, cmap=plt.cm.Blues, edgecolors='blue', s=10)
    plt.scatter(xline, y, c=y, cmap=plt.cm.Blues, edgecolors='red', s=10)
    for a, b in zip(xline, yline):
        plt.text(a, b + 0.003, '%.4f' % b, ha='center', va='bottom', fontsize=9)
    for a, b in zip(xline, y):
        plt.text(a, b + 0.003, '%.4f' % b, ha='center', va='bottom', fontsize=9)
    plt.plot(xline, yline,label='Accuracy rate')
    plt.plot(xline, y,label='Non spam accuracy')
    # python要用show展现出来图
    plt.legend()
    plt.show()

if __name__ == '__main__':
    for k in range(60,100,5):
        flag=k/100
        print(flag)
        acc_score = []
        rec_score = []
        for i2 in range(60,100,2):#0.75 0.62  0.65  0.70
            flag2=i2/100
            #print(flag2)
            get_full_data_csv(flag)
            x_train,y_train = load_data(url="full_data_t.csv")
            x_test,y_test = load_data(url="test.csv")

            y_test = y_test.values
            res = get_res(x_train,y_train,x_test,flag2)
            size=len(res)
            right = 0
            recall = 0
            sumr = 0
                #print(res)
                #print(y_test[0][0])
            for i in range(0,size):
                if res[i] == y_test[i][0]:
                    right=right+1
                if y_test[i][0] == 0:  #非垃圾邮件
                    sumr = sumr + 1
                    if res[i] == 0:
                        recall = recall + 1
            acc = right/size    #总体正确率
            rec = recall/sumr   #非垃圾邮件正确率
            print(acc,rec,k/100,i2/100)
            acc_score.append(acc)
            rec_score.append(rec)
        print(acc_score)
        print(rec_score)
        #showScore(flag,acc_score, rec_score)
        #print(acc,rec)
        #print(recall,sumr)

