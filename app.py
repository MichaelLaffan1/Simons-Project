import psycopg2
from flask import Flask
from flask import render_template

app = Flask(__name__)
# default port
t_host = 'localhost' 
# port for Postgres
t_port = "5432"      
# Database name
t_dbname = "NYCRestaurants" 
# Username
t_user = "postgres"  
# Password (password must be same as one for database)    
t_password = "Password" 
# Connection to database
db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname,
user=t_user, password=t_password)
db_cursor = db_conn.cursor()

@app.route("/import")
def csv_import():
    # Trap errors for opening the file
    try:
        t_path_n_file = "NYCRestaurants.csv"
        f_contents = open(t_path_n_file, 'r')
    except psycopg2.Error as e:
        t_message = "Database error: " + e + "/n open() text file: " + t_path_n_file
        return render_template("error_page.html", t_message = t_message)
    # Trap errors for copying the array to our database
    try:
        db_cursor.copy_from(f_contents, "tbl_restaurants", columns=('t_CAMIS',
        't_DBA', 't_BORO', 't_BUILDING', 't_STREET', 't_ZIPCODE', 't_PHONE',
        't_CUISINE_DESCRIPTION', 't_INSPECTION_DATE', 't_ACTION', 't_VIOLATION_CODE',
        't_VIOLATION_DESCRIPTION', 't_CRITICAL_FLAG', 't_SCORE', 't_GRADE', 
        't_GRADE_DATE', 't_RECORD_DATE', 't_INSPECTION_TYPE', 't_LATITUDE',
        't_LONGITUDE', 't_COMMUNITY_BOARD', 't_COUNCIL_DISTRICT', 't_CENSUS_TRACT',
        't_BIN', 't_BBL', 't_NTA'), sep =",")
    except psycopg2.Error as e:
        t_message = "Database error: " + e + "/n copy_from"
        return render_template("error_page.html", t_message = t_message)
    
    db_cursor.close()
    db_conn.close()

# What you see when running on localhost:80
@app.route("/")
def hello():
    return '<h1> Hello there </h1>'

# Allows application to run on localhost:80
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)