from flask import Flask, session
import datetime
# from flask import render_template, request
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import MySQLConnection, Error
#date format: 2021-03-12 YYYY-MM-DD

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
  session.modified = True
  session['history'] = {}
  session.clear()
  print(session)
  # print("History added to session at login page")
  # print(session['history'])
  return render_template("login.html")

def order_history_to_session(userId):
    session.modified = True

    history = {}
    p = None
    p = mydb.cursor(buffered=True, dictionary=True)

    p.execute('SELECT product.title, history.productId, history.orderId, orders.date FROM product, history INNER JOIN orders ON history.orderId=orders.orderId AND orders.userId=%s WHERE product.productId=history.productId  ORDER BY date ASC' , (userId,))

    
    rows = p.fetchall()

    # products = p.fetchall()
    mydb.commit()
    p.close() 
    # print(rows)
    history = {}
    for row in rows:
      row['date'] = str(row['date'])
      if row['date'] in history:
        history.get(str(row['date'])).append(row)
      else:
        history[str(row['date'])] = [row]
 
    session['history'] = history  
    # print(session['history'])
    # for key, values in session['history'].items():
    #   print("key")
    #   print(key)
    #   for v in values:
    #     print(v['orderId'])
    #     print(v['title'])




    return 0;




@app.route('/history',methods=['GET', 'POST'])
def history():
  if session:
    dict = session['history']
  return render_template('history.html', dict=dict)

@app.route('/login',methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form.get("username")
    password = request.form.get("password")

    c = None
    c = mydb.cursor(buffered=True, dictionary=True)

    p = None
    p = mydb.cursor(buffered=True, dictionary=True)
    
    # p = mydb.cursor(buffered=True)

    p.execute("SELECT * FROM product")
    products = p.fetchall()

    c.execute('SELECT * FROM user WHERE username=%s AND passwordHash=%s', (username, password))


    
    user = c.fetchone()
   
    if user is None:
      c.close()
      return render_template('register.html', message='Please Sign Up first to Login!')
    else:
      uname = user['username']
      upass = user['passwordHash'] 

      if uname == username and upass == password:
        session.modified = True
        session['username'] = username
        session['total_price'] = 0
        session['cart_item'] = cart_item = {}
        userId = user['userId']
        order_history_to_session(userId)
        mydb.commit()
        c.close()
        return redirect(url_for('products'))



    return render_template('login.html')

def getProductTitleById(productId):
  c = None
  c = mydb.cursor(buffered=True)
  c.execute('SELECT title FROM product WHERE productId =%s', (productId,))
  title = c.fetchone()
  title = title[0]
  mydb.commit()
  c.close()
  return title

# @app.route('/logout')  
# def logout():
#   session.pop('username', None)
#   flash("You have been logged out!")
#   return redirect(url_for('.login'))

@app.route('/logout')
def logout():
  session.pop('token', None)
  session.clear()
  message = 'You were logged out' 
  resp = app.make_response(render_template('login.html', message=message))
  resp.set_cookie('token', expires=0)
  return resp   

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
    
  
  
  session['product_list'] = product_list
  return render_template('products.html', dict=dict)

@app.route('/add', methods=['GET', 'POST'])
def add_product_to_cart():
  session.modified = True
  c = None 
  order_c = None
  
  _quantity = int(request.form['quantity'])
  _title = request.form['title'] # it gives the name user clicked
  quantity = int(request.form['quantity'])
  title = request.form['title']
  flag = int(request.form['flag'])
  print("pressed")
  print(title)
   
  
  # print("title")
  if not title in session['product_list']:
    # print("please enter valid entry!")
    error = "Please, enter a valid entry!"
    message = "please enter valid entry!"
    return render_template('alert.html', error=error)

  # print(session['product_list'])
  # for data in session['product_list']:
  #   print(data[1])
    


  if _title and _quantity and request.method == 'POST':






    c = mydb.cursor(buffered=True, dictionary=True)

    # order_c = mydb.cursor(buffered=True, dictionary=True)

     
  
    # username = session['username']    
    # order_c.execute('SELECT userId FROM user WHERE username =%s', (username,))

    # # tuple
    # userId = order_c.fetchone()
    # # Convert tuple to int
    # userId = userId['userId']
    
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
      # order_c.execute('UPDATE orders SET quantity=%s, date=%s WHERE userId=%s AND productId=%s', (running_qty, date, userId, productId))
      # update_product(productId, running_qty)


    else:
      print("The item does NOT exist " + _title)
      
      
      session['cart_item'][row['title']] = row



      print(session['cart_item'])
      # check for the stock avaliability

      productId = session['cart_item'][title]['productId']

      if stock_status(productId, quantity):
        session['cart_item'][title]['status'] = "In stock"
      else:
        session['cart_item'][title]['status'] = "Out of stock"
      

      for key, val in session['cart_item'].items():
        if key == _title:
          
          session['cart_item'][key]['running_qty'] = _quantity

          # stock_quantity = session['cart_item'][key]['quantity'] - _quantity
          # session['cart_item'][key]['quantity'] = stock_quantity

          # do not sum the current product price if it's out of stock
          status = session['cart_item'][title]['status']
          if status is "In stock":
            current_products_price = session['cart_item'][key]['price'] * _quantity
            old_price = session['total_price'] 
            new_products_price = old_price + current_products_price
            session['total_price'] = new_products_price 
      

          # Inserting to the database
          # productId = session['cart_item'][title]['productId']
          # running_qty = session['cart_item'][title]['running_qty']
          # price = session['cart_item'][title]['price']
          # date = datetime.date.today()

          # order_c.execute('INSERT INTO orders  (orderId, userId, date) VALUES (%s, %s, %s)', (0, userId, date))
    
    mydb.commit()

  # this if statement redirect to the page where the order come from
  if flag is 0:
    print("product page")
    return redirect(url_for('products'))
  elif flag is 1:
    print("history page")
    return render_template('history.html') 

  
def stock_status(productId, requested_qty):
  
  c = None
  c = mydb.cursor(buffered=True, dictionary=True)
  c.execute('SELECT quantity FROM product WHERE productId =%s', (productId,))

  # tuple
  quantity = c.fetchone()
  # Convert tuple to int
  quantity = quantity['quantity']
  print("quantity")
  print(quantity)
  if quantity >= requested_qty:
    return True
  else: False  

  mydb.commit()
  c.close()


@app.route('/test', methods=['GET', 'POST'])
def test():
  return "Test Page"
#/<string:message>
@app.route('/alert', methods=['GET', 'POST'])
def alert(message):
  return render_template('alert.html', message)  



@app.route('/payment', methods=['GET', 'POST'])
def payment():

  session.modified = True
  payment_c = None
  payment_c = mydb.cursor(buffered=True, dictionary=True)
  # payment_c.execute('INSERT INTO orders  (orderId, userId, date) VALUES (%s, %s, %s)', (0, userId, date))
  # Get the product 
  # print("Payment function...")
  if session['cart_item']:
    for key, value in session['cart_item'].items():
      # print(key)
      # add a new key to the item_cart and set it to true
      session['cart_item'][key]['stock'] = True

      # assign product_id for query operation
      productId = session['cart_item'][key]['productId']
      # req_qty = session['cart_item'][key]['running_qty']
      payment_c.execute('SELECT quantity FROM product WHERE productId =%s', (productId,))

      # tuple
      quantity = payment_c.fetchone()
      # print("test")
      # print(quantity)
      # Convert tuple to int
      quantity = quantity['quantity']
      # print(quantity)

      client_qty = session['cart_item'][key]['running_qty']
      # check the quantity is avaliable in the stock
      if client_qty > quantity:
         session['cart_item'][key]['stock'] = False
        #  print("Out of stock")
        #  print(session['cart_item'][key]['stock'])  
      # else:
          # print("In stock")
          # print(session['cart_item'][key]['stock'])
  else:
    return redirect(url_for('products'))

  return render_template('payment.html')


@app.route('/delete_product/<string:title>')
def delete_product_from_product(title):
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
      session['cart_item'].pop(key)
      break
   
  return redirect(url_for('.products'))
 except Exception as e:
  print(e)


@app.route('/delete_checkout/<string:title>')
def delete_product_from_checkout(title):
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
      session['cart_item'].pop(key)
      break
   
  return redirect(url_for('.checkout'))
 except Exception as e:
  print(e)



@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
  return render_template('checkout.html')

  return render_template('checkout.html')


@app.route('/empty', methods=['GET', 'POST'])
def empty_cart():
 try:
  session.modified = True
  # print(session['cart_item'])
  session['cart_item'] = {}
  session['total_price'] = 0
  # print(session['cart_item'])
  return redirect(url_for('.checkout'))
 except Exception as e:
  print(e)


@app.route('/register', methods=['GET', 'POST'])
def register():

  if request.method == 'POST':
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")


    c = mydb.cursor()

    c.execute('INSERT INTO user (username, first_name, last_name, email, passwordHash)  VALUES (%s, %s, %s, %s, %s)', (username, fname, lname, email, password))
    

    mydb.commit()
    c.close()
    
    return redirect(url_for('home'))

  ## Otherwise return register page on get request
  return render_template('register.html')







app.run(host='0.0.0.0', port=8080)