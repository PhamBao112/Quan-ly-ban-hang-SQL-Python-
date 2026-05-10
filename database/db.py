import mysql.connector

def get_conn():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",            # Mật khẩu kết nối
        database="qlbmt"        # Tên CSDL để kết nối
    )