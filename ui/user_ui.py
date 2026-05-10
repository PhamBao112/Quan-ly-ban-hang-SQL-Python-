import tkinter as tk
from tkinter import ttk, messagebox
from database.db import get_conn

def user_window(parent):
    # 1. Sửa kích thước thành 1000x600 (cho bằng trang chủ)
    win = tk.Toplevel(parent)
    win.title('Quản lí người dùng')
    win.geometry('1000x600') 
    
    # Tạo frame trên cùng để chứa nút Back và Add
    top = ttk.Frame(win)
    top.pack(fill=tk.X, padx=8, pady=6)

    # --- NÚT BACK (Thêm theo yêu cầu) ---
    ttk.Button(top, text='⬅ Quay lại', command=win.destroy).pack(side=tk.LEFT)
    
    # Nút Add User (Đưa lên trên góc phải cho gọn)
    ttk.Button(top, text='Add user', command=lambda: add()).pack(side=tk.RIGHT)

    # Cấu hình bảng
    columns = ('user_id', 'username', 'Fullname', 'role')
    tree = ttk.Treeview(win, columns=columns, show='headings')
    
    # Sửa lại tiêu đề cột cho đẹp xíu nhưng vẫn giữ nguyên logic
    headers = {'user_id': 'ID', 'username': 'Username', 'Fullname': 'Fullname', 'role': 'Role'}
    for col in columns: 
        tree.heading(col, text=headers[col])
        tree.column(col, width=150)
        
    tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)

# --- NÚT XÓA ---

    def delete():
        sel = tree.selection()
        if not sel: 
            messagebox.showwarning("Chú ý", "Chưa chọn dòng nào để xóa!")
            return
        
        # Lấy thông tin dòng đang chọn
        row = tree.item(sel[0])['values']
        uid, uname = row[0], row[1]
        
        # Xác nhận xóa
        if messagebox.askyesno("Xác nhận", f"Bạn muốn xóa tài khoản: {uname}?"):
            try:
                conn = get_conn(); cur = conn.cursor()                      # Mở kết nối
                cur.execute("DELETE FROM users WHERE user_id = %s", (uid,))  # Xóa user theo ID
                conn.commit(); cur.close(); conn.close()                    # Đóng kết nối
                load() # Tải lại bảng sau khi xóa
                messagebox.showinfo("OK", "Đã xóa thành công")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

    ttk.Button(top, text='Xóa', command=delete).pack(side=tk.RIGHT, padx=5)


    def load():
        try:
            conn = get_conn()
            cur = conn.cursor(dictionary=True)
            cur.execute('SELECT user_id, username, Fullname, role FROM users')
            rows = cur.fetchall()
            cur.close(); conn.close()
            
            for r in tree.get_children(): tree.delete(r)
            # Giữ nguyên cách lấy dữ liệu của bạn
            for r in rows: 
                tree.insert('', tk.END, values=(r['user_id'], r['username'], r['Fullname'], r['role']))
        except Exception as e: 
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {e}")

    # Hàm thêm User (Giữ nguyên logic u, p, r, fu của bạn)

    def add():
        f = tk.Toplevel(win)
        f.title('Add user')
        f.geometry('400x400')
        
        # Nhập Username
        tk.Label(f, text='Username').pack(pady=(10,0))
        u = tk.Entry(f); u.pack()
        
        # Nhập Password
        tk.Label(f, text='Password').pack(pady=(10,0))
        p = tk.Entry(f); p.pack()
        
        # Nhập Role
        tk.Label(f, text='Role').pack(); r = tk.Entry(f); r.pack()

        # Nhập Fullname
        tk.Label(f, text="Fullname").pack(pady=(10,0))
        fu = tk.Entry(f); fu.pack()

        def save():
            try:
                conn = get_conn()
                cur = conn.cursor()
                # Insert y hệt code gốc
                cur.execute('INSERT INTO users (username, password, role, Fullname) VALUES (%s, %s, %s, %s)',
                            (u.get(), p.get(), r.get() or 'user', fu.get()))
                conn.commit()
                cur.close(); conn.close()
                f.destroy()
                load()
                messagebox.showinfo("OK", "Đã thêm user")
            except Exception as e: 
                messagebox.showerror("Lỗi", str(e))

        tk.Button(f, text='Save', command=save).pack(pady=20)
    
    # Load dữ liệu lần đầu
    load()