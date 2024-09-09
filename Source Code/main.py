from flask import Flask, request, render_template, session, redirect
import pymysql
import os
conn = pymysql.connect(host="localhost", user="root", password="sai@54321", db="eCommerce")
cursor = conn.cursor()
app = Flask(__name__)
app.secret_key = "session"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = APP_ROOT + "/static/products"
admin_username = "admin"
admin_password = "admin"


@app.route('/')
def index():
    product_name = request.args.get("product_name")
    if product_name !=None:
        query = "SELECT * FROM products WHERE product_name LIKE '%" + product_name + "%'"
    else:
        query = "SELECT * FROM products"

    cursor.execute(query)
    products = cursor.fetchall()
    return render_template("index.html", products=products)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/admin_login1", methods=['post'])
def admin_login():
    username = request.form.get("username")
    password = request.form.get("password")
    session['role'] = "admin"
    if username == admin_username and password == admin_password:
        return redirect("/admin_head")
    else:
        return render_template("msg.html", message="Invalid login details")


@app.route("/admin_head")
def admin_head():
    return render_template("admin_head.html")


@app.route("/customer_login1", methods=['post'])
def customer_login_action():
    email = request.form.get("email")
    password = request.form.get("customer_password")
    count = cursor.execute("select * from customers where email='" + str(email) + "' and password='" + str(password) + "' ")
    if count > 0:
        customer = cursor.fetchall()
        session['customer_id'] = customer[0][0]
        session['role'] = 'customer'
        return redirect("/customer_head")
    else:
        return render_template("msg.html", message="Invalid login details")


@app.route("/customer_head")
def customer_home():
    customer_id = session['customer_id']
    cursor.execute("select * from customers where customer_id ='" + str(customer_id) + "'")
    customer = cursor.fetchone()
    return render_template("customer_head.html", customer=customer)


@app.route("/customer_registration")
def customer_registration():
    return render_template("customer_registration.html")


@app.route("/customer_registration1", methods=["post"])
def customer_registration1():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    phone = request.form.get("phone")
    address = request.form.get("address")
    count = cursor.execute("select * from customers where email = '"+str(email)+"'")
    if count > 0:
        return render_template("msg.html", message="Duplicate Email")
    count = cursor.execute("select * from customers where phone = '" + str(phone) + "'")
    if count > 0:
        return render_template("msg.html", message="Duplicate Phone Number")
    try:
        cursor.execute("insert into customers(name,email,password,phone,address)values('"+str(name)+"','"+str(email)+"','"+str(password)+"','"+str(phone)+"','"+str(address)+"')")
        conn.commit()
        return redirect("/login")
    except Exception as e:
        print(e)
        return render_template("msg.html", message="Something Went Wrong")


@app.route("/view_products")
def view_products():
    product_name  = request.args.get("product_name")
    if session['role'] == 'customer':
        customer_id = session['customer_id']
        cursor.execute("select * from customers where customer_id ='" + str(customer_id) + "'")
    customer = cursor.fetchone()
    if product_name != None:
        query = "select * from products where product_name like'%" + product_name + "%'"
    else:
        query = "select * from products"
    cursor.execute(query)
    products = cursor.fetchall()

    return render_template("view_products.html", products=products , customer=customer)


@app.route("/add_products")
def add_products():
    return render_template("add_products.html")


@app.route("/add_product1", methods=['post'])
def add_product1():
    category = request.form.get("category")
    product_name = request.form.get("product_name")
    image = request.files.get("image")
    price = request.form.get("price")
    quantity = request.form.get("quantity")
    description = request.form.get("description")
    colour = request.form.get("colour")
    path = APP_ROOT + "/" + image.filename
    image.save(path)
    cursor.execute("insert into products(category,product_name,image,price,quantity,discount,discount_price,description,colour,ratings)values('"+str(category)+"','"+str(product_name)+"','"+str(image.filename)+"','"+str(price)+"','"+str(quantity)+"',0,'"+str(price)+"','"+str(description)+"','"+str(colour)+"',4)")
    conn.commit()
    return redirect("/view_products")


@app.route("/update_quantity")
def update_quantity():
    product_id = request.args.get("product_id")
    discount = request.args.get("discount")
    price = request.args.get("price")
    price = int(price)
    dis_price = (float(discount) * int(price)) / 100
    discount_price = float(price) - float(dis_price)
    cursor.execute("update products set discount='" + str(discount) + "', discount_price='" + str(discount_price) + "' where product_id='" + str(product_id) + "'")
    conn.commit()
    return redirect("/view_products")


@app.route("/add_cart", methods=['post'])
def add_cart():
    product_id = request.form.get("product_id")
    quantity = request.form.get("quantity")
    customer_id = session['customer_id']
    count = cursor.execute("select * from cart where customer_id='"+str(customer_id)+"' and status='cart'")
    if count > 0:
        customer_orders = cursor.fetchall()
        customer_order_id = customer_orders[0][0]
    else:
        cursor.execute("insert into cart(customer_id,status)values('"+str(customer_id)+"','cart')")
        conn.commit()
        customer_order_id = cursor.lastrowid
    count = cursor.execute("select * from orders where product_id='"+str(product_id)+"' and cart_id='"+str(customer_order_id)+"'")
    if count > 0:
        cursor.execute("update orders set quantity=quantity+'"+str(quantity)+"' where product_id='"+str(product_id)+"'")
        conn.commit()
        return redirect("/view_cart")
    else:
        cursor.execute("insert into orders(product_id,cart_id,quantity,status)values('"+str(product_id)+"','"+str(customer_order_id)+"','"+str(quantity)+"', 'Added to cart')")
        conn.commit()
        return redirect("/view_cart")




@app.route("/view_cart")
def view_cart():
    role = session['role']
    type = request.args.get("type")
    if session['role'] == 'customer':
        customer_id = session['customer_id']
        cursor.execute("select * from customers where customer_id ='" + str(customer_id) + "'")
    customer = cursor.fetchone()
    if role == 'admin':
        if type == 'ordered':
            query = "select * from cart where (status='ordered')"
        elif type == 'processing':
            query = "select * from cart where (status='dispatched')"
        elif type == 'history':
            query = "select * from cart where (status='cancelled' or status='delivered')"
    elif role == 'customer':
        customer_id = session['customer_id']
        if type == 'cart':
            query = "select * from cart where customer_id='"+str(customer_id)+"' and (status='cart')"
        elif type == 'processing':
            query = "select * from cart where customer_id='"+str(customer_id)+"' and (status='ordered' or status='dispatched')"
        elif type == 'history':
            query = "select * from cart where customer_id='"+str(customer_id)+"' and (status='cancelled' or status='delivered' or status='Out Of Stock')"
    cursor.execute(query)
    customer_orders = cursor.fetchall()
    return render_template("view_cart.html", float=float, customer=customer, round=round, customer_orders=customer_orders, get_customer_by_customer_id=get_customer_by_customer_id, get_customer_order_items_by_customer_order_id=get_customer_order_items_by_customer_order_id, get_product_by_product_id=get_product_by_product_id, int=int)



def get_customer_by_customer_id(customer_id):
    cursor.execute("select * from customers where customer_id='"+str(customer_id)+"'")
    customers = cursor.fetchall()
    return customers[0]


def get_customer_order_items_by_customer_order_id(cart_id):
    print(cart_id)
    cursor.execute("select * from orders where cart_id='"+str(cart_id)+"'")
    customer_order_items = cursor.fetchall()
    print(customer_order_items)
    return customer_order_items


def get_product_by_product_id(product_id):
    cursor.execute("select * from products where product_id = '"+str(product_id)+"'")
    products = cursor.fetchall()
    return products[0]


@app.route("/order_now")
def order_now():
    if session['role'] == 'customer':
        customer_id = session['customer_id']
        cursor.execute("select * from customers where customer_id ='" + str(customer_id) + "'")
    customer = cursor.fetchone()
    customer_order_id = request.args.get("customer_order_id")
    totalPrice = request.args.get("totalPrice")
    tax1 = float(totalPrice) * float(8 / 100)
    tax = round(tax1, 2)
    total_price = float(totalPrice) + float(tax)
    total_price = round(total_price, 2)
    cursor.execute("select * from orders where order_id='"+str(customer_order_id)+"'")
    return render_template("order.html", customer_order_id=customer_order_id, customer=customer, totalPrice=totalPrice, total_price=total_price)


@app.route("/remove_from_cart")
def remove_from_cart():
    customer_order_item_id = request.args.get("customer_order_item_id")
    cursor.execute("select * from orders where ='"+str(customer_order_item_id)+"'")
    customer_order_items = cursor.fetchall()
    customer_order_id = customer_order_items[0][2]
    cursor.execute("delete from orders where order_id='"+str(customer_order_item_id)+"'")
    conn.commit()
    count = cursor.execute("select * from orders where order_id='"+str(customer_order_id)+"'")
    if count == 0:
        cursor.execute("delete from cart where order_id='"+str(customer_order_id)+"'")
        conn.commit()
        return render_template("msg.html", message="removed successfully")
    else:
        return redirect("/view_cart?type=cart")


@app.route("/pay_amount")
def pay_amount():
    customer_order_id = request.args.get("customer_order_id")
    cursor.execute("update cart set status='ordered' where cart_id = '" + str(customer_order_id) + "'")
    conn.commit()
    if session['role'] == 'customer':
        customer_id = session['customer_id']
        cursor.execute("select * from customers where customer_id ='" + str(customer_id) + "'")
    customer = cursor.fetchone()
    return render_template("msg.html", message="ordered successfully",customer=customer)


@app.route("/set_status")
def set_status():
    customer_order_id = request.args.get("customer_order_id")
    status = request.args.get("status")
    cursor.execute("update cart set status='"+str(status)+"' where cart_id='"+str(customer_order_id)+"'")
    conn.commit()
    if session['role'] == 'customer':
        customer_id = session['customer_id']
        cursor.execute("select * from customers where customer_id ='" + str(customer_id) + "'")
    customer = cursor.fetchone()
    return render_template("msg.html", message="status updated successfully", customer=customer)


@app.route("/wishlist_items")
def wishlist_items():
    product_id = request.args.get("product_id")
    cursor.execute("update products set status='Add To Wishlist' where product_id='"+str(product_id)+"'")
    return redirect("/view_products")


@app.route("/wishlist")
def wishlist():
    cursor.execute("select * from products where status='Add To Wishlist'")
    products = cursor.fetchall()
    if session['role'] == 'customer':
        customer_id = session['customer_id']
        cursor.execute("select * from customers where customer_id ='" + str(customer_id) + "'")
    customer = cursor.fetchone()
    return render_template("wishlist.html", products=products , customer=customer)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


app.run(debug=True)