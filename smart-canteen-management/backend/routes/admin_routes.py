from flask import Blueprint, render_template, redirect, session, url_for
from backend.database.db_config import get_db_connection

admin_bp = Blueprint(
    "admin_bp",
    __name__,
    url_prefix="/admin",
    template_folder="../../frontend/templates"
)

# ---------------- ADMIN DASHBOARD ----------------
@admin_bp.route("/dashboard")
def dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("auth_bp.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT COUNT(*) AS pending_count FROM orders WHERE status='pending'"
    )
    pending_count = cursor.fetchone()["pending_count"]

    cursor.close()
    conn.close()

    return render_template(
        "admin_dashboard.html",
        pending_count=pending_count
    )

# ---------------- VIEW ALL ORDERS ----------------
@admin_bp.route("/orders")
def orders():
    if session.get("role") != "admin":
        return redirect(url_for("auth_bp.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            o.id,
            u.name AS user_name,
            p.name AS product_name,
            o.quantity,
            o.status,
            o.order_time
        FROM orders o
        JOIN users u ON o.user_id = u.id
        JOIN products p ON o.product_id = p.id
        ORDER BY o.order_time DESC
    """)

    orders = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("admin_orders.html", orders=orders)

# ---------------- ACCEPT ORDER ----------------
@admin_bp.route("/accept/<int:order_id>")
def accept_order(order_id):
    if session.get("role") != "admin":
        return redirect(url_for("auth_bp.login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE orders SET status='accepted' WHERE id=%s",
        (order_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("admin_bp.orders"))

# ---------------- REJECT ORDER ----------------
@admin_bp.route("/reject/<int:order_id>")
def reject_order(order_id):
    if session.get("role") != "admin":
        return redirect(url_for("auth_bp.login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE orders SET status='rejected' WHERE id=%s",
        (order_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("admin_bp.orders"))
