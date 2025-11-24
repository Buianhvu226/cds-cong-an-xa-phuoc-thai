from flask import Blueprint, request, jsonify
from services.asset_service import AssetService
from utils.validation import validate_asset_data
from utils.auth import require_auth, require_admin, get_current_user
from datetime import datetime

bp = Blueprint('assets', __name__)
asset_service = AssetService()

@bp.route('/<asset_type>', methods=['GET'])
@require_auth
def get_assets(asset_type):
    """Get list of assets by type"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        filters = dict(request.args)
        
        # Remove pagination params from filters
        filters.pop('page', None)
        filters.pop('per_page', None)
        filters.pop('search', None)
        
        result = asset_service.get_assets(asset_type, page, per_page, search, filters)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<asset_type>', methods=['POST'])
@require_auth
def create_asset(asset_type):
    """Create new asset"""
    try:
        data = request.get_json()
        
        # Validate data
        validation_error = validate_asset_data(asset_type, data)
        if validation_error:
            return jsonify({'error': validation_error}), 400
        
        result = asset_service.create_asset(asset_type, data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<asset_type>/<asset_id>', methods=['GET'])
@require_auth
def get_asset(asset_type, asset_id):
    """Get single asset by ID"""
    try:
        result = asset_service.get_asset(asset_type, asset_id)
        if not result:
            return jsonify({'error': 'Asset not found'}), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<asset_type>/<asset_id>', methods=['PUT'])
@require_auth
def update_asset(asset_type, asset_id):
    """Update asset"""
    try:
        data = request.get_json()
        
        # Validate data
        validation_error = validate_asset_data(asset_type, data, is_update=True)
        if validation_error:
            return jsonify({'error': validation_error}), 400
        
        result = asset_service.update_asset(asset_type, asset_id, data)
        if not result:
            return jsonify({'error': 'Asset not found'}), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<asset_type>/<asset_id>', methods=['DELETE'])
@require_admin
def delete_asset(asset_type, asset_id):
    """Soft delete asset - Only admin"""
    try:
        result = asset_service.delete_asset(asset_type, asset_id)
        if not result:
            return jsonify({'error': 'Asset not found'}), 404
        return jsonify({'message': 'Asset deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<asset_type>/export', methods=['GET'])
@require_admin
def export_assets(asset_type):
    """Export assets to Excel - Only admin"""
    from flask import send_file
    import os
    
    try:
        filters = dict(request.args)
        file_path = asset_service.export_to_excel(asset_type, filters)
        
        if os.path.exists(file_path):
            return send_file(
                file_path,
                as_attachment=True,
                download_name=f"{asset_type}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<asset_type>/import/template', methods=['GET'])
def download_import_template(asset_type):
    """Download Excel template for import"""
    from flask import send_file
    import os
    
    try:
        file_path = asset_service.create_import_template(asset_type)
        
        if os.path.exists(file_path):
            return send_file(
                file_path,
                as_attachment=True,
                download_name=f"mau_nhap_{asset_type}.xlsx",
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        else:
            return jsonify({'error': 'Template not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<asset_type>/import', methods=['POST'])
@require_admin
def import_assets(asset_type):
    """Import assets from Excel file - Only admin"""
    from werkzeug.utils import secure_filename
    import os
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file extension
        if not file.filename.endswith(('.xlsx', '.xls')):
            return jsonify({'error': 'Invalid file format. Please upload Excel file (.xlsx or .xls)'}), 400
        
        # Save uploaded file
        upload_dir = 'imports'
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = os.path.join(upload_dir, f"{timestamp}_{filename}")
        file.save(filepath)
        
        # Import data
        result = asset_service.import_from_excel(filepath, asset_type)
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

