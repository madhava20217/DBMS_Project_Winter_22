#TODO: product site: product rating average and take details 
#from sql queries
#TODO: make a page for showing previous orders of the customer

from flask import Blueprint, render_template, flash, request, flash, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user
import mysql.connector
from .User import User
from . import connect_db, getcursor, db_commit, mydb

views = Blueprint('views', __name__)

@views.route('/')
def home1():
    print(current_user.get_id())
    return render_template("Home1.html")

@views.route('/2')
def home2():
    return render_template("Home2.html")

@views.route('/3')
def home3():
    return render_template("Home3.html")

@views.route('/4')
def home4():
    return render_template("Home4.html")

@views.route('/5')
def home5():
    return render_template("Home5.html")

@views.route('/product', methods=['GET','POST'])
def product():
    # get product id, name, price, discount, and customer id 
    if request.method == 'POST':
        #TODO here
        # print("added to cart")
        quantity = request.form.get('quantity')


        flash('Added to Cart!', category='success')
        pass
    return render_template("Product.html", prod_name = "adfadsf", prod_price = "53", prod_discount = "1", user=current_user)

@views.route('/cart')
@login_required
def cart():
    try:
        mydb
    except NameError as e:
        connect_db()

    print(current_user)

    cursor = getcursor()
    query = "select * from Customer where email_address = %s"
    cursor.execute(query, [current_user.get_id()])
    temp = list(iter(cursor.fetchall()))
    cursor.close()
    prod_list = []
    final_list = []
    if len(temp) != 0:
        cursor2 = getcursor()
        query2 = "select * from Shopping_Cart where customer_ID = %s"
        cursor2.execute(query2, [temp[0][0]])
        prod_list = list(iter(cursor2.fetchall()))
        cursor2.close()

        for prod in prod_list:
            query3 = "select * from Product where Product_ID = %s"
            cursor3 = getcursor()
            cursor3.execute(query3, [prod[1]])
            prod_details = list(iter(cursor3.fetchall()))
            cursor3.close()
            final_list.append((prod, prod_details))

    # Structure of final_list:
    # [((customer_id, product_id, quantity), [(product_id, price, name, discount, gst)]),.....]

    return render_template("Cart.html", user=current_user, prod_list=final_list)

@views.route('/order')
@login_required
def order():
    try:
        mydb
    except NameError as e:
        connect_db()

    print(current_user.get_id())
    cursor = getcursor()
    try:
        query = "select * from Customer_Order where Customer_ID = %s"
        cursor.execute(query, [current_user.get_id()])
        orders_list = list(iter(cursor.fetchall()))
        
    except Exception as e:
        print(e)

    cursor.close()
    print(orders_list)

    return render_template("Order.html", user=current_user, orders_list = orders_list)
