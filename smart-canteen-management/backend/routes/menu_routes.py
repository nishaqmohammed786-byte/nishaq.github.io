from flask import Blueprint, render_template, session, redirect, url_for
from backend.database.db_config import get_db_connection

menu_bp = Blueprint("menu_bp", __name__)

# ---------------- MENU PAGE ----------------
@menu_bp.route("/menu")
def menu():   # 🔥 FIXED FUNCTION NAME
    if "user_id" not in session:
        return redirect(url_for("auth_bp.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("menu.html", products=products)
