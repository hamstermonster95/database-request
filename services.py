
import pandas as pd
import psycopg2
from sqlalchemy import create_engine






engine = create_engine('postgres://Analytics:pe817e57a697cec3465b3786454373e603974f2481bc4884a587fd59213c591ba@ec2-34-246-15-148.eu-west-1.compute.amazonaws.com:5432/d45o17p5ncfeid')

def get_recipes():
	key_values=pd.read_sql('SELECT * FROM key_values', engine)
	return key_values