from flask import Blueprint, request, jsonify
from services.notification_service import NotificationService

bp = Blueprint('notifications', __name__)
notification_service = NotificationService()

@bp.route('', methods=['GET'])
def get_notifications():
    """Get all notifications/alerts"""
    try:
        priority = request.args.get('priority', None)  # 'high', 'medium', 'low'
        limit = request.args.get('limit', None, type=int)
        
        result = notification_service.get_notifications(priority, limit)
        return jsonify(result), 200
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in get_notifications: {error_details}")
        # Return empty list instead of error
        return jsonify([]), 200

@bp.route('/count', methods=['GET'])
def get_notification_count():
    """Get notification count by priority"""
    try:
        result = notification_service.get_notification_counts()
        return jsonify(result), 200
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in get_notification_count: {error_details}")
        # Return empty counts instead of error
        return jsonify({
            'high': 0,
            'medium': 0,
            'low': 0,
            'total': 0
        }), 200

