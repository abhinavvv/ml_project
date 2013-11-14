import numpy as np
import csv

def readdata(filename):
    reader = np.genfromtxt(filename, dtype = float, delimiter=',')
    return reader

def writetofile(filename, data):
    csvfile = file(filename, 'wb') ## write to a csv file
    writer = csv.writer(csvfile)
    writer.writerows(data)
    csvfile.close()

def linearInterpolation(a):
    numrows = len(a)
    numcolumns = len(a[0])
    temp = np.zeros((numrows,numcolumns))
    temp = a[:,:]
    for i in range(1,numcolumns):
        finish = 0
        for j in range(numrows-1):
            k=j
            while True:
                if (a[j,i] == a[k+1,i]):
                    k=k+1
                    if k == numrows - 1:
                        temp[j+1,i] = (a[j,i]+a[j-1,i])/2
                        finish = 1
                        break
                else:
                    break
            if finish == 1:
                break
            temp[j+1,i] = (a[j,i] + a[k+1,i])/2 if k > j else a[j+1,i]
    return temp

raw_data = readdata('raw.csv')
interpolated = linearInterpolation(raw_data)
writetofile('interpolated.csv', interpolated)
