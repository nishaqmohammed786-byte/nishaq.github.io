from flask import Blueprint, redirect, session, url_for, render_template
from backend.database.db_config import get_db_connection

order_bp = Blueprint("order_bp", __name__)

# ---------------- PLACE ORDER ----------------
@order_bp.route("/order/<int:product_id>", methods=["POST"])
def order(product_id):
    if "user_id" not in session:
        return redirect(url_for("auth_bp.login"))

    user_id = session["user_id"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO orders (user_id, product_id, quantity, status) VALUES (%s,%s,%s,'pending')",
        (user_id, product_id, 1)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("order_bp.my_orders"))


# ---------------- MY ORDERS (USER) ----------------
@order_bp.route("/my-orders")
def my_orders():
    if "user_id" not in session:
        return redirect(url_for("auth_bp.login"))

    user_id = session["user_id"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            o.id,
            p.name AS product_name,
            o.quantity,
            o.status,
            o.order_time
        FROM orders o
        JOIN products p ON o.product_id = p.id
        WHERE o.user_id = %s
        ORDER BY o.order_time DESC
    """, (user_id,))

    orders = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("user_orders.html", orders=orders)
