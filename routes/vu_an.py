from flask import Blueprint, request, jsonify
from models import VuAn, BiCan, TamGiam, TinBao
from database import db
from utils.auth import require_auth, require_admin, get_current_user
from datetime import datetime, timedelta
from sqlalchemy import func, or_

bp = Blueprint('vu_an', __name__)

@bp.route('', methods=['GET'])
@require_auth
def get_vu_an_list():
    """Danh sách vụ án với search, filter, pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '').strip()
        trang_thai = request.args.get('trang_thai', '').strip()
        bien_phap = request.args.get('bien_phap_ngan_chan', '').strip()
        dieu_tra_vien = request.args.get('dieu_tra_vien', '').strip()
        
        query = VuAn.query.filter_by(is_deleted=False)
        
        # Search
        if search:
            query = query.filter(
                or_(
                    VuAn.toi_danh.ilike(f'%{search}%'),
                    VuAn.dieu_luat.ilike(f'%{search}%'),
                    VuAn.noi_xay_ra.ilike(f'%{search}%'),
                    VuAn.thong_tin_vu_an.ilike(f'%{search}%'),
                    VuAn.so_khoi_to_vu_an.ilike(f'%{search}%')
                )
            )
        
        # Filter
        if trang_thai:
            query = query.filter(VuAn.trang_thai == trang_thai)
        if bien_phap:
            query = query.filter(VuAn.bien_phap_ngan_chan == bien_phap)
        if dieu_tra_vien:
            query = query.filter(VuAn.dieu_tra_vien.ilike(f'%{dieu_tra_vien}%'))
        
        # Pagination
        total = query.count()
        items = query.order_by(VuAn.stt.desc()).offset((page - 1) * per_page).limit(per_page).all()
        
        # Include tin_bao info if exists
        result_items = []
        for item in items:
            item_dict = item.to_dict()
            if item.tin_bao_id:
                tin_bao = TinBao.query.get(item.tin_bao_id)
                if tin_bao:
                    item_dict['tin_bao_stt'] = tin_bao.stt
            result_items.append(item_dict)
        
        return jsonify({
            'items': result_items,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }), 200
    except Exception as e:
        import traceback
        print(f"Error in get_vu_an_list: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@bp.route('', methods=['POST'])
@require_auth
def create_vu_an():
    """Tạo vụ án mới (độc lập hoặc từ tin báo)"""
    try:
        data = request.get_json()
        
        # Validation
        if not data.get('dieu_luat'):
            return jsonify({'error': 'Điều luật bắt buộc nhập'}), 400
        if not data.get('toi_danh'):
            return jsonify({'error': 'Tội danh bắt buộc nhập'}), 400
        if not data.get('ngay_xay_ra'):
            return jsonify({'error': 'Ngày xảy ra bắt buộc nhập'}), 400
        if not data.get('noi_xay_ra'):
            return jsonify({'error': 'Nơi xảy ra bắt buộc nhập'}), 400
        if not data.get('thong_tin_vu_an'):
            return jsonify({'error': 'Thông tin vụ án bắt buộc nhập'}), 400
        if not data.get('dieu_tra_vien'):
            return jsonify({'error': 'Điều tra viên bắt buộc nhập'}), 400
        
        # Auto-generate STT
        max_stt = db.session.query(func.max(VuAn.stt)).scalar() or 0
        new_stt = max_stt + 1
        
        # Parse dates
        ngay_xay_ra = datetime.strptime(data['ngay_xay_ra'], '%Y-%m-%d').date() if data.get('ngay_xay_ra') else None
        ngay_phan_cong = datetime.strptime(data['ngay_phan_cong'], '%Y-%m-%d').date() if data.get('ngay_phan_cong') else None
        ngay_khoi_to_vu_an = datetime.strptime(data['ngay_khoi_to_vu_an'], '%Y-%m-%d').date() if data.get('ngay_khoi_to_vu_an') else None
        ngay_het_han = datetime.strptime(data['ngay_het_han'], '%Y-%m-%d').date() if data.get('ngay_het_han') else None
        ngay_chuyen_tu_tin_bao = datetime.strptime(data['ngay_chuyen_tu_tin_bao'], '%Y-%m-%d').date() if data.get('ngay_chuyen_tu_tin_bao') else None
        
        vu_an = VuAn(
            stt=new_stt,
            tin_bao_id=data.get('tin_bao_id'),
            dieu_luat=data['dieu_luat'],
            toi_danh=data['toi_danh'],
            ngay_xay_ra=ngay_xay_ra,
            noi_xay_ra=data['noi_xay_ra'],
            thong_tin_vu_an=data['thong_tin_vu_an'],
            so_qd_phan_cong_ptt=data.get('so_qd_phan_cong_ptt'),
            so_qd_phan_cong_dtv=data.get('so_qd_phan_cong_dtv'),
            ngay_phan_cong=ngay_phan_cong,
            so_khoi_to_vu_an=data.get('so_khoi_to_vu_an'),
            ngay_khoi_to_vu_an=ngay_khoi_to_vu_an,
            tong_so_bi_can=data.get('tong_so_bi_can', 0),
            thong_tin_bi_can=data.get('thong_tin_bi_can', ''),
            bien_phap_ngan_chan=data.get('bien_phap_ngan_chan'),
            so_khoi_to_bi_can=data.get('so_khoi_to_bi_can'),
            ngay_khoi_to_bi_can=datetime.strptime(data['ngay_khoi_to_bi_can'], '%Y-%m-%d').date() if data.get('ngay_khoi_to_bi_can') else None,
            dang_vien=data.get('dang_vien'),
            ket_qua_giai_quyet=data.get('ket_qua_giai_quyet'),
            bi_can_giai_quyet=data.get('bi_can_giai_quyet'),
            dieu_tra_vien=data['dieu_tra_vien'],
            can_bo_quan_ly_ho_so=data.get('can_bo_quan_ly_ho_so'),
            don_vi=data.get('don_vi', 'CAX Phước Thái'),
            kiem_sat_vien=data.get('kiem_sat_vien'),
            ngay_het_han=ngay_het_han,
            tinh_trang_ho_so=data.get('tinh_trang_ho_so'),
            ghi_chu=data.get('ghi_chu'),
            trang_thai=data.get('trang_thai', 'Mới tạo'),
            ngay_chuyen_tu_tin_bao=ngay_chuyen_tu_tin_bao
        )
        
        db.session.add(vu_an)
        db.session.commit()
        
        return jsonify({'message': 'Tạo vụ án thành công', 'data': vu_an.to_dict()}), 201
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': f'Lỗi định dạng ngày: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<vu_an_id>', methods=['GET'])
@require_auth
def get_vu_an_detail(vu_an_id):
    """Chi tiết vụ án kèm danh sách bị can"""
    try:
        vu_an = VuAn.query.filter_by(id=vu_an_id, is_deleted=False).first()
        if not vu_an:
            return jsonify({'error': 'Vụ án không tồn tại'}), 404
        
        result = vu_an.to_dict()
        
        # Thêm thông tin tin báo nếu có
        if vu_an.tin_bao_id:
            tin_bao = TinBao.query.get(vu_an.tin_bao_id)
            if tin_bao:
                result['tin_bao'] = {
                    'id': tin_bao.id,
                    'stt': tin_bao.stt,
                    'dieu_luat': tin_bao.dieu_luat
                }
        
        # Thêm danh sách bị can
        bi_can_list = BiCan.query.filter_by(vu_an_id=vu_an_id, is_deleted=False).all()
        result['bi_can_list'] = [bc.to_dict() for bc in bi_can_list]
        
        # Thêm danh sách tạm giam
        tam_giam_list = TamGiam.query.filter_by(vu_an_id=vu_an_id, is_deleted=False).all()
        result['tam_giam_list'] = [tg.to_dict() for tg in tam_giam_list]
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<vu_an_id>', methods=['PUT'])
@require_auth
def update_vu_an(vu_an_id):
    """Cập nhật vụ án"""
    try:
        vu_an = VuAn.query.filter_by(id=vu_an_id, is_deleted=False).first()
        if not vu_an:
            return jsonify({'error': 'Vụ án không tồn tại'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'dieu_luat' in data:
            vu_an.dieu_luat = data['dieu_luat']
        if 'toi_danh' in data:
            vu_an.toi_danh = data['toi_danh']
        if 'ngay_xay_ra' in data:
            vu_an.ngay_xay_ra = datetime.strptime(data['ngay_xay_ra'], '%Y-%m-%d').date()
        if 'noi_xay_ra' in data:
            vu_an.noi_xay_ra = data['noi_xay_ra']
        if 'thong_tin_vu_an' in data:
            vu_an.thong_tin_vu_an = data['thong_tin_vu_an']
        if 'so_qd_phan_cong_ptt' in data:
            vu_an.so_qd_phan_cong_ptt = data['so_qd_phan_cong_ptt']
        if 'so_qd_phan_cong_dtv' in data:
            vu_an.so_qd_phan_cong_dtv = data['so_qd_phan_cong_dtv']
        if 'ngay_phan_cong' in data:
            vu_an.ngay_phan_cong = datetime.strptime(data['ngay_phan_cong'], '%Y-%m-%d').date() if data['ngay_phan_cong'] else None
        if 'dieu_tra_vien' in data:
            vu_an.dieu_tra_vien = data['dieu_tra_vien']
        if 'can_bo_quan_ly_ho_so' in data:
            vu_an.can_bo_quan_ly_ho_so = data['can_bo_quan_ly_ho_so']
        if 'kiem_sat_vien' in data:
            vu_an.kiem_sat_vien = data['kiem_sat_vien']
        if 'ngay_het_han' in data:
            vu_an.ngay_het_han = datetime.strptime(data['ngay_het_han'], '%Y-%m-%d').date() if data['ngay_het_han'] else None
        if 'tinh_trang_ho_so' in data:
            vu_an.tinh_trang_ho_so = data['tinh_trang_ho_so']
        if 'ghi_chu' in data:
            vu_an.ghi_chu = data['ghi_chu']
        if 'ket_qua_giai_quyet' in data:
            vu_an.ket_qua_giai_quyet = data['ket_qua_giai_quyet']
        if 'bi_can_giai_quyet' in data:
            vu_an.bi_can_giai_quyet = data['bi_can_giai_quyet']
        if 'trang_thai' in data:
            vu_an.trang_thai = data['trang_thai']
        
        vu_an.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': 'Cập nhật vụ án thành công', 'data': vu_an.to_dict()}), 200
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': f'Lỗi định dạng ngày: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<vu_an_id>', methods=['DELETE'])
@require_admin
def delete_vu_an(vu_an_id):
    """Xóa vụ án (soft delete)"""
    try:
        vu_an = VuAn.query.filter_by(id=vu_an_id, is_deleted=False).first()
        if not vu_an:
            return jsonify({'error': 'Vụ án không tồn tại'}), 404
        
        vu_an.is_deleted = True
        vu_an.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': 'Xóa vụ án thành công'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<vu_an_id>/khoi-to', methods=['POST'])
@require_auth
def khoi_to_vu_an(vu_an_id):
    """Khởi tố vụ án"""
    try:
        vu_an = VuAn.query.filter_by(id=vu_an_id, is_deleted=False).first()
        if not vu_an:
            return jsonify({'error': 'Vụ án không tồn tại'}), 404
        
        # Validation: Chưa được khởi tố
        if vu_an.so_khoi_to_vu_an:
            return jsonify({'error': 'Vụ án đã được khởi tố trước đó'}), 400
        
        data = request.get_json()
        
        if not data.get('so_khoi_to_vu_an'):
            return jsonify({'error': 'Số khởi tố vụ án bắt buộc nhập'}), 400
        if not data.get('ngay_khoi_to_vu_an'):
            return jsonify({'error': 'Ngày khởi tố vụ án bắt buộc nhập'}), 400
        
        # Check unique số khởi tố
        existing = VuAn.query.filter_by(so_khoi_to_vu_an=data['so_khoi_to_vu_an'], is_deleted=False).first()
        if existing and existing.id != vu_an_id:
            return jsonify({'error': 'Số khởi tố vụ án đã tồn tại'}), 400
        
        ngay_khoi_to = datetime.strptime(data['ngay_khoi_to_vu_an'], '%Y-%m-%d').date()
        
        # Validation: Ngày khởi tố không sau hôm nay
        if ngay_khoi_to > datetime.utcnow().date():
            return jsonify({'error': 'Ngày khởi tố không được sau hôm nay'}), 400
        
        # Update
        vu_an.so_khoi_to_vu_an = data['so_khoi_to_vu_an']
        vu_an.ngay_khoi_to_vu_an = ngay_khoi_to
        vu_an.trang_thai = 'Khởi tố vụ án'
        vu_an.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': f'Vụ án STT {vu_an.stt} đã được khởi tố thành công',
            'data': vu_an.to_dict()
        }), 200
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': f'Lỗi định dạng ngày: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<vu_an_id>/ket-qua', methods=['PUT'])
@require_auth
def update_ket_qua(vu_an_id):
    """Cập nhật kết quả giải quyết vụ án"""
    try:
        vu_an = VuAn.query.filter_by(id=vu_an_id, is_deleted=False).first()
        if not vu_an:
            return jsonify({'error': 'Vụ án không tồn tại'}), 404
        
        data = request.get_json()
        
        if 'ket_qua_giai_quyet' in data:
            vu_an.ket_qua_giai_quyet = data['ket_qua_giai_quyet']
        if 'bi_can_giai_quyet' in data:
            vu_an.bi_can_giai_quyet = data['bi_can_giai_quyet']
        if 'trang_thai' in data:
            vu_an.trang_thai = data['trang_thai']
        
        vu_an.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': 'Cập nhật kết quả giải quyết thành công', 'data': vu_an.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

