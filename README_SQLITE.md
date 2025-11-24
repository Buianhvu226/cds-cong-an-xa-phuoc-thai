# Hướng Dẫn Sử Dụng SQLite

Dự án đã được chuyển sang sử dụng SQLite thay vì Supabase để dễ dàng hơn cho development local.

## Setup

1. **Cài đặt dependencies:**

```bash
pip install -r requirements.txt
```

2. **Khởi tạo database:**

```bash
python init_db.py
```

Script này sẽ:

- Tạo file `database.db` trong thư mục `backend/`
- Tạo tất cả các tables cần thiết
- Thêm dữ liệu mẫu (seed data)

3. **Chạy ứng dụng:**

```bash
python app.py
```

Database sẽ được tạo tự động tại: `backend/database.db`

## Cấu hình

File `.env` không cần thiết nữa, nhưng bạn có thể tùy chỉnh:

```env
# Database path (mặc định: sqlite:///backend/database.db)
DATABASE_URL=sqlite:///path/to/your/database.db

# Flask config
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000
```

## Lợi ích của SQLite

- ✅ Không cần setup server database
- ✅ File database duy nhất, dễ backup
- ✅ Nhanh và nhẹ cho development
- ✅ Dễ dàng migrate sang PostgreSQL sau này (SQLAlchemy hỗ trợ)

## Migration sang PostgreSQL (nếu cần)

Nếu sau này muốn chuyển sang PostgreSQL, chỉ cần thay đổi `DATABASE_URL`:

```env
DATABASE_URL=postgresql://user:password@localhost/dbname
```

Code không cần thay đổi vì đã sử dụng SQLAlchemy ORM.

## Backup Database

Để backup, chỉ cần copy file `database.db`:

```bash
cp backend/database.db backend/database_backup.db
```

## Reset Database

Để reset database về trạng thái ban đầu:

```bash
# Xóa file database
rm backend/database.db

# Chạy lại init script
python init_db.py
```
