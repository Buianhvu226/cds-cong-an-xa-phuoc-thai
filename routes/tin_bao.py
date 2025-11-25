from flask import Blueprint, request, jsonify, send_file
from models import TinBao, VuAn, LichSuChuyenDoi
from database import db
from utils.auth import require_auth, require_admin, get_current_user
from datetime import datetime, date
import re
from sqlalchemy import func, or_
import pandas as pd
import io
import uuid
from openpyxl.utils import get_column_letter
from collections import Counter

bp = Blueprint('tin_bao', __name__)

@bp.route('', methods=['GET'])
@require_auth
def get_tin_bao_list():
    """Danh sách tin báo với search, filter, pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '').strip()
        trang_thai = request.args.get('trang_thai', '').strip()
        cong_an_phu_trach = request.args.get('cong_an_phu_trach', '').strip()
        
        query = TinBao.query.filter_by(is_deleted=False)
        
        # Search
        if search:
            query = query.filter(
                or_(
                    TinBao.dieu_luat.ilike(f'%{search}%'),
                    TinBao.ten_nguon_tin.ilike(f'%{search}%'),
                    TinBao.noi_xay_ra.ilike(f'%{search}%'),
                    TinBao.noi_dung_nguon_tin.ilike(f'%{search}%')
                )
            )
        
        # Filter
        if trang_thai:
            query = query.filter(TinBao.trang_thai == trang_thai)
        if cong_an_phu_trach:
            query = query.filter(TinBao.cong_an_phu_trach.ilike(f'%{cong_an_phu_trach}%'))
        
        # Pagination
        total = query.count()
        items = query.order_by(TinBao.stt.desc()).offset((page - 1) * per_page).limit(per_page).all()
        
        return jsonify({
            'items': [item.to_dict() for item in items],
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }), 200
    except Exception as e:
        import traceback
        print(f"Error in get_tin_bao_list: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@bp.route('', methods=['POST'])
@require_auth
def create_tin_bao():
    """Tạo tin báo mới"""
    try:
        data = request.get_json()
        
        # Validation
        if not data.get('dieu_luat') or len(data.get('dieu_luat', '')) < 5:
            return jsonify({'error': 'Điều luật bắt buộc nhập, tối thiểu 5 ký tự'}), 400
        if not data.get('ngay_xay_ra'):
            return jsonify({'error': 'Ngày xảy ra bắt buộc nhập'}), 400
        if not data.get('noi_xay_ra') or len(data.get('noi_xay_ra', '')) < 5:
            return jsonify({'error': 'Nơi xảy ra bắt buộc nhập'}), 400
        if not data.get('noi_dung_nguon_tin') or len(data.get('noi_dung_nguon_tin', '')) < 20:
            return jsonify({'error': 'Nội dung bắt buộc, mô tả chi tiết (tối thiểu 20 ký tự)'}), 400
        
        # Auto-generate STT
        max_stt = db.session.query(func.max(TinBao.stt)).scalar() or 0
        new_stt = max_stt + 1
        
        # Parse dates
        ngay_xay_ra = datetime.strptime(data['ngay_xay_ra'], '%Y-%m-%d').date() if data.get('ngay_xay_ra') else None
        ngay_phan_cong = datetime.strptime(data['ngay_phan_cong'], '%Y-%m-%d').date() if data.get('ngay_phan_cong') else None
        ngay_het_han = datetime.strptime(data['ngay_het_han'], '%Y-%m-%d').date() if data.get('ngay_het_han') else None
        
        tin_bao = TinBao(
            stt=new_stt,
            dieu_luat=data['dieu_luat'],
            ten_nguon_tin=data.get('ten_nguon_tin'),
            ngay_xay_ra=ngay_xay_ra,
            noi_xay_ra=data['noi_xay_ra'],
            noi_dung_nguon_tin=data['noi_dung_nguon_tin'],
            so_qd_phan_cong_ptt=data.get('so_qd_phan_cong_ptt'),
            so_qd_phan_cong_dtv=data.get('so_qd_phan_cong_dtv'),
            ngay_phan_cong=ngay_phan_cong,
            ket_qua_giai_quyet=data.get('ket_qua_giai_quyet'),
            dia_chi_bi_hai=data.get('dia_chi_bi_hai'),
            thong_tin_doi_tuong=data.get('thong_tin_doi_tuong'),
            cong_an_phu_trach=data.get('cong_an_phu_trach'),
            don_vi=data.get('don_vi', 'CAX Phước Thái'),
            kiem_sat_vien=data.get('kiem_sat_vien'),
            gia_han=data.get('gia_han', 0),
            ngay_het_han=ngay_het_han,
            tinh_trang_ho_so=data.get('tinh_trang_ho_so'),
            ghi_chu=data.get('ghi_chu'),
            trang_thai=data.get('trang_thai', 'Tiếp nhận')
        )
        
        db.session.add(tin_bao)
        db.session.commit()
        
        return jsonify({'message': 'Tạo tin báo thành công', 'data': tin_bao.to_dict()}), 201
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': f'Lỗi định dạng ngày: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<tin_bao_id>', methods=['GET'])
@require_auth
def get_tin_bao_detail(tin_bao_id):
    """Chi tiết tin báo"""
    try:
        tin_bao = TinBao.query.filter_by(id=tin_bao_id, is_deleted=False).first()
        if not tin_bao:
            return jsonify({'error': 'Tin báo không tồn tại'}), 404
        
        return jsonify(tin_bao.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<tin_bao_id>', methods=['PUT'])
@require_auth
def update_tin_bao(tin_bao_id):
    """Cập nhật tin báo"""
    try:
        tin_bao = TinBao.query.filter_by(id=tin_bao_id, is_deleted=False).first()
        if not tin_bao:
            return jsonify({'error': 'Tin báo không tồn tại'}), 404
        
        data = request.get_json()
        
        # Validation
        if data.get('dieu_luat') and len(data['dieu_luat']) < 5:
            return jsonify({'error': 'Điều luật tối thiểu 5 ký tự'}), 400
        if data.get('noi_xay_ra') and len(data['noi_xay_ra']) < 5:
            return jsonify({'error': 'Nơi xảy ra tối thiểu 5 ký tự'}), 400
        if data.get('noi_dung_nguon_tin') and len(data['noi_dung_nguon_tin']) < 20:
            return jsonify({'error': 'Nội dung tối thiểu 20 ký tự'}), 400
        
        # Update fields
        if 'dieu_luat' in data:
            tin_bao.dieu_luat = data['dieu_luat']
        if 'ten_nguon_tin' in data:
            tin_bao.ten_nguon_tin = data['ten_nguon_tin']
        if 'ngay_xay_ra' in data:
            tin_bao.ngay_xay_ra = datetime.strptime(data['ngay_xay_ra'], '%Y-%m-%d').date()
        if 'noi_xay_ra' in data:
            tin_bao.noi_xay_ra = data['noi_xay_ra']
        if 'noi_dung_nguon_tin' in data:
            tin_bao.noi_dung_nguon_tin = data['noi_dung_nguon_tin']
        if 'so_qd_phan_cong_ptt' in data:
            tin_bao.so_qd_phan_cong_ptt = data['so_qd_phan_cong_ptt']
        if 'so_qd_phan_cong_dtv' in data:
            tin_bao.so_qd_phan_cong_dtv = data['so_qd_phan_cong_dtv']
        if 'ngay_phan_cong' in data:
            tin_bao.ngay_phan_cong = datetime.strptime(data['ngay_phan_cong'], '%Y-%m-%d').date() if data['ngay_phan_cong'] else None
        if 'ket_qua_giai_quyet' in data:
            tin_bao.ket_qua_giai_quyet = data['ket_qua_giai_quyet']
        if 'dia_chi_bi_hai' in data:
            tin_bao.dia_chi_bi_hai = data['dia_chi_bi_hai']
        if 'thong_tin_doi_tuong' in data:
            tin_bao.thong_tin_doi_tuong = data['thong_tin_doi_tuong']
        if 'cong_an_phu_trach' in data:
            tin_bao.cong_an_phu_trach = data['cong_an_phu_trach']
        if 'kiem_sat_vien' in data:
            tin_bao.kiem_sat_vien = data['kiem_sat_vien']
        if 'gia_han' in data:
            tin_bao.gia_han = data['gia_han']
        if 'ngay_het_han' in data:
            tin_bao.ngay_het_han = datetime.strptime(data['ngay_het_han'], '%Y-%m-%d').date() if data['ngay_het_han'] else None
        if 'tinh_trang_ho_so' in data:
            tin_bao.tinh_trang_ho_so = data['tinh_trang_ho_so']
        if 'ghi_chu' in data:
            tin_bao.ghi_chu = data['ghi_chu']
        if 'trang_thai' in data:
            tin_bao.trang_thai = data['trang_thai']
        
        tin_bao.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': 'Cập nhật tin báo thành công', 'data': tin_bao.to_dict()}), 200
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': f'Lỗi định dạng ngày: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<tin_bao_id>', methods=['DELETE'])
@require_admin
def delete_tin_bao(tin_bao_id):
    """Xóa tin báo (soft delete)"""
    try:
        tin_bao = TinBao.query.filter_by(id=tin_bao_id, is_deleted=False).first()
        if not tin_bao:
            return jsonify({'error': 'Tin báo không tồn tại'}), 404
        
        tin_bao.is_deleted = True
        tin_bao.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': 'Xóa tin báo thành công'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<tin_bao_id>/chuyen-thanh-vu-an', methods=['POST'])
@require_auth
def chuyen_thanh_vu_an(tin_bao_id):
    """Chuyển đổi tin báo thành vụ án - HÀNH ĐỘNG CHÍNH"""
    try:
        tin_bao = TinBao.query.filter_by(id=tin_bao_id, is_deleted=False).first()
        if not tin_bao:
            return jsonify({'error': 'Tin báo không tồn tại'}), 404
        
        # Validation: Kiểm tra chưa được chuyển
        if tin_bao.vu_an_id:
            return jsonify({'error': 'Tin báo đã được chuyển thành vụ án trước đó'}), 400
        
        # Validation: Trạng thái hợp lệ
        if tin_bao.trang_thai not in ['Tiếp nhận', 'Đang điều tra']:
            return jsonify({'error': f'Không thể chuyển tin báo có trạng thái: {tin_bao.trang_thai}'}), 400
        
        # Validation: Dữ liệu tối thiểu
        if not tin_bao.dieu_luat or not tin_bao.ngay_xay_ra or not tin_bao.noi_xay_ra or not tin_bao.noi_dung_nguon_tin:
            return jsonify({'error': 'Tin báo thiếu thông tin bắt buộc để chuyển đổi'}), 400
        
        data = request.get_json() or {}
        current_user = get_current_user()
        
        # Auto-generate STT vụ án
        max_stt = db.session.query(func.max(VuAn.stt)).scalar() or 0
        new_stt = db.session.query(func.max(VuAn.stt)).scalar() or 0
        new_stt = max_stt + 1
        
        # Parse dates
        ngay_chuyen = datetime.utcnow().date()
        
        # Tạo vụ án mới - Sao chép dữ liệu từ tin báo
        vu_an = VuAn(
            stt=new_stt,
            tin_bao_id=tin_bao.id,
            dieu_luat=tin_bao.dieu_luat,
            toi_danh=data.get('toi_danh', tin_bao.dieu_luat),  # Có thể nhập mới hoặc copy
            ngay_xay_ra=tin_bao.ngay_xay_ra,
            noi_xay_ra=tin_bao.noi_xay_ra,
            thong_tin_vu_an=tin_bao.noi_dung_nguon_tin,
            so_qd_phan_cong_ptt=tin_bao.so_qd_phan_cong_ptt,
            so_qd_phan_cong_dtv=tin_bao.so_qd_phan_cong_dtv,
            ngay_phan_cong=tin_bao.ngay_phan_cong,
            so_khoi_to_vu_an=None,  # Chờ nhập sau
            ngay_khoi_to_vu_an=None,
            tong_so_bi_can=0,
            thong_tin_bi_can='',
            bien_phap_ngan_chan=None,
            dieu_tra_vien=tin_bao.cong_an_phu_trach or '',
            don_vi=tin_bao.don_vi or 'CAX Phước Thái',
            trang_thai='Mới tạo',
            ngay_chuyen_tu_tin_bao=ngay_chuyen
        )
        
        db.session.add(vu_an)
        db.session.flush()  # Để lấy ID của vụ án mới
        
        # Cập nhật tin báo
        tin_bao.trang_thai = 'Chuyển thành vụ án'
        tin_bao.vu_an_id = vu_an.id
        tin_bao.updated_at = datetime.utcnow()
        
        # Ghi lịch sử chuyển đổi
        lich_su = LichSuChuyenDoi(
            tin_bao_id=tin_bao.id,
            vu_an_id=vu_an.id,
            ngay_chuyen=datetime.utcnow(),
            nguoi_chuyen=current_user.full_name if current_user else 'System',
            ly_do=data.get('ly_do', 'Điều tra phát hiện là vụ án'),
            ghi_chu=data.get('ghi_chu')
        )
        
        db.session.add(lich_su)
        db.session.commit()
        
        return jsonify({
            'message': f'Đã chuyển tin báo STT {tin_bao.stt} thành vụ án STT {vu_an.stt} thành công',
            'tin_bao': tin_bao.to_dict(),
            'vu_an': vu_an.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<tin_bao_id>/preview-vu-an', methods=['GET'])
@require_auth
def preview_vu_an(tin_bao_id):
    """Preview dữ liệu sẽ được copy khi chuyển đổi"""
    try:
        tin_bao = TinBao.query.filter_by(id=tin_bao_id, is_deleted=False).first()
        if not tin_bao:
            return jsonify({'error': 'Tin báo không tồn tại'}), 404
        
        # Trả về dữ liệu sẽ được copy
        preview_data = {
            'dieu_luat': tin_bao.dieu_luat,
            'toi_danh': tin_bao.dieu_luat,  # Mặc định copy điều luật
            'ngay_xay_ra': tin_bao.ngay_xay_ra.isoformat() if tin_bao.ngay_xay_ra else None,
            'noi_xay_ra': tin_bao.noi_xay_ra,
            'thong_tin_vu_an': tin_bao.noi_dung_nguon_tin,
            'so_qd_phan_cong_ptt': tin_bao.so_qd_phan_cong_ptt,
            'so_qd_phan_cong_dtv': tin_bao.so_qd_phan_cong_dtv,
            'ngay_phan_cong': tin_bao.ngay_phan_cong.isoformat() if tin_bao.ngay_phan_cong else None,
            'dieu_tra_vien': tin_bao.cong_an_phu_trach,
            'don_vi': tin_bao.don_vi
        }
        
        return jsonify(preview_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/export-template', methods=['GET'])
@require_auth
def export_template():
    """Xuất file Excel mẫu đúng định dạng thực tế đang sử dụng"""
    try:
        template_columns = [
            'STT',
            'Điều luật',
            'Tên nguồn tin',
            'Ngày xảy ra',
            'Nơi xảy ra',
            'Nội dung nguồn tin',
            'Số QĐ phân công PTT/Trưởng CAX ủy quyền',
            'Số QĐ phân công ĐTV',
            'Ngày phân công',
            'Kết quả giải quyết (Khởi tố, Không KT, TĐC, chuyển)',
            'Bị can (đối với vụ khởi tố)',
            'Số QĐ',
            'Ngày ra QĐ',
            'Điều tra viên',
            'Cán bộ quản lý hồ sơ',
            'Đơn vị',
            'Kiểm sát viên',
            'Gia hạn',
            'Ngày hết hạn',
            'Tình trạng hồ sơ',
            'Ghi chú'
        ]

        sample_rows = [
            [
                1173,
                'Trộm cắp tài sản',
                'Nguyễn Văn A',
                '2025-11-01',
                'ấp 6, xã Phước Thái, tỉnh Đồng Nai',
                'Khoảng 07 giờ ngày 01/11/2025 anh Nguyễn Văn A trình báo bị mất chiếc xe máy...',
                '11145',
                '',
                '2025-11-02',
                'Tiếp nhận',
                '',
                '',
                '',
                'Nguyễn Tấn Lợi',
                '',
                'CAX Phước Thái',
                '',
                0,
                '',
                'Chưa hoàn thành',
                ''
            ],
            [
                1174,
                'Gây rối trật tự công cộng',
                'Trần Thị B',
                '2025-11-02',
                'ấp 7, xã Phước Thái, tỉnh Đồng Nai',
                'Khoảng 10 giờ ngày 02/11/2025 chị Trần Thị B trình báo có nhóm thanh niên gây rối...',
                '',
                '',
                '',
                'Đang điều tra',
                '',
                '',
                '',
                'Trần Văn C',
                'Nguyễn Văn D',
                'CAX Phước Thái',
                '',
                0,
                '',
                '',
                ''
            ]
        ]

        df = pd.DataFrame(sample_rows, columns=template_columns)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Tin báo', index=False)
            worksheet = writer.sheets['Tin báo']

            for idx, col in enumerate(df.columns, 1):
                max_length = max(
                    df[col].astype(str).map(len).max(),
                    len(str(col))
                )
                col_letter = get_column_letter(idx)
                worksheet.column_dimensions[col_letter].width = min(max_length + 2, 55)

        output.seek(0)

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='Mau_Import_Tin_Bao.xlsx'
        )
    except Exception as e:
        import traceback
        print(f"Error in export_template: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@bp.route('/import', methods=['POST'])
@require_auth
def import_tin_bao():
    """Import tin báo từ file Excel"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Không tìm thấy file'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Chưa chọn file'}), 400
        
        if not file.filename.endswith(('.xlsx', '.xls')):
            return jsonify({'error': 'File phải là định dạng Excel (.xlsx hoặc .xls)'}), 400
        
        # Đọc file Excel
        df = pd.read_excel(file, sheet_name=0)
        
        # Validate columns (theo đúng header file thực tế)
        required_columns = ['Điều luật', 'Ngày xảy ra', 'Nơi xảy ra', 'Nội dung nguồn tin']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return jsonify({
                'error': f'Thiếu các cột bắt buộc: {", ".join(missing_columns)}'
            }), 400

        # Pre-validate STT trong file để tránh trùng với dữ liệu hiện có
        stt_map_by_row = {}
        provided_stts = []
        stt_errors = []
        if 'STT' in df.columns:
            for index, row in df.iterrows():
                stt_raw = row.get('STT')
                if pd.notna(stt_raw) and str(stt_raw).strip() != '':
                    try:
                        stt_int = int(float(stt_raw))
                        stt_map_by_row[index] = stt_int
                        provided_stts.append(stt_int)
                    except ValueError:
                        row_number = index + 2
                        stt_errors.append(f"Dòng {row_number}: STT phải là số nguyên")

        if stt_errors:
            return jsonify({'error': 'STT không hợp lệ trong file import', 'details': stt_errors}), 400

        duplicate_stts = [value for value, count in Counter(provided_stts).items() if count > 1]
        if duplicate_stts:
            duplicate_stts.sort()
            return jsonify({
                'error': 'Trùng STT ngay trong file import',
                'conflict_stt': duplicate_stts,
                'message': 'Mỗi tin báo phải có STT duy nhất. Vui lòng chỉnh sửa file trước khi import.'
            }), 400

        if provided_stts:
            existing_conflicts = (
                TinBao.query
                .filter(TinBao.is_deleted == False, TinBao.stt.in_(provided_stts))
                .with_entities(TinBao.stt)
                .all()
            )
            if existing_conflicts:
                conflict_values = sorted({stt for (stt,) in existing_conflicts})
                return jsonify({
                    'error': 'STT đã tồn tại trong hệ thống',
                    'conflict_stt': conflict_values,
                    'message': 'Vui lòng xóa các tin báo có STT này trong hệ thống trước khi import file Excel mới.'
                }), 400

        # Dọn sạch các bản ghi đã bị soft-delete để tránh chiếm STT
        TinBao.query.filter_by(is_deleted=True).delete(synchronize_session=False)

        def parse_date_field(raw_value, label, row_number, allow_empty=False):
            if allow_empty and (pd.isna(raw_value) or str(raw_value).strip() == ''):
                return None

            if raw_value is None or (isinstance(raw_value, float) and pd.isna(raw_value)):
                if allow_empty:
                    return None
                raise ValueError(f"Dòng {row_number}: {label} bắt buộc")

            if isinstance(raw_value, datetime):
                return raw_value.date()
            if isinstance(raw_value, date):
                return raw_value
            if isinstance(raw_value, pd.Timestamp):
                return raw_value.date()

            # Excel serial numbers
            if isinstance(raw_value, (int, float)):
                try:
                    return (pd.to_datetime('1899-12-30') + pd.to_timedelta(raw_value, unit='D')).date()
                except Exception:
                    raise ValueError(f"Dòng {row_number}: {label} không hợp lệ (giá trị số)")

            text = str(raw_value).strip()
            if text == '':
                if allow_empty:
                    return None
                raise ValueError(f"Dòng {row_number}: {label} bắt buộc")

            allowed_formats = [
                '%Y-%m-%d',
                '%d/%m/%Y',
                '%d-%m-%Y',
                '%d.%m.%Y',
                '%Y/%m/%d',
                '%d %m %Y'
            ]
            for fmt in allowed_formats:
                try:
                    return datetime.strptime(text, fmt).date()
                except ValueError:
                    continue

            try:
                return pd.to_datetime(text, dayfirst=True).date()
            except Exception:
                raise ValueError(f"Dòng {row_number}: {label} không hợp lệ (hỗ trợ các định dạng YYYY-MM-DD, DD/MM/YYYY, DD-MM-YYYY)")

        max_stt = db.session.query(func.max(TinBao.stt)).scalar() or 0
        success_count = 0
        error_count = 0
        errors = []

        def parse_int_field(raw_value):
            if pd.isna(raw_value) or str(raw_value).strip() == '':
                return 0
            try:
                return int(float(raw_value))
            except (ValueError, TypeError):
                text = str(raw_value)
                digits = re.findall(r'\d+', text)
                if digits:
                    return int(digits[0])
                return 0

        for index, row in df.iterrows():
            row_number = index + 2  # header = row 1
            try:
                provided_stt = stt_map_by_row.get(index)
                if provided_stt is not None:
                    stt_value = provided_stt
                    if provided_stt > max_stt:
                        max_stt = provided_stt
                else:
                    max_stt += 1
                    stt_value = max_stt

                dieu_luat = str(row.get('Điều luật', '')).strip()
                noi_xay_ra = str(row.get('Nơi xảy ra', '')).strip()
                noi_dung = str(row.get('Nội dung nguồn tin', '')).strip()

                if not dieu_luat or len(dieu_luat) < 2:
                    errors.append(f"Dòng {row_number}: Điều luật bắt buộc, tối thiểu 2 ký tự")
                    error_count += 1
                    continue

                if not noi_xay_ra or len(noi_xay_ra) < 5:
                    errors.append(f"Dòng {row_number}: Nơi xảy ra bắt buộc, tối thiểu 5 ký tự")
                    error_count += 1
                    continue

                if not noi_dung or len(noi_dung) < 20:
                    errors.append(f"Dòng {row_number}: Nội dung nguồn tin bắt buộc, tối thiểu 20 ký tự")
                    error_count += 1
                    continue

                try:
                    ngay_xay_ra = parse_date_field(row.get('Ngày xảy ra'), 'Ngày xảy ra', row_number)
                except ValueError as e:
                    errors.append(str(e))
                    error_count += 1
                    continue

                try:
                    ngay_phan_cong = parse_date_field(row.get('Ngày phân công'), 'Ngày phân công', row_number, allow_empty=True)
                except ValueError as e:
                    errors.append(str(e))
                    error_count += 1
                    continue

                try:
                    ngay_het_han = parse_date_field(row.get('Ngày hết hạn'), 'Ngày hết hạn', row_number, allow_empty=True)
                except ValueError as e:
                    errors.append(str(e))
                    error_count += 1
                    continue

                gia_han_value = parse_int_field(row.get('Gia hạn'))

                trang_thai_from_file = str(row.get('Kết quả giải quyết (Khởi tố, Không KT, TĐC, chuyển)', '')).strip() if pd.notna(row.get('Kết quả giải quyết (Khởi tố, Không KT, TĐC, chuyển)')) else ''

                extra_notes = []
                so_qd_text = str(row.get('Số QĐ', '')).strip() if pd.notna(row.get('Số QĐ')) else ''
                if so_qd_text:
                    extra_notes.append(f"Số QĐ: {so_qd_text}")
                ngay_ra_qd_text = str(row.get('Ngày ra QĐ', '')).strip() if pd.notna(row.get('Ngày ra QĐ')) else ''
                if ngay_ra_qd_text:
                    extra_notes.append(f"Ngày ra QĐ: {ngay_ra_qd_text}")
                can_bo_quan_ly = str(row.get('Cán bộ quản lý hồ sơ', '')).strip() if pd.notna(row.get('Cán bộ quản lý hồ sơ')) else ''
                if can_bo_quan_ly:
                    extra_notes.append(f"Cán bộ quản lý hồ sơ: {can_bo_quan_ly}")
                ghi_chu_raw = str(row.get('Ghi chú', '')).strip() if pd.notna(row.get('Ghi chú')) else ''
                if ghi_chu_raw:
                    extra_notes.append(ghi_chu_raw)

                tin_bao = TinBao(
                    stt=stt_value,
                    dieu_luat=dieu_luat,
                    ten_nguon_tin=str(row.get('Tên nguồn tin', '')).strip() if pd.notna(row.get('Tên nguồn tin')) else None,
                    ngay_xay_ra=ngay_xay_ra,
                    noi_xay_ra=noi_xay_ra,
                    noi_dung_nguon_tin=noi_dung,
                    so_qd_phan_cong_ptt=str(row.get('Số QĐ phân công PTT/Trưởng CAX ủy quyền', '')).strip() if pd.notna(row.get('Số QĐ phân công PTT/Trưởng CAX ủy quyền')) else None,
                    so_qd_phan_cong_dtv=str(row.get('Số QĐ phân công ĐTV', '')).strip() if pd.notna(row.get('Số QĐ phân công ĐTV')) else None,
                    ngay_phan_cong=ngay_phan_cong,
                    ket_qua_giai_quyet=trang_thai_from_file if trang_thai_from_file else None,
                    dia_chi_bi_hai=None,
                    thong_tin_doi_tuong=str(row.get('Bị can (đối với vụ khởi tố)', '')).strip() if pd.notna(row.get('Bị can (đối với vụ khởi tố)')) else None,
                    cong_an_phu_trach=str(row.get('Điều tra viên', '')).strip() if pd.notna(row.get('Điều tra viên')) else None,
                    don_vi=str(row.get('Đơn vị', 'CAX Phước Thái')).strip() if pd.notna(row.get('Đơn vị')) else 'CAX Phước Thái',
                    kiem_sat_vien=str(row.get('Kiểm sát viên', '')).strip() if pd.notna(row.get('Kiểm sát viên')) else None,
                    gia_han=gia_han_value,
                    ngay_het_han=ngay_het_han,
                    tinh_trang_ho_so=str(row.get('Tình trạng hồ sơ', '')).strip() if pd.notna(row.get('Tình trạng hồ sơ')) else None,
                    ghi_chu=' | '.join(extra_notes) if extra_notes else None,
                    trang_thai=trang_thai_from_file if trang_thai_from_file else 'Tiếp nhận'
                )

                db.session.add(tin_bao)
                success_count += 1

            except Exception as e:
                errors.append(f"Dòng {row_number}: {str(e)}")
                error_count += 1
                continue
        
        db.session.commit()
        
        return jsonify({
            'message': f'Import thành công {success_count} tin báo',
            'success_count': success_count,
            'error_count': error_count,
            'errors': errors[:10]  # Chỉ trả về 10 lỗi đầu tiên
        }), 200
        
    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"Error in import_tin_bao: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

