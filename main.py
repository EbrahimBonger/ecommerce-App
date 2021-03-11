from flask import Flask, session
import datetime
# from flask import render_template, request
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import MySQLConnection, Error
# from python_mysql_dbconfig import read_db_config


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

@app.route('/logout')  
def logout():
  session.pop('username', None)
  flash("You have been logged out!")
  return redirect(url_for('.login'))

@app.route('/products/', methods=['GET', 'POST'])
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
  product_list = []
  # row[2] represents the category index in the tuple
  for row in rows:
    # row['running_qty'] = 0
    # print("running_qty")
    # print(row)
    if row[2] in dict:
        dict.get(row[2]).append(row)
        product_list.append(row[1])
    else:
        dict[row[2]] = [row]
        product_list.append(row[1])
    
  
  # TO DO: store as a dict to keep track of the quantity
  
  session['product_list'] = product_list
  return render_template('products.html', dict=dict)

@app.route('/add', methods=['GET', 'POST'])
def add_product_to_cart():
  session.modified = True
  c = None 
  order_c = None
  
  _quantity = int(request.form['quantity'])
  _title = request.form['title'] # it gives the name user clicked
  title = request.form['title']
  
  print("title")
  if not title in session['product_list']:
    print("please enter valid entry!")
    error = "Please, enter a valid entry!"
    message = "please enter valid entry!"
    return render_template('alert.html', error=error)

  # print(session['product_list'])
  # for data in session['product_list']:
  #   print(data[1])
    
  if _quantity <= 0 or None:
    return
  if _title and _quantity and request.method == 'POST':

    # check for the stock avaliability
    c = mydb.cursor(buffered=True, dictionary=True)
    order_c = mydb.cursor(buffered=True, dictionary=True)

     
  
    username = session['username']    
    order_c.execute('SELECT userId FROM user WHERE username =%s', (username,))

    # tuple
    userId = order_c.fetchone()
    # Convert tuple to int
    userId = userId['userId']
    
    given = _title
    checkQuery = ("SELECT * FROM product WHERE title=%s")
    userAuthInfo = (given,)
    c.execute(checkQuery, userAuthInfo)

    row = c.fetchone()

        # check if the product already added to the cart and the user has modifiyed the quantity
    if _title in session['cart_item']:
      print("The item does exist " + _title)

      # add the old running back to the stock
      old_running_qty = session['cart_item'][title]['running_qty']
      old_stock_qty = session['cart_item'][title]['quantity']
      session['cart_item'][title]['quantity'] = old_running_qty + old_stock_qty
      #replace it by the new running quantity
      session['cart_item'][title]['running_qty'] = _quantity

      item_price = session['cart_item'][title]['price']
      new_total_price = _quantity * item_price
      session['total_price'] = new_total_price
      stock_quantity = session['cart_item'][title]['quantity'] - _quantity
      session['cart_item'][title]['quantity'] = stock_quantity
      

      #upate the database with user changes
      productId = session['cart_item'][title]['productId']
      running_qty = session['cart_item'][title]['running_qty']
      price = session['cart_item'][title]['price']
      date = datetime.date.today()
      order_c.execute('UPDATE orders SET (quantity=%s, date=%s, WHERE userId=%s AND productId=%s)', (running_qty, date, userId, productId))
      update_product(productId, running_qty)


    else:
      print("The item does NOT exist " + _title)
      session['cart_item'][row['title']] = row
      for key, val in session['cart_item'].items():
        if key == _title:
          
          session['cart_item'][key]['running_qty'] = _quantity

          stock_quantity = session['cart_item'][key]['quantity'] - _quantity
          session['cart_item'][key]['quantity'] = stock_quantity
          current_products_price = session['cart_item'][key]['price'] * _quantity
          old_price = session['total_price'] 
          current_products_price = old_price + current_products_price
          session['total_price'] = current_products_price 
      

          # Inserting to the database
          productId = session['cart_item'][title]['productId']
          running_qty = session['cart_item'][title]['running_qty']
          price = session['cart_item'][title]['price']
          date = datetime.date.today()

          order_c.execute('INSERT INTO orders  (userId, productId, quantity, price, date) VALUES (%s, %s, %s, %s, %s)', (userId, productId, running_qty, price, date))


    # Order table schema
    # CREATE TABLE `orders` (
    # `orderId` BIGINT NOT NULL AUTO_INCREMENT,
    # `userId` BIGINT NULL DEFAULT NULL,
    # `productId` BIGINT NOT NULL,
    # `quantity` SMALLINT(6) NOT NULL DEFAULT 0,
    # `price` FLOAT NOT NULL DEFAULT 0,
    # `date` DATE,
    # PRIMARY KEY (`orderId`, `productId`)
    # );

     


    
    
    mydb.commit()


  return redirect(url_for('products'))

@app.route('/test', methods=['GET', 'POST'])
def test():
  return "Test Page"
#/<string:message>
@app.route('/alert', methods=['GET', 'POST'])
def alert(message):
  return render_template('alert.html', message)  

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


def update_product(productId, quantity):
    # read database configuration
    db_config = read_db_config()

    # prepare query and data
    query = """ UPDATE orders
                SET quantity = %s
                WHERE productId = %s """

    data = (title, book_id)

    try:
        conn = MySQLConnection(**db_config)

        # update product quantity
        cursor = conn.cursor()
        cursor.execute(query, data)

        # accept the changes
        conn.commit()

    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()


app.run(host='0.0.0.0', port=8080)
