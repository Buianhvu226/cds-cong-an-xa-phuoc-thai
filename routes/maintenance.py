from flask import Blueprint, request, jsonify
from services.maintenance_service import MaintenanceService
from utils.auth import require_auth, require_admin

bp = Blueprint('maintenance', __name__)
maintenance_service = MaintenanceService()

@bp.route('/<asset_id>', methods=['GET'])
@require_auth
def get_maintenance_history(asset_id):
    """Get maintenance history for an asset"""
    try:
        ma_tai_san = request.args.get('ma_tai_san', asset_id)
        result = maintenance_service.get_history(ma_tai_san)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<asset_id>', methods=['POST'])
@require_auth
def create_maintenance_record(asset_id):
    """Create new maintenance record"""
    try:
        data = request.get_json()
        ma_tai_san = data.get('ma_tai_san') or request.args.get('ma_tai_san') or asset_id
        data['ma_tai_san'] = ma_tai_san
        
        result = maintenance_service.create_record(data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<record_id>', methods=['PUT'])
@require_auth
def update_maintenance_record(record_id):
    """Update maintenance record"""
    try:
        data = request.get_json()
        result = maintenance_service.update_record(record_id, data)
        if not result:
            return jsonify({'error': 'Record not found'}), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<record_id>', methods=['DELETE'])
@require_admin
def delete_maintenance_record(record_id):
    """Delete maintenance record - Only admin"""
    try:
        result = maintenance_service.delete_record(record_id)
        if not result:
            return jsonify({'error': 'Record not found'}), 404
        return jsonify({'message': 'Record deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

