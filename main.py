from flask import Flask, session
# from flask import render_template, request
from flask import Flask, render_template, request, redirect, url_for

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
  return render_template("login.html")



#@app.route('/',methods=['GET', 'POST'])
@app.route('/login',methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form.get("username")
    password = request.form.get("password")
    

    c = mydb.cursor(buffered=True)
    # p = mydb.cursor(buffered=True)

    # p.execute("SELECT * FROM product")
    # products = p.fetchall()

    c.execute('SELECT * FROM user WHERE username=%s AND passwordHash=%s', (username, password))

    users = c.fetchone()
    if users is None:
      c.close()
      return render_template('register.html', message='Please Sign Up first to Login!')
    mydb.commit()
    c.close()

    # the usesr grabs a cart upon first entry
    session.modified = True
    for key in list(session.keys()):
     session.pop(key)
    # print(session)
    if not 'cart_item' in session:
      
      session['total_price'] = 0
      session['cart_item'] = cart_item = {}
    
    session['username'] = username

    return redirect(url_for('products'))

  

@app.route('/products', methods=['GET', 'POST'])
def products():
#  try:
  # conn = mysql.connect()
  p = mydb.cursor(buffered=True)
  p.execute('SELECT * FROM product')
  
  rows = p.fetchall()
  # products = p.fetchall()
  mydb.commit()
  p.close() 
  # print(rows)
  dict = {}
  # row[2] represents the category index in the tuple
  for row in rows:
    # row['running_qty'] = 0
    # print("running_qty")
    # print(row)
    if row[2] in dict:
        dict.get(row[2]).append(row)
    else:
        dict[row[2]] = [row]
    
  # print(dict)
  return render_template('products.html', dict=dict)

@app.route('/add', methods=['GET', 'POST'])
def add_product_to_cart():
  session.modified = True
  c = None  
  _quantity = int(request.form['quantity'])
  _title = request.form['title'] # it gives the name user clicked
  title = request.form['title']
  print("title "+_title)
  if _quantity <= 0 or None:
    return
  if _title and _quantity and request.method == 'POST':





    c = mydb.cursor(buffered=True, dictionary=True)
    
    
    given = _title
    checkQuery = ("SELECT * FROM product WHERE title=%s")
    userAuthInfo = (given,)
    c.execute(checkQuery, userAuthInfo)

    row = c.fetchone()

        # check if the product already added to the cart and the user has modifiyed the quantity
    if _title in session['cart_item']:
      
      modified_item = title
      old_total_price = session['total_price']
      old_qty = session['cart_item'][title]['running_qty']
      item_price = session['cart_item'][title]['price']
      substract_from_toatal = old_qty * item_price
      new_total_price = old_total_price - substract_from_toatal
      session['total_price'] = new_total_price

    session['cart_item'][row['title']] = row
    print(session)
    for key, val in session['cart_item'].items():
      if key == _title:
        
        session['cart_item'][key]['running_qty'] = _quantity

        new_quantity = session['cart_item'][key]['quantity'] - _quantity
        session['cart_item'][key]['quantity'] = new_quantity
        # print("running_qty ")
        # print(_quantity)
        # print(session['cart_item'][key]['running_qty'])
        # print(session)
        # session['cart_item'][key]['quantity'] -= _quantity
        current_products_price = session['cart_item'][key]['price'] * _quantity
        old_price = session['total_price'] 
        current_products_price = old_price + current_products_price
        session['total_price'] = current_products_price 
      
      

    
    mydb.commit()



  return redirect(url_for('products'))

@app.route('/calculate', methods=['GET', 'POST'])
def calculate_on_checkout():
  # c  = mydb.cursor()
  _quantity = int(request.form['quantity'])
  _title = request.form['title']
  print("_title and quantity")
  print(_title)
  print(_quantity)
  
  if _quantity and _title and request.method == 'POST':
    
    
    all_total_price = 0
    all_total_quantity = 0

    session.modified = True
    if 'cart_item' in session:
    #  if the product already exist, add the quantity and price of the existing
      if row['title'] in session['cart_item']:
        for key, value in session['cart_item'].items():
          old_quantity = session['cart_item'][key]['quantity']
          total_quantity = old_quantity + _quantity
          session['cart_item'][key]['quantity'] = total_quantity
          session['cart_item'][key]['total_price'] = total_quantity * row['price']
    
    for key, value in session['cart_item'].items():

     individual_quantity = session['cart_item'][key]['quantity']
     individual_price = session['cart_item'][key]['price']

     all_total_quantity = all_total_quantity + individual_quantity
     all_total_price = all_total_price + individual_price
  else:
    # session['cart_item'] = itemArray
    all_total_quantity = all_total_quantity + _quantity
    all_total_price = all_total_price + _quantity * row['price']
    
  session['all_total_quantity'] = all_total_quantity
  session['all_total_price'] = all_total_price

  return redirect(url_for('checkout'))

@app.route('/delete/<string:title>')
def delete_product(title):
 try:
  all_total_price = 0
  all_total_quantity = 0
  session.modified = True
   
  for key, val in session['cart_item'].items():

     if title == key:    
      # adjust the total price
      removed_price = session['cart_item'][key]['running_qty'] * session['cart_item'][key]['price']
      old_price = session['total_price']
      session['total_price'] = old_price - removed_price
      # session['cart_item'][key]['running_qty']
      session['cart_item'].pop(key)
      break


   
  return redirect(url_for('.checkout'))
 except Exception as e:
  print(e)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():

  return render_template('checkout.html')
@app.route('/empty', methods=['GET', 'POST'])
def empty_cart():
 try:
  session.modified = True
  print(session['cart_item'])
  session['cart_item'] = {}
  session['total_price'] = 0
  print(session['cart_item'])
  return redirect(url_for('.checkout'))
 except Exception as e:
  print(e)





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

def array_merge( first_array , second_array ):
 if isinstance( first_array , list ) and isinstance( second_array , list ):
  return first_array + second_array
 elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
  return dict( list( first_array.items() ) + list( second_array.items() ) )
 elif isinstance( first_array , set ) and isinstance( second_array , set ):
  return first_array.union( second_array )
 return False  

def close(self):
    self.cursor.close()
    self.connection.close()

def execute(self, sql):
    return self.cursor.execute(sql)

def fetchall(self):
    return self.cursor.fetchall()

def commit(self):
    #self.cursor.close()
    self.connection.commit() 


app.run(host='0.0.0.0', port=8080)
