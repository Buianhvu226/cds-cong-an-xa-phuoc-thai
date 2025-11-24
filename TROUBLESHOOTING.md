# Troubleshooting Guide

## Lỗi 500 khi gọi API

### Lỗi: GET /api/dashboard/stats 500 (INTERNAL SERVER ERROR)

**Nguyên nhân**: Database chưa được khởi tạo hoặc tables chưa tồn tại.

**Giải pháp**:

1. Kiểm tra database đã được khởi tạo chưa:
```bash
python check_db.py
```

2. Nếu chưa, chạy script khởi tạo:
```bash
python init_db.py
```

3. Đảm bảo file `database.db` tồn tại trong thư mục `backend/`

4. Khởi động lại Flask server:
```bash
python app.py
```

### Lỗi: "pie is not a registered controller"

**Nguyên nhân**: Chart.js PieController chưa được import và register.

**Giải pháp**: Đã được sửa trong `frontend/src/components/dashboard/PieChart.vue`. Nếu vẫn gặp lỗi:

1. Xóa `node_modules` và cài lại:
```bash
cd frontend
rm -rf node_modules
npm install
```

2. Khởi động lại dev server:
```bash
npm run dev
```

### Lỗi: Database connection error

**Nguyên nhân**: 
- File database.db không tồn tại
- Quyền truy cập file bị hạn chế
- Database bị corrupt

**Giải pháp**:

1. Xóa file database cũ (nếu có):
```bash
rm backend/database.db
```

2. Chạy lại init script:
```bash
python init_db.py
```

### Lỗi: ModuleNotFoundError

**Nguyên nhân**: Thiếu dependencies.

**Giải pháp**:

1. Cài đặt lại dependencies:
```bash
pip install -r requirements.txt
```

2. Đảm bảo virtual environment đã được kích hoạt.

### Lỗi CORS

**Nguyên nhân**: Frontend và backend chạy trên ports khác nhau.

**Giải pháp**:

1. Kiểm tra `CORS_ORIGINS` trong `.env` hoặc `config.py`
2. Đảm bảo frontend URL được thêm vào danh sách CORS
3. Khởi động lại backend server

## Kiểm tra Database

Để kiểm tra database đã được setup đúng chưa:

```bash
python check_db.py
```

Script này sẽ:
- Kiểm tra các tables đã tồn tại
- Đếm số records trong mỗi table
- Báo lỗi nếu thiếu gì đó

## Reset Database

Nếu muốn reset database về trạng thái ban đầu:

```bash
# Xóa database
rm backend/database.db

# Khởi tạo lại
python init_db.py
```

## Kiểm tra Logs

Nếu gặp lỗi, kiểm tra console logs:

1. **Backend**: Xem output trong terminal chạy `python app.py`
2. **Frontend**: Xem console trong browser (F12)

## Common Issues

### 1. Port đã được sử dụng

**Lỗi**: `Address already in use`

**Giải pháp**: 
- Thay đổi port trong `config.py` hoặc `.env`
- Hoặc kill process đang dùng port đó

### 2. SQLite database locked

**Lỗi**: `database is locked`

**Giải pháp**:
- Đảm bảo chỉ có một instance của Flask app đang chạy
- Kiểm tra xem có process nào đang truy cập database không

### 3. Import errors

**Lỗi**: `ModuleNotFoundError: No module named 'xxx'`

**Giải pháp**:
- Đảm bảo virtual environment đã được kích hoạt
- Chạy `pip install -r requirements.txt`
- Kiểm tra Python path

