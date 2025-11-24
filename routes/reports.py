from flask import Blueprint, request, jsonify, send_file
from services.report_service import ReportService
from utils.auth import require_auth, require_admin
import os

bp = Blueprint('reports', __name__)
report_service = ReportService()

@bp.route('/<report_type>', methods=['GET'])
@require_auth
def get_report(report_type):
    """Get report by type"""
    try:
        # report_type: 'summary', 'by_category', 'inspection_due', 'expiring'
        filters = dict(request.args)
        result = report_service.generate_report(report_type, filters)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<report_type>/export', methods=['GET'])
@require_admin
def export_report(report_type):
    """Export report to Excel - Only admin"""
    try:
        filters = dict(request.args)
        file_path = report_service.export_report(report_type, filters)
        
        if os.path.exists(file_path):
            filename = os.path.basename(file_path)
            return send_file(
                file_path,
                as_attachment=True,
                download_name=filename,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

