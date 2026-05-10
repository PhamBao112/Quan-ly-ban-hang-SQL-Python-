from database.db import get_conn

def check_login(username, password):
    """Kiểm tra tên đăng nhập và mật khẩu"""
    try:
        conn = get_conn()
        if not conn: return None
        cur = conn.cursor(dictionary=True) # Sử dụng dictionary=True để lấy kết quả dưới dạng dict

        # Thực hiện truy vấn kiểm tra username và password trong bảng users
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        
        user = cur.fetchone()
        conn.close()
        return user
    except Exception as e:
        print(f"Lỗi Auth: {e}")
        return None