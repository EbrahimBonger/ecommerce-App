from flask import Flask, session
from flask import render_template, request
import mysql.connector
#import sqlite3

app = Flask('app')
app.secret_key = b'mysecretkey'

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

@app.route('/login',methods=['GET', 'POST'])
#@app.route('/',methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form.get("username")
    password = request.form.get("password")
    

    c = mydb.cursor()

    c.execute('SELECT * FROM user WHERE username=%s AND passwordHash=%s', (username, password))

    result =  c.fetchone()
    if result is None:
      c.close()
      return render_template('register.html',message='Incorrect username or password')
    
    c.close()
    session['username'] = username
    return render_template('loggedin.html',message="Welcome %s" % (username)) 

@app.route('/register', methods=['GET', 'POST'])
def register():

  if request.method == 'POST':
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    username = request.form.get("user")
    password = request.form.get("pass")


    c = mydb.cursor()

    c.execute('INSERT INTO user (username, first_name, last_name, email, passwordHash)  VALUES (%s, %s, %s, %s, %s)', (username, fname, lname, email, password))

    mydb.commit()
    c.close()
    
    return render_template('registered.html')

  ## Otherwise return register page on get request
  return render_template('register.html')

@app.route('/user',methods=['GET'])
def user():
  return render_template('loggedin.html',message="Hello %s" % (session['username']))


app.run(host='0.0.0.0', port=8080)
