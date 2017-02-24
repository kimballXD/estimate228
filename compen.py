# -*- coding: utf-8 -*-
"""
Created on Sat Feb 04 16:38:40 2017

@author: Wu
"""

import os
import re
import pandas as pd
import numpy as np

os.chdir('c:/coding/228')
data=pd.read_csv('compensate.txt',sep='\t')

for col in ['age']:
    data[col]=data[col].fillna(0)
for col in ['name', 'town', 'profession1', 'profession2', 'compenDate', 'regDate', 'type']:
    data[col]=data[col].fillna('')


for col in ['compenDate','regDate']:
    data[col]=data[col].apply(lambda x:'0'+x if re.match('^[0-9]{3}$',x) else x)
    data[col]=data[col].str.replace('?','0')
    data[col]=data[col].apply(lambda x:'1947'+x if re.match('^[0-9]{4}$',x) else x)
    

def compareDate(row):
    if all([row['compenDate'],row['regDate']]) and row['compenDate']==row['regDate']:
        return 'agree'
    elif all([row['compenDate'],row['regDate']]) and row['compenDate']!=row['regDate']:
        return 'agreeMonth' if row['compenDate'][4:6]==row['regDate'][4:6] else 'disagree'
        
    elif not any([row['compenDate'],row['regDate']]):
        return 'na'
    else:
        return 'compenDate' if row['compenDate']!='' else 'regDate'
        
def genDate(row):
    if row['compareDate']=='agree':
        return row['compenDate']
    elif row['compareDate']=='disagree':
        # manully check data to comfrim that compenDate were more reasonable in most cases
        return row['compenDate'] 
    elif row['compareDate'] in ['compenDate','regDate']:
        return row[row['compareDate']]
    elif row['compareDate']=='na':
        return np.nan
        
data['compareDate']=data.apply(compareDate,axis=1)
data['cleanDate']=data.apply(genDate,axis=1)
output=data.drop(['compenDate','regDate'],axis=1)
output.to_csv('cleanCompenData.csv',encoding='utf8',sep='\t')
#%%

#%%

chen=pd.read_csv('chen.txt',sep='\t')
chen['group']=chen['age'].apply(lambda x:x>14 and x <69)
chen2=chen.loc[chen['group']==True,:]

chenSum=chen.groupby('sex').apply(lambda gData: gData.apply(lambda col: col.sum(),axis=0))
chenSum=chenSum.drop(['age','sex'],axis=1)
#chenSum=chenSum.reset_index()

chenSum2=chen2.groupby('sex').apply(lambda gData: gData.apply(lambda col: col.sum(),axis=0))
chenSum2=chenSum2.drop(['age','sex'],axis=1)
#chenSum2=chenSum2.reset_index()

prop2=np.divide(np.matrix(chenSum2).astype(float),np.matrix(chenSum).astype(float))
prop2=pd.DataFrame(prop2)
prop2.columns=chenSum.columns
prop2.index=chenSum2.index
g47=241071-114192+29569
#%%
for col in ['reg46', 'estimate1', 'estimate2', 'estimate3', 'estimate4']:
#    print col, chenSum2.loc[chenSum2['sex']=='male','reg47'].tolist()[0]-chenSum2.loc[chenSum2['sex']=='male',col].tolist()[0]-g47
#    print col, g47-(chenSum['reg47'].sum()-chenSum[col].sum())
     print col
     print chen['reg47']-chen[col]

chen3=chen2.copy()     
for col in ['reg46', 'estimate1', 'estimate2', 'estimate3', 'estimate4']:
    chen3[col]=chen3['reg47']-chen3[col]
    print col, g47*prop2.loc['male','reg46']-(chenSum2.loc['male','reg47']-chenSum2.loc['male',col])
    
#%%




