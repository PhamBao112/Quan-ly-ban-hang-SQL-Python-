import pandas as pd
from database.db import get_conn

# --- SỬA DÒNG NÀY: Thêm customer_name=None ---

def create_order(user_id, items, customer_name=None):
    conn = get_conn()
    cur = conn.cursor()
    try:
        total = sum(i['quantity'] * i['price'] for i in items)  # Tính tổng tiền
        
        # 1. Tạo đơn hàng trong bảng orders
        c_name = customer_name if customer_name else "Khách lẻ"  # Nếu không có tên thì gán là Khách lẻ

        # Thêm đơn hàng vào bảng orders
        cur.execute("INSERT INTO orders (user_id, total, customer_name) VALUES (%s,%s,%s)", 
                    (user_id, total, c_name))
        oid = cur.lastrowid
        
        # 2. Lưu chi tiết từng sản phẩm vào bảng order_items
        for it in items:
            cur.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s,%s,%s,%s)", 
                        (oid, it['product_id'], it['quantity'], it['price']))
            
        conn.commit()       # Lưu thay đổi vào cơ sở dữ liệu
        return oid          # Trả về ID đơn hàng
    except Exception as e:
        print(f"Lỗi tạo đơn: {e}")
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def fetch_orders():
    conn = get_conn()
    try:
        # Lấy danh sách đơn hàng kèm tên người dùng
        sql = """
        SELECT order_id, customer_name, total, created_at 
        FROM orders 
        ORDER BY created_at DESC
        """
        return pd.read_sql(sql, conn)
    except Exception as e:
        print(f"Lỗi lấy đơn hàng: {e}")
        return None
    finally:
        conn.close()

def get_order_details(order_id):
    conn = get_conn()
    try:
        sql = """
        SELECT p.product_name, oi.quantity, oi.price 
        FROM order_items oi 
        JOIN products p ON oi.product_id = p.product_id 
        WHERE oi.order_id = %s
        """
        return pd.read_sql(sql, conn, params=(order_id,))
    except Exception:
        return pd.DataFrame()
    finally:
        conn.close()