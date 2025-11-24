from flask import Blueprint, request, jsonify
from models import BiCan, VuAn, TamGiam
from database import db
from utils.auth import require_auth, require_admin, get_current_user
from datetime import datetime, timedelta

bp = Blueprint('bi_can', __name__)

@bp.route('/vu-an/<vu_an_id>/bi-can', methods=['GET'])
@require_auth
def get_bi_can_list(vu_an_id):
    """Danh sách bị can trong vụ án"""
    try:
        vu_an = VuAn.query.filter_by(id=vu_an_id, is_deleted=False).first()
        if not vu_an:
            return jsonify({'error': 'Vụ án không tồn tại'}), 404
        
        bi_can_list = BiCan.query.filter_by(vu_an_id=vu_an_id, is_deleted=False).order_by(BiCan.created_at).all()
        
        return jsonify([bc.to_dict() for bc in bi_can_list]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/vu-an/<vu_an_id>/bi-can', methods=['POST'])
@require_auth
def create_bi_can(vu_an_id):
    """Thêm bị can vào vụ án"""
    try:
        vu_an = VuAn.query.filter_by(id=vu_an_id, is_deleted=False).first()
        if not vu_an:
            return jsonify({'error': 'Vụ án không tồn tại'}), 404
        
        data = request.get_json()
        
        # Validation
        if not data.get('ho_ten') or len(data.get('ho_ten', '')) < 5:
            return jsonify({'error': 'Họ tên bắt buộc nhập, tối thiểu 5 ký tự'}), 400
        if not data.get('nam_sinh'):
            return jsonify({'error': 'Năm sinh bắt buộc nhập'}), 400
        if not data.get('dia_chi_thuong_tru'):
            return jsonify({'error': 'Địa chỉ thường trú bắt buộc nhập'}), 400
        if not data.get('bien_phap_ngan_chan'):
            return jsonify({'error': 'Biện pháp ngăn chặn bắt buộc chọn'}), 400
        
        # Validation năm sinh
        nam_sinh = int(data['nam_sinh'])
        current_year = datetime.now().year
        if nam_sinh < 1900 or nam_sinh > current_year:
            return jsonify({'error': f'Năm sinh không hợp lệ (1900 - {current_year})'}), 400
        
        # Tạo bị can
        bi_can = BiCan(
            vu_an_id=vu_an_id,
            ho_ten=data['ho_ten'],
            nam_sinh=nam_sinh,
            dia_chi_thuong_tru=data['dia_chi_thuong_tru'],
            so_cmnd=data.get('so_cmnd'),
            nghe_nghiep=data.get('nghe_nghiep'),
            dang_vien=data.get('dang_vien', False),
            bien_phap_ngan_chan=data['bien_phap_ngan_chan'],
            trang_thai='Chưa khởi tố'
        )
        
        db.session.add(bi_can)
        db.session.flush()
        
        # Cập nhật vụ án: tăng tổng số bị can
        vu_an.tong_so_bi_can = (vu_an.tong_so_bi_can or 0) + 1
        
        # Cập nhật thông tin bị can (danh sách text)
        bi_can_list = BiCan.query.filter_by(vu_an_id=vu_an_id, is_deleted=False).all()
        thong_tin_list = [f"{bc.ho_ten} ({bc.nam_sinh})" for bc in bi_can_list]
        vu_an.thong_tin_bi_can = ', '.join(thong_tin_list)
        
        # Nếu biện pháp = "Tạm giam" → Tự động tạo record tạm giam
        if data['bien_phap_ngan_chan'] == 'Tạm giam':
            ngay_bat_giam = datetime.utcnow().date()
            # Mặc định 30 ngày (có thể điều chỉnh)
            ngay_het_han = ngay_bat_giam + timedelta(days=30)
            
            tam_giam = TamGiam(
                vu_an_id=vu_an_id,
                bi_can_id=bi_can.id,
                ngay_bat_giam=ngay_bat_giam,
                ngay_het_han_giam=ngay_het_han,
                ly_do_tam_giam=data.get('ly_do_tam_giam', 'Khởi tố bị can'),
                trang_thai_giam='Đang giam'
            )
            db.session.add(tam_giam)
        
        vu_an.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Thêm bị can thành công',
            'data': bi_can.to_dict()
        }), 201
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': f'Lỗi dữ liệu: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/vu-an/<vu_an_id>/bi-can/<bi_can_id>', methods=['GET'])
@require_auth
def get_bi_can_detail(vu_an_id, bi_can_id):
    """Chi tiết bị can"""
    try:
        bi_can = BiCan.query.filter_by(id=bi_can_id, vu_an_id=vu_an_id, is_deleted=False).first()
        if not bi_can:
            return jsonify({'error': 'Bị can không tồn tại'}), 404
        
        return jsonify(bi_can.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/vu-an/<vu_an_id>/bi-can/<bi_can_id>', methods=['PUT'])
@require_auth
def update_bi_can(vu_an_id, bi_can_id):
    """Cập nhật bị can"""
    try:
        bi_can = BiCan.query.filter_by(id=bi_can_id, vu_an_id=vu_an_id, is_deleted=False).first()
        if not bi_can:
            return jsonify({'error': 'Bị can không tồn tại'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'ho_ten' in data:
            if len(data['ho_ten']) < 5:
                return jsonify({'error': 'Họ tên tối thiểu 5 ký tự'}), 400
            bi_can.ho_ten = data['ho_ten']
        if 'nam_sinh' in data:
            nam_sinh = int(data['nam_sinh'])
            current_year = datetime.now().year
            if nam_sinh < 1900 or nam_sinh > current_year:
                return jsonify({'error': f'Năm sinh không hợp lệ (1900 - {current_year})'}), 400
            bi_can.nam_sinh = nam_sinh
        if 'dia_chi_thuong_tru' in data:
            bi_can.dia_chi_thuong_tru = data['dia_chi_thuong_tru']
        if 'so_cmnd' in data:
            bi_can.so_cmnd = data['so_cmnd']
        if 'nghe_nghiep' in data:
            bi_can.nghe_nghiep = data['nghe_nghiep']
        if 'dang_vien' in data:
            bi_can.dang_vien = data['dang_vien']
        if 'bien_phap_ngan_chan' in data:
            bi_can.bien_phap_ngan_chan = data['bien_phap_ngan_chan']
        
        bi_can.updated_at = datetime.utcnow()
        
        # Cập nhật thông tin bị can ở vụ án
        vu_an = bi_can.vu_an
        bi_can_list = BiCan.query.filter_by(vu_an_id=vu_an_id, is_deleted=False).all()
        thong_tin_list = [f"{bc.ho_ten} ({bc.nam_sinh})" for bc in bi_can_list]
        vu_an.thong_tin_bi_can = ', '.join(thong_tin_list)
        vu_an.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({'message': 'Cập nhật bị can thành công', 'data': bi_can.to_dict()}), 200
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': f'Lỗi dữ liệu: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/vu-an/<vu_an_id>/bi-can/<bi_can_id>', methods=['DELETE'])
@require_admin
def delete_bi_can(vu_an_id, bi_can_id):
    """Xóa bị can"""
    try:
        bi_can = BiCan.query.filter_by(id=bi_can_id, vu_an_id=vu_an_id, is_deleted=False).first()
        if not bi_can:
            return jsonify({'error': 'Bị can không tồn tại'}), 404
        
        vu_an = bi_can.vu_an
        
        # Soft delete
        bi_can.is_deleted = True
        bi_can.updated_at = datetime.utcnow()
        
        # Cập nhật vụ án: giảm tổng số bị can
        vu_an.tong_so_bi_can = max(0, (vu_an.tong_so_bi_can or 0) - 1)
        
        # Cập nhật thông tin bị can
        bi_can_list = BiCan.query.filter_by(vu_an_id=vu_an_id, is_deleted=False).all()
        thong_tin_list = [f"{bc.ho_ten} ({bc.nam_sinh})" for bc in bi_can_list]
        vu_an.thong_tin_bi_can = ', '.join(thong_tin_list) if thong_tin_list else ''
        vu_an.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({'message': 'Xóa bị can thành công'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/bi-can/<bi_can_id>/khoi-to', methods=['POST'])
@require_auth
def khoi_to_bi_can(bi_can_id):
    """Khởi tố bị can"""
    try:
        bi_can = BiCan.query.filter_by(id=bi_can_id, is_deleted=False).first()
        if not bi_can:
            return jsonify({'error': 'Bị can không tồn tại'}), 404
        
        # Validation: Chưa được khởi tố
        if bi_can.so_khoi_to_bi_can:
            return jsonify({'error': 'Bị can đã được khởi tố trước đó'}), 400
        
        data = request.get_json()
        
        if not data.get('so_khoi_to_bi_can'):
            return jsonify({'error': 'Số khởi tố bị can bắt buộc nhập'}), 400
        if not data.get('ngay_khoi_to'):
            return jsonify({'error': 'Ngày khởi tố bắt buộc nhập'}), 400
        
        ngay_khoi_to = datetime.strptime(data['ngay_khoi_to'], '%Y-%m-%d').date()
        
        # Validation: Ngày khởi tố không sau hôm nay
        if ngay_khoi_to > datetime.utcnow().date():
            return jsonify({'error': 'Ngày khởi tố không được sau hôm nay'}), 400
        
        # Update bị can
        bi_can.so_khoi_to_bi_can = data['so_khoi_to_bi_can']
        bi_can.ngay_khoi_to = ngay_khoi_to
        bi_can.trang_thai = 'Đã khởi tố'
        if 'bien_phap_ngan_chan' in data:
            bi_can.bien_phap_ngan_chan = data['bien_phap_ngan_chan']
        bi_can.updated_at = datetime.utcnow()
        
        # Nếu biện pháp = "Tạm giam" → Tạo/cập nhật tạm giam
        if data.get('bien_phap_ngan_chan') == 'Tạm giam':
            # Kiểm tra đã có tạm giam chưa
            tam_giam = TamGiam.query.filter_by(bi_can_id=bi_can_id, is_deleted=False).first()
            
            if not tam_giam:
                ngay_bat_giam = ngay_khoi_to
                ngay_het_han = data.get('ngay_het_han_giam')
                if ngay_het_han:
                    ngay_het_han = datetime.strptime(ngay_het_han, '%Y-%m-%d').date()
                else:
                    # Mặc định 30 ngày
                    ngay_het_han = ngay_bat_giam + timedelta(days=30)
                
                tam_giam = TamGiam(
                    vu_an_id=bi_can.vu_an_id,
                    bi_can_id=bi_can_id,
                    ngay_bat_giam=ngay_bat_giam,
                    ngay_het_han_giam=ngay_het_han,
                    ly_do_tam_giam=data.get('ly_do_tam_giam', 'Khởi tố bị can'),
                    trang_thai_giam='Đang giam'
                )
                db.session.add(tam_giam)
            else:
                # Cập nhật tạm giam hiện có
                if data.get('ngay_het_han_giam'):
                    tam_giam.ngay_het_han_giam = datetime.strptime(data['ngay_het_han_giam'], '%Y-%m-%d').date()
                tam_giam.trang_thai_giam = 'Đang giam'
                tam_giam.updated_at = datetime.utcnow()
        
        # Cập nhật vụ án
        vu_an = bi_can.vu_an
        vu_an.so_khoi_to_bi_can = data['so_khoi_to_bi_can']  # Lưu số khởi tố bị can đầu tiên
        vu_an.ngay_khoi_to_bi_can = ngay_khoi_to
        if vu_an.trang_thai == 'Khởi tố vụ án':
            vu_an.trang_thai = 'Khởi tố bị can'
        elif vu_an.trang_thai == 'Mới tạo':
            vu_an.trang_thai = 'Khởi tố bị can'
        vu_an.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': f'Bị can {bi_can.ho_ten} đã được khởi tố thành công',
            'data': bi_can.to_dict()
        }), 200
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': f'Lỗi định dạng ngày: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

