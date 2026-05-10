import tkinter as tk
from tkinter import ttk, messagebox
from models.order_model import fetch_orders, get_order_details

def history_window(parent):
    win = tk.Toplevel(parent)
    win.title('Lịch sử mua hàng')
    win.geometry('1100x600')

    # --- THANH CÔNG CỤ ---
    top = tk.Frame(win, bg="#f0f0f0", pady=5)
    top.pack(fill=tk.X)
    ttk.Button(top, text='⬅ Quay lại', command=win.destroy).pack(side=tk.LEFT, padx=10)
    tk.Label(top, text="LỊCH SỬ GIAO DỊCH", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(side=tk.LEFT)

    # --- GIAO DIỆN CHÍNH (Chia 2 cột) ---
    paned = tk.PanedWindow(win, orient=tk.HORIZONTAL)
    paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # 1. KHUNG TRÁI: DANH SÁCH ĐƠN HÀNG
    frame_left = ttk.LabelFrame(paned, text="Danh sách đơn hàng")
    paned.add(frame_left)

    cols_order = ('id', 'cust', 'date', 'total')
    tree_order = ttk.Treeview(frame_left, columns=cols_order, show='headings')
    tree_order.heading('id', text='#ID');      tree_order.column('id', width=50, anchor='center')
    tree_order.heading('cust', text='Khách hàng'); tree_order.column('cust', width=150)
    tree_order.heading('date', text='Ngày tạo');   tree_order.column('date', width=120)
    tree_order.heading('total', text='Tổng tiền'); tree_order.column('total', width=100, anchor='e')
    tree_order.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # 2. KHUNG PHẢI: CHI TIẾT ĐƠN HÀNG
    frame_right = ttk.LabelFrame(paned, text="Chi tiết đơn hàng")
    paned.add(frame_right)

    cols_detail = ('name', 'sl', 'price', 'subtotal')
    tree_detail = ttk.Treeview(frame_right, columns=cols_detail, show='headings')
    tree_detail.heading('name', text='Sản phẩm');  tree_detail.column('name', width=200)
    tree_detail.heading('sl', text='SL');          tree_detail.column('sl', width=40, anchor='center')
    tree_detail.heading('price', text='Đơn giá');  tree_detail.column('price', width=100, anchor='e')
    tree_detail.heading('subtotal', text='Thành tiền'); tree_detail.column('subtotal', width=100, anchor='e')
    tree_detail.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # --- LOGIC XỬ LÝ ---
    def load_orders():
        for r in tree_order.get_children(): tree_order.delete(r)
        df = fetch_orders()
        if df is not None:
            for _, r in df.iterrows():
                # Format tiền
                total_str = f"{r['total']:,.0f}".replace(",", ".")
                cust_name = r['customer_name'] if r['customer_name'] else "Khách lẻ"
                tree_order.insert('', tk.END, values=(r['order_id'], cust_name, r['created_at'], total_str))

    def on_order_select(event):
        sel = tree_order.selection()  # Lấy dòng được chọn
        if not sel: return
        
        # Lấy ID đơn hàng đang chọn
        order_id = tree_order.item(sel[0])['values'][0]
        
        # Xóa chi tiết cũ và tải chi tiết mới
        for r in tree_detail.get_children(): tree_detail.delete(r)  
        df = get_order_details(order_id)     
        
        if df is not None:              # Kiểm tra nếu có dữ liệu
            for _, r in df.iterrows():  # Duyệt từng dòng kết quả
                price_str = f"{r['price']:,.0f}".replace(",", ".")
                subtotal = r['price'] * r['quantity']   # Tính thành tiền
                sub_str = f"{subtotal:,.0f}".replace(",", ".")
                
                # Thêm vào bảng chi tiết
                tree_detail.insert('', tk.END, values=(r['product_name'], r['quantity'], price_str, sub_str))

    # Gán sự kiện click
    tree_order.bind('<<TreeviewSelect>>', on_order_select)
    
    # Nút làm mới
    ttk.Button(frame_left, text="Tải lại danh sách", command=load_orders).pack(pady=5)
    
    load_orders()