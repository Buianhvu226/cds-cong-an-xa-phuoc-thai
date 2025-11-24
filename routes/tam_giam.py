from flask import Blueprint, request, jsonify
from models import TamGiam, VuAn, BiCan
from database import db
from utils.auth import require_auth, require_admin, get_current_user
from datetime import datetime, timedelta
from sqlalchemy import func, or_

bp = Blueprint('tam_giam', __name__)

@bp.route('', methods=['GET'])
@require_auth
def get_tam_giam_list():
    """Danh sách tạm giam với search, filter, pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '').strip()
        trang_thai = request.args.get('trang_thai_giam', '').strip()
        
        query = TamGiam.query.filter_by(is_deleted=False)
        
        # Search
        if search:
            query = query.join(BiCan).filter(
                or_(
                    BiCan.ho_ten.ilike(f'%{search}%'),
                    VuAn.toi_danh.ilike(f'%{search}%')
                )
            )
        
        # Filter
        if trang_thai:
            query = query.filter(TamGiam.trang_thai_giam == trang_thai)
        
        # Pagination
        total = query.count()
        items = query.order_by(TamGiam.ngay_bat_giam.desc()).offset((page - 1) * per_page).limit(per_page).all()
        
        # Include thông tin bị can và vụ án
        result_items = []
        for item in items:
            item_dict = item.to_dict()
            bi_can = BiCan.query.get(item.bi_can_id)
            vu_an = VuAn.query.get(item.vu_an_id)
            if bi_can:
                item_dict['bi_can'] = {
                    'ho_ten': bi_can.ho_ten,
                    'nam_sinh': bi_can.nam_sinh
                }
            if vu_an:
                item_dict['vu_an'] = {
                    'stt': vu_an.stt,
                    'toi_danh': vu_an.toi_danh
                }
            result_items.append(item_dict)
        
        return jsonify({
            'items': result_items,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('', methods=['POST'])
@require_auth
def create_tam_giam():
    """Tạo tạm giam"""
    try:
        data = request.get_json()
        
        # Validation
        if not data.get('vu_an_id'):
            return jsonify({'error': 'Vụ án bắt buộc chọn'}), 400
        if not data.get('bi_can_id'):
            return jsonify({'error': 'Bị can bắt buộc chọn'}), 400
        if not data.get('ngay_bat_giam'):
            return jsonify({'error': 'Ngày bắt giam bắt buộc nhập'}), 400
        if not data.get('ngay_het_han_giam'):
            return jsonify({'error': 'Ngày hết hạn giam bắt buộc nhập'}), 400
        if not data.get('ly_do_tam_giam'):
            return jsonify({'error': 'Lý do tạm giam bắt buộc nhập'}), 400
        
        # Parse dates
        ngay_bat_giam = datetime.strptime(data['ngay_bat_giam'], '%Y-%m-%d').date()
        ngay_het_han = datetime.strptime(data['ngay_het_han_giam'], '%Y-%m-%d').date()
        
        # Validation: Ngày hết hạn phải sau ngày bắt
        if ngay_het_han <= ngay_bat_giam:
            return jsonify({'error': 'Ngày hết hạn giam phải sau ngày bắt giam'}), 400
        
        tam_giam = TamGiam(
            vu_an_id=data['vu_an_id'],
            bi_can_id=data['bi_can_id'],
            ngay_bat_giam=ngay_bat_giam,
            ngay_het_han_giam=ngay_het_han,
            ly_do_tam_giam=data['ly_do_tam_giam'],
            trang_thai_giam=data.get('trang_thai_giam', 'Đang giam'),
            ghi_chu=data.get('ghi_chu')
        )
        
        db.session.add(tam_giam)
        db.session.commit()
        
        return jsonify({'message': 'Tạo tạm giam thành công', 'data': tam_giam.to_dict()}), 201
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': f'Lỗi định dạng ngày: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<tam_giam_id>', methods=['GET'])
@require_auth
def get_tam_giam_detail(tam_giam_id):
    """Chi tiết tạm giam"""
    try:
        tam_giam = TamGiam.query.filter_by(id=tam_giam_id, is_deleted=False).first()
        if not tam_giam:
            return jsonify({'error': 'Tạm giam không tồn tại'}), 404
        
        result = tam_giam.to_dict()
        
        # Include thông tin bị can và vụ án
        bi_can = BiCan.query.get(tam_giam.bi_can_id)
        vu_an = VuAn.query.get(tam_giam.vu_an_id)
        if bi_can:
            result['bi_can'] = bi_can.to_dict()
        if vu_an:
            result['vu_an'] = {
                'stt': vu_an.stt,
                'toi_danh': vu_an.toi_danh
            }
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<tam_giam_id>', methods=['PUT'])
@require_auth
def update_tam_giam(tam_giam_id):
    """Cập nhật tạm giam (hết hạn, giải phóng)"""
    try:
        tam_giam = TamGiam.query.filter_by(id=tam_giam_id, is_deleted=False).first()
        if not tam_giam:
            return jsonify({'error': 'Tạm giam không tồn tại'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'ngay_bat_giam' in data:
            tam_giam.ngay_bat_giam = datetime.strptime(data['ngay_bat_giam'], '%Y-%m-%d').date()
        if 'ngay_het_han_giam' in data:
            tam_giam.ngay_het_han_giam = datetime.strptime(data['ngay_het_han_giam'], '%Y-%m-%d').date()
        if 'ly_do_tam_giam' in data:
            tam_giam.ly_do_tam_giam = data['ly_do_tam_giam']
        if 'trang_thai_giam' in data:
            tam_giam.trang_thai_giam = data['trang_thai_giam']
        if 'ghi_chu' in data:
            tam_giam.ghi_chu = data['ghi_chu']
        
        tam_giam.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': 'Cập nhật tạm giam thành công', 'data': tam_giam.to_dict()}), 200
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': f'Lỗi định dạng ngày: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<tam_giam_id>', methods=['DELETE'])
@require_admin
def delete_tam_giam(tam_giam_id):
    """Xóa tạm giam (soft delete)"""
    try:
        tam_giam = TamGiam.query.filter_by(id=tam_giam_id, is_deleted=False).first()
        if not tam_giam:
            return jsonify({'error': 'Tạm giam không tồn tại'}), 404
        
        tam_giam.is_deleted = True
        tam_giam.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': 'Xóa tạm giam thành công'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

