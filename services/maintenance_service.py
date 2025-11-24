from database import db
from models import (
    LichSuKiemTraBaoTri,
    DanhSachVuKhiCongCuHoTro,
    DanhSachPhuongTien,
    DanhSachThietBiKyThuatNghiepVu,
    DanhSachThietBiVanPhongDoanhTrai,
    DanhSachTrangThietBiThuy
)
from utils.date_utils import calculate_next_inspection_date
from datetime import datetime, date

class MaintenanceService:
    def __init__(self):
        self.asset_models = [
            DanhSachVuKhiCongCuHoTro,
            DanhSachPhuongTien,
            DanhSachThietBiKyThuatNghiepVu,
            DanhSachThietBiVanPhongDoanhTrai,
            DanhSachTrangThietBiThuy
        ]
        self.cycle_overrides = {
            'danh_sach_trang_thiet_bi_thuy': '6 tháng'
        }
    
    def get_history(self, ma_tai_san):
        """Get maintenance history for an asset"""
        records = LichSuKiemTraBaoTri.query.filter_by(
            ma_tai_san=ma_tai_san
        ).order_by(LichSuKiemTraBaoTri.ngay_thuc_hien.desc()).all()
        
        return [record.to_dict() for record in records]
    
    def create_record(self, data):
        """Create new maintenance record"""
        # Convert date string to date object
        if 'ngay_thuc_hien' in data and isinstance(data['ngay_thuc_hien'], str):
            data['ngay_thuc_hien'] = datetime.fromisoformat(data['ngay_thuc_hien']).date()
        
        record = LichSuKiemTraBaoTri(**data)
        db.session.add(record)
        db.session.commit()
        
        # Auto-update ngay_kiem_tra_gan_nhat in asset table (BR-005)
        if record.ngay_thuc_hien:
            self._update_asset_inspection_date(data['ma_tai_san'], record.ngay_thuc_hien)
        
        return record.to_dict()
    
    def update_record(self, record_id, data):
        """Update maintenance record"""
        record = LichSuKiemTraBaoTri.query.get(record_id)
        if not record:
            return None
        
        # Convert date string to date object
        if 'ngay_thuc_hien' in data and isinstance(data['ngay_thuc_hien'], str):
            data['ngay_thuc_hien'] = datetime.fromisoformat(data['ngay_thuc_hien']).date()
        
        for key, value in data.items():
            if hasattr(record, key):
                setattr(record, key, value)
        
        db.session.commit()
        return record.to_dict()
    
    def delete_record(self, record_id):
        """Delete maintenance record"""
        record = LichSuKiemTraBaoTri.query.get(record_id)
        if not record:
            return None
        
        db.session.delete(record)
        db.session.commit()
        return record.to_dict()
    
    def _update_asset_inspection_date(self, ma_tai_san, ngay_thuc_hien):
        """Update ngay_kiem_tra_gan_nhat in asset tables"""
        for model_class in self.asset_models:
            asset = model_class.query.filter_by(
                ma_tai_san=ma_tai_san,
                is_deleted=False
            ).first()
            
            if asset:
                table_name = asset.__table__.name
                dinh_ky_kiem_tra = getattr(asset, 'dinh_ky_kiem_tra', None)
                if not dinh_ky_kiem_tra and table_name in self.cycle_overrides:
                    dinh_ky_kiem_tra = self.cycle_overrides[table_name]
                
                # Calculate next inspection date
                ngay_kiem_tra_tiep_theo = None
                if dinh_ky_kiem_tra:
                    ngay_str = ngay_thuc_hien.isoformat() if isinstance(ngay_thuc_hien, date) else str(ngay_thuc_hien)
                    ngay_kiem_tra_tiep_theo = calculate_next_inspection_date(ngay_str, dinh_ky_kiem_tra)
                
                # Update asset
                asset.ngay_kiem_tra_gan_nhat = ngay_thuc_hien
                asset.updated_at = datetime.utcnow()
                
                if ngay_kiem_tra_tiep_theo:
                    if isinstance(ngay_kiem_tra_tiep_theo, str):
                        asset.ngay_kiem_tra_tiep_theo = datetime.fromisoformat(ngay_kiem_tra_tiep_theo).date()
                    elif isinstance(ngay_kiem_tra_tiep_theo, date):
                        asset.ngay_kiem_tra_tiep_theo = ngay_kiem_tra_tiep_theo
                
                db.session.commit()
                break
