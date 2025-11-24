-- Seed Data for Asset Management System

-- Insert sample data for danh_sach_vu_khi_cong_cu_ho_tro
INSERT INTO danh_sach_vu_khi_cong_cu_ho_tro (
    ma_tai_san, ma_danh_muc, ten_tai_san, don_vi_tinh, nam_su_dung, so_luong,
    nguyen_gia, gia_tri_con_lai, so_hieu, loai_tai_san, thuc_te_ban_giao,
    dinh_ky_kiem_tra, vi_tri_tai_san, nguoi_su_dung, ngay_kiem_tra_gan_nhat,
    ngay_kiem_tra_tiep_theo, ket_qua_kiem_tra, nam_het_han, phuong_thuc_xu_ly, ghi_chu
) VALUES
('VK2511001', 'Súng', 'Súng AKM báng gấp', 'Khẩu', 2016, 1, 9481024, 9481024, '141759', 'Đặc biệt', 'Có', '6 tháng', NULL, NULL, '2025-06-01', '2025-12-01', 'Đạt', NULL, 'Tiếp tục sử dụng', NULL),
('VK2511002', 'Công cụ hỗ trợ', 'Gậy điện tử 3 khúc Titan M3', 'Chiếc', 2020, 1, 1700000, 1700000, 'TB-TT79 0320-3648', 'Chuyên dụng', 'Có', '6 tháng', NULL, NULL, '2025-05-15', '2025-11-15', 'Đạt', NULL, 'Tiếp tục sử dụng', NULL),
('VK2511003', 'Đạn', 'Đạn AK thường', 'Viên', NULL, 60, NULL, NULL, NULL, 'Đặc biệt', 'Có', '12 tháng', NULL, NULL, '2025-01-01', '2026-01-01', 'Đạt', NULL, 'Tiếp tục sử dụng', NULL),
('VK2511004', 'Súng', 'Súng CZ 75 P-07 Duty', 'Khẩu', 2018, 1, 12500000, 10000000, 'CZ-2018-001', 'Chuyên dụng', 'Có', '6 tháng', 'Kho vũ khí', 'Đội trưởng A', '2025-07-01', '2026-01-01', 'Đạt', NULL, 'Tiếp tục sử dụng', NULL),
('VK2511005', 'Công cụ hỗ trợ', 'Dùi cui điện', 'Chiếc', 2021, 2, 2500000, 2000000, 'DC-2021-001', 'Chuyên dụng', 'Có', '3 tháng', 'Phòng trang bị', NULL, '2025-08-15', '2025-11-15', 'Đạt', NULL, 'Tiếp tục sử dụng', NULL);

-- Insert sample data for danh_sach_phuong_tien
INSERT INTO danh_sach_phuong_tien (
    ma_tai_san, danh_muc_phuong_tien, ten_phuong_tien, don_vi_tinh, nguyen_gia, so_luong,
    bien_so_ky_hieu, so_khung_so_than_vo, so_may, nam_trang_bi, loai_tai_san, thuc_te_ban_giao,
    ngay_dang_kiem, ngay_thay_nhot, ngay_thay_vo, sua_chua, phi_duong_bo, nam_het_han,
    phuong_thuc_xu_ly, dinh_ky_kiem_tra, ngay_kiem_tra_gan_nhat, ngay_kiem_tra_tiep_theo,
    ket_qua_kiem_tra, ghi_chu
) VALUES
('PT2511001', 'Ô tô', 'Suzuki Carry/Vandao-ANTT 1.5 xăng 4x2', 'Chiếc', 378800000, 1, '60A-009.87', 'MHYHDC61TMJ912829', 'K15BT1297661', 2024, 'Chuyên dụng', 'Có', '2025-10-01', '2025-08-15', '2025-07-01', NULL, NULL, NULL, NULL, '3 tháng', '2025-08-15', '2025-11-15', 'Đạt', NULL),
('PT2511002', 'Moto', 'Honda Future FI 125cc', 'Chiếc', 30690000, 1, '60B1-003.22', 'RLHJC7643LY010607', 'JC90E-0041083', 2020, 'Quản lý', 'Có', '2025-09-01', '2025-07-20', '2025-06-15', NULL, NULL, NULL, NULL, '3 tháng', '2025-10-20', '2026-01-20', 'Đạt', NULL),
('PT2511003', 'Ô tô', 'Toyota Vios 1.5E', 'Chiếc', 450000000, 1, '60A-123.45', 'TOYOTA-2023-001', 'ENG-2023-001', 2023, 'Quản lý', 'Có', '2025-12-01', '2025-09-01', '2025-08-01', 'Thay lốp mới', 'Đã nộp', 2026, 'Tiếp tục sử dụng', '3 tháng', '2025-09-01', '2025-12-01', 'Đạt', NULL),
('PT2511004', 'Moto', 'Yamaha Exciter 150', 'Chiếc', 45000000, 1, '60B2-456.78', 'YAMAHA-2022-001', 'ENG-2022-001', 2022, 'Chuyên dụng', 'Có', '2025-11-01', '2025-08-15', '2025-07-15', NULL, NULL, 2026, 'Tiếp tục sử dụng', '3 tháng', '2025-08-15', '2025-11-15', 'Đạt', NULL);

-- Insert sample data for danh_sach_thiet_bi_ky_thuat_nghiep_vu
INSERT INTO danh_sach_thiet_bi_ky_thuat_nghiep_vu (
    ma_tai_san, ten_tai_san, nam_su_dung, so_luong, nguyen_gia, gia_tri_con_lai,
    loai_tai_san, thuc_te_ban_giao, dinh_ky_kiem_tra, ngay_kiem_tra_gan_nhat,
    ngay_kiem_tra_tiep_theo, ket_qua_kiem_tra, nam_het_han, phuong_thuc_xu_ly, ghi_chu
) VALUES
('TB2511001', 'Máy ảnh KTS Pentax K70', 2021, 1, 19548000, 19548000, 'Chuyên dụng', 'Có', '6 tháng', '2025-05-01', '2025-11-01', 'Đạt', NULL, 'Tiếp tục sử dụng', NULL),
('TB2511002', 'Máy phát điện 5-5-5 KVA', 2021, 1, 26699692, 26699692, 'Chuyên dụng', 'Có', '6 tháng', '2025-04-15', '2025-10-15', 'Đạt', NULL, 'Tiếp tục sử dụng', NULL),
('TB2511003', 'Máy quay phim Sony HDR-CX405', 2020, 1, 8500000, 6000000, 'Chuyên dụng', 'Có', '6 tháng', '2025-06-01', '2025-12-01', 'Đạt', NULL, 'Tiếp tục sử dụng', NULL),
('TB2511004', 'Máy đo tốc độ Laser', 2019, 1, 15000000, 10000000, 'Chuyên dụng', 'Có', '12 tháng', '2025-01-01', '2026-01-01', 'Đạt', NULL, 'Tiếp tục sử dụng', NULL),
('TB2511005', 'Máy tính bảng iPad Pro', 2022, 2, 25000000, 20000000, 'Quản lý', 'Có', '6 tháng', '2025-07-01', '2026-01-01', 'Đạt', NULL, 'Tiếp tục sử dụng', NULL);

-- Insert sample data for danh_sach_thiet_bi_van_phong_doanh_trai
INSERT INTO danh_sach_thiet_bi_van_phong_doanh_trai (
    ma_tai_san, ten_tai_san, nam_su_dung, so_luong, nguyen_gia, gia_tri_con_lai,
    loai_tai_san, thuc_te_ban_giao, hinh_thuc, su_kien, chi_phi, dinh_ky_kiem_tra,
    ngay_kiem_tra_gan_nhat, ngay_kiem_tra_tiep_theo, ket_qua_kiem_tra, nam_het_han,
    phuong_thuc_xu_ly, ghi_chu
) VALUES
('VP2511001', 'Máy in Canon LBP 226DW', 2020, 1, 0, 0, 'Quản lý', 'Có', 'Bàn giao', NULL, NULL, '6 tháng', '2025-06-01', '2025-12-01', 'Đạt', NULL, 'Tiếp tục sử dụng', NULL),
('VP2511002', 'Máy vi tính Dell Optiplex 5080 SFF', 2020, 1, 0, 0, 'Quản lý', 'Chưa thấy', 'Bàn giao', NULL, NULL, '6 tháng', NULL, NULL, NULL, NULL, 'Tiếp tục sử dụng', NULL),
('VP2511003', 'Máy điều hòa Daikin 1.5HP', 2021, 3, 12000000, 9000000, 'Quản lý', 'Có', 'Mua mới', NULL, NULL, '12 tháng', '2025-01-01', '2026-01-01', 'Đạt', NULL, 'Tiếp tục sử dụng', NULL),
('VP2511004', 'Tủ lạnh Panasonic 150L', 2020, 1, 8000000, 5000000, 'Quản lý', 'Có', 'Mua mới', 'Sửa chữa', 500000, '12 tháng', '2025-05-01', '2026-05-01', 'Đạt', NULL, 'Tiếp tục sử dụng', 'Đã sửa chữa tháng 5/2025'),
('VP2511005', 'Bàn ghế văn phòng', 2019, 10, 5000000, 3000000, 'Quản lý', 'Có', 'Bàn giao', NULL, NULL, '12 tháng', '2025-01-01', '2026-01-01', 'Đạt', NULL, 'Tiếp tục sử dụng', NULL);

-- Insert sample data for lich_su_kiem_tra_bao_tri
INSERT INTO lich_su_kiem_tra_bao_tri (
    ma_tai_san, loai_hinh, ngay_thuc_hien, nguoi_thuc_hien, chi_tiet_cong_viec,
    chi_phi, ket_qua, ghi_chu
) VALUES
('VK2511001', 'Kiểm tra', '2025-06-01', 'Nguyễn Văn A', 'Kiểm tra định kỳ 6 tháng', 0, 'Đạt', 'Tất cả bộ phận hoạt động bình thường'),
('VK2511002', 'Kiểm tra', '2025-05-15', 'Trần Thị B', 'Kiểm tra định kỳ 6 tháng', 0, 'Đạt', NULL),
('PT2511001', 'Bảo trì', '2025-08-15', 'Lê Văn C', 'Thay nhớt và kiểm tra động cơ', 500000, 'Đạt', 'Động cơ hoạt động tốt'),
('PT2511002', 'Bảo trì', '2025-07-20', 'Phạm Thị D', 'Thay nhớt và lọc gió', 300000, 'Đạt', NULL),
('TB2511001', 'Kiểm tra', '2025-05-01', 'Hoàng Văn E', 'Kiểm tra định kỳ máy ảnh', 0, 'Đạt', 'Máy hoạt động tốt'),
('VP2511001', 'Kiểm tra', '2025-06-01', 'Võ Thị F', 'Kiểm tra máy in', 0, 'Đạt', NULL),
('VP2511004', 'Sửa chữa', '2025-05-01', 'Đặng Văn G', 'Sửa chữa tủ lạnh bị hỏng', 500000, 'Đạt', 'Đã thay block lạnh');

-- Insert sample data for danh_muc_loai_tai_san
INSERT INTO danh_muc_loai_tai_san (ma_danh_muc, ten_danh_muc, loai_tai_san_chinh, mo_ta) VALUES
('SUNG', 'Súng', 'VK-VLN-CCHT', 'Các loại súng phục vụ công tác'),
('DAN', 'Đạn', 'VK-VLN-CCHT', 'Các loại đạn dược'),
('CCHT', 'Công cụ hỗ trợ', 'VK-VLN-CCHT', 'Các công cụ hỗ trợ như gậy, dùi cui'),
('OTO', 'Ô tô', 'PT', 'Phương tiện ô tô'),
('MOTO', 'Moto', 'PT', 'Phương tiện xe máy'),
('PT_THUY', 'Phương tiện thủy', 'PT', 'Phương tiện đường thủy'),
('TB_KTNV', 'Thiết bị KTNV', 'KTNV', 'Thiết bị kỹ thuật nghiệp vụ'),
('TB_VP', 'Thiết bị Văn phòng', 'VP-DT', 'Thiết bị văn phòng và doanh trại');

