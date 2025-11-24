"""
Script to seed sample data into database
Run this after database tables are created (via Flask-Migrate or init_db.py)
"""
from flask import Flask
from config import Config
from database import db
from models import (
    DanhSachVuKhiCongCuHoTro,
    DanhSachPhuongTien,
    DanhSachThietBiKyThuatNghiepVu,
    DanhSachThietBiVanPhongDoanhTrai,
    DanhSachTrangThietBiThuy
)
from datetime import date

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def seed_data():
    """Seed sample data"""
    with app.app_context():
        # Check if data already exists
        total_count = (
            DanhSachVuKhiCongCuHoTro.query.count() +
            DanhSachPhuongTien.query.count() +
            DanhSachThietBiKyThuatNghiepVu.query.count() +
            DanhSachThietBiVanPhongDoanhTrai.query.count() +
            DanhSachTrangThietBiThuy.query.count()
        )
        if total_count > 0:
            print(f"⚠ Data already exists ({total_count} records).")
            print("   Will skip records that already exist (based on ma_tai_san).")
        
        added_count = 0
        skipped_count = 0
        
        # Seed weapons
        weapons_data = [
            {
                'ma_tai_san': 'VK2511001',
                'ma_danh_muc': 'Súng',
                'ten_tai_san': 'Súng AKM báng gấp',
                'don_vi_tinh': 'Khẩu',
                'nam_su_dung': 2016,
                'so_luong': 1,
                'nguyen_gia': 9481024,
                'gia_tri_con_lai': 9481024,
                'so_hieu': '141759',
                'loai_tai_san': 'Đặc biệt',
                'thuc_te_ban_giao': 'Có',
                'dinh_ky_kiem_tra': '6 tháng',
                'ngay_kiem_tra_gan_nhat': date(2025, 6, 1),
                'ngay_kiem_tra_tiep_theo': date(2025, 12, 1),
                'ket_qua_kiem_tra': 'Đạt',
                'phuong_thuc_xu_ly': 'Tiếp tục sử dụng'
            },
            {
                'ma_tai_san': 'VK2511002',
                'ma_danh_muc': 'Công cụ hỗ trợ',
                'ten_tai_san': 'Gậy điện tử 3 khúc Titan M3',
                'don_vi_tinh': 'Chiếc',
                'nam_su_dung': 2020,
                'so_luong': 1,
                'nguyen_gia': 1700000,
                'gia_tri_con_lai': 1700000,
                'so_hieu': 'TB-TT79 0320-3648',
                'loai_tai_san': 'Chuyên dụng',
                'thuc_te_ban_giao': 'Có',
                'dinh_ky_kiem_tra': '6 tháng',
                'ngay_kiem_tra_gan_nhat': date(2025, 5, 15),
                'ngay_kiem_tra_tiep_theo': date(2025, 11, 15),
                'ket_qua_kiem_tra': 'Đạt',
                'phuong_thuc_xu_ly': 'Tiếp tục sử dụng'
            },
            {
                'ma_tai_san': 'VK2511003',
                'ma_danh_muc': 'Đạn',
                'ten_tai_san': 'Đạn 7.62x39mm',
                'don_vi_tinh': 'Viên',
                'nam_su_dung': 2023,
                'so_luong': 1000,
                'nguyen_gia': 5000000,
                'gia_tri_con_lai': 5000000,
                'so_hieu': 'DAN-001',
                'loai_tai_san': 'Đặc biệt',
                'thuc_te_ban_giao': 'Có',
                'dinh_ky_kiem_tra': '1 tháng',
                'ngay_kiem_tra_gan_nhat': date(2025, 7, 1),
                'ngay_kiem_tra_tiep_theo': date(2025, 8, 1),
                'ket_qua_kiem_tra': 'Đạt',
                'phuong_thuc_xu_ly': 'Tiếp tục sử dụng'
            }
        ]
        
        for data in weapons_data:
            # Check if already exists
            existing = DanhSachVuKhiCongCuHoTro.query.filter_by(ma_tai_san=data['ma_tai_san']).first()
            if existing:
                skipped_count += 1
                continue
            weapon = DanhSachVuKhiCongCuHoTro(**data)
            db.session.add(weapon)
            added_count += 1
        
        # Seed vehicles
        vehicles_data = [
            {
                'ma_tai_san': 'PT2511001',
                'danh_muc_phuong_tien': 'Ô tô',
                'ten_phuong_tien': 'Suzuki Carry/Vandao-ANTT 1.5 xăng 4x2 (Indonesia)',
                'don_vi_tinh': 'Chiếc',
                'nguyen_gia': 378800000,
                'so_luong': 1,
                'bien_so_ky_hieu': '60A-009.87',
                'so_khung_so_than_vo': 'MHYHDC61TMJ912829',
                'so_may': 'K15BT1297661',
                'nam_trang_bi': 2024,
                'loai_tai_san': 'Chuyên dụng',
                'thuc_te_ban_giao': 'Có',
                'ngay_dang_kiem': date(2025, 10, 1),
                'ngay_thay_nhot': date(2025, 8, 15),
                'ngay_thay_vo': date(2025, 7, 1),
                'dinh_ky_kiem_tra': '3 tháng',
                'ngay_kiem_tra_gan_nhat': date(2025, 8, 15),
                'ngay_kiem_tra_tiep_theo': date(2025, 11, 15),
                'ket_qua_kiem_tra': 'Đạt',
                'phuong_thuc_xu_ly': 'Tiếp tục sử dụng'
            },
            {
                'ma_tai_san': 'PT2511002',
                'danh_muc_phuong_tien': 'Moto',
                'ten_phuong_tien': 'Honda WaveS 110 (CA xã)',
                'don_vi_tinh': 'Chiếc',
                'nguyen_gia': 18700000,
                'so_luong': 1,
                'bien_so_ky_hieu': '60C1-000.13',
                'so_khung_so_than_vo': '002738',
                'so_may': '1030054',
                'nam_trang_bi': 2013,
                'loai_tai_san': 'Quản lý',
                'thuc_te_ban_giao': 'Có',
                'ngay_dang_kiem': date(2025, 9, 1),
                'ngay_thay_nhot': date(2025, 7, 1),
                'ngay_thay_vo': date(2025, 6, 1),
                'dinh_ky_kiem_tra': '3 tháng',
                'ngay_kiem_tra_gan_nhat': date(2025, 7, 1),
                'ngay_kiem_tra_tiep_theo': date(2025, 10, 1),
                'ket_qua_kiem_tra': 'Đạt',
                'phuong_thuc_xu_ly': 'Tiếp tục sử dụng'
            },
            {
                'ma_tai_san': 'PT2511003',
                'danh_muc_phuong_tien': 'Moto',
                'ten_phuong_tien': 'Honda Future FI 125cc CAX',
                'don_vi_tinh': 'Chiếc',
                'nguyen_gia': 30690000,
                'so_luong': 1,
                'bien_so_ky_hieu': '60B1-003.22',
                'so_khung_so_than_vo': 'RLHJC7643LY010607',
                'so_may': 'JC90E-0041083',
                'nam_trang_bi': 2020,
                'loai_tai_san': 'Quản lý',
                'thuc_te_ban_giao': 'Có',
                'ngay_dang_kiem': date(2025, 8, 1),
                'ngay_thay_nhot': date(2025, 6, 15),
                'ngay_thay_vo': date(2025, 5, 1),
                'dinh_ky_kiem_tra': '3 tháng',
                'ngay_kiem_tra_gan_nhat': date(2025, 6, 15),
                'ngay_kiem_tra_tiep_theo': date(2025, 9, 15),
                'ket_qua_kiem_tra': 'Đạt',
                'phuong_thuc_xu_ly': 'Tiếp tục sử dụng'
            }
        ]
        
        for data in vehicles_data:
            # Check if already exists
            existing = DanhSachPhuongTien.query.filter_by(ma_tai_san=data['ma_tai_san']).first()
            if existing:
                skipped_count += 1
                continue
            vehicle = DanhSachPhuongTien(**data)
            db.session.add(vehicle)
            added_count += 1
        
        # Seed water equipment
        water_data = [
            {
                'ma_tai_san': 'TT2511001',
                'danh_muc_trang_thiet_bi': 'Phao áo',
                'ten_trang_bi': 'Phao áo cứu sinh tiêu chuẩn',
                'don_vi_tinh': 'Chiếc',
                'nguyen_gia': 500000,
                'so_luong': 10,
                'ma_hieu': 'PA-001',
                'nam_trang_bi': 2023,
                'loai_tai_san': 'Chuyên dụng',
                'ngay_kiem_tra_gan_nhat': date(2025, 6, 1),
                'ngay_kiem_tra_tiep_theo': date(2025, 12, 1),
                'ket_qua_kiem_tra': 'Đạt',
                'nam_het_han': 2026,
                'phuong_thuc_xu_ly': 'Tiếp tục sử dụng'
            },
            {
                'ma_tai_san': 'TT2511002',
                'danh_muc_trang_thiet_bi': 'Phao tròn',
                'ten_trang_bi': 'Phao tròn cứu sinh đường kính 50cm',
                'don_vi_tinh': 'Cái',
                'nguyen_gia': 800000,
                'so_luong': 5,
                'ma_hieu': 'PT-001',
                'nam_trang_bi': 2022,
                'loai_tai_san': 'Chuyên dụng',
                'ngay_kiem_tra_gan_nhat': date(2025, 5, 15),
                'ngay_kiem_tra_tiep_theo': date(2025, 11, 15),
                'ket_qua_kiem_tra': 'Đạt',
                'nam_het_han': 2027,
                'phuong_thuc_xu_ly': 'Tiếp tục sử dụng'
            },
            {
                'ma_tai_san': 'TT2511003',
                'danh_muc_trang_thiet_bi': 'Phao cứu sinh',
                'ten_trang_bi': 'Phao cứu sinh tự động',
                'don_vi_tinh': 'Chiếc',
                'nguyen_gia': 1200000,
                'so_luong': 8,
                'ma_hieu': 'PC-001',
                'nam_trang_bi': 2024,
                'loai_tai_san': 'Chuyên dụng',
                'ngay_kiem_tra_gan_nhat': date(2025, 7, 1),
                'ngay_kiem_tra_tiep_theo': date(2026, 1, 1),
                'ket_qua_kiem_tra': 'Đạt',
                'nam_het_han': 2028,
                'phuong_thuc_xu_ly': 'Tiếp tục sử dụng'
            }
        ]
        
        for data in water_data:
            # Check if already exists
            existing = DanhSachTrangThietBiThuy.query.filter_by(ma_tai_san=data['ma_tai_san']).first()
            if existing:
                skipped_count += 1
                continue
            water = DanhSachTrangThietBiThuy(**data)
            db.session.add(water)
            added_count += 1
        
        # Seed technical equipment
        technical_data = [
            {
                'ma_tai_san': 'TB2511001',
                'ten_tai_san': 'Máy tính để bàn Dell OptiPlex 7090',
                'nam_su_dung': 2021,
                'so_luong': 5,
                'nguyen_gia': 15000000,
                'gia_tri_con_lai': 9000000,
                'loai_tai_san': 'Quản lý',
                'thuc_te_ban_giao': 'Có',
                'dinh_ky_kiem_tra': '6 tháng',
                'ngay_kiem_tra_gan_nhat': date(2025, 6, 1),
                'ngay_kiem_tra_tiep_theo': date(2025, 12, 1),
                'ket_qua_kiem_tra': 'Đạt',
                'nam_het_han': 2026,
                'phuong_thuc_xu_ly': 'Tiếp tục sử dụng'
            },
            {
                'ma_tai_san': 'TB2511002',
                'ten_tai_san': 'Máy in HP LaserJet Pro M404dn',
                'nam_su_dung': 2020,
                'so_luong': 2,
                'nguyen_gia': 8000000,
                'gia_tri_con_lai': 4000000,
                'loai_tai_san': 'Quản lý',
                'thuc_te_ban_giao': 'Có',
                'dinh_ky_kiem_tra': '6 tháng',
                'ngay_kiem_tra_gan_nhat': date(2025, 5, 15),
                'ngay_kiem_tra_tiep_theo': date(2025, 11, 15),
                'ket_qua_kiem_tra': 'Đạt',
                'nam_het_han': 2027,
                'phuong_thuc_xu_ly': 'Tiếp tục sử dụng'
            },
            {
                'ma_tai_san': 'TB2511003',
                'ten_tai_san': 'Camera giám sát Hikvision DS-2CD2T47G1-L',
                'nam_su_dung': 2022,
                'so_luong': 8,
                'nguyen_gia': 5000000,
                'gia_tri_con_lai': 3500000,
                'loai_tai_san': 'Chuyên dụng',
                'thuc_te_ban_giao': 'Có',
                'dinh_ky_kiem_tra': '6 tháng',
                'ngay_kiem_tra_gan_nhat': date(2025, 7, 1),
                'ngay_kiem_tra_tiep_theo': date(2026, 1, 1),
                'ket_qua_kiem_tra': 'Đạt',
                'nam_het_han': 2028,
                'phuong_thuc_xu_ly': 'Tiếp tục sử dụng'
            },
            {
                'ma_tai_san': 'TB2511004',
                'ten_tai_san': 'Máy quét vân tay ZKTeco K40',
                'nam_su_dung': 2023,
                'so_luong': 3,
                'nguyen_gia': 12000000,
                'gia_tri_con_lai': 10000000,
                'loai_tai_san': 'Chuyên dụng',
                'thuc_te_ban_giao': 'Có',
                'dinh_ky_kiem_tra': '6 tháng',
                'ngay_kiem_tra_gan_nhat': date(2025, 6, 20),
                'ngay_kiem_tra_tiep_theo': date(2025, 12, 20),
                'ket_qua_kiem_tra': 'Đạt',
                'nam_het_han': 2029,
                'phuong_thuc_xu_ly': 'Tiếp tục sử dụng'
            }
        ]
        
        for data in technical_data:
            # Check if already exists
            existing = DanhSachThietBiKyThuatNghiepVu.query.filter_by(ma_tai_san=data['ma_tai_san']).first()
            if existing:
                skipped_count += 1
                continue
            technical = DanhSachThietBiKyThuatNghiepVu(**data)
            db.session.add(technical)
            added_count += 1
        
        # Seed office equipment
        office_data = [
            {
                'ma_tai_san': 'VP2511001',
                'ten_tai_san': 'Bàn làm việc văn phòng',
                'nam_su_dung': 2020,
                'so_luong': 10,
                'nguyen_gia': 3000000,
                'gia_tri_con_lai': 1500000,
                'loai_tai_san': 'Quản lý',
                'thuc_te_ban_giao': 'Có',
                'hinh_thuc': 'Mua mới',
                'su_kien': 'Sửa chữa',
                'chi_phi': 500000,
                'dinh_ky_kiem_tra': '6 tháng',
                'ngay_kiem_tra_gan_nhat': date(2025, 6, 1),
                'ngay_kiem_tra_tiep_theo': date(2025, 12, 1),
                'ket_qua_kiem_tra': 'Đạt',
                'nam_het_han': 2026,
                'phuong_thuc_xu_ly': 'Tiếp tục sử dụng'
            },
            {
                'ma_tai_san': 'VP2511002',
                'ten_tai_san': 'Ghế xoay văn phòng',
                'nam_su_dung': 2021,
                'so_luong': 15,
                'nguyen_gia': 2000000,
                'gia_tri_con_lai': 1200000,
                'loai_tai_san': 'Quản lý',
                'thuc_te_ban_giao': 'Có',
                'hinh_thuc': 'Mua mới',
                'su_kien': None,
                'chi_phi': None,
                'dinh_ky_kiem_tra': '6 tháng',
                'ngay_kiem_tra_gan_nhat': date(2025, 5, 15),
                'ngay_kiem_tra_tiep_theo': date(2025, 11, 15),
                'ket_qua_kiem_tra': 'Đạt',
                'nam_het_han': 2027,
                'phuong_thuc_xu_ly': 'Tiếp tục sử dụng'
            },
            {
                'ma_tai_san': 'VP2511003',
                'ten_tai_san': 'Tủ đựng hồ sơ 4 ngăn',
                'nam_su_dung': 2019,
                'so_luong': 5,
                'nguyen_gia': 4000000,
                'gia_tri_con_lai': 2000000,
                'loai_tai_san': 'Quản lý',
                'thuc_te_ban_giao': 'Có',
                'hinh_thuc': 'Bàn giao',
                'su_kien': 'Tu bổ',
                'chi_phi': 800000,
                'dinh_ky_kiem_tra': '6 tháng',
                'ngay_kiem_tra_gan_nhat': date(2025, 7, 1),
                'ngay_kiem_tra_tiep_theo': date(2026, 1, 1),
                'ket_qua_kiem_tra': 'Đạt',
                'nam_het_han': 2028,
                'phuong_thuc_xu_ly': 'Tiếp tục sử dụng'
            },
            {
                'ma_tai_san': 'VP2511004',
                'ten_tai_san': 'Máy lạnh Daikin 1.5HP',
                'nam_su_dung': 2022,
                'so_luong': 3,
                'nguyen_gia': 18000000,
                'gia_tri_con_lai': 14000000,
                'loai_tai_san': 'Quản lý',
                'thuc_te_ban_giao': 'Có',
                'hinh_thuc': 'Mua mới',
                'su_kien': 'Cải tạo/nâng cấp',
                'chi_phi': 2000000,
                'dinh_ky_kiem_tra': '6 tháng',
                'ngay_kiem_tra_gan_nhat': date(2025, 6, 20),
                'ngay_kiem_tra_tiep_theo': date(2025, 12, 20),
                'ket_qua_kiem_tra': 'Đạt',
                'nam_het_han': 2029,
                'phuong_thuc_xu_ly': 'Tiếp tục sử dụng'
            }
        ]
        
        for data in office_data:
            # Check if already exists
            existing = DanhSachThietBiVanPhongDoanhTrai.query.filter_by(ma_tai_san=data['ma_tai_san']).first()
            if existing:
                skipped_count += 1
                continue
            office = DanhSachThietBiVanPhongDoanhTrai(**data)
            db.session.add(office)
            added_count += 1
        
        try:
            db.session.commit()
            
            # Print summary
            print("\n✓ Seed data completed!")
            print(f"   - Added: {added_count} new records")
            if skipped_count > 0:
                print(f"   - Skipped: {skipped_count} existing records (already in database)")
            print(f"\n   Breakdown:")
            print(f"   - Vũ khí, VLN, CCHT: {len(weapons_data)} records")
            print(f"   - Phương tiện: {len(vehicles_data)} records")
            print(f"   - Trang thiết bị thủy: {len(water_data)} records")
            print(f"   - Thiết bị KTNV: {len(technical_data)} records")
            print(f"   - Thiết bị VP & DT: {len(office_data)} records")
            total = len(weapons_data) + len(vehicles_data) + len(water_data) + len(technical_data) + len(office_data)
            print(f"   - Total available: {total} records")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error inserting data: {str(e)}")
            raise

if __name__ == '__main__':
    print("Seeding sample data...")
    seed_data()
    print("\n✓ Done!")

