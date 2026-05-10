import tkinter as tk
from tkinter import ttk
from ui.product_ui import product_window
from ui.order_ui import order_window
from ui.user_ui import user_window
from ui.history_ui import history_window

def open_main_window(user):
    win = tk.Tk()
    win.title('Trang chủ')
    win.geometry('1000x600')
    lbl = ttk.Label(win, text=f"Xin chào: {user['username']} ({user['role']})", font=('Arial',12,'bold'))
    lbl.pack(pady=8)
    btn_frame = ttk.Frame(win)
    btn_frame.pack(pady=10)
    ttk.Button(btn_frame, text='Quản lý sản phẩm', width=20, command=lambda: product_window(win)).grid(row=0, column=0, padx=6, pady=6)
    ttk.Button(btn_frame, text='Quản lý đơn hàng', width=20, command=lambda: order_window(win)).grid(row=0, column=1, padx=6, pady=6)
    ttk.Button(btn_frame, text='Quản lý người dùng', width=20, command=lambda: user_window(win)).grid(row=0, column=2, padx=6, pady=6)
    ttk.Button(btn_frame, text='Lịch sử mua hàng', width=20, 
           command=lambda: history_window(win)).grid(row=1, column=0, padx=6, pady=6)
    win.mainloop()