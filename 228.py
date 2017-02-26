# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 07:37:51 2017

@author: Wu
"""

import os
import math
import pandas as pd
import numpy as np
os.chdir('c:/coding/228')


#%%

# estimate 1 : using SDR to estimate 228 daeth count
# SDR means "Sexualized Death Ratio"


data=pd.read_csv('data.txt',sep='\t')
data.loc[:,'SDR']=data.apply(lambda row:float(row['male'])/row['female'],axis=1)
inciData=data.loc[(data['year']==1947) & (data['month'].isin([3,4,5])) ,:]

# different versions of SDR estimation
normalData=data.loc[(data['year']!=1947) & (data['month'].isin([3,4,5])) ,:]
meanSDR=normalData.groupby('month').apply(lambda gData:gData['SDR'].mean())
crossYearSDR=normalData.groupby('month').apply(lambda g:float(g['male'].sum())/g['female'].sum())

#caculation
def estimate(data,SDR,estimateName='228Estimate'):
    data.loc[:,'SDR']=SDR.tolist()
    data.loc[:,'maleEstimate']=data.apply(lambda row:row['female']*row['SDR'],axis=1)
    data.loc[:,estimateName]=data.apply(lambda row:row['male']-row['maleEstimate'],axis=1)
    estimate=data[estimateName].sum()
    return data,estimate

data1_1, estimate1_1 = estimate(inciData, crossYearSDR)
print data1_1
print 'estimate1_1, which presented in the 170225 conference : {}\n'.format(math.ceil(estimate1_1))

data1_2, estimate1_2 = estimate(inciData, meanSDR)
print data1_2
print 'estimate1_2, which used meanSDR: {}\n'.format(math.ceil(estimate1_2))

#%%

#estimate 2: using death date in compensation data to modify estimate 1
execfile('cleanCompenData.py')
compen=pd.read_csv('cleanCompenData.txt',sep='\t')
compen['deathDate']=compen['deathDate'].fillna('')
compen['deathDate']=compen['deathDate'].astype('str')
compen['monthSince1947']=compen['deathDate'].apply(lambda x:int(x[4:6])+(int(x[:4])-1947)*12 if x!='' else None)

monDeath=compen['monthSince1947'].value_counts(dropna=False)

def combineMonth(x):
    if x==2:
        return u'1947年二月'
    elif x>2 and x<6:
        return u'1947年三到五月'
    elif np.isnan(x) or x is None:
        return u'無死亡時間'
    else:
        return u'1947年六月以後'
        
monDeath=monDeath.groupby(combineMonth).sum()
monDeath=monDeath.reindex_axis([u'1947年二月',u'1947年三到五月',u'1947年六月以後',u'無死亡時間'])

monDeath=monDeath.drop(u'無死亡時間')
monDeath=pd.DataFrame({u'死亡人數':monDeath,u'所佔比例':monDeath/monDeath.sum()})


estimate2_1= estimate1_1/monDeath.loc[u'1947年三到五月',u'所佔比例']
print 'estimate2_1, which modified estimate1_1(presented in conferenece) : {}\n'.format(math.ceil(estimate2_1))

estimate2_2= estimate1_2/monDeath.loc[u'1947年三到五月',u'所佔比例']
print 'estimate2_2, which modified estimate1_2: {}\n'.format(math.ceil(estimate2_2))


#%%

#Appendix: estimating the error margin of 228 daeth count estimation using SDR
testData=data.loc[(data['year']==1947) & (~data['month'].isin([3,4,5])) ,:]
testNormalData=data.loc[(data['year']!=1947) & (~data['month'].isin([3,4,5])) ,:]

testMeanSDR=testNormalData.groupby('month').apply(lambda gData:gData['SDR'].mean())
testCrossYearSDR=testNormalData.groupby('month').apply(lambda g:float(g['male'].sum())/g['female'].sum())

testData1_1, errorEstimate1_1=estimate(testData, testMeanSDR, estimateName='errorEstimate')
print testData1_1
print '\naverage estimation error of male normal death, using cross year SDR:{}\n'.format(
        -1*errorEstimate1_1/testData['male'].sum())

testData1_2, errorEstimate1_2=estimate(testData,testCrossYearSDR,estimateName='errorEstimate')
print testData1_2
print '\naverage estimation error of male normal death, using meanSDR:{}\n'.format(
        -1*errorEstimate1_2/testData['male'].sum())              


