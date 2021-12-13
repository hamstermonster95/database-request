from .forms import LocationForm, OrderForm, TestForm, ByPosForm, Loading
from django.http import HttpResponse
import json 
import pandas as pd
from django.shortcuts import render, redirect
from django.urls import reverse
from celery.result import AsyncResult
import time
from django.views.generic import FormView, TemplateView
import numpy as np
from datetime import datetime, timedelta
import psycopg2
from sqlalchemy import create_engine
import sqlite3
import requests








    


def todf(obj):
	df = pd.DataFrame(obj)
	df.columns = df.iloc[0]
	df.columns = df.columns.str.split("\n").str[1]
	df = df.drop([0])
	return df


def todf1(obj):
	df = pd.DataFrame(obj)
	return df

class LocationView(FormView):
	template_name= 'location.html'
	form_class = LocationForm

	def get_location(request):
		if request.method == 'POST':

				form = request.POST
				
				order_numbr = form['order_number']
				lab = form['lab']
				component=form['component']
				

				engine = create_engine('postgresql://rpm_analyst:0223b547-57ac-47b4-8f23-340c24ad2986@rpm-postgres.postgres.database.azure.com/rpm_db_prod')

				global patients

				patients = pd.read_sql("SELECT patient_id, date_of_birth, gender_id, office_id FROM patients", engine)
				patients['gender_id']=patients['gender_id'].astype(str)

				patients = patients.replace(
					'388d85f2-3016-41d3-a7cf-024ba1b3e16d', '0')
				patients = patients.replace(
					'ae2015ac-1262-4742-b2b0-f2b15c5b75e8', '1')

				now = pd.Timestamp('now')
				now = now.tz_localize('UTC')

				patients['date_of_birth'] = pd.to_datetime(patients['date_of_birth'], format='%Y-%m-%d')
				from dateutil.relativedelta import relativedelta

				for index, value in patients['date_of_birth'].iteritems():
					rdelta = relativedelta(now, value)
					patients['date_of_birth'][index]=rdelta.years
	    
				patients=patients.rename(columns={'date_of_birth':'age'})

				patients = patients.drop(columns=['office_id'])
				orders= pd.read_sql('SELECT order_id, patient_id, created_date FROM orders', engine)

				bloodtests= pd.read_sql('SELECT blood_test_id, order_id, lab_id FROM blood_tests', engine)

				
				orders['patient_id']= orders['patient_id'].astype(str)
				patients['patient_id']= patients['patient_id'].astype(str)		
				merged_inner = pd.merge(left=patients, right=orders, left_on='patient_id', right_on='patient_id')

				merged_inner=merged_inner.dropna(axis=0, how='any')
				merged_inner['created_date'] = pd.to_datetime(merged_inner['created_date'], format='%Y-%m-%d')
				merged_inner['orderoforder'] = merged_inner.groupby(['patient_id'])['created_date'].rank(ascending=True, method='dense').astype(int)
	
				if (order_numbr == '1'):
					merged_inner = merged_inner[merged_inner['orderoforder'] == 1]

					
					merged_inner['order_id']=merged_inner['order_id'].astype(str)
					bloodtests['order_id']=bloodtests['order_id'].astype(str)
					merged_inner = pd.merge(left=merged_inner, right=bloodtests, left_on='order_id', right_on='order_id')
					
					merged_inner = merged_inner.drop(columns=['orderoforder', 'created_date', 'blood_test_id'])

						
				elif (order_numbr == '2'):
					merged_inner = merged_inner[merged_inner['orderoforder'] == 2]

					
					merged_inner = pd.merge(left=merged_inner, right=bloodtests, left_on='order_id', right_on='order_id')
					
					merged_inner = merged_inner.drop(columns=['orderoforder', 'created_date', 'blood_test_id'])

					
						

						
				else:
					merged_inner = merged_inner[merged_inner['orderoforder'] == 3]

					
					merged_inner = pd.merge(left=merged_inner, right=bloodtests, left_on='order_id', right_on='order_id')
					
					merged_inner = merged_inner.drop(columns=['orderoforder', 'created_date', 'blood_test_id'])
				merged_inner['lab_id']=merged_inner['lab_id'].astype(str)

				if (lab=='Chromolab / KDL'):
					merged_inner=merged_inner[merged_inner['lab_id']=='dbeb7d4f-5842-40de-80e0-3fb634478969']
				elif (lab=='Medsi / Chromolab'):
					merged_inner=merged_inner[merged_inner['lab_id']=='c86ba035-fa9c-4f6b-897d-0688760cd3c9']
				elif (lab=='Invitro'):
					merged_inner=merged_inner[merged_inner['lab_id']=='ec739fa6-786c-47da-adea-b71fdbc8b939']
				elif (lab=='Medical Diagnosis'):
					merged_inner=merged_inner[merged_inner['lab_id']=='012317fe-3a5c-4027-9264-4859948013f5']
				elif (lab=='TDL'):
					merged_inner=merged_inner[merged_inner['lab_id']=='4c8659a1-376e-4ccf-aaab-451cd8cdf31a']						
				elif (lab=='Lenco'):
					merged_inner=merged_inner[merged_inner['lab_id']=='5d453c28-ae2b-4f24-81f3-f9036c397971']
				elif (lab=='FML ME'):
					merged_inner=merged_inner[merged_inner['lab_id']=='c15b79f1-cea6-4b7d-b7de-52ee5ab6bfa2']
				elif (lab=='EMC'):
					merged_inner=merged_inner[merged_inner['lab_id']=='bd1c0624-65e2-4551-a342-a3dc83a1182d']
				elif (lab=='Medichecks'):
					merged_inner=merged_inner[merged_inner['lab_id']=='1ab1eb83-fd00-45e3-84f7-9123a30ef0fc']
				else:
					merged_inner=merged_inner.replace('1ab1eb83-fd00-45e3-84f7-9123a30ef0fc', 'Medichecks')
					merged_inner=merged_inner.replace('bd1c0624-65e2-4551-a342-a3dc83a1182d', 'EMC')
					merged_inner=merged_inner.replace('c15b79f1-cea6-4b7d-b7de-52ee5ab6bfa2', 'FML ME')
					merged_inner=merged_inner.replace('5d453c28-ae2b-4f24-81f3-f9036c397971', 'Lenco')
					merged_inner=merged_inner.replace('4c8659a1-376e-4ccf-aaab-451cd8cdf31a', 'TDL')
					merged_inner=merged_inner.replace('ec739fa6-786c-47da-adea-b71fdbc8b939', 'Invitro')
					merged_inner=merged_inner.replace('c86ba035-fa9c-4f6b-897d-0688760cd3c9', 'Medsi / Chromolab')
					merged_inner=merged_inner.replace('012317fe-3a5c-4027-9264-4859948013f5', 'Medical Diagnosis')
					merged_inner=merged_inner.replace('dbeb7d4f-5842-40de-80e0-3fb634478969', 'Chromolab / KDL')

				formulas = pd.read_sql("SELECT formula_id, order_id FROM formulas", engine)
				formulas['order_id']=formulas['order_id'].astype(str)
				merged_inner['order_id']=merged_inner['order_id'].astype(str)

				merged_inner = pd.merge(merged_inner, formulas, left_on='order_id', right_on='order_id', how='left')
				merged_inner['formula_id']=merged_inner['formula_id'].astype(str)

				final=merged_inner

				


				key_values=pd.read_sql("SELECT * FROM key_values WHERE key= 'components'", engine)
				components= key_values['value'][0]
				components=todf(components)

				if (component=='Vitamine Komplex'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='443f48b6-9c0c-4a95-a854-5f873e81c150'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Vitamine Komplex'})
				if (component=='Spurenelemente SE Komplex'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='a6251dd8-9de9-4245-98b2-18ed972164d9'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Spurenelemente SE Komplex'})
				if (component=='Coenzym Q10 retard'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='78ef525e-d3bd-46f2-baae-229770db867c'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Coenzym Q10 retard'})
				if (component=='Chrom [Chromium]'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='4c6a7433-8bb5-4fac-90a3-c6d63a24d014'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Chrom [Chromium]'})
				if (component=='Eisen [Iron]'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='ab0d7ef6-e040-4d76-b809-d3c93c7d504b'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Eisen [Iron]'})
				if (component=='Folsäure [Folic acid]'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='33699af8-baf4-4a03-add2-9622cb2b9080'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Folsäure [Folic acid]'})
				if (component=='Glutathion'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='270ca680-0090-4cde-8f20-56521e8e52bb'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Glutathion'})
				if (component=='Inositol Hexanicotinat'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='95e170d3-f2d8-42b0-b764-9bc3c4e7df35'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Inositol Hexanicotinat'})
				if (component=='Isoflavone Extrakt'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='29374e1c-0c86-41e0-9753-ba92eaa22acf'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Isoflavone Extrakt'})
				if (component=='Glutamin (L-)'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='9c903e91-9cd7-45d6-9cdc-8a1f526df61d'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Glutamin (L-)'})

				if (component=='Griffonia simplicifolia [L-5-HTP]'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='bfb24c64-33ff-4b4f-bc02-4e1032081ed4'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Griffonia simplicifolia [L-5-HTP]'})
				if (component=='Lysin (L-)'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='258b3e84-5298-4544-8e76-b9e095fe23e6'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Lysin (L-)'})
				if (component=='Tryptophan (L-)'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='f2241ea3-32c9-497f-aab2-c4c1aa0afaf2'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Tryptophan (L-)'})
				if (component=='Rhodiola Extrakt'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='01e32bfd-febd-45ef-a411-1a5a2b487a2a'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Rhodiola Extrakt'})
				if (component=='Selen [Selenium]'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='3d937066-c79d-403c-b965-ccb4c82aa5c2'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Selen [Selenium]'})
				if (component=='Silymarin Extrakt'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='272ac6b9-170b-4994-aa86-270c2ab32365'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Silymarin Extrakt'})

				if (component=='Vitamin B1'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='f95164b7-cd27-419f-b185-e5fde4ee1b96'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Vitamin B1'})
				if (component=='Vitamin B6'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='5e74ba5d-9cea-42e3-bf22-c96a46cfb913'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Vitamin B6'})
				if (component=='Vitamin B12'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='5daab7ec-e3d3-432a-b32e-62c66bddb850'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Vitamin B12'})
				if (component=='Vitamin C'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='38c42b07-2bf8-4b05-b643-ff8a253c53f3'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Vitamin C'})
				if (component=='Vitamin D3'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='eb20d706-0f02-4a54-9f5e-c5441d5e2798'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Vitamin D3'})
				if (component=='Vitamin K2'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='e8b55456-ee34-4684-87b7-1366713fb4aa'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Vitamin K2'})
				if (component=='Vitamin E NAT Komplex'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='6a190e2b-61a7-403f-9045-61d9c7b09ff8'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Vitamin E NAT Komplex'})
				if (component=='Zink'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='253e2017-1b3e-4b59-8b4c-77bde175546e'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Zink'})
				if (component=='Tyrosin (L-)'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='c892dba1-bd61-4385-afdb-6785d77b1346'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Tyrosin (L-)'})
				if (component=='Liponsäure (α-) [Lipoic acid]'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='0600bfca-6c38-474b-a027-7634b477e214'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Liponsäure (α-) [Lipoic acid]'})
				if (component=='Bioflavonoide Komplex'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='42894e44-4d95-4b91-b403-9b187dc0b32c'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Bioflavonoide Komplex'})

				if (component=='Biotin'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='73142242-fb7f-437a-8be5-862c6c824f93'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Biotin'})
				if (component=='Curcumin und Piperin'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='759f1a83-f4cf-4fce-b6e2-b4e311d1668b'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Curcumin und Piperin'})
				if (component=='Ginseng Extrakt'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='fc34d81a-26cf-4c9c-b567-b452f216a063'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Ginseng Extrakt'})
				if (component=='Glucosaminsulfat'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='9ceda665-d9e6-44c9-b3e4-65098e5fb2ce'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Glucosaminsulfat'})
				if (component=='Kupfer [Copper]'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='9f68d5bc-1448-44e5-bd51-d1a13dcfb1f6'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Kupfer [Copper]'})
				if (component=='Lycopen'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='95ca0544-3dd5-4409-8f91-3eece96b116b'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Lycopen'})
				if (component=='Methylsulfonylmethan (MSM)'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='b45ba586-955b-4ad9-beca-ec58f8c9f2af'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Methylsulfonylmethan (MSM)'})
				if (component=='Chondroitinsulfat [Chondroitin sulphate]'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='db77a45b-e2a8-4e3f-a613-33b679f2ea99'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Chondroitinsulfat [Chondroitin sulphate]'})
				if (component=='OPC Grape Seed'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='efa05b25-881c-4e49-95f5-0e4f1b65b19a'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'OPC Grape Seed'})
				if (component=='Leucin (L-)'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='c146183c-8dad-4b83-bbef-c1108a72302a'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Leucin (L-)'})
				if (component=='Isoleucin (L-)'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='77632855-f4d6-4f84-a7cb-8f44fb707306'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Isoleucin (L-)'})
				if (component=='Ginkgo Extrakt'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='c7e43d61-de25-4988-ac23-b834abbebd23'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Ginkgo Extrakt'})

				if (component=='Kreatin'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='65721346-9b2d-4e17-82bd-054e9ad897b8'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Kreatin'})
				if (component=='Carnosin (L-)'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='c323cd05-d957-48f4-8dea-85eccbb56964'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Carnosin (L-)'})
				if (component=='Glycin'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='f66682a1-33c9-4bdb-b0f7-157bca4e545c'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Glycin'})
				if (component=='Selenhefe [Selenium yeast]'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='da20cf8d-dc5e-4d21-9c2a-5abad0c10ee2'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Selenhefe [Selenium yeast]'})
				if (component=='Magnesium'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='3554840b-dfc5-423b-b29e-bb3c7f9042e4'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Magnesium'})
				if (component=='Kalium [Potassium]'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='d77d0227-11ad-44a6-85a3-1d1e0b1fb497'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Kalium [Potassium]'})
				if (component=='Calcium L-(+)-Lactat Komplex'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='b05478f7-137c-4c9f-8225-d050181125cc'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Calcium L-(+)-Lactat Komplex'})
				if (component=='Taurin'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='5df7e0e1-da09-4c60-a91c-ef526628c964'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Taurin'})
				if (component=='Arginin (L-)'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='3ef16167-f8df-4318-9bb8-3ee32c9727cf'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Arginin (L-)'})
				if (component=='Carnitin (L-)'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='7d55cfe0-f2fa-4cc1-95cd-9d653799a647'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Carnitin (L-)'})
				if (component=='Aminomix NAC'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='a76527ab-8c0f-4968-bb26-34f929568864'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Aminomix NAC'})
				if (component=='Aroma Orange [Flavour orange]'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='b4ae5d35-4536-4cdd-8b95-52e6c5a26131'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Aroma Orange [Flavour orange]'})
				if (component=='Antioxidantien [Antioxidants]'):
					recipes = pd.read_sql("SELECT formula_id, final_dose FROM recipes WHERE component_id='42d97619-26e4-4852-94d7-84c9937abf61'", engine)
					recipes['formula_id']=recipes['formula_id'].astype(str)
					final = pd.merge(left=final, right=recipes, left_on='formula_id', right_on='formula_id', how='left')
					final = final.rename(columns={'final_dose': 'Antioxidantien [Antioxidants]'})



				final=final.dropna()
				final = final.drop(columns=['order_id', 'lab_id', 'formula_id'])

				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment;filename=dbrequest.csv'
				csv_data = final.to_csv(index=False)


				response.write(csv_data)




				return response
		   
		else:
			
				context = {} 
				context['form'] = LocationForm()
				return render(request, 'location.html', context)
			
					


