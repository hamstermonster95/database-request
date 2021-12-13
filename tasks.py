
from django.conf import settings
import requests
import urllib
import urllib.request as urllib2
import json
import pandas as pd
import numpy as np
from tempfile import TemporaryFile
import base64
from django.shortcuts import render, redirect
from celery.decorators import task
from celery.utils.log import get_task_logger
import base64
from celery.worker.request import Request


@task(name="get_data")
def get_data():

        
    engine = create_engine('postgres://Analytics:pe817e57a697cec3465b3786454373e603974f2481bc4884a587fd59213c591ba@ec2-34-246-15-148.eu-west-1.compute.amazonaws.com:5432/d45o17p5ncfeid')
    key_values = pd.read_sql('SELECT * FROM key_values', engine)
    resultPositions= key_values['value'][1]
    panelPositions= key_values['value'][8]
    labs=key_values['value'][22]
    resultPositions=todf(resultPositions)
    panelPositions=todf(panelPositions)
    labs=todf(labs)
    database_url = 'postgres://eyubuloglbxgpo:0bb4b2888e3a7794bcaa965d73e7e13301ad2b1585cbaf7e9ee1f1b4cd6e9591@ec2-184-73-198-174.compute-1.amazonaws.com:5432/d4ee7jenm82fu'

    engine1 = create_engine(database_url)
    merged_inner= pd.read_sql('SELECT * FROM merged_innez', engine1)                
    resultz= pd.read_sql('SELECT * FROM results', engine1)  

    bypos = form['bypos']
    

    if (bypos == 'by result position'):
        resultz['result_position_id']=resultz['result_position_id'].astype(str)
        resultpos = resultz['result_id'].unique()

                # In[92]:

                # In[93]:
        resultz['result_position_id']=resultz['result_position_id'].astype(str)
        grouped = resultz.groupby('result_position_id')

                    # In[94]:

                    
        final = merged_inner
        a = 0
                    
        names = []
                    #russianpanelpos = unite['64aa8df1-6dc1-4cdd-956f-033f343ecd72'].to_list()

        biochem = resultpos  # faster!

        for name, group in grouped:
            print(name)
            if name in biochem:
                names.append(name)
                b = group
                b = pd.DataFrame(b)
                b = b[['blood_test_id', 'absolute_value']]
                b['blood_test_id']=b['blood_test_id'].astype(str)
                final['blood_test_id']=final['blood_test_id'].astype(str)
                final = pd.merge(left=final, right=b, left_on='blood_test_id', right_on='blood_test_id', how='left')
                final = final.rename(columns={'absolute_value': name})
                a = a+1
                print(a)

        final = final.drop_duplicates()

                    # In[97]:

        old_names = final.columns[3:]

        refranges = pd.DataFrame(columns=['result position id'])
        refranges['result position id'] = old_names

        refranges = pd.merge(refranges, resultPositions, left_on='result position id',
                                         right_on='result position id', how='left')

        new_names = refranges['reference ranges']
        final.rename(columns=dict(zip(old_names, new_names)), inplace=True)

                    # In[98]:
                    
        final = final.dropna(how='all')
                    
        final.to_sql(name='merged_inbnez', con=engine1, index = False, if_exists= 'replace')
                # In[100]:

    elif (bypos == 'by panel position'):
        resultz['panel_position_id']=resultz['panel_position_id'].astype(str)
        panelpos = resultz['panel_position_id'].unique()

                # In[101]:
                    
        grouped = resultz.groupby('panel_position_id')

                    # In[102]:

        final = merged_inner
        a = 0
                    
        names = []
                    #russianpanelpos = unite['64aa8df1-6dc1-4cdd-956f-033f343ecd72'].to_list()

        biochem = panelpos  # faster!

        for name, group in grouped:
            print(name)
            if name in biochem:
                names.append(name)
                b = group
                b = pd.DataFrame(b)
                b = b[['blood_test_id', 'absolute_value']]
                b['blood_test_id']=b['blood_test_id'].astype(str)
                final['blood_test_id']=final['blood_test_id'].astype(str)
                final = pd.merge(left=final, right=b, left_on='blood_test_id', right_on='blood_test_id', how='left')
                final = final.rename(columns={'absolute_value': name})
                a = a+1
                print(a)

        final = final.drop_duplicates()

        old_names = final.columns[3:]

        labz = pd.DataFrame(columns=['id'])
        labz['id'] = old_names

                    

        labz = pd.merge(labz, panelPositions, left_on='id',right_on='id', how='left')

        labz = pd.merge(labz, labs, left_on='lab',right_on='id', how='left')

        new_names = labz['name in lab']
        final.rename(columns=dict(zip(old_names, new_names)), inplace=True)
                    
                    # In[109]:
                    #info = final[['patient id', 'gender', 'age']]
                    #final.index = final['patient id']

                    #final = final.drop(columns={'patient id', 'gender', 'age', 'order id',
        final = final.dropna(how='all')
        final.to_sql(name='merged_innez', con=engine1, index = False, if_exists= 'replace')
                    #final = pd. merge(info, final,  right_on=final.index,
                    #                 left_on='patient id', how='right')

                    


                # In[140]:

    elif (bypos == 'by normal position'):

        final = merged_inner
        a = 0
                    
        names = []
                    #russianpanelpos = unite['64aa8df1-6dc1-4cdd-956f-033f343ecd72'].to_list()
        b = resultz
        b = b[['blood_test_id', 'absolute_value']]
        b['blood_test_id']=b['blood_test_id'].astype(str)
        final['blood_test_id']=final['blood_test_id'].astype(str)
        final = pd.merge(left=final, right=b, left_on='blood_test_id',right_on='blood_test_id', how='left')
        final = final.rename(columns={'absolute_value': tests})
                    

        final = final.dropna(how='any')
        final.to_sql(name='merged_innez', con=engine1, index = False, if_exists= 'replace')


@task(name="get_data1")
def get_data1():
        



        return data1

			