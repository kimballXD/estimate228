# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 07:21:43 2017

@author: Wu
"""

import os
import re
import pandas as pd

#read file
os.chdir('c:/coding/228')
rawCompen=pd.read_csv('compensate.txt',sep='\t')


# fill na by column type
for col in ['age']:
    rawCompen[col]=rawCompen[col].fillna(0)
for col in ['name', 'town', 'profession1', 'profession2', 'compenDate', 'regDate', 'type']:
    rawCompen[col]=rawCompen[col].fillna('')


# formating death date 
for col in ['compenDate','regDate']:
    rawCompen[col]=rawCompen[col].apply(lambda x:'0'+x if re.match('^[0-9]{3}$',x) else x)
    rawCompen[col]=rawCompen[col].str.replace('?','0')
    rawCompen[col]=rawCompen[col].apply(lambda x:'1947'+x if re.match('^[0-9]{4}$',x) else x)


# choose a valid death date   
def compareDate(row):
    if all([row['compenDate'],row['regDate']]) and row['compenDate']==row['regDate']:
        return 'agree'
    elif all([row['compenDate'],row['regDate']]) and row['compenDate']!=row['regDate']:
        return 'agreeMonth' if row['compenDate'][4:6]==row['regDate'][4:6] else 'disagree'
        
    elif not any([row['compenDate'],row['regDate']]):
        return 'na'
    else:
        return 'compenDate' if row['compenDate']!='' else 'regDate'
        
def cleanDate(row):
    if row['compareDate']=='agree':
        return row['compenDate']
    elif row['compareDate']=='disagree':
        # manully check rawCompen to comfrim that compenDate were more reasonable in most cases
        return row['compenDate'] 
    elif row['compareDate'] in ['compenDate','regDate']:
        return row[row['compareDate']]
    elif row['compareDate']=='na':
        return ''
        
rawCompen['compareDate']=rawCompen.apply(compareDate,axis=1)
rawCompen['deathDate']=rawCompen.apply(cleanDate,axis=1)


# formating rawCompen output
output=rawCompen.drop(['compenDate','regDate','compareDate'],axis=1)
output.to_csv('cleanCompenrawCompen.txt',encoding='utf8',sep='\t',index=False)