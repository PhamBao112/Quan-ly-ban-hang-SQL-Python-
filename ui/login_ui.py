import tkinter as tk
from tkinter import messagebox
from api.auth import check_login
from ui.main_ui import open_main_window

def open_login():
    win = tk.Tk()
    win.title("Hệ Thống Quản Lý - Đăng Nhập")
    win.geometry("1000x600")     
    win.configure(bg="#f2f2f2")  

    # --- KHUNG FORM ĐĂNG NHẬP (CARD) ---
    # Tạo một khung trắng nằm chính giữa màn hình
    frame = tk.Frame(win, bg="white", padx=40, pady=40, relief=tk.RIDGE, bd=1)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER) # Căn giữa tuyệt đối

    # Tiêu đề
    tk.Label(frame, text="ĐĂNG NHẬP", font=("Arial", 20, "bold"), bg="white", fg="#333").pack(pady=(0, 20))

    # Ô nhập Username
    tk.Label(frame, text="Username:", font=("Arial", 10), bg="white").pack(anchor=tk.W)
    user = tk.Entry(frame, width=35, font=("Arial", 11), bg="#fafafa")
    user.pack(pady=5, ipady=3) 

    # Ô nhập Password
    tk.Label(frame, text="Password:", font=("Arial", 10), bg="white").pack(anchor=tk.W, pady=(10, 0))
    pwd = tk.Entry(frame, show="*", width=35, font=("Arial", 11), bg="#fafafa")
    pwd.pack(pady=5, ipady=3)

    # Hàm xử lý
    
    def do_login(event=None):                  # event=None giúp hàm hoạt động khi nhấn Enter
        u = check_login(user.get(), pwd.get()) # Gọi hàm kiểm tra đăng nhập
        if u:
            messagebox.showinfo("Chào mừng", f"Xin chào {u['username']}!")
            win.destroy()
            open_main_window(u)
        else:
            messagebox.showerror("Lỗi", "Tài khoản hoặc mật khẩu không đúng!")

    # Tạo nút bấm Đăng nhập
    btn = tk.Button(frame, text="ĐĂNG NHẬP", command=do_login, 
                    bg="#2196F3", fg="white", font=("Arial", 10, "bold"), 
                    width=30, height=2, cursor="hand2", relief=tk.FLAT)
    btn.pack(pady=20)

    win.bind('<Return>', do_login)  # Gán sự kiện phím Enter gọi hàm đăng nhập
    win.mainloop()