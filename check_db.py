"""
Script to check if database is initialized
"""
from app import app, db
from models import (
    DanhSachVuKhiCongCuHoTro,
    DanhSachPhuongTien,
    DanhSachThietBiKyThuatNghiepVu,
    DanhSachThietBiVanPhongDoanhTrai
)

with app.app_context():
    try:
        # Check if tables exist
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        required_tables = [
            'danh_sach_vu_khi_cong_cu_ho_tro',
            'danh_sach_phuong_tien',
            'danh_sach_thiet_bi_ky_thuat_nghiep_vu',
            'danh_sach_thiet_bi_van_phong_doanh_trai'
        ]
        
        missing_tables = [t for t in required_tables if t not in tables]
        
        if missing_tables:
            print(f"❌ Database chưa được khởi tạo!")
            print(f"   Thiếu các tables: {', '.join(missing_tables)}")
            print(f"   Chạy: python init_db.py")
            exit(1)
        else:
            print("✅ Database đã được khởi tạo đầy đủ")
            
            # Check data
            count_weapons = DanhSachVuKhiCongCuHoTro.query.count()
            count_vehicles = DanhSachPhuongTien.query.count()
            count_technical = DanhSachThietBiKyThuatNghiepVu.query.count()
            count_office = DanhSachThietBiVanPhongDoanhTrai.query.count()
            
            print(f"   - Vũ khí: {count_weapons} records")
            print(f"   - Phương tiện: {count_vehicles} records")
            print(f"   - Thiết bị KTNV: {count_technical} records")
            print(f"   - Thiết bị VP-DT: {count_office} records")
            
            if count_weapons + count_vehicles + count_technical + count_office == 0:
                print("⚠️  Database trống, chạy: python init_db.py để thêm dữ liệu mẫu")
    except Exception as e:
        print(f"❌ Lỗi khi kiểm tra database: {str(e)}")
        print(f"   Chạy: python init_db.py để khởi tạo database")
        exit(1)

