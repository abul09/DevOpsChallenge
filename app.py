from flask import Flask
import boto3
import os

app = Flask(__name__)

ENDPOINT="dme5x378l95dqt.c0jbwiuniblc.us-east-1.rds.amazonaws.com"
PORT="3306"
USER="MyUser"
REGION="us-east-1"
DBNAME="MyDatabase"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

session = boto3.Session(profile_name='default')
rds = session.client('rds')

@app.route('/')
def hello_world():
	return 'Hello World!'

@app.route('/api/pet/<pet_name>')
def get_pet(pet_name):
	token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)

	try:
		conn =  mysql.connector.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT, database=DBNAME)
		cur = conn.cursor()
		cur.execute(f"""SELECT name, owner, species FROM pet WHERE name={pet_name}""")
		query_results = cur.fetchall()
		
		return query_results
	except Exception as e:
		return "Database connection failed due to {}".format(e)

if __name__ == "__main__":
	app.run()
