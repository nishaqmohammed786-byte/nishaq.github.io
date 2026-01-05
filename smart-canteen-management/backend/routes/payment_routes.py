from flask import Blueprint, render_template, redirect, session, request, flash
import mysql.connector

payment_bp = Blueprint("payment_bp", __name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="canteen_db"
    )

@payment_bp.route("/pay/<int:order_id>", methods=["GET", "POST"])
def pay(order_id):
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Fetch order details
    cursor.execute("""
        SELECT o.id, o.quantity, p.name AS product_name, p.price
        FROM orders o
        JOIN products p ON o.product_id = p.id
        WHERE o.id=%s AND o.user_id=%s
    """, (order_id, session["user_id"]))

    order = cursor.fetchone()

    if not order:
        cursor.close()
        db.close()
        return "Order not found"

    total = order["quantity"] * order["price"]

    # When user confirms payment
    if request.method == "POST":
        cursor.execute(
            "UPDATE orders SET status='paid' WHERE id=%s",
            (order_id,)
        )
        db.commit()

        cursor.close()
        db.close()

        # FLASH MESSAGE
        flash("Payment successful! Thank you for your order.", "success")
        return redirect("/my-orders")

    cursor.close()
    db.close()

    return render_template("payment.html", order=order, total=total)
