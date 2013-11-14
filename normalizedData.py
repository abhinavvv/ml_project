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
            temp[i+1,j] = ((data[i+1,j] - data[i,j])/data[i,j])*100
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
    reader = np.genfromtxt(filename, dtype = float, delimiter=',')
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
writetofile('toAnalyze.csv', difference)
scaler = preprocessing.StandardScaler().fit(difference)
scaler.transform(difference)    ## scaling the features to have 0 mean
writetofile('scaled.csv', difference)
