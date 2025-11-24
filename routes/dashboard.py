from flask import Blueprint, jsonify, request
from services.dashboard_service import DashboardService
from utils.auth import require_auth

bp = Blueprint('dashboard', __name__)
dashboard_service = DashboardService()

@bp.route('/stats', methods=['GET'])
@require_auth
def get_stats():
    """Get dashboard statistics"""
    try:
        result = dashboard_service.get_stats()
        return jsonify(result), 200
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in get_stats: {error_details}")
        return jsonify({
            'error': str(e),
            'message': 'Có lỗi xảy ra khi lấy thống kê. Vui lòng kiểm tra database đã được khởi tạo chưa.'
        }), 500

@bp.route('/alerts', methods=['GET'])
@require_auth
def get_alerts():
    """Get top priority alerts"""
    try:
        limit = request.args.get('limit', 5, type=int)
        result = dashboard_service.get_top_alerts(limit)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

