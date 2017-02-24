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
normalData=data.loc[(data['year']!=1947) & (data['month'].isin([3,4,5])) ,:]
normalData.loc[:,'SDR']=normalData.apply(lambda row:float(row['male'])/row['female'],axis=1)
normalSDR=normalData.groupby('month').apply(lambda gData:gData['SDR'].mean())

inciData=data.loc[(data['year']==1947) & (data['month'].isin([3,4,5])) ,:]
inciData.loc[:,'SMRR']=normalSDR.tolist()
inciData.loc[:,'maleEstimate']=inciData.apply(lambda row:row['female']*row['SMRR'],axis=1)
inciData.loc[:,'228Estimate']=inciData.apply(lambda row:row['male']-row['maleEstimate'],axis=1)
estimate1=inciData['228Estimate'].sum()
print 'estimate1: {}'.format(math.ceil(estimate1))
#%%%


#estimate 2: using death date in compensation data to modify estimate 1
execfile('cleanCompenData.py')
compen=pd.read_csv('cleanCompenData.txt',sep='\t')
compen['deathDate']=data['deathDate'].fillna('')
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
estimate2=estimate1/monDeath.loc[u'1947年三到五月',u'所佔比例']
print 'estimate2: {}'.format(math.ceil(estimate2))


#%%

