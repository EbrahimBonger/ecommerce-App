from flask import Flask, session
from collections import OrderedDict
from datetime import datetime
from decimal import Decimal
# from flask import render_template, request
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import MySQLConnection, Error
#date format: 2021-03-12 YYYY-MM-DD

#import sqlite3

app = Flask('app')
app.secret_key = b'mysecretkey'

mydb = mysql.connector.connect(
    # host="ec2-100-26-20-223.compute-1.amazonaws.com",
    host="ec2-52-86-184-238.compute-1.amazonaws.com",
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
    history = {}
    for row in rows:
      row['date'] = str(row['date'])
      if row['date'] in history:
        history.get(str(row['date'])).append(row)
      else:
        history[str(row['date'])] = [row]
 
    session['history'] = history  
 

    return 0;




@app.route('/history',methods=['GET', 'POST'])
def history():
  if session:
    # ordered_data = sorted(dict.items(), key = lambda x:datetime.strptime(x[0], '%y-%m-%d'), reverse=True)
    # ordered = OrderedDict(sorted(dict.items(), key=lambda t: t[0]))
    # new_d = OrderedDict(sorted(dict.items()))
    userId = session['userId']
    dict = order_history_to_session(userId)  
 
    
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
      return render_template('register.html', message='Please, Create account')
    else:
      uname = user['username']
      upass = user['passwordHash'] 

      if uname == username and upass == password:
        session.modified = True
        session['username'] = username
        session['total_price'] = 0
        session['cart_item'] = cart_item = {}
        userId = user['userId']
        session['userId'] = userId
      
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

def getProductQuantity(productId):
  c = None
  c = mydb.cursor(buffered=True)
  c.execute('SELECT quantity FROM product WHERE productId =%s', (productId,))
  quantity = c.fetchone()
 
  quantity = quantity[0]
  mydb.commit()
  c.close()
  return quantity





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
  dict = {}
  product_list = []
  # row[2] represents the category index in the tuple
  for row in rows:

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

   
  
  if not title in session['product_list']:
    error = "Please, enter a valid input..."
    message = "please enter valid entry!"
    return render_template('alert.html', error=error)




  if _title and _quantity and request.method == 'POST':




    c = mydb.cursor(buffered=True, dictionary=True)

 
    
    given = _title
    checkQuery = ("SELECT * FROM product WHERE title=%s")
    userAuthInfo = (given,)
    c.execute(checkQuery, userAuthInfo)

    row = c.fetchone()

    stock_quantity = row['quantity']

   


    


    # check if the product already added to the cart and the user has modifiyed the quantity
    if _title in session['cart_item']:
      print("The item does exist " + _title)

      # update the quantity
      session['cart_item'][title]['running_qty'] = _quantity



    #  title = session['cart_item'][title]['title']

      if stock_status(stock_quantity, quantity):
        session['cart_item'][title]['status'] = "In stock"
        current_products_price = session['cart_item'][title]['price'] * _quantity
        old_price = session['total_price'] 
        new_products_price = old_price + current_products_price
        session['total_price'] = new_products_price 

      else:
        session['cart_item'][title]['status'] = "Out of stock"
      

    else:
      print("The item does NOT exist " + _title)
      
      # add the product to the cart

      session['cart_item'][row['title']] = row
      session['cart_item'][title]['des'] = str(descreption(title))
      session['cart_item'][title]['img'] = str(imagepath(title))
    
      session['cart_item'][title]['running_qty'] = _quantity

      if stock_status(stock_quantity, quantity):
        
        session['cart_item'][title]['status'] = "In stock"
        current_products_price = session['cart_item'][title]['price'] * _quantity
        old_price = session['total_price'] 
        new_products_price = old_price + current_products_price
        session['total_price'] = new_products_price

      else:
        session['cart_item'][title]['status'] = "Out of stock"
      

      

          # Inserting to the database
          # productId = session['cart_item'][title]['productId']
          # running_qty = session['cart_item'][title]['running_qty']
          # price = session['cart_item'][title]['price']
          # date = datetime.date.today()

          # order_c.execute('INSERT INTO orders  (orderId, userId, date) VALUES (%s, %s, %s)', (0, userId, date))
    
    mydb.commit()

  # this if statement redirect to the page where the order come from
  if flag is 0:
    return redirect(url_for('products'))
  elif flag is 1:
    return render_template('history.html') 

  
def stock_status(stock_quantity, quantity):
  

  if stock_quantity >= quantity:
    return True
  else: False  



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

  final_products = {}
  final_total_price = 0




  for key in list(session['cart_item']):
    
    status = session['cart_item'][key]['status']


    
    running_qty = session['cart_item'][key]['running_qty']
    price = session['cart_item'][key]['price'] * running_qty
   
    if not status == "In stock":

      session['cart_item'].pop(key)
 
    else:  
      print("Found")


 

  vat = (session['total_price'] /100)*19

  total_price_vat_included = session['total_price'] + vat

  total_price_vat_included = Decimal(total_price_vat_included)

  total_price_vat_included = round(total_price_vat_included, 2)
  
  session['total_price'] = total_price_vat_included

  vat = Decimal(vat)

  vat = round(vat, 2)
   
  session['vat'] = vat


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

@app.route('/success', methods=['GET', 'POST'])
def success():

  print("success head")
 

  # card_number and card_holder and expires and cvv and 

  if request.method == 'POST':
    
    card_number = request.form.get("card_number")
    card_holder = request.form.get("card_holder")
    expires = request.form.get("expires")
    cvv = request.form.get("cvv")

    session.modified = True
    insert_c = None
    update_c  = None
    select_c = None

    print("success body")
    insert_c = mydb.cursor(buffered=True, dictionary=True)
    update_c = mydb.cursor(buffered=True, dictionary=True)
    select_c = mydb.cursor(buffered=True, dictionary=True)

    date = datetime.now()
    userId = session['userId']

    #  INSERT INTO `orders` ( `orderId`, `userId`, `date`) VALUES
    # (1, 1, '2020-05-09' );

    # insert user order
    insert_c.execute('INSERT INTO orders  (userId, date) VALUES (%s, %s)', (userId, date))
    

    # then get the orderId from orders table
    # select_c.execute('SELECT orderId FROM orders WHERE userId=%s', (userId,))
    select_c.execute('SELECT orderId FROM orders ORDER BY orderId DESC LIMIT 1')
    orderId = select_c.fetchone()
    print(orderId)
    orderId = orderId['orderId']
    

    # insert the the product purchased into history table and update on product table

    for key, val in session['cart_item'].items():
      # set variables that needs to be updated
      productId = session['cart_item'][key]['productId']
      running_qty = session['cart_item'][key]['running_qty']
      quantity = getProductQuantity(productId)
      new_quantity = quantity - running_qty

      update_c.execute('UPDATE product SET quantity=%s WHERE productId=%s', (new_quantity, productId))

      insert_c.execute('INSERT INTO history  (userId, orderId, productId) VALUES (%s, %s, %s)', (userId, orderId, productId))

    insert_c.close
    update_c.close  
    select_c.close

    mydb.commit()

    session['cart_item'] = {}
    session['total_price'] = 0

    return render_template('success.html')

  else:
    return "Something went wrong. Please, try agin..."


        










  



@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
  return render_template('checkout.html')

 


@app.route('/empty', methods=['GET', 'POST'])
def empty_cart():
 try:
  session.modified = True
  session['cart_item'] = {}
  session['total_price'] = 0
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
    password2 = request.form.get("password2")


    c = mydb.cursor()

    c.execute('INSERT INTO user (username, first_name, last_name, email, passwordHash)  VALUES (%s, %s, %s, %s, %s)', (username, fname, lname, email, password))
    

    mydb.commit()
    c.close()
    
    return redirect(url_for('home'))

  ## Otherwise return register page on get request
  print("register page")
  return render_template('register.html')


def descreption(title):
  
  product_des = { 'Growth Oil' : 'Beards, like plants, need a strong base to grow from and plenty of hydration to reach their full potential.',

  
  'Sandalwood Balm' :'Inspired by the traditional ceremony of Galungan, our Coconut + Sandalwood Body Balm is an aromatic celebration of Bali.',

  'Beard Shampoo' : 'Our Beard Supplements are composed of essential nutrients that support the growth of healthy hair, skin, nails and connective tissues.',

  'Sandalwood Oil' : 'Grow The Perfect Beard With This Combo Designed To Maximize Results.',

  'Beard Wash' : 'Our Beard Supplements are composed of essential nutrients that support the growth of healthy hair, skin, nails and connective tissues.',

  'Beard Wax' : 'This professional-grade moustache wax was designed to help keep your moustache healthy and looking great.',

  'Beard Trimmer' : 'This kit includes the PT45 Trimmer with LED display stand & 8 trimmer guides',

  'Beard Brush' : 'Grow The Perfect Beard With This Combo Designed To Maximize Results.',

  'Snapback Army Green': 'CREATED FOR BEARDED INDIVIDUALS, THIS HAT IS SURE TO COMPLIMENT THOSE PROUD TO LIVE THE NO SHAVE LIFE.',

  'Snapback Heather Gray' : 'BEARDED INDIVIDUALS, THIS HAT IS SURE TO COMPLIMENT THOSE PROUD TO LIVE THE NO SHAVE LIFE.' 
  }

  return product_des.get(title)


def imagepath(title):
  image_path = { 'Growth Oil' : 'image/Growth_ Oil.jpg',

  
  'Sandalwood Balm' : 'image/Sandalwood_Balm.jpg',

  'Beard Shampoo' : 'image/Beard_Shampoo.jpg',

  'Sandalwood Oil' : 'image/Sandalwood_Oil.jpg',

  'Beard Wash' : 'image/Beard_Wash.jpg',

  'Beard Wax' : 'image/Beard_Wax.jpg',

  'Beard Trimmer' : 'image/Beard_Trimmer.jpg',

  'Beard Brush' : 'image/Beard_Brush.jpg',

  'Snapback Army Green': 'image/Snapback_Army_Green.jpg',

  'Snapback Heather Gray' : 'image/Snapback_Heather_Gray.jpg' 
  }

  return image_path.get(title)

  
  
  


  
  












app.run(host='0.0.0.0', port=8080)
