[![Work in Repl.it](https://classroom.github.com/assets/work-in-replit-14baed9a392b3a25080506f3b7b6d57f295ec2978f6f33ec97e36a161684cbe9.svg)](https://classroom.github.com/online_ide?assignment_repo_id=4203877&assignment_repo_type=AssignmentRepo)
# Homework: Shopping Cart Web App

**Your Name**
 - your_email@gwu.edu
 - your github username
 - your EC2 or repl link to live webpage

## Description
This homework will have you develop a web store application.  **This is an individual** assignment; you may discuss general Python/SQL techniques with other students, but all code that you write must be your own! You are expected to implement the following "from scratch", i.e., you may use the basic Flask libraries, templating abilities, etc, but you may not use 3rd party libraries to provide significant portions of functionality.

**Deadline:** Monday 3/8/21, before class

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


## Grading levels
You have to complete all the requirements for a level before you can move to the next one.

### Base level 85% of the grade
- [ ] Database schema and scripts to create and populate the tables.
  - [ ] This must be kept in the `store_schema.sql` file.
  - [ ] Credit will be given for either sqlite or MySQL database syntax.
- [ ] Minimal web interface: web page does not look professional, minimal styling, no form checks.
- [ ] The user can see all the products the store sells; minimum of 10 products.
- [ ] The user can search for a specific item by name.
- [ ] The user can see all the products in a specific category; minimum of 3 categories.
- [ ] The user can login, but not create a new account.
  - [ ] Users who are not in the DB can't login.
  - [ ] Must include a sample user named `testuser` with password `testpass`
- [ ] The logged in user can view, add to, edit, check out or delete the cart.
- [ ] The database is updated when a user buys or checks out.
- [ ] The store doesn't let a user buy negative amounts or more than is in the inventory.

### Medium level takes you to 95%
- [ ] A new user can sign up.
- [ ] A logged in user can see his/her previous order history.
- [ ] The front end is user friendly: website is easy and intuitive to navigate, no server error messages are presented to to user (if an error occurs, give a user friendly message).
- [ ] Website style: products have pictures.

### Prime level takes you to 100%
- [ ] Database uses MySQL instead of sqlite and Flask web server runs in AWS
- [ ] Implement client-side validation for input forms (e.g. quantity added to cart can't be negative) using Javascript.
- [ ] The logged in user can sort its orders by date.
- [ ] The logged in user can search for a product in his/her past orders.
- [ ] Website inspires a professional look: has logo, product descriptions, etc.

## Submission
To submit your work you must carefully do the following:
  - Fill in your personal info and link at the top of this file
  - Check off (i.e., fill in a `- [X]`) every task you fully completed in the Grading Levels listed above
  - Create an Issue in your repository titled "Ready to Grade"
  - If using AWS, be sure your server will continue running
  - You may not make any edits to your files after you create your issue.
