import numpy as np
import csv
from sklearn import preprocessing
from sklearn import svm

def difference(data):
    numrows=len(data)
    numcolumns=len(data[0])
    temp = np.zeros((numrows, numcolumns))
    for i in range(numrows-1):
        for j in range(numcolumns):
            temp[i+1,j] = ((float(data[i+1,j]) - float(data[i,j]))/float(data[i,j]))*100
    result = temp[1:,:]
    return result

def binarize(label):
    num = len(label)
    for i in range(num):
        if label[i] >= 0:
            label[i] = 1  ## positive = 1
        else:
            label[i] = 0  ## negative = 0
    return
    
def readdata(filename):
    reader = np.genfromtxt(filename, dtype = np.ndarray, delimiter=',')
    return reader

def writetofile(filename, data):
    csvfile = file(filename, 'wb') ## write to a csv file
    writer = csv.writer(csvfile)
    writer.writerows(data)
    csvfile.close()

raw_data = readdata('interpolated.csv')
numcolumns = len(raw_data[0])
data = raw_data[:,1:numcolumns]
difference = difference(data) ## all values before preprocessing
attribute = np.array([[1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0,13.0,14.0,15.0,16.0]])
difference = np.vstack((attribute,difference))
##for i in range(len(difference)):
##    if difference[i,0] >0:
##        difference[i,0] = 1
##    else:
##        difference[i,0] = 0
##writetofile('readyToLearnDiscrete.csv', difference)
##writetofile('readyToLearn.csv', difference)
##features = difference[:,1:]
##label = difference[:,0]
##scaler = preprocessing.StandardScaler().fit(features)
##scaler.transform(features)    ## scaling the features to have 0 mean
##binarize(label)
##clf = svm.SVC()
##clf.fit(features, label)

