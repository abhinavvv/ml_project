import numpy as np
import csv
import Quandl as qd

def buildData(data, column_num):
    data_builder = np.empty((0,2)) ## store only two columns: date and close price
    numrows = len(data)  ## number of rows in raw data
    for i in range(numrows):
        inter = np.hstack((data[i][0],data[i][column_num])) ## inter: used to stack the 'date(first column)' and 'feature' together
        data_builder = np.vstack((data_builder,inter))  ## pile up the data example by example
    return data_builder
    
def writetofile(filename, data):
    csvfile = file(filename, 'wb') ## write to a csv file
    writer = csv.writer(csvfile)
    writer.writerows(data)
    csvfile.close()

def align(base, other):  ## align the data according to Nasdaq trading dates
    numrows = len(base)
    numrows_other = len(other)
    container = np.zeros((numrows,1))  ## could be np.zeros((numrows,1),dtype = 'object')
    flag = 0
    if numrows > numrows_other:
        iteration = numrows_other
        flag = 1
    else:
        iteration = numrows        
    for i in range(iteration):
        if base[i,0] == other[i,0]:    ## if base[i,0] == other[i,0] then just keep that entry in 'container'
            container[i] = other[i,1]
        if base[i,0] < other[i,0]:
            if i == 0:    ## if there's dismatch between the begining date
                container[i] = other[i,1]   ## keep this entry in 'container'
            else:
                for k in range(i-1,-1,-1):
                    if base[i,0] == other[k,0] or base[i,0] > other[k,0]:  ## search upward along 'other'
                        container[i] = other[k,1]
                        break           
        if base[i,0] > other[i,0]:
            for k in range(i+1, numrows_other):      ## search downward along 'other'
                if base[i,0] == other [k,0]:
                    container[i] = other[k,1]
                    break
                if base[i,0] < other[k,0]:
                    container[i] = other[k-1,1]    ## for missing date in 'other', use the previous(maybe several days behind) day's data
                    break
    if flag == 1:   ## if base has more data entries than other
        for i in range(iteration, numrows):
            if base[i,0] == other[numrows_other-1,0]:
                container[i] = other[numrows_other-1,1]
            elif base[i,0] < other[numrows_other-1,0]:
                for k in range(numrows_other-2,-1,-1):
                    if base[i,0] ==  other[k,0] or base[i,0] > other[k,0]:
                        container[i] = other[k,1]
                        break
            else:
                container[i] = other[numrows_other-1,1]             
    result = np.hstack((base, container))   ## align one feather(in 'other') a time
    return result

def normalize(data):
    numrows=len(data)
    numcolumns=len(data[0])
    for i in range(1,numrows):
        for j in range(1,numcolumns-1):
            data[i,j] = (data[i,j] - data[i-1,j])/data[i-1,j]
    data = data[1:,:]
    return

startdate = '2002-01-25'
enddate = '2003-07-26'
data_nasdaq = qd.get('YAHOO/INDEX_IXIC', authtoken='YpYfVsyPaCGms8nrWRRM', \
                  trim_start = startdate, trim_end = enddate, \
                  collapse='daily', returns='numpy')

data_nikkei225 = qd.get('YAHOO/INDEX_N225', authtoken='YpYfVsyPaCGms8nrWRRM', \
                  trim_start = startdate, trim_end = enddate, \
                  collapse='daily', returns='numpy')

data_HengSeng = qd.get('YAHOO/INDEX_HSI', authtoken='YpYfVsyPaCGms8nrWRRM', \
                  trim_start = startdate, trim_end = enddate, \
                  collapse='daily', returns='numpy')

data_silver = qd.get('OFDP/SILVER_5', authtoken='YpYfVsyPaCGms8nrWRRM', \
                  trim_start = startdate, trim_end = enddate, \
                  collapse='daily', returns='numpy')
                  
data_gspc = qd.get('YAHOO/INDEX_GSPC', authtoken='YpYfVsyPaCGms8nrWRRM', \
                  trim_start = startdate, trim_end = enddate, \
                  collapse='daily', returns='numpy')

nasdaq = buildData(data_nasdaq, 4)
nikkei225 = buildData(data_nikkei225, 4)
hengseng = buildData(data_HengSeng, 4)
gspc = buildData(data_gspc,4)
silver = buildData(data_silver, 1)


raw_data = align(nasdaq, nikkei225)
raw_data = align(raw_data, hengseng)
raw_data = align(raw_data, silver)

writetofile('raw.csv',raw_data)






