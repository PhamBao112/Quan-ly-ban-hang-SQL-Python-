import tkinter as tk
from tkinter import ttk, messagebox
from models.order_model import create_order
from models.product_model import fetch_products

def order_window(parent):
    win = tk.Toplevel(parent)
    win.title('Quản lí đơn hàng')
    win.geometry('1100x600') # Kích thước cửa sổ

    # THANH TOOLBAR 
    top = tk.Frame(win, bg="#f0f0f0", pady=5)
    top.pack(fill=tk.X)
    ttk.Button(top, text='⬅ Quay lại', command=win.destroy).pack(side=tk.LEFT, padx=10)
    tk.Label(top, text="QUẢN LÝ ĐƠN HÀNG", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(side=tk.LEFT, padx=10)

    # GIAO DIỆN CHÍNH 
    main_frame = tk.Frame(win)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # CỘT TRÁI: DANH SÁCH SẢN PHẨM
    left = ttk.LabelFrame(main_frame, text="DANH SÁCH SẢN PHẨM")
    left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
    cols = ('id', 'name', 'price')
    tree = ttk.Treeview(left, columns=cols, show='headings')
    tree.heading('id', text='ID');    tree.column('id', width=40, anchor='center')
    tree.heading('name', text='Tên sản phẩm'); tree.column('name', width=300)
    tree.heading('price', text='Giá bán'); tree.column('price', width=120, anchor='e')
    tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # CỘT PHẢI: THANH TOÁN 
    right = ttk.LabelFrame(main_frame, text="Thông tin thanh toán")
    right.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0), ipadx=10)

    # A. Tên khách hàng
    tk.Label(right, text="Tên khách hàng:", anchor='w').pack(fill=tk.X, padx=5, pady=(5,0))
    ent_customer = ttk.Entry(right)
    ent_customer.pack(fill=tk.X, padx=5, pady=5)

    # B. Số lượng & Nút Thêm vào giỏ
    row_add = tk.Frame(right)
    row_add.pack(fill=tk.X, padx=5, pady=5)
    tk.Label(row_add, text="Số lượng:").pack(side=tk.LEFT)
    spin_qty = tk.Spinbox(row_add, from_=1, to=100, width=5)
    spin_qty.pack(side=tk.LEFT, padx=5)
    
    # Hàm thêm 
    cart = []                       # Khởi tạo giỏ hàng 
    def add_to_cart():
        sel = tree.selection()
        if not sel: return
        
        # Lấy dữ liệu sản phẩm chọn
        item = tree.item(sel[0])['values']   # Lấy dữ liệu từ dòng được chọn
        pid = item[0]
        name = item[1]
        price = float(str(item[2]).replace(".", ""))  # Giá sản phẩm (tách dấu chấm)
        qty = int(spin_qty.get())                   # Số lượng người dùng chọn
        total_line = price * qty                    # Tổng tiền cho dòng sản phẩm
        cart.append({'product_id': pid, 'name': name, 'price': price, 'quantity': qty}) # Lưu vào giỏ hàng

        # Format tiền tệ:
        total_str = f"{total_line:,.0f}".replace(",", ".")
        tree_cart.insert('', tk.END, values=(name, qty, total_str))  # Thêm vào bảng giỏ hàng
        update_total()                              # Cập nhật tổng tiền 
    ttk.Button(row_add, text='Thêm vào giỏ >>', command=add_to_cart).pack(side=tk.RIGHT)

    # C. Bảng Giỏ hàng 
    tk.Label(right, text="Giỏ hàng hiện tại:", font=("Arial", 9, "bold")).pack(anchor='w', padx=5, pady=(10,0))
    cols_cart = ('name', 'qty', 'total')
    tree_cart = ttk.Treeview(right, columns=cols_cart, show='headings', height=10)
    tree_cart.heading('name', text='Sản phẩm'); tree_cart.column('name', width=180)
    tree_cart.heading('qty', text='SL');        tree_cart.column('qty', width=40, anchor='center')
    tree_cart.heading('total', text='Thành tiền'); tree_cart.column('total', width=100, anchor='e')
    tree_cart.pack(fill=tk.X, padx=5, pady=5)

    # D. Tổng cộng 
    lbl_total = tk.Label(right, text="TỔNG CỘNG: 0 VNĐ", fg="red", font=("Arial", 14, "bold"))
    lbl_total.pack(pady=10)

    # E. Nút Xóa món & Thanh toán
    def update_total():
        total = sum(item['price'] * item['quantity'] for item in cart)
        total_str = f"{total:,.0f}".replace(",", ".")
        lbl_total.config(text=f"TỔNG CỘNG: {total_str} VNĐ")

    def delete_item():
        sel = tree_cart.selection()
        if not sel: return
        
        # Xóa trong logic cart 
        idx = tree_cart.index(sel[0])
        cart.pop(idx)
        
        # Xóa trên giao diện
        tree_cart.delete(sel[0])
        update_total()

    ttk.Button(right, text='Xóa món đang chọn', command=delete_item).pack(anchor='e', padx=5)
    ttk.Separator(right, orient='horizontal').pack(fill='x', pady=15)

    def place_order():
        if not cart: return messagebox.showwarning('Trống', 'Giỏ hàng đang trống!')
        try:
            cust_name = ent_customer.get().strip() or "Khách lẻ"
            oid = create_order(1, cart, customer_name=cust_name)
            messagebox.showinfo('Thành công', f'Đã lưu đơn hàng #{oid}\nKhách: {cust_name}')
            
            # Reset
            cart.clear()
            for row in tree_cart.get_children(): tree_cart.delete(row)
            lbl_total.config(text="TỔNG CỘNG: 0 VNĐ")
            ent_customer.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror('Lỗi', str(e))

    # Nút Thanh toán 
    btn_pay = tk.Button(right, text='THANH TOÁN & LƯU', bg="white", fg="#2196F3", 
                        font=("Arial", 10, "bold"), pady=10, command=place_order)
    btn_pay.pack(fill=tk.X, padx=5, pady=5)

    # Load dữ liệu sản phẩm
    def load_products():
        for r in tree.get_children(): tree.delete(r)
        rows = fetch_products()
        for r in rows:
            raw_price = r.get('sale_price', 0)
            price_str = f"{raw_price:,.0f}".replace(",", ".")
            tree.insert('', tk.END, values=(r['product_id'], r['product_name'], price_str))
    load_products()