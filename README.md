
# e-commerce Web App Demo

![ecommerceAppDemo](https://user-images.githubusercontent.com/35973818/120252233-ed0b1c80-c251-11eb-876b-c346e7db7c19.gif)



## Application Requirements
The website should be able to display products being sold in several categories. A user visiting your web store application can search for products (i.e., search for a specific item name and display that item) or display all items in a certain category. The website should display the available quantity for each product.

Only a logged in user can add products to a shopping cart and "buy" various quantities of products by checking out. To "buy" a product means to reduce the quantity from that product with the quantity that was "bought" (i.e. your database should be updated to reflect the reduction in quantity of items after purchase). 

A logged in user shopping cart can be viewed, edited, checked out or deleted. A logged in user can also see his/her orders history if there are any.

## Implementation
- Python Flask will be used for all the server side scripting.
- The cart should be implemented with Session variables. Hint: the session should be based on the user login.
  - This means the shopping cart should *not* be stored in your database.
- Check user input: do not allow me to buy -2 boxes of detergent or, 100 boxes if you only have 1 in stock.
- Keep minimum information about customers: username and password, first and last name. We are not interested in addresses at this point.
- For the base level you can use sqlite as your database, but to earn a perfect score you must use mysql hosted on Amazon Web Services
- For the base level you can use Repl.it to host your python web application, but to earn a perfect score you must run it on AWS.
- If you use AWS you will need to ensure that it is continuously running until we perform grading!
- Where details are not specified in the assignment, you should assume something "reasonable" that you think the client will expect.


### Features
- [X] A new user can sign up.
- [X] A logged in user can see his/her previous order history.
- [X] The front end is user friendly: website is easy and intuitive to navigate, no server error messages are presented to to user (if an error occurs, give a user friendly message).
- [X] Website style: products have pictures.

