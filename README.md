# Hệ thống Quản lý Bán hàng (LT Python)

Ứng dụng quản lý bán hàng được xây dựng bằng Python, kết hợp với hệ quản trị cơ sở dữ liệu MySQL. Dự án được phân chia cấu trúc thư mục rõ ràng theo module (api, models, ui, database).

## Chức năng chính
- Quản lý sản phẩm (Laptop, linh kiện), danh mục và thương hiệu.
- Quản lý người dùng, phân quyền đăng nhập.
- Quản lý đơn hàng, giỏ hàng và lịch sử giao dịch.
- Lưu trữ hình ảnh sản phẩm và theo dõi biến động giá.

## Công nghệ sử dụng
- Ngôn ngữ: Python
- Cơ sở dữ liệu: MySQL (XAMPP)
- Thư viện yêu cầu: Xem chi tiết trong `requirements.txt`

## Hướng dẫn cài đặt và chạy dự án

**1. Thiết lập Cơ sở dữ liệu (Database)**
- Cài đặt và khởi động Apache và MySQL trên **XAMPP**.
- Mở phpMyAdmin (http://localhost/phpmyadmin).
- Tạo một database mới (kiểm tra file db.py để biết tên database bạn đang cấu hình, ví dụ: `shop_db`).
- Import file `qlbmt.sql` có sẵn trong thư mục gốc vào database vừa tạo.

**2. Cài đặt môi trường Python**
```bash
git clone [https://github.com/PhamBao112/Quan-ly-ban-hang-SQL-Python-.git](https://github.com/PhamBao112/Quan-ly-ban-hang-SQL-Python-.git)
cd Quan-ly-ban-hang-SQL-Python-
pip install -r requirements.txt
