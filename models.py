from database import db
from datetime import datetime
import uuid as uuid_lib

class BaseModel(db.Model):
    """Base model with common fields"""
    __abstract__ = True
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid_lib.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)

class DanhSachVuKhiCongCuHoTro(BaseModel):
    __tablename__ = 'danh_sach_vu_khi_cong_cu_ho_tro'
    
    ma_tai_san = db.Column(db.String(50), unique=True, nullable=False)
    ma_danh_muc = db.Column(db.String(20), nullable=False)
    ten_tai_san = db.Column(db.String(255), nullable=False)
    don_vi_tinh = db.Column(db.String(20), nullable=False)
    nam_su_dung = db.Column(db.Integer)
    so_luong = db.Column(db.Integer, nullable=False, default=1)
    nguyen_gia = db.Column(db.Numeric(15, 0))
    gia_tri_con_lai = db.Column(db.Numeric(15, 0))
    so_hieu = db.Column(db.String(100))
    loai_tai_san = db.Column(db.String(50))
    thuc_te_ban_giao = db.Column(db.String(10))
    dinh_ky_kiem_tra = db.Column(db.String(20))
    vi_tri_tai_san = db.Column(db.String(100))
    nguoi_su_dung = db.Column(db.String(100))
    ngay_kiem_tra_gan_nhat = db.Column(db.Date)
    ngay_kiem_tra_tiep_theo = db.Column(db.Date)
    ket_qua_kiem_tra = db.Column(db.String(20))
    nam_het_han = db.Column(db.Integer)
    phuong_thuc_xu_ly = db.Column(db.String(50))
    ghi_chu = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'ma_tai_san': self.ma_tai_san,
            'ma_danh_muc': self.ma_danh_muc,
            'ten_tai_san': self.ten_tai_san,
            'don_vi_tinh': self.don_vi_tinh,
            'nam_su_dung': self.nam_su_dung,
            'so_luong': self.so_luong,
            'nguyen_gia': float(self.nguyen_gia) if self.nguyen_gia else None,
            'gia_tri_con_lai': float(self.gia_tri_con_lai) if self.gia_tri_con_lai else None,
            'so_hieu': self.so_hieu,
            'loai_tai_san': self.loai_tai_san,
            'thuc_te_ban_giao': self.thuc_te_ban_giao,
            'dinh_ky_kiem_tra': self.dinh_ky_kiem_tra,
            'vi_tri_tai_san': self.vi_tri_tai_san,
            'nguoi_su_dung': self.nguoi_su_dung,
            'ngay_kiem_tra_gan_nhat': self.ngay_kiem_tra_gan_nhat.isoformat() if self.ngay_kiem_tra_gan_nhat else None,
            'ngay_kiem_tra_tiep_theo': self.ngay_kiem_tra_tiep_theo.isoformat() if self.ngay_kiem_tra_tiep_theo else None,
            'ket_qua_kiem_tra': self.ket_qua_kiem_tra,
            'nam_het_han': self.nam_het_han,
            'phuong_thuc_xu_ly': self.phuong_thuc_xu_ly,
            'ghi_chu': self.ghi_chu,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_deleted': self.is_deleted
        }

class DanhSachPhuongTien(BaseModel):
    __tablename__ = 'danh_sach_phuong_tien'
    
    ma_tai_san = db.Column(db.String(50), unique=True, nullable=False)
    danh_muc_phuong_tien = db.Column(db.String(50), nullable=False)
    ten_phuong_tien = db.Column(db.String(255), nullable=False)
    don_vi_tinh = db.Column(db.String(20), nullable=False)
    nguyen_gia = db.Column(db.Numeric(15, 0))
    so_luong = db.Column(db.Integer, nullable=False, default=1)
    bien_so_ky_hieu = db.Column(db.String(50))
    so_khung_so_than_vo = db.Column(db.String(100))
    so_may = db.Column(db.String(100))
    nam_trang_bi = db.Column(db.Integer)
    loai_tai_san = db.Column(db.String(50))
    thuc_te_ban_giao = db.Column(db.String(10))
    ngay_dang_kiem = db.Column(db.Date)
    ngay_thay_nhot = db.Column(db.Date)
    ngay_thay_vo = db.Column(db.Date)
    sua_chua = db.Column(db.Text)
    phi_duong_bo = db.Column(db.Text)
    nam_het_han = db.Column(db.Integer)
    phuong_thuc_xu_ly = db.Column(db.String(50))
    dinh_ky_kiem_tra = db.Column(db.String(20))
    ngay_kiem_tra_gan_nhat = db.Column(db.Date)
    ngay_kiem_tra_tiep_theo = db.Column(db.Date)
    ket_qua_kiem_tra = db.Column(db.String(20))
    ghi_chu = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'ma_tai_san': self.ma_tai_san,
            'danh_muc_phuong_tien': self.danh_muc_phuong_tien,
            'ten_phuong_tien': self.ten_phuong_tien,
            'don_vi_tinh': self.don_vi_tinh,
            'nguyen_gia': float(self.nguyen_gia) if self.nguyen_gia else None,
            'so_luong': self.so_luong,
            'bien_so_ky_hieu': self.bien_so_ky_hieu,
            'so_khung_so_than_vo': self.so_khung_so_than_vo,
            'so_may': self.so_may,
            'nam_trang_bi': self.nam_trang_bi,
            'loai_tai_san': self.loai_tai_san,
            'thuc_te_ban_giao': self.thuc_te_ban_giao,
            'ngay_dang_kiem': self.ngay_dang_kiem.isoformat() if self.ngay_dang_kiem else None,
            'ngay_thay_nhot': self.ngay_thay_nhot.isoformat() if self.ngay_thay_nhot else None,
            'ngay_thay_vo': self.ngay_thay_vo.isoformat() if self.ngay_thay_vo else None,
            'sua_chua': self.sua_chua,
            'phi_duong_bo': self.phi_duong_bo,
            'nam_het_han': self.nam_het_han,
            'phuong_thuc_xu_ly': self.phuong_thuc_xu_ly,
            'dinh_ky_kiem_tra': self.dinh_ky_kiem_tra,
            'ngay_kiem_tra_gan_nhat': self.ngay_kiem_tra_gan_nhat.isoformat() if self.ngay_kiem_tra_gan_nhat else None,
            'ngay_kiem_tra_tiep_theo': self.ngay_kiem_tra_tiep_theo.isoformat() if self.ngay_kiem_tra_tiep_theo else None,
            'ket_qua_kiem_tra': self.ket_qua_kiem_tra,
            'ghi_chu': self.ghi_chu,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_deleted': self.is_deleted
        }

class DanhSachThietBiKyThuatNghiepVu(BaseModel):
    __tablename__ = 'danh_sach_thiet_bi_ky_thuat_nghiep_vu'
    
    ma_tai_san = db.Column(db.String(50), unique=True, nullable=False)
    ten_tai_san = db.Column(db.String(255), nullable=False)
    nam_su_dung = db.Column(db.Integer)
    so_luong = db.Column(db.Integer, nullable=False)
    nguyen_gia = db.Column(db.Numeric(15, 0))
    gia_tri_con_lai = db.Column(db.Numeric(15, 0))
    loai_tai_san = db.Column(db.String(50))
    thuc_te_ban_giao = db.Column(db.String(10))
    dinh_ky_kiem_tra = db.Column(db.String(20))
    ngay_kiem_tra_gan_nhat = db.Column(db.Date)
    ngay_kiem_tra_tiep_theo = db.Column(db.Date)
    ket_qua_kiem_tra = db.Column(db.String(20))
    nam_het_han = db.Column(db.Integer)
    phuong_thuc_xu_ly = db.Column(db.String(50))
    ghi_chu = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'ma_tai_san': self.ma_tai_san,
            'ten_tai_san': self.ten_tai_san,
            'nam_su_dung': self.nam_su_dung,
            'so_luong': self.so_luong,
            'nguyen_gia': float(self.nguyen_gia) if self.nguyen_gia else None,
            'gia_tri_con_lai': float(self.gia_tri_con_lai) if self.gia_tri_con_lai else None,
            'loai_tai_san': self.loai_tai_san,
            'thuc_te_ban_giao': self.thuc_te_ban_giao,
            'dinh_ky_kiem_tra': self.dinh_ky_kiem_tra,
            'ngay_kiem_tra_gan_nhat': self.ngay_kiem_tra_gan_nhat.isoformat() if self.ngay_kiem_tra_gan_nhat else None,
            'ngay_kiem_tra_tiep_theo': self.ngay_kiem_tra_tiep_theo.isoformat() if self.ngay_kiem_tra_tiep_theo else None,
            'ket_qua_kiem_tra': self.ket_qua_kiem_tra,
            'nam_het_han': self.nam_het_han,
            'phuong_thuc_xu_ly': self.phuong_thuc_xu_ly,
            'ghi_chu': self.ghi_chu,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_deleted': self.is_deleted
        }

class DanhSachThietBiVanPhongDoanhTrai(BaseModel):
    __tablename__ = 'danh_sach_thiet_bi_van_phong_doanh_trai'
    
    ma_tai_san = db.Column(db.String(50), unique=True, nullable=False)
    ten_tai_san = db.Column(db.String(255), nullable=False)
    nam_su_dung = db.Column(db.Integer)
    so_luong = db.Column(db.Integer, nullable=False)
    nguyen_gia = db.Column(db.Numeric(15, 0))
    gia_tri_con_lai = db.Column(db.Numeric(15, 0))
    loai_tai_san = db.Column(db.String(50))
    thuc_te_ban_giao = db.Column(db.String(10))
    hinh_thuc = db.Column(db.String(50))
    su_kien = db.Column(db.String(50))
    chi_phi = db.Column(db.Numeric(15, 0))
    dinh_ky_kiem_tra = db.Column(db.String(20))
    ngay_kiem_tra_gan_nhat = db.Column(db.Date)
    ngay_kiem_tra_tiep_theo = db.Column(db.Date)
    ket_qua_kiem_tra = db.Column(db.String(20))
    nam_het_han = db.Column(db.Integer)
    phuong_thuc_xu_ly = db.Column(db.String(50))
    ghi_chu = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'ma_tai_san': self.ma_tai_san,
            'ten_tai_san': self.ten_tai_san,
            'nam_su_dung': self.nam_su_dung,
            'so_luong': self.so_luong,
            'nguyen_gia': float(self.nguyen_gia) if self.nguyen_gia else None,
            'gia_tri_con_lai': float(self.gia_tri_con_lai) if self.gia_tri_con_lai else None,
            'loai_tai_san': self.loai_tai_san,
            'thuc_te_ban_giao': self.thuc_te_ban_giao,
            'hinh_thuc': self.hinh_thuc,
            'su_kien': self.su_kien,
            'chi_phi': float(self.chi_phi) if self.chi_phi else None,
            'dinh_ky_kiem_tra': self.dinh_ky_kiem_tra,
            'ngay_kiem_tra_gan_nhat': self.ngay_kiem_tra_gan_nhat.isoformat() if self.ngay_kiem_tra_gan_nhat else None,
            'ngay_kiem_tra_tiep_theo': self.ngay_kiem_tra_tiep_theo.isoformat() if self.ngay_kiem_tra_tiep_theo else None,
            'ket_qua_kiem_tra': self.ket_qua_kiem_tra,
            'nam_het_han': self.nam_het_han,
            'phuong_thuc_xu_ly': self.phuong_thuc_xu_ly,
            'ghi_chu': self.ghi_chu,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_deleted': self.is_deleted
        }

class LichSuKiemTraBaoTri(db.Model):
    __tablename__ = 'lich_su_kiem_tra_bao_tri'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid_lib.uuid4()))
    ma_tai_san = db.Column(db.String(50), nullable=False)
    loai_hinh = db.Column(db.String(50), nullable=False)
    ngay_thuc_hien = db.Column(db.Date, nullable=False)
    nguoi_thuc_hien = db.Column(db.String(100))
    chi_tiet_cong_viec = db.Column(db.Text)
    chi_phi = db.Column(db.Numeric(15, 0))
    ket_qua = db.Column(db.String(20))
    ghi_chu = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'ma_tai_san': self.ma_tai_san,
            'loai_hinh': self.loai_hinh,
            'ngay_thuc_hien': self.ngay_thuc_hien.isoformat() if self.ngay_thuc_hien else None,
            'nguoi_thuc_hien': self.nguoi_thuc_hien,
            'chi_tiet_cong_viec': self.chi_tiet_cong_viec,
            'chi_phi': float(self.chi_phi) if self.chi_phi else None,
            'ket_qua': self.ket_qua,
            'ghi_chu': self.ghi_chu,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class DanhSachTrangThietBiThuy(BaseModel):
    __tablename__ = 'danh_sach_trang_thiet_bi_thuy'
    
    ma_tai_san = db.Column(db.String(50), unique=True, nullable=False)
    danh_muc_trang_thiet_bi = db.Column(db.String(50), nullable=False)
    ten_trang_bi = db.Column(db.String(255), nullable=False)
    don_vi_tinh = db.Column(db.String(20), nullable=False)
    nguyen_gia = db.Column(db.Numeric(15, 0))
    so_luong = db.Column(db.Integer, nullable=False, default=1)
    ma_hieu = db.Column(db.String(100))
    nam_trang_bi = db.Column(db.Integer)
    loai_tai_san = db.Column(db.String(50))
    ngay_kiem_tra_gan_nhat = db.Column(db.Date)
    ngay_kiem_tra_tiep_theo = db.Column(db.Date)
    ket_qua_kiem_tra = db.Column(db.String(20))
    nam_het_han = db.Column(db.Integer)
    phuong_thuc_xu_ly = db.Column(db.String(50))
    ghi_chu = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'ma_tai_san': self.ma_tai_san,
            'danh_muc_trang_thiet_bi': self.danh_muc_trang_thiet_bi,
            'ten_trang_bi': self.ten_trang_bi,
            'don_vi_tinh': self.don_vi_tinh,
            'nguyen_gia': float(self.nguyen_gia) if self.nguyen_gia else None,
            'so_luong': self.so_luong,
            'ma_hieu': self.ma_hieu,
            'nam_trang_bi': self.nam_trang_bi,
            'loai_tai_san': self.loai_tai_san,
            'ngay_kiem_tra_gan_nhat': self.ngay_kiem_tra_gan_nhat.isoformat() if self.ngay_kiem_tra_gan_nhat else None,
            'ngay_kiem_tra_tiep_theo': self.ngay_kiem_tra_tiep_theo.isoformat() if self.ngay_kiem_tra_tiep_theo else None,
            'ket_qua_kiem_tra': self.ket_qua_kiem_tra,
            'nam_het_han': self.nam_het_han,
            'phuong_thuc_xu_ly': self.phuong_thuc_xu_ly,
            'ghi_chu': self.ghi_chu,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_deleted': self.is_deleted
        }

class DanhMucLoaiTaiSan(db.Model):
    __tablename__ = 'danh_muc_loai_tai_san'
    
    ma_danh_muc = db.Column(db.String(20), primary_key=True)
    ten_danh_muc = db.Column(db.String(100), nullable=False)
    loai_tai_san_chinh = db.Column(db.String(50), nullable=False)
    mo_ta = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'ma_danh_muc': self.ma_danh_muc,
            'ten_danh_muc': self.ten_danh_muc,
            'loai_tai_san_chinh': self.loai_tai_san_chinh,
            'mo_ta': self.mo_ta
        }

class User(BaseModel):
    __tablename__ = 'users'
    
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='chuyen_vien')  # admin hoặc chuyen_vien
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def is_admin(self):
        return self.role == 'admin'


# ==================== PHASE 2: QUẢN LÝ TIN BÁO & VỤ ÁN ====================

class TinBao(BaseModel):
    """Tin báo đang hiện hành"""
    __tablename__ = 'tin_bao'
    
    stt = db.Column(db.Integer, nullable=False, unique=True)
    dieu_luat = db.Column(db.String(255), nullable=False)
    ten_nguon_tin = db.Column(db.String(255))
    ngay_xay_ra = db.Column(db.Date, nullable=False)
    noi_xay_ra = db.Column(db.Text, nullable=False)
    noi_dung_nguon_tin = db.Column(db.Text, nullable=False)
    so_qd_phan_cong_ptt = db.Column(db.String(100))
    so_qd_phan_cong_dtv = db.Column(db.String(100))
    ngay_phan_cong = db.Column(db.Date)
    ket_qua_giai_quyet = db.Column(db.String(50))
    dia_chi_bi_hai = db.Column(db.Text)
    thong_tin_doi_tuong = db.Column(db.Text)
    cong_an_phu_trach = db.Column(db.String(100))
    don_vi = db.Column(db.String(100), default='CAX Phước Thái')
    kiem_sat_vien = db.Column(db.String(100))
    gia_han = db.Column(db.Integer, default=0)
    ngay_het_han = db.Column(db.Date)
    tinh_trang_ho_so = db.Column(db.String(100))
    ghi_chu = db.Column(db.Text)
    trang_thai = db.Column(db.String(50), nullable=False, default='Tiếp nhận')
    vu_an_id = db.Column(db.String(36), db.ForeignKey('vu_an.id', ondelete='SET NULL'), nullable=True)
    
    # Relationship
    vu_an = db.relationship('VuAn', backref='tin_bao_list', foreign_keys=[vu_an_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'stt': self.stt,
            'dieu_luat': self.dieu_luat,
            'ten_nguon_tin': self.ten_nguon_tin,
            'ngay_xay_ra': self.ngay_xay_ra.isoformat() if self.ngay_xay_ra else None,
            'noi_xay_ra': self.noi_xay_ra,
            'noi_dung_nguon_tin': self.noi_dung_nguon_tin,
            'so_qd_phan_cong_ptt': self.so_qd_phan_cong_ptt,
            'so_qd_phan_cong_dtv': self.so_qd_phan_cong_dtv,
            'ngay_phan_cong': self.ngay_phan_cong.isoformat() if self.ngay_phan_cong else None,
            'ket_qua_giai_quyet': self.ket_qua_giai_quyet,
            'dia_chi_bi_hai': self.dia_chi_bi_hai,
            'thong_tin_doi_tuong': self.thong_tin_doi_tuong,
            'cong_an_phu_trach': self.cong_an_phu_trach,
            'don_vi': self.don_vi,
            'kiem_sat_vien': self.kiem_sat_vien,
            'gia_han': self.gia_han,
            'ngay_het_han': self.ngay_het_han.isoformat() if self.ngay_het_han else None,
            'tinh_trang_ho_so': self.tinh_trang_ho_so,
            'ghi_chu': self.ghi_chu,
            'trang_thai': self.trang_thai,
            'vu_an_id': self.vu_an_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class VuAn(BaseModel):
    """Vụ án đang được điều tra"""
    __tablename__ = 'vu_an'
    
    stt = db.Column(db.Integer, nullable=False, unique=True)
    tin_bao_id = db.Column(db.String(36), db.ForeignKey('tin_bao.id', ondelete='SET NULL'), nullable=True)
    dieu_luat = db.Column(db.String(255), nullable=False)
    toi_danh = db.Column(db.String(255), nullable=False)
    ngay_xay_ra = db.Column(db.Date, nullable=False)
    noi_xay_ra = db.Column(db.Text, nullable=False)
    thong_tin_vu_an = db.Column(db.Text, nullable=False)
    so_qd_phan_cong_ptt = db.Column(db.String(100))
    so_qd_phan_cong_dtv = db.Column(db.String(100))
    ngay_phan_cong = db.Column(db.Date)
    so_khoi_to_vu_an = db.Column(db.String(100))
    ngay_khoi_to_vu_an = db.Column(db.Date)
    tong_so_bi_can = db.Column(db.Integer, default=0)
    thong_tin_bi_can = db.Column(db.Text)
    bien_phap_ngan_chan = db.Column(db.String(100))
    so_khoi_to_bi_can = db.Column(db.String(100))
    ngay_khoi_to_bi_can = db.Column(db.Date)
    dang_vien = db.Column(db.String(100))
    ket_qua_giai_quyet = db.Column(db.String(100))
    bi_can_giai_quyet = db.Column(db.Text)
    dieu_tra_vien = db.Column(db.String(100), nullable=False)
    can_bo_quan_ly_ho_so = db.Column(db.String(100))
    don_vi = db.Column(db.String(100), default='CAX Phước Thái')
    kiem_sat_vien = db.Column(db.String(100))
    ngay_het_han = db.Column(db.Date)
    tinh_trang_ho_so = db.Column(db.String(100))
    ghi_chu = db.Column(db.Text)
    trang_thai = db.Column(db.String(50), nullable=False, default='Mới tạo')
    ngay_chuyen_tu_tin_bao = db.Column(db.Date)
    
    # Relationships
    bi_can_list = db.relationship('BiCan', backref='vu_an', lazy=True, cascade='all, delete-orphan')
    tam_giam_list = db.relationship('TamGiam', backref='vu_an', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'stt': self.stt,
            'tin_bao_id': self.tin_bao_id,
            'dieu_luat': self.dieu_luat,
            'toi_danh': self.toi_danh,
            'ngay_xay_ra': self.ngay_xay_ra.isoformat() if self.ngay_xay_ra else None,
            'noi_xay_ra': self.noi_xay_ra,
            'thong_tin_vu_an': self.thong_tin_vu_an,
            'so_qd_phan_cong_ptt': self.so_qd_phan_cong_ptt,
            'so_qd_phan_cong_dtv': self.so_qd_phan_cong_dtv,
            'ngay_phan_cong': self.ngay_phan_cong.isoformat() if self.ngay_phan_cong else None,
            'so_khoi_to_vu_an': self.so_khoi_to_vu_an,
            'ngay_khoi_to_vu_an': self.ngay_khoi_to_vu_an.isoformat() if self.ngay_khoi_to_vu_an else None,
            'tong_so_bi_can': self.tong_so_bi_can,
            'thong_tin_bi_can': self.thong_tin_bi_can,
            'bien_phap_ngan_chan': self.bien_phap_ngan_chan,
            'so_khoi_to_bi_can': self.so_khoi_to_bi_can,
            'ngay_khoi_to_bi_can': self.ngay_khoi_to_bi_can.isoformat() if self.ngay_khoi_to_bi_can else None,
            'dang_vien': self.dang_vien,
            'ket_qua_giai_quyet': self.ket_qua_giai_quyet,
            'bi_can_giai_quyet': self.bi_can_giai_quyet,
            'dieu_tra_vien': self.dieu_tra_vien,
            'can_bo_quan_ly_ho_so': self.can_bo_quan_ly_ho_so,
            'don_vi': self.don_vi,
            'kiem_sat_vien': self.kiem_sat_vien,
            'ngay_het_han': self.ngay_het_han.isoformat() if self.ngay_het_han else None,
            'tinh_trang_ho_so': self.tinh_trang_ho_so,
            'ghi_chu': self.ghi_chu,
            'trang_thai': self.trang_thai,
            'ngay_chuyen_tu_tin_bao': self.ngay_chuyen_tu_tin_bao.isoformat() if self.ngay_chuyen_tu_tin_bao else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class BiCan(BaseModel):
    """Bị can trong vụ án"""
    __tablename__ = 'bi_can'
    
    vu_an_id = db.Column(db.String(36), db.ForeignKey('vu_an.id', ondelete='CASCADE'), nullable=False)
    ho_ten = db.Column(db.String(100), nullable=False)
    nam_sinh = db.Column(db.Integer, nullable=False)
    dia_chi_thuong_tru = db.Column(db.Text, nullable=False)
    so_cmnd = db.Column(db.String(20))
    nghe_nghiep = db.Column(db.String(100))
    dang_vien = db.Column(db.Boolean, default=False)
    bien_phap_ngan_chan = db.Column(db.String(100))
    so_khoi_to_bi_can = db.Column(db.String(100))
    ngay_khoi_to = db.Column(db.Date)
    trang_thai = db.Column(db.String(50), default='Chưa khởi tố')
    
    # Relationships
    tam_giam_list = db.relationship('TamGiam', backref='bi_can', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'vu_an_id': self.vu_an_id,
            'ho_ten': self.ho_ten,
            'nam_sinh': self.nam_sinh,
            'dia_chi_thuong_tru': self.dia_chi_thuong_tru,
            'so_cmnd': self.so_cmnd,
            'nghe_nghiep': self.nghe_nghiep,
            'dang_vien': self.dang_vien,
            'bien_phap_ngan_chan': self.bien_phap_ngan_chan,
            'so_khoi_to_bi_can': self.so_khoi_to_bi_can,
            'ngay_khoi_to': self.ngay_khoi_to.isoformat() if self.ngay_khoi_to else None,
            'trang_thai': self.trang_thai,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class LichSuChuyenDoi(BaseModel):
    """Lịch sử chuyển đổi tin báo → vụ án"""
    __tablename__ = 'lich_su_chuyen_doi'
    
    tin_bao_id = db.Column(db.String(36), db.ForeignKey('tin_bao.id', ondelete='CASCADE'), nullable=False)
    vu_an_id = db.Column(db.String(36), db.ForeignKey('vu_an.id', ondelete='CASCADE'), nullable=False)
    ngay_chuyen = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    nguoi_chuyen = db.Column(db.String(100))
    ly_do = db.Column(db.Text)
    ghi_chu = db.Column(db.Text)
    
    # Relationships
    tin_bao = db.relationship('TinBao', foreign_keys=[tin_bao_id])
    vu_an = db.relationship('VuAn', foreign_keys=[vu_an_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'tin_bao_id': self.tin_bao_id,
            'vu_an_id': self.vu_an_id,
            'ngay_chuyen': self.ngay_chuyen.isoformat() if self.ngay_chuyen else None,
            'nguoi_chuyen': self.nguoi_chuyen,
            'ly_do': self.ly_do,
            'ghi_chu': self.ghi_chu,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class TamGiam(BaseModel):
    """Tạm giam - Liên kết với vụ án"""
    __tablename__ = 'tam_giam'
    
    vu_an_id = db.Column(db.String(36), db.ForeignKey('vu_an.id', ondelete='CASCADE'), nullable=False)
    bi_can_id = db.Column(db.String(36), db.ForeignKey('bi_can.id', ondelete='CASCADE'), nullable=False)
    ngay_bat_giam = db.Column(db.Date, nullable=False)
    ngay_het_han_giam = db.Column(db.Date, nullable=False)
    ly_do_tam_giam = db.Column(db.Text, nullable=False)
    trang_thai_giam = db.Column(db.String(50), default='Đang giam')
    ghi_chu = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'vu_an_id': self.vu_an_id,
            'bi_can_id': self.bi_can_id,
            'ngay_bat_giam': self.ngay_bat_giam.isoformat() if self.ngay_bat_giam else None,
            'ngay_het_han_giam': self.ngay_het_han_giam.isoformat() if self.ngay_het_han_giam else None,
            'ly_do_tam_giam': self.ly_do_tam_giam,
            'trang_thai_giam': self.trang_thai_giam,
            'ghi_chu': self.ghi_chu,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

