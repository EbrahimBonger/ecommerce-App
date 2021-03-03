from flask import Flask, session
from flask import render_template, request
import mysql.connector
#import sqlite3

app = Flask('app')

mydb = mysql.connector.connect(
    host="ec2-100-26-20-223.compute-1.amazonaws.com",
    user="ebrahim5",
    password="seas",
    database="cs2541db"
)



@app.route('/')

def home():
  # Render the homepage 
  #return 'Hello World'
  return render_template("index.html")

# @app.route('/login',methods=['GET', 'POST'])
@app.route('/',methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form.get("username")
    password = request.form.get("password")

    c = mydb.cursor()

    c.execute('SELECT * FROM user WHERE username=%s AND password=%s', (username, password))

    result =  c.fetchone()
    if result is None:
      c.close()
      return render_template('loggedin.html',message='Incorrect username or password')
    
    c.close()
    session['username'] = username
  return render_template('loggedin.html',message="Welcome %s" % (username)) 

app.run(host='0.0.0.0', port=8080)
