from .forms import LocationForm, OrderForm, TestForm, ByPosForm, Loading
from django_globals import globals
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
from celery.result import AsyncResult
from getdb.tasks import get_data, get_data1


def todf(obj):
	df = pd.DataFrame(obj)
	df.columns = df.iloc[0]
	df.columns = df.columns.str.split("\n").str[1]
	df = df.drop([0])
	return df


class LocationView(FormView):
	template_name= 'location.html'
	form_class = LocationForm

	def get_location(request):
		if request.method == 'POST':

				form = request.POST
				location = form['localization']
				engine = create_engine('postgres://Analytics:pe817e57a697cec3465b3786454373e603974f2481bc4884a587fd59213c591ba@ec2-34-246-15-148.eu-west-1.compute.amazonaws.com:5432/d45o17p5ncfeid')

				

				if (location == 'Moscow'):
					patients = pd.read_sql("SELECT patient_id, date_of_birth, gender_id, office_id FROM patients WHERE office_id='2719288b-5819-4e59-be88-3cc1c610d1d4'", engine)
						

				elif (location == 'London'):
					patients = pd.read_sql("SELECT patient_id, date_of_birth, gender_id, office_id FROM patients WHERE office_id='e3d80617-207c-457c-8229-356b2067afdf'", engine)


				elif (location == 'All'):
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



				database_url = 'postgres://eyubuloglbxgpo:0bb4b2888e3a7794bcaa965d73e7e13301ad2b1585cbaf7e9ee1f1b4cd6e9591@ec2-184-73-198-174.compute-1.amazonaws.com:5432/d4ee7jenm82fu'

				engine1 = create_engine(database_url)
				patients.to_sql(name='patientz', con=engine1, index = False, if_exists= 'replace') 



				return redirect('/order/')
		   
		else:
			
				context = {} 
				context['form'] = LocationForm()
				return render(request, 'location.html', context)
			
					


class OrderView(FormView):
	template_name= 'order.html'
	form_class = OrderForm

	def get_order(request):
		if request.method == 'POST':
				global merged_inner

				
				form = request.POST

				order_numbr = form['order_number']

				engine = create_engine('postgres://Analytics:pe817e57a697cec3465b3786454373e603974f2481bc4884a587fd59213c591ba@ec2-34-246-15-148.eu-west-1.compute.amazonaws.com:5432/d45o17p5ncfeid')
							
							
				orders= pd.read_sql('SELECT order_id, patient_id, created_date FROM orders', engine)

				bloodtests= pd.read_sql('SELECT blood_test_id, order_id FROM blood_tests', engine)
				database_url = 'postgres://eyubuloglbxgpo:0bb4b2888e3a7794bcaa965d73e7e13301ad2b1585cbaf7e9ee1f1b4cd6e9591@ec2-184-73-198-174.compute-1.amazonaws.com:5432/d4ee7jenm82fu'

				engine1 = create_engine(database_url)
				patients= pd.read_sql('SELECT * FROM patientz', engine1)
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
					
					merged_inner = merged_inner.drop(columns=['orderoforder', 'created_date', 'order_id'])

						
				elif (order_numbr == '2'):
					merged_inner = merged_inner[merged_inner['orderoforder'] == 2]

					
					merged_inner['order_id']=merged_inner['order_id'].astype(str)
					bloodtests['order_id']=bloodtests['order_id'].astype(str)
					merged_inner = pd.merge(left=merged_inner, right=bloodtests, left_on='order_id', right_on='order_id')
					
					merged_inner = merged_inner.drop(columns=['orderoforder', 'created_date', 'order_id'])

					
						

						
				else:
					merged_inner = merged_inner[merged_inner['orderoforder'] == 3]

					
					merged_inner['order_id']=merged_inner['order_id'].astype(str)
					bloodtests['order_id']=bloodtests['order_id'].astype(str)
					merged_inner = pd.merge(left=merged_inner, right=bloodtests, left_on='order_id', right_on='order_id')
					
					merged_inner = merged_inner.drop(columns=['orderoforder', 'created_date', 'order_id'])


					#merged_inner['created_date'] = pd.to_datetime(
					#	merged_inner['created_date'], format='%Y-%m-%d')
				#order_numbr = int(order_numbr)

				merged_inner.to_sql(name='merged_innez', con=engine1, index = False, if_exists='replace')

							
				


				return redirect('/test/')
		else: 
				context = {} 
				context['form'] = OrderForm()
				return render(request, 'order.html', context)


class TestView(FormView):
	template_name= 'test.html'
	form_class = TestForm 

	def get_test(request):
		if request.method == 'POST':

				form = request.POST


				tests = form['tests']
				
				database_url = 'postgres://eyubuloglbxgpo:0bb4b2888e3a7794bcaa965d73e7e13301ad2b1585cbaf7e9ee1f1b4cd6e9591@ec2-184-73-198-174.compute-1.amazonaws.com:5432/d4ee7jenm82fu'

				engine1 = create_engine(database_url)
				merged_inner= pd.read_sql('SELECT * FROM merged_innez', engine1)				



				if (tests == 'Vitamin D'):
					engine = create_engine('postgres://Analytics:pe817e57a697cec3465b3786454373e603974f2481bc4884a587fd59213c591ba@ec2-34-246-15-148.eu-west-1.compute.amazonaws.com:5432/d45o17p5ncfeid')
					resultz = pd.read_sql("SELECT blood_test_id, absolute_value FROM results WHERE normal_position_id= '5c6ad87c-39b9-48f5-8e4a-8744170ec464'", engine)
					

					final = merged_inner
			                    #russianpanelpos = unite['64aa8df1-6dc1-4cdd-956f-033f343ecd72'].to_list()
					b = resultz
					b = b[['blood_test_id', 'absolute_value']]
					b['blood_test_id']=b['blood_test_id'].astype(str)
					final['blood_test_id']=final['blood_test_id'].astype(str)
					final = pd.merge(left=final, right=b, left_on='blood_test_id',right_on='blood_test_id', how='left')
					final = final.rename(columns={'absolute_value': tests})
			                    

					final = final.dropna(how='any')
					final=final.drop(columns=['blood_test_id'])
					

				elif(tests == 'Vitamin B9 (Folic acid)'):
					engine = create_engine('postgres://Analytics:pe817e57a697cec3465b3786454373e603974f2481bc4884a587fd59213c591ba@ec2-34-246-15-148.eu-west-1.compute.amazonaws.com:5432/d45o17p5ncfeid')
					resultz = pd.read_sql("SELECT blood_test_id, absolute_value  FROM results WHERE normal_position_id= '6f753b31-61ab-4980-a5e3-f5b22597ac08'", engine)
					names = []
			                    #russianpanelpos = unite['64aa8df1-6dc1-4cdd-956f-033f343ecd72'].to_list()
					b = resultz
					b = b[['blood_test_id', 'absolute_value']]
					b['blood_test_id']=b['blood_test_id'].astype(str)
					final['blood_test_id']=final['blood_test_id'].astype(str)
					final = pd.merge(left=final, right=b, left_on='blood_test_id',right_on='blood_test_id', how='left')
					final = final.rename(columns={'absolute_value': tests})
			                    

					final = final.dropna(how='any')
					final=final.drop(columns=['blood_test_id'])
					       
				elif(tests == 'Triglycerides'):
					engine = create_engine('postgres://Analytics:pe817e57a697cec3465b3786454373e603974f2481bc4884a587fd59213c591ba@ec2-34-246-15-148.eu-west-1.compute.amazonaws.com:5432/d45o17p5ncfeid')
					resultz = pd.read_sql("SELECT blood_test_id, absolute_value  FROM results WHERE normal_position_id= '35abf5bc-7b1f-443c-b4d4-e304f3a5c696'", engine)

					    
					final = merged_inner			                    #russianpanelpos = unite['64aa8df1-6dc1-4cdd-956f-033f343ecd72'].to_list()
					b = resultz
					b = b[['blood_test_id', 'absolute_value']]
					b['blood_test_id']=b['blood_test_id'].astype(str)
					final['blood_test_id']=final['blood_test_id'].astype(str)
					final = pd.merge(left=final, right=b, left_on='blood_test_id',right_on='blood_test_id', how='left')
					final = final.rename(columns={'absolute_value': tests})
			                    

					final = final.dropna(how='any')
					final=final.drop(columns=['blood_test_id'])
				elif(tests == 'Creatinine'):
					engine = create_engine('postgres://Analytics:pe817e57a697cec3465b3786454373e603974f2481bc4884a587fd59213c591ba@ec2-34-246-15-148.eu-west-1.compute.amazonaws.com:5432/d45o17p5ncfeid')
					resultz = pd.read_sql("SELECT blood_test_id, absolute_value  FROM results WHERE normal_position_id= '5f467d4b-cdd3-4723-b9a1-f4810e6a1345'", engine)

					    
					final = merged_inner			                    #russianpanelpos = unite['64aa8df1-6dc1-4cdd-956f-033f343ecd72'].to_list()
					b = resultz
					b = b[['blood_test_id', 'absolute_value']]
					b['blood_test_id']=b['blood_test_id'].astype(str)
					final['blood_test_id']=final['blood_test_id'].astype(str)
					final = pd.merge(left=final, right=b, left_on='blood_test_id',right_on='blood_test_id', how='left')
					final = final.rename(columns={'absolute_value': tests})
			                    

					final = final.dropna(how='any')
					final=final.drop(columns=['blood_test_id'])	
				elif(tests == 'AST'):
					engine = create_engine('postgres://Analytics:pe817e57a697cec3465b3786454373e603974f2481bc4884a587fd59213c591ba@ec2-34-246-15-148.eu-west-1.compute.amazonaws.com:5432/d45o17p5ncfeid')
					resultz = pd.read_sql("SELECT blood_test_id, absolute_value  FROM results WHERE normal_position_id= '0dccda1a-8845-41b5-8078-0df3a0d4005e'", engine)

					    
					final = merged_inner			                    #russianpanelpos = unite['64aa8df1-6dc1-4cdd-956f-033f343ecd72'].to_list()
					b = resultz
					b = b[['blood_test_id', 'absolute_value']]
					b['blood_test_id']=b['blood_test_id'].astype(str)
					final['blood_test_id']=final['blood_test_id'].astype(str)
					final = pd.merge(left=final, right=b, left_on='blood_test_id',right_on='blood_test_id', how='left')
					final = final.rename(columns={'absolute_value': tests})
			                    

					final = final.dropna(how='any')
					final=final.drop(columns=['blood_test_id'])
				elif(tests == 'ALT'):
					engine = create_engine('postgres://Analytics:pe817e57a697cec3465b3786454373e603974f2481bc4884a587fd59213c591ba@ec2-34-246-15-148.eu-west-1.compute.amazonaws.com:5432/d45o17p5ncfeid')
					resultz = pd.read_sql("SELECT blood_test_id, absolute_value  FROM results WHERE normal_position_id= '510b415a-3d22-42dc-ab3c-3d12857821e8'", engine)

					    
					final = merged_inner			                    #russianpanelpos = unite['64aa8df1-6dc1-4cdd-956f-033f343ecd72'].to_list()
					b = resultz
					b = b[['blood_test_id', 'absolute_value']]
					b['blood_test_id']=b['blood_test_id'].astype(str)
					final['blood_test_id']=final['blood_test_id'].astype(str)
					final = pd.merge(left=final, right=b, left_on='blood_test_id',right_on='blood_test_id', how='left')
					final = final.rename(columns={'absolute_value': tests})
			                    

					final = final.dropna(how='any')
					final=final.drop(columns=['blood_test_id'])     
				elif(tests == 'Uric acid'):
					engine = create_engine('postgres://Analytics:pe817e57a697cec3465b3786454373e603974f2481bc4884a587fd59213c591ba@ec2-34-246-15-148.eu-west-1.compute.amazonaws.com:5432/d45o17p5ncfeid')
					resultz = pd.read_sql("SELECT blood_test_id, absolute_value  FROM results WHERE normal_position_id= '937b223e-8bb6-4708-a422-6ea6bd3f6cc4'", engine)

					    
					final = merged_inner			                    #russianpanelpos = unite['64aa8df1-6dc1-4cdd-956f-033f343ecd72'].to_list()
					b = resultz
					b = b[['blood_test_id', 'absolute_value']]
					b['blood_test_id']=b['blood_test_id'].astype(str)
					final['blood_test_id']=final['blood_test_id'].astype(str)
					final = pd.merge(left=final, right=b, left_on='blood_test_id',right_on='blood_test_id', how='left')
					final = final.rename(columns={'absolute_value': tests})
			                    

					final = final.dropna(how='any')
					final=final.drop(columns=['blood_test_id'])   					
				elif(tests == 'Total cholesterol'):
					engine = create_engine('postgres://Analytics:pe817e57a697cec3465b3786454373e603974f2481bc4884a587fd59213c591ba@ec2-34-246-15-148.eu-west-1.compute.amazonaws.com:5432/d45o17p5ncfeid')
					resultz = pd.read_sql("SELECT blood_test_id, absolute_value  FROM results WHERE normal_position_id= '4319cee7-db11-4099-a531-dd31e8462dba'", engine)

					    
					final = merged_inner			                    #russianpanelpos = unite['64aa8df1-6dc1-4cdd-956f-033f343ecd72'].to_list()
					b = resultz
					b = b[['blood_test_id', 'absolute_value']]
					b['blood_test_id']=b['blood_test_id'].astype(str)
					final['blood_test_id']=final['blood_test_id'].astype(str)
					final = pd.merge(left=final, right=b, left_on='blood_test_id',right_on='blood_test_id', how='left')
					final = final.rename(columns={'absolute_value': tests})
			                    

					final = final.dropna(how='any')
					final=final.drop(columns=['blood_test_id'])   
				elif(tests == 'Homocysteine'):
					engine = create_engine('postgres://Analytics:pe817e57a697cec3465b3786454373e603974f2481bc4884a587fd59213c591ba@ec2-34-246-15-148.eu-west-1.compute.amazonaws.com:5432/d45o17p5ncfeid')
					resultz = pd.read_sql("SELECT blood_test_id, absolute_value  FROM results WHERE normal_position_id= '3443ed7a-3d52-4d5e-b0db-c302bb3b4a80'", engine)

					    
					final = merged_inner			                    #russianpanelpos = unite['64aa8df1-6dc1-4cdd-956f-033f343ecd72'].to_list()
					b = resultz
					b = b[['blood_test_id', 'absolute_value']]
					b['blood_test_id']=b['blood_test_id'].astype(str)
					final['blood_test_id']=final['blood_test_id'].astype(str)
					final = pd.merge(left=final, right=b, left_on='blood_test_id',right_on='blood_test_id', how='left')
					final = final.rename(columns={'absolute_value': tests})
			                    

					final = final.dropna(how='any')
					final=final.drop(columns=['blood_test_id'])   					
				final.to_sql(name='merged_innez', con=engine1, index = False, if_exists='replace') 
				return redirect('/finale/')	#panelPositions= key_values['value'][19]

		else:
				context = {} 
				context['form'] = TestForm()
				return render(request, 'test.html', context)


class ByPosView(FormView):
	template_name= 'bypos.html'
	form_class = ByPosForm 

	def get_position(request):
		if request.method == 'POST':

				form = request.POST
				database_url = 'postgres://eyubuloglbxgpo:0bb4b2888e3a7794bcaa965d73e7e13301ad2b1585cbaf7e9ee1f1b4cd6e9591@ec2-184-73-198-174.compute-1.amazonaws.com:5432/d4ee7jenm82fu'

				engine1 = create_engine(database_url)
				merged_inner= pd.read_sql('SELECT * FROM finalz', engine1)                
				resultz= pd.read_sql('SELECT * FROM results', engine1)  

				bypos = form['bypos']
    
				final = merged_inner
				a = 0
		                    
				names = []
		                    #russianpanelpos = unite['64aa8df1-6dc1-4cdd-956f-033f343ecd72'].to_list()
				b = resultz
				b = b[['blood_test_id', 'absolute_value']]
				b['blood_test_id']=b['blood_test_id'].astype(str)
				final['blood_test_id']=final['blood_test_id'].astype(str)
				final = pd.merge(left=final, right=b, left_on='blood_test_id',right_on='blood_test_id', how='left')
				final = final.rename(columns={'absolute_value': globals.request})
		                    

				final = final.dropna(how='any')
				final=final.drop(columns=['blood_test_id'])
				final.to_sql(name='merged_innez', con=engine1, index = False, if_exists= 'replace')


				return redirect('/finale/')

		else:
				context = {} 
				context['form'] = ByPosForm()
				return render(request, 'bypos.html', context)

import csv
from django.http import HttpResponse
from django.template import loader, Context

# and others imported modules...


class FinaleView1(FormView):
	template_name = 'resultz.html'

	def get_button(request):
		if request.method == 'POST':
			database_url = 'postgres://eyubuloglbxgpo:0bb4b2888e3a7794bcaa965d73e7e13301ad2b1585cbaf7e9ee1f1b4cd6e9591@ec2-184-73-198-174.compute-1.amazonaws.com:5432/d4ee7jenm82fu'

			engine = create_engine(database_url)
			final= pd.read_sql('SELECT * FROM merged_innez', engine)		
			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment;filename=dbrequest.csv'
			csv_data = final.to_csv(index=False)


			response.write(csv_data)
			return response
		else:
			return render(request, 'resultz.html')
		


	
		















