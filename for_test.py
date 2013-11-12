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

def shift(base,other):
    container = np.zeros((len(base),1))
    temp = []
    j=1
    if len(base) > len(other): #to make both of equal size
        for i in range(len(base)-len(other)):
            other_value = [other[len(other)-1][0],other[len(other)-1][1]]
            temp.append(other_value)
        for i in range(len(temp)):
            other = np.vstack((other,temp[i]))
    for i in range(len(base)): # based out of nasdaq date 
        if other[i,0] > base[i,0]:  #suppose other date is greater we check if this is the best date thats greater
            j=i
            while (other[j,0] > base[i,0]) and (j!=0):
                j = j-1
            j = j+1 if j+1 < len(other) else j
            container[i] = other[j,1]
        if other[i,0] <= base[i,0]:  #suppose other date is lesser we go to best greatest date
            j=i
            while(other[j,0] <= base[i,0]):
                if j+1 < len(other):
                    j = j+1
                else:
                    break
            container[i] = other[j,1]
    result = np.hstack((base, container))
    return result

startdate = '2007-01-04'
enddate = '2011-12-04'
data_nasdaq = qd.get('YAHOO/INDEX_IXIC', authtoken='YpYfVsyPaCGms8nrWRRM', \
                  trim_start = startdate, trim_end = enddate, \
                  collapse='daily', returns='numpy')   ## Nasdaq

data_nikkei225 = qd.get('YAHOO/INDEX_N225', authtoken='YpYfVsyPaCGms8nrWRRM', \
                  trim_start = startdate, trim_end = enddate, \
                  collapse='daily', returns='numpy')    ## Japan Nikkei225

data_HengSeng = qd.get('YAHOO/INDEX_HSI', authtoken='YpYfVsyPaCGms8nrWRRM', \
                  trim_start = startdate, trim_end = enddate, \
                  collapse='daily', returns='numpy')  ## HK Hang Seng Index

data_ASX200 = qd.get('YAHOO/INDEX_AXJO', authtoken='YpYfVsyPaCGms8nrWRRM', \
                         trim_start = startdate, trim_end = enddate, \
                         collapse='daily', returns='numpy')  ## Australia Securities Exchange

data_STI = qd.get('YAHOO/INDEX_STI', authtoken='YpYfVsyPaCGms8nrWRRM', \
                         trim_start = startdate, trim_end = enddate, \
                         collapse='daily', returns='numpy')     ## Singapore Straits Times Index

data_silver = qd.get('OFDP/SILVER_5', authtoken='YpYfVsyPaCGms8nrWRRM', \
                  trim_start = startdate, trim_end = enddate, \
                  collapse='daily', returns='numpy')  ## London fixing price

data_gold = qd.get('OFDP/GOLD_1', authtoken='YpYfVsyPaCGms8nrWRRM', \
                  trim_start = startdate, trim_end = enddate, \
                  collapse='daily', returns='numpy')  ## London AM fixing price

data_oil = qd.get('FRED/DCOILWTICO', authtoken='YpYfVsyPaCGms8nrWRRM', \
                  trim_start = startdate, trim_end = enddate, \
                  collapse='daily', returns='numpy')  ## New York West Texax Intermediate Futures Price

data_JPY = qd.get('QUANDL/USDJPY', authtoken='YpYfVsyPaCGms8nrWRRM', \
                  trim_start = startdate, trim_end = enddate, \
                  collapse='daily', returns='numpy')  ## USD vs JPY from Quandle, amalgamation of rates

data_EUR = qd.get('QUANDL/EURUSD', authtoken='YpYfVsyPaCGms8nrWRRM', \
                  trim_start = startdate, trim_end = enddate, \
                  collapse='daily', returns='numpy')  ## EUR vs USD from Quandle, amalgamation of rates

data_AUD = qd.get('QUANDL/USDAUD', authtoken='YpYfVsyPaCGms8nrWRRM', \
                  trim_start = startdate, trim_end = enddate, \
                  collapse='daily', returns='numpy')  ## USD vs AUD from Quandle, amalgamation of rates

## filter in only relevant columns(date and price)
nasdaq = buildData(data_nasdaq, 4)
nikkei225 = buildData(data_nikkei225, 4)
hengseng = buildData(data_HengSeng, 4)
silver = buildData(data_silver, 1)
sti = buildData(data_STI, 4)
asx = buildData(data_ASX200, 4)
gold = buildData(data_gold, 1)
oil = buildData(data_oil, 1)
jpy = buildData(data_JPY, 1)
eur = buildData(data_EUR, 1)
aud = buildData(data_AUD, 1)
## align the data according to Nasdaq trading dates
raw_data = align(nasdaq, nikkei225)
raw_data = align(raw_data, hengseng)
raw_data = align(raw_data, sti)
#raw_data = shift(raw_data,sti)
#raw_data = align(raw_data, asx)
raw_data = shift(raw_data, asx)
raw_data = align(raw_data, gold)
raw_data = align(raw_data, silver)
#raw_data = shift(raw_data, oil)
raw_data = align(raw_data, oil)
raw_data = align(raw_data, jpy)
#raw_data = shift(raw_data,jpy)
raw_data = align(raw_data, eur)
raw_data = align(raw_data, aud)
writetofile('raw.csv',raw_data)







