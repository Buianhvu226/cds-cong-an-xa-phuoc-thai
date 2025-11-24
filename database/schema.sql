-- Database Schema for Asset Management System - Công An Xã Phước Thái

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table: danh_sach_vu_khi_cong_cu_ho_tro
CREATE TABLE IF NOT EXISTS danh_sach_vu_khi_cong_cu_ho_tro (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ma_tai_san VARCHAR(50) UNIQUE NOT NULL,
    ma_danh_muc VARCHAR(20) NOT NULL, -- 'Súng', 'Đạn', 'Công cụ hỗ trợ'
    ten_tai_san VARCHAR(255) NOT NULL,
    don_vi_tinh VARCHAR(20) NOT NULL, -- 'Viên', 'Chiếc', 'Khẩu'
    nam_su_dung INTEGER,
    so_luong INTEGER NOT NULL DEFAULT 1,
    nguyen_gia DECIMAL(15,0),
    gia_tri_con_lai DECIMAL(15,0),
    so_hieu VARCHAR(100),
    loai_tai_san VARCHAR(50), -- 'Chuyên dụng', 'Đặc biệt'
    thuc_te_ban_giao VARCHAR(10), -- 'Có', 'Không'
    dinh_ky_kiem_tra VARCHAR(20), -- '1 tháng', '3 tháng', '6 tháng', '12 tháng'
    vi_tri_tai_san VARCHAR(100),
    nguoi_su_dung VARCHAR(100),
    ngay_kiem_tra_gan_nhat DATE,
    ngay_kiem_tra_tiep_theo DATE,
    ket_qua_kiem_tra VARCHAR(20), -- 'Đạt', 'Không đạt'
    nam_het_han INTEGER,
    phuong_thuc_xu_ly VARCHAR(50), -- 'Tiếp tục sử dụng', 'Ngưng sử dụng'
    ghi_chu TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_deleted BOOLEAN DEFAULT FALSE
);

-- Table: danh_sach_phuong_tien
CREATE TABLE IF NOT EXISTS danh_sach_phuong_tien (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ma_tai_san VARCHAR(50) UNIQUE NOT NULL,
    danh_muc_phuong_tien VARCHAR(50) NOT NULL, -- 'Ô tô', 'Moto', 'Phương tiện thủy'
    ten_phuong_tien VARCHAR(255) NOT NULL,
    don_vi_tinh VARCHAR(20) NOT NULL,
    nguyen_gia DECIMAL(15,0),
    so_luong INTEGER NOT NULL DEFAULT 1,
    bien_so_ky_hieu VARCHAR(50),
    so_khung_so_than_vo VARCHAR(100),
    so_may VARCHAR(100),
    nam_trang_bi INTEGER,
    loai_tai_san VARCHAR(50),
    thuc_te_ban_giao VARCHAR(10),
    ngay_dang_kiem DATE,
    ngay_thay_nhot DATE,
    ngay_thay_vo DATE,
    sua_chua TEXT,
    phi_duong_bo TEXT,
    nam_het_han INTEGER,
    phuong_thuc_xu_ly VARCHAR(50),
    dinh_ky_kiem_tra VARCHAR(20),
    ngay_kiem_tra_gan_nhat DATE,
    ngay_kiem_tra_tiep_theo DATE,
    ket_qua_kiem_tra VARCHAR(20),
    ghi_chu TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_deleted BOOLEAN DEFAULT FALSE
);

-- Table: danh_sach_thiet_bi_ky_thuat_nghiep_vu
CREATE TABLE IF NOT EXISTS danh_sach_thiet_bi_ky_thuat_nghiep_vu (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ma_tai_san VARCHAR(50) UNIQUE NOT NULL,
    ten_tai_san VARCHAR(255) NOT NULL,
    nam_su_dung INTEGER,
    so_luong INTEGER NOT NULL,
    nguyen_gia DECIMAL(15,0),
    gia_tri_con_lai DECIMAL(15,0),
    loai_tai_san VARCHAR(50),
    thuc_te_ban_giao VARCHAR(10),
    dinh_ky_kiem_tra VARCHAR(20),
    ngay_kiem_tra_gan_nhat DATE,
    ngay_kiem_tra_tiep_theo DATE,
    ket_qua_kiem_tra VARCHAR(20),
    nam_het_han INTEGER,
    phuong_thuc_xu_ly VARCHAR(50),
    ghi_chu TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_deleted BOOLEAN DEFAULT FALSE
);

-- Table: danh_sach_thiet_bi_van_phong_doanh_trai
CREATE TABLE IF NOT EXISTS danh_sach_thiet_bi_van_phong_doanh_trai (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ma_tai_san VARCHAR(50) UNIQUE NOT NULL,
    ten_tai_san VARCHAR(255) NOT NULL,
    nam_su_dung INTEGER,
    so_luong INTEGER NOT NULL,
    nguyen_gia DECIMAL(15,0),
    gia_tri_con_lai DECIMAL(15,0),
    loai_tai_san VARCHAR(50),
    thuc_te_ban_giao VARCHAR(10),
    hinh_thuc VARCHAR(50), -- 'Mua mới', 'Bàn giao'
    su_kien VARCHAR(50), -- 'Sửa chữa', 'Tu bổ', 'Nâng cấp'
    chi_phi DECIMAL(15,0),
    dinh_ky_kiem_tra VARCHAR(20),
    ngay_kiem_tra_gan_nhat DATE,
    ngay_kiem_tra_tiep_theo DATE,
    ket_qua_kiem_tra VARCHAR(20),
    nam_het_han INTEGER,
    phuong_thuc_xu_ly VARCHAR(50),
    ghi_chu TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_deleted BOOLEAN DEFAULT FALSE
);

-- Table: lich_su_kiem_tra_bao_tri
CREATE TABLE IF NOT EXISTS lich_su_kiem_tra_bao_tri (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ma_tai_san VARCHAR(50) NOT NULL,
    loai_hinh VARCHAR(50) NOT NULL, -- 'Kiểm tra', 'Bảo trì', 'Sửa chữa'
    ngay_thuc_hien DATE NOT NULL,
    nguoi_thuc_hien VARCHAR(100),
    chi_tiet_cong_viec TEXT,
    chi_phi DECIMAL(15,0),
    ket_qua VARCHAR(20), -- 'Đạt', 'Không đạt'
    ghi_chu TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table: danh_muc_loai_tai_san
CREATE TABLE IF NOT EXISTS danh_muc_loai_tai_san (
    ma_danh_muc VARCHAR(20) PRIMARY KEY,
    ten_danh_muc VARCHAR(100) NOT NULL,
    loai_tai_san_chinh VARCHAR(50) NOT NULL, -- 'VK-VLN-CCHT', 'PT', 'KTNV', 'VP-DT'
    mo_ta TEXT
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_vk_ma_tai_san ON danh_sach_vu_khi_cong_cu_ho_tro(ma_tai_san);
CREATE INDEX IF NOT EXISTS idx_vk_is_deleted ON danh_sach_vu_khi_cong_cu_ho_tro(is_deleted);
CREATE INDEX IF NOT EXISTS idx_vk_ngay_kiem_tra ON danh_sach_vu_khi_cong_cu_ho_tro(ngay_kiem_tra_tiep_theo);

CREATE INDEX IF NOT EXISTS idx_pt_ma_tai_san ON danh_sach_phuong_tien(ma_tai_san);
CREATE INDEX IF NOT EXISTS idx_pt_is_deleted ON danh_sach_phuong_tien(is_deleted);
CREATE INDEX IF NOT EXISTS idx_pt_ngay_kiem_tra ON danh_sach_phuong_tien(ngay_kiem_tra_tiep_theo);

CREATE INDEX IF NOT EXISTS idx_tb_ma_tai_san ON danh_sach_thiet_bi_ky_thuat_nghiep_vu(ma_tai_san);
CREATE INDEX IF NOT EXISTS idx_tb_is_deleted ON danh_sach_thiet_bi_ky_thuat_nghiep_vu(is_deleted);
CREATE INDEX IF NOT EXISTS idx_tb_ngay_kiem_tra ON danh_sach_thiet_bi_ky_thuat_nghiep_vu(ngay_kiem_tra_tiep_theo);

CREATE INDEX IF NOT EXISTS idx_vp_ma_tai_san ON danh_sach_thiet_bi_van_phong_doanh_trai(ma_tai_san);
CREATE INDEX IF NOT EXISTS idx_vp_is_deleted ON danh_sach_thiet_bi_van_phong_doanh_trai(is_deleted);
CREATE INDEX IF NOT EXISTS idx_vp_ngay_kiem_tra ON danh_sach_thiet_bi_van_phong_doanh_trai(ngay_kiem_tra_tiep_theo);

CREATE INDEX IF NOT EXISTS idx_ls_ma_tai_san ON lich_su_kiem_tra_bao_tri(ma_tai_san);
CREATE INDEX IF NOT EXISTS idx_ls_ngay_thuc_hien ON lich_su_kiem_tra_bao_tri(ngay_thuc_hien);

