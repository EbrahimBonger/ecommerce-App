from flask import Flask, session
from flask import render_template, request
# import mysql.connector
import sqlite3

app = Flask('app')

@app.route('/')
def hello_world():
  return 'Hello, World!'

app.run(host='0.0.0.0', port=8080)
