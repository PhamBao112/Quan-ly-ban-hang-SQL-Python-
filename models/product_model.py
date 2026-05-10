# models/product_model.py
from database.db import get_conn

def fetch_products(search=None):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    sql = """
    SELECT p.product_id, p.product_name, b.brand_name, pr.sale_price, pr.original_price, pr.discount_percent, r.rating, r.total_reviews
    FROM products p
    LEFT JOIN brands b ON p.brand_id = b.brand_id
    LEFT JOIN product_prices pr ON p.product_id = pr.product_id
    LEFT JOIN product_reviews r ON p.product_id = r.product_id
    """
    params = []
    if search:
        sql += " WHERE p.product_name LIKE %s OR b.brand_name LIKE %s"
        q = f"%{search}%"
        params = [q, q]
    sql += " ORDER BY p.product_id DESC"
    cur.execute(sql, params)
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows


def delete_product(product_id):
    conn = get_conn()
    cur = conn.cursor()
    try:
        # Xóa sản phẩm theo ID
        cur.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()