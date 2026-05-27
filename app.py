from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
from MySQLdb.cursors import DictCursor

app = Flask(__name__)
app.secret_key = "seasons_cafe_secret_key"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "seasons_cafe_db"

mysql = MySQL(app)

CAFE = {
    "name": "Seasons Cafe Nashik",
    "display_name": "Sea Sons Cafe N Restro",
    "tagline": "Scan • Order • Enjoy",
    "address": "Floor 1 & 2, KBT Circle, Gangapur Road, Saubhagya Nagar, Manik Nagar, College Road, Nashik",
    "phone": "+91 72768 36833",
    "cost": "₹800 for two approx.",
    "cuisines": "Pizza, Bakery, Burger, Fast Food, Desserts, Sandwich, Cafe, Coffee",
    "upi_id": "seasoncafe@upi",
    "upi_name": "Sea Sons Cafe N Restro"
}


@app.route("/")
def index():
    table_no = request.args.get("table", "")
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM menu_items WHERE availability='Available' ORDER BY category, item_name")
    menu_items = cur.fetchall()
    cur.close()
    categories = sorted(set(item["category"] for item in menu_items))
    return render_template("index.html", cafe=CAFE, menu_items=menu_items, categories=categories, table_no=table_no)


@app.route("/checkout")
def checkout():
    table_no = request.args.get("table", "")
    return render_template("checkout.html", cafe=CAFE, table_no=table_no)


@app.route("/place_order", methods=["POST"])
def place_order():
    data = request.get_json()
    cart = data.get("cart", [])

    if not data.get("customer_name") or not cart:
        return jsonify({"success": False, "message": "Please enter name and add at least one item."})

    total_amount = sum(float(item["price"]) * int(item["quantity"]) for item in cart)
    payment_method = data.get("payment_method", "Pay at Counter")

    if payment_method == "UPI Online Payment":
        payment_status = "Pending Verification"
    else:
        payment_status = "Pending"

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO orders (customer_name, phone, table_no, total_amount, payment_method, payment_status, order_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        data.get("customer_name"),
        data.get("phone"),
        data.get("table_no"),
        total_amount,
        payment_method,
        payment_status,
        "Pending"
    ))

    order_id = cur.lastrowid

    for item in cart:
        subtotal = float(item["price"]) * int(item["quantity"])
        cur.execute("""
            INSERT INTO order_items (order_id, item_id, item_name, quantity, price, subtotal)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            order_id,
            item["id"],
            item["name"],
            item["quantity"],
            item["price"],
            subtotal
        ))

    mysql.connection.commit()
    cur.close()
    return jsonify({"success": True, "order_id": order_id})


@app.route("/success/<int:order_id>")
def success(order_id):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM orders WHERE order_id=%s", (order_id,))
    order = cur.fetchone()
    cur.execute("SELECT * FROM order_items WHERE order_id=%s", (order_id,))
    items = cur.fetchall()
    cur.close()
    return render_template("success.html", cafe=CAFE, order=order, items=items)


@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cur = mysql.connection.cursor(DictCursor)
        cur.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
        admin = cur.fetchone()
        cur.close()

        if admin:
            session["admin_logged_in"] = True
            return redirect(url_for("dashboard"))
        error = "Invalid username or password"

    return render_template("admin_login.html", cafe=CAFE, error=error)


@app.route("/dashboard")
def dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM orders ORDER BY order_time DESC")
    orders = cur.fetchall()

    total_sales = sum(float(order["total_amount"]) for order in orders if order["order_status"] != "Cancelled")
    pending_count = sum(1 for order in orders if order["order_status"] == "Pending")

    for order in orders:
        cur.execute("SELECT * FROM order_items WHERE order_id=%s", (order["order_id"],))
        order["items"] = cur.fetchall()

    cur.close()
    return render_template("dashboard.html", cafe=CAFE, orders=orders, total_sales=total_sales, pending_count=pending_count)


@app.route("/update_status/<int:order_id>", methods=["POST"])
def update_status(order_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    cur = mysql.connection.cursor()
    cur.execute("UPDATE orders SET order_status=%s WHERE order_id=%s", (request.form["order_status"], order_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("dashboard"))


@app.route("/update_payment/<int:order_id>", methods=["POST"])
def update_payment(order_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    cur = mysql.connection.cursor()
    cur.execute("UPDATE orders SET payment_status=%s WHERE order_id=%s", (request.form["payment_status"], order_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("dashboard"))


@app.route("/bill/<int:order_id>")
def bill(order_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM orders WHERE order_id=%s", (order_id,))
    order = cur.fetchone()
    cur.execute("SELECT * FROM order_items WHERE order_id=%s", (order_id,))
    items = cur.fetchall()
    cur.close()

    return render_template("bill.html", cafe=CAFE, order=order, items=items)


@app.route("/manage_menu", methods=["GET", "POST"])
def manage_menu():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    cur = mysql.connection.cursor(DictCursor)

    if request.method == "POST":
        cur.execute("""
            INSERT INTO menu_items (item_name, category, price, description, image, availability)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            request.form["item_name"],
            request.form["category"],
            request.form["price"],
            request.form["description"],
            request.form["image"],
            request.form["availability"]
        ))
        mysql.connection.commit()

    cur.execute("SELECT * FROM menu_items ORDER BY category, item_name")
    menu_items = cur.fetchall()
    cur.close()
    return render_template("manage_menu.html", cafe=CAFE, menu_items=menu_items)


@app.route("/update_menu/<int:item_id>", methods=["POST"])
def update_menu(item_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE menu_items SET item_name=%s, category=%s, price=%s, description=%s, image=%s, availability=%s
        WHERE item_id=%s
    """, (
        request.form["item_name"],
        request.form["category"],
        request.form["price"],
        request.form["description"],
        request.form["image"],
        request.form["availability"],
        item_id
    ))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("manage_menu"))


@app.route("/delete_menu/<int:item_id>")
def delete_menu(item_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM menu_items WHERE item_id=%s", (item_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("manage_menu"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("admin_login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)