import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog # SỬA: Thêm thư viện thiếu
from database.db import get_conn # SỬA: Thêm hàm kết nối DB
from models.product_model import fetch_products, delete_product
import shutil
from api.recommender import recommend_products
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)

def product_window(parent):
    # Kiểm tra xem đã có cửa sổ con chưa và cửa sổ đó còn mở không
    if hasattr(parent, 'win_product') and parent.win_product.winfo_exists():
        parent.win_product.lift()  # Kéo cửa sổ cũ lên trên cùng
        parent.win_product.focus() # Đặt chuột vào đó
        return
    win = tk.Toplevel(parent)
    parent.win_product = win       #QUAN TRỌNG: Lưu cửa sổ này lại để lần sau kiểm tra
    win.title('Quản lý sản phẩm')
    win.geometry('1000x600')
    top = ttk.Frame(win)
    top.pack(fill=tk.X, padx=8, pady=6)
    ttk.Button(top, text='⬅ Quay lại', command=win.destroy).pack(side=tk.LEFT, padx=5)  # Nút Quay lại
    
    # SỬA: Thêm hàm giả để nút Xuất Excel không bị lỗi
    def export_products_excel():
        messagebox.showinfo("Thông báo", "Chức năng đang phát triển")

    tk.Label(top, text='Tìm:').pack(side=tk.LEFT)
    s = tk.Entry(top); s.pack(side=tk.LEFT, padx=6)
    ttk.Button(top, text='Tìm', command=lambda: load()).pack(side=tk.LEFT)
    ttk.Button(top, text='Thêm', command=lambda: open_form()).pack(side=tk.RIGHT, padx=6)
    ttk.Button(top, text='Xuất Excel', command=lambda: export_products_excel()).pack(side=tk.RIGHT, padx=6)

    cols = ('ID','Tên Sản phẩm','Hãng','Giá bán')
    tree = ttk.Treeview(win, columns=cols, show='headings')
    for c in cols:
        tree.heading(c, text=c)
    tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)
    
    # -------------Nút xóa của Quản lí sản phẩm ----------------------------------------------
    def delete_handler():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sản phẩm cần xóa!")
            return
        
        # Hỏi xác nhận
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa sản phẩm này?"):
            try:
                pid = int(tree.item(sel[0])['values'][0])
                delete_product(pid) # Gọi hàm xóa
                messagebox.showinfo("Thành công", "Đã xóa sản phẩm!")
                load() # Tải lại bảng
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không xóa được (Có thể do ràng buộc đơn hàng).\nChi tiết: {e}")
    
    # Tạo nút bấm
    ttk.Button(top, text='Xóa', command=delete_handler).pack(side=tk.RIGHT, padx=6)
    # -----------------------------------------------------------


    def load():
        for r in tree.get_children(): tree.delete(r)
        rows = fetch_products(search=s.get().strip() or None)
        for r in rows:
            raw_price = r.get('sale_price', 0)
            price_str = f"{raw_price:,.0f}".replace(",", ".")
            # SỬA: Thêm xử lý nếu giá trị bị None để tránh lỗi hiển thị
            tree.insert('', tk.END, values=(
                r['product_id'], 
                r['product_name'], 
                r['brand_name'], 
                price_str  # <--- Dùng biến này mới hiện dấu chấm
            ))

    def open_form(product=None):
        f = tk.Toplevel(win);
        f.title('Product Form');
        f.geometry('480x520')
        
        # SỬA: Thêm hàm upload ảnh để nút bấm hoạt động
        def upload_image(entries):
            filename = filedialog.askopenfilename()
            if filename:
                messagebox.showinfo("Ảnh", f"Đã chọn: {filename}")
                # Logic copy ảnh bạn có thể thêm sau

        # --- Định nghĩa các hàm Database BÊN TRONG open_form theo yêu cầu của bạn ---
        def get_product(product_id):
            conn = get_conn()
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM products WHERE product_id=%s", (product_id,))
            row = cur.fetchone()
            cur.close(); conn.close()
            return row

        def insert_product(data):
            conn = get_conn()
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO products (brand_id, category_id, product_name, short_description, weight, cpu, gpu, ram, ssd) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                data.get('brand_id'), data.get('category_id',1), data['product_name'], data.get('short_description'), data.get('weight'), data.get('cpu'), data.get('gpu'), data.get('ram'), data.get('ssd')
                ))
                pid = cur.lastrowid
                cur.execute("INSERT INTO product_prices (product_id, original_price, sale_price, discount_percent, gift_value) VALUES (%s,%s,%s,%s,%s)", (pid, data.get('original_price',0), data.get('sale_price',0), data.get('discount_percent',0), data.get('gift_value',0)))
                cur.execute("INSERT INTO product_reviews (product_id, rating, total_reviews) VALUES (%s,%s,%s)", (pid, data.get('rating',0), data.get('total_reviews',0)))
                conn.commit()
                return pid
            except Exception:
                conn.rollback()
                raise
            finally:
                cur.close(); conn.close()

        def update_product(product_id, data):
            conn = get_conn()
            cur = conn.cursor()
            try:
                cur.execute("UPDATE products SET brand_id=%s, category_id=%s, product_name=%s, short_description=%s, weight=%s, cpu=%s, gpu=%s, ram=%s, ssd=%s WHERE product_id=%s", (
                data.get('brand_id'), data.get('category_id',1), data['product_name'], data.get('short_description'), data.get('weight'), data.get('cpu'), data.get('gpu'), data.get('ram'), data.get('ssd'), product_id))
                cur.execute("UPDATE product_prices SET original_price=%s, sale_price=%s, discount_percent=%s, gift_value=%s WHERE product_id=%s", (data.get('original_price'), data.get('sale_price'), data.get('discount_percent'), data.get('gift_value'), product_id))
                cur.execute("UPDATE product_reviews SET rating=%s, total_reviews=%s WHERE product_id=%s", (data.get('rating',0), data.get('total_reviews',0), product_id))
                conn.commit()
                return True
            except Exception:
                conn.rollback(); raise
            finally:
                cur.close(); conn.close()
        # ---------------------------------------------------------------------------

        labels = ['Tên', 'Hãng', 'Mô tả', 'Trọng lượng', 'CPU', 'GPU', 'RAM', 'SSD', 'Giá gốc', 'Giá bán', '% giảm']
        entries = {}
        for i, lbl in enumerate(labels):
            ttk.Label(f, text=lbl).grid(row=i, column=0, sticky=tk.W, pady=4)
            ent = ttk.Entry(f);
            ent.grid(row=i, column=1, sticky=tk.EW, padx=6)
            entries[lbl] = ent
        ttk.Button(f, text='Upload ảnh', command=lambda: upload_image(entries)).grid(row=len(labels), column=0, pady=8)

        # --- Nếu có product thì load dữ liệu cũ ---
        def get_brand_id(brand_name):
                    brand_name = brand_name.strip()
                    if not brand_name: return 1 # Nếu để trống thì mặc định là 1 (HP)
                    
                    conn = get_conn()
                    cur = conn.cursor()
                    try:
                        # Tìm xem hãng đã có chưa
                        cur.execute("SELECT brand_id FROM brands WHERE brand_name = %s", (brand_name,))
                        row = cur.fetchone()
                        if row: 
                            return row[0] # Nếu có rồi thì lấy ID
                        else:
                            # Nếu chưa có thì tạo mới luôn
                            cur.execute("INSERT INTO brands (brand_name) VALUES (%s)", (brand_name,))
                            conn.commit()
                            return cur.lastrowid
                    except:
                        return 1 # Nếu lỗi thì về mặc định
                    finally:
                        cur.close(); conn.close()       

        def save():
            try:
                input_brand = entries['Hãng'].get()      # Lấy tên hãng từ ô nhập {def get_brand_id(brand_name)}
                data = {
                'product_name': entries['Tên'].get(),
                'short_description': entries['Mô tả'].get(),
                'weight': float(entries['Trọng lượng'].get() or 0),
                'cpu': entries['CPU'].get(),
                'gpu': entries['GPU'].get(),
                'ram': entries['RAM'].get(),
                'ssd': entries['SSD'].get(),
                'original_price': int(entries['Giá gốc'].get() or 0),
                'sale_price': int(entries['Giá bán'].get() or 0),
                'discount_percent': int(entries['% giảm'].get() or 0),
                'brand_id': get_brand_id(input_brand),                              # Đây là code cứng, chỉ gán giá trị đc cho sẵn, ở đây là HP
                'category_id': 1                            # Tương tự
                }
                
                # SỬA: Logic kiểm tra pid để tránh lỗi khi Update
                if product:
                    update_product(product['product_id'], data)
                    messagebox.showinfo('OK','Đã cập nhật')
                else:
                    pid = insert_product(data)
                    if pid:
                        messagebox.showinfo('OK','Đã thêm')
                
                load()
                f.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

        ttk.Button(f, text='Lưu', command=save).grid(row=len(labels)+1, column=1, sticky=tk.E)


        def upload_image(entries):
            path = filedialog.askopenfilename(title='Chọn ảnh')
            if not path: return
            fname = os.path.basename(path)
            dest = os.path.join(UPLOAD_FOLDER, fname)
            shutil.copy(path, dest)
            messagebox.showinfo('OK', f'Đã lưu ảnh: {dest}')

    def show_recommend():
            sel = tree.selection()          #Lấy danh sách các dòng đang được chọn trong bảng
            if not sel: return          
            pid = int(tree.item(sel[0])['values'][0])   #Lấy product_id từ dòng đầu tiên được chọn
            recs = recommend_products(pid, top_k=4)     #Gọi hàm gợi ý sản phẩm, lấy 4 sản phẩm
            messagebox.showinfo('Recommend', f'Gợi ý: {recs}')

    ttk.Button(top, text='Gợi ý', command=show_recommend).pack(side=tk.RIGHT, padx=6)
    load()

    # Load dữ liệu lần đầu
    load()