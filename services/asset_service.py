from database import db
from models import (
    DanhSachVuKhiCongCuHoTro,
    DanhSachPhuongTien,
    DanhSachThietBiKyThuatNghiepVu,
    DanhSachThietBiVanPhongDoanhTrai,
    DanhSachTrangThietBiThuy
)
from utils.date_utils import calculate_next_inspection_date, generate_asset_code
from datetime import datetime
from sqlalchemy import or_, and_

class AssetService:
    def __init__(self):
        # Map asset types to model classes
        self.model_map = {
            'weapons': DanhSachVuKhiCongCuHoTro,
            'vehicles': DanhSachPhuongTien,
            'technical': DanhSachThietBiKyThuatNghiepVu,
            'office': DanhSachThietBiVanPhongDoanhTrai,
            'water': DanhSachTrangThietBiThuy
        }
    
    def get_assets(self, asset_type, page=1, per_page=20, search='', filters=None):
        """Get paginated list of assets"""
        model_class = self.model_map.get(asset_type)
        if not model_class:
            raise ValueError(f"Invalid asset type: {asset_type}")
        
        # Base query
        query = model_class.query.filter_by(is_deleted=False)
        
        # Apply search
        if search:
            search_pattern = f'%{search}%'
            if asset_type == 'weapons':
                query = query.filter(
                    or_(
                        DanhSachVuKhiCongCuHoTro.ma_tai_san.like(search_pattern),
                        DanhSachVuKhiCongCuHoTro.ten_tai_san.like(search_pattern),
                        DanhSachVuKhiCongCuHoTro.so_hieu.like(search_pattern)
                    )
                )
            elif asset_type == 'vehicles':
                query = query.filter(
                    or_(
                        DanhSachPhuongTien.ma_tai_san.like(search_pattern),
                        DanhSachPhuongTien.ten_phuong_tien.like(search_pattern),
                        DanhSachPhuongTien.bien_so_ky_hieu.like(search_pattern)
                    )
                )
            elif asset_type == 'water':
                query = query.filter(
                    or_(
                        DanhSachTrangThietBiThuy.ma_tai_san.like(search_pattern),
                        DanhSachTrangThietBiThuy.ten_trang_bi.like(search_pattern),
                        DanhSachTrangThietBiThuy.ma_hieu.like(search_pattern)
                    )
                )
            else:
                query = query.filter(
                    or_(
                        model_class.ma_tai_san.like(search_pattern),
                        model_class.ten_tai_san.like(search_pattern)
                    )
                )
        
        # Apply filters
        if filters:
            for key, value in filters.items():
                if value and hasattr(model_class, key):
                    query = query.filter(getattr(model_class, key) == value)
        
        # Get total count
        total = query.count()
        
        # Pagination
        offset = (page - 1) * per_page
        items = query.offset(offset).limit(per_page).all()
        
        return {
            'data': [item.to_dict() for item in items],
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }
    
    def get_asset(self, asset_type, asset_id):
        """Get single asset by ID"""
        model_class = self.model_map.get(asset_type)
        if not model_class:
            raise ValueError(f"Invalid asset type: {asset_type}")
        
        asset = model_class.query.filter_by(id=asset_id, is_deleted=False).first()
        return asset.to_dict() if asset else None
    
    def create_asset(self, asset_type, data):
        """Create new asset"""
        model_class = self.model_map.get(asset_type)
        if not model_class:
            raise ValueError(f"Invalid asset type: {asset_type}")
        
        # Auto-generate mã tài sản if not provided
        if not data.get('ma_tai_san'):
            prefix_map = {
                'weapons': 'VK',
                'vehicles': 'PT',
                'technical': 'TB',
                'office': 'VP',
                'water': 'TT'
            }
            prefix = prefix_map.get(asset_type, 'TS')
            data['ma_tai_san'] = self._generate_asset_code(prefix, model_class)
        
        # Auto-calculate ngay_kiem_tra_tiep_theo if needed
        if data.get('ngay_kiem_tra_gan_nhat'):
            if asset_type == 'water' or asset_type == 'technical' or asset_type == 'office':
                # Water equipment, Technical equipment, and Office equipment: 6 months period
                if data.get('ngay_kiem_tra_gan_nhat'):
                    next_date = calculate_next_inspection_date(
                        data['ngay_kiem_tra_gan_nhat'],
                        '6 tháng'
                    )
                    if next_date:
                        data['ngay_kiem_tra_tiep_theo'] = next_date
            elif data.get('dinh_ky_kiem_tra'):
                next_date = calculate_next_inspection_date(
                    data['ngay_kiem_tra_gan_nhat'],
                    data['dinh_ky_kiem_tra']
                )
                if next_date:
                    data['ngay_kiem_tra_tiep_theo'] = next_date
        
        # Convert date strings to date objects
        for key in ['ngay_kiem_tra_gan_nhat', 'ngay_kiem_tra_tiep_theo']:
            if key in data and data[key] and isinstance(data[key], str):
                data[key] = datetime.fromisoformat(data[key]).date()
        
        # Create new asset
        asset = model_class(**data)
        db.session.add(asset)
        db.session.commit()
        
        return asset.to_dict()
    
    def update_asset(self, asset_type, asset_id, data):
        """Update asset"""
        model_class = self.model_map.get(asset_type)
        if not model_class:
            raise ValueError(f"Invalid asset type: {asset_type}")
        
        asset = model_class.query.filter_by(id=asset_id, is_deleted=False).first()
        if not asset:
            return None
        
        # Don't allow updating ma_tai_san
        data.pop('ma_tai_san', None)
        
        # Recalculate ngay_kiem_tra_tiep_theo if relevant fields changed
        if data.get('ngay_kiem_tra_gan_nhat'):
            ngay_kiem_tra_gan_nhat = data.get('ngay_kiem_tra_gan_nhat', asset.ngay_kiem_tra_gan_nhat)
            
            if asset_type == 'water' or asset_type == 'technical' or asset_type == 'office':
                # Water equipment, Technical equipment, and Office equipment: 6 months period
                if ngay_kiem_tra_gan_nhat:
                    if isinstance(ngay_kiem_tra_gan_nhat, str):
                        ngay_kiem_tra_gan_nhat = datetime.fromisoformat(ngay_kiem_tra_gan_nhat).date()
                    next_date = calculate_next_inspection_date(ngay_kiem_tra_gan_nhat, '6 tháng')
                    if next_date:
                        data['ngay_kiem_tra_tiep_theo'] = next_date
            elif data.get('dinh_ky_kiem_tra'):
                dinh_ky_kiem_tra = data.get('dinh_ky_kiem_tra', asset.dinh_ky_kiem_tra)
                if ngay_kiem_tra_gan_nhat and dinh_ky_kiem_tra:
                    if isinstance(ngay_kiem_tra_gan_nhat, str):
                        ngay_kiem_tra_gan_nhat = datetime.fromisoformat(ngay_kiem_tra_gan_nhat).date()
                    next_date = calculate_next_inspection_date(ngay_kiem_tra_gan_nhat, dinh_ky_kiem_tra)
                    if next_date:
                        data['ngay_kiem_tra_tiep_theo'] = next_date
        
        # Convert date strings to date objects
        for key in ['ngay_kiem_tra_gan_nhat', 'ngay_kiem_tra_tiep_theo']:
            if key in data and data[key] and isinstance(data[key], str):
                data[key] = datetime.fromisoformat(data[key]).date()
        
        # Update fields
        for key, value in data.items():
            if hasattr(asset, key):
                setattr(asset, key, value)
        
        asset.updated_at = datetime.utcnow()
        db.session.commit()
        
        return asset.to_dict()
    
    def delete_asset(self, asset_type, asset_id):
        """Soft delete asset"""
        model_class = self.model_map.get(asset_type)
        if not model_class:
            raise ValueError(f"Invalid asset type: {asset_type}")
        
        asset = model_class.query.filter_by(id=asset_id, is_deleted=False).first()
        if not asset:
            return None
        
        asset.is_deleted = True
        asset.updated_at = datetime.utcnow()
        db.session.commit()
        
        return asset.to_dict()
    
    def _generate_asset_code(self, prefix, model_class):
        """Generate unique asset code"""
        now = datetime.now()
        yy = str(now.year)[-2:]
        mm = str(now.month).zfill(2)
        search_pattern = f"{prefix}{yy}{mm}"
        
        # Get existing codes for this month
        existing = model_class.query.filter(
            model_class.ma_tai_san.like(f'{search_pattern}%')
        ).all()
        
        # Find highest sequence number
        max_seq = 0
        for item in existing:
            ma_tai_san = item.ma_tai_san
            if ma_tai_san.startswith(search_pattern):
                try:
                    seq = int(ma_tai_san[-3:])
                    max_seq = max(max_seq, seq)
                except ValueError:
                    pass
        
        # Generate next sequence
        next_seq = max_seq + 1
        return f"{search_pattern}{str(next_seq).zfill(3)}"
    
    def export_to_excel(self, asset_type, filters=None):
        """Export assets to Excel"""
        from services.export_service import ExportService
        
        # Get all assets (no pagination for export)
        model_class = self.model_map.get(asset_type)
        if not model_class:
            raise ValueError(f"Invalid asset type: {asset_type}")
        
        query = model_class.query.filter_by(is_deleted=False)
        
        # Apply filters if any
        if filters:
            for key, value in filters.items():
                if value and hasattr(model_class, key):
                    query = query.filter(getattr(model_class, key) == value)
        
        assets = query.all()
        assets_dict = [asset.to_dict() for asset in assets]
        
        # Export to Excel
        export_service = ExportService()
        filepath = export_service.export_assets_to_excel(assets_dict, asset_type, filters)
        
        return filepath
    
    def import_from_excel(self, filepath, asset_type):
        """Import assets from Excel file"""
        from services.import_service import ImportService
        from utils.validation import validate_asset_data
        from database import db
        
        import_service = ImportService()
        errors = []
        success_count = 0
        skipped_count = 0
        
        # Get model class
        model_class = self.model_map.get(asset_type)
        if not model_class:
            return {'success': False, 'errors': [f"Invalid asset type: {asset_type}"], 'success_count': 0, 'skipped_count': 0}
        
        # Process rows from Excel
        row_num = 2  # Start from row 2 (after header)
        header_errors = []
        
        for item in import_service.import_from_excel(filepath, asset_type):
            # Check if this is an error result
            if isinstance(item, dict) and 'success' in item:
                if not item.get('success'):
                    # Header validation failed
                    return item
                header_errors = item.get('errors', [])
                continue
            
            # This is a row data
            row_num += 1
            row_data = item
            
            try:
                # Validate data
                validation_error = validate_asset_data(asset_type, row_data)
                if validation_error:
                    errors.append(f"Dòng {row_num}: {validation_error}")
                    skipped_count += 1
                    continue
                
                # Generate ma_tai_san if not provided
                if not row_data.get('ma_tai_san'):
                    row_data['ma_tai_san'] = self._generate_ma_tai_san(asset_type)
                
                # Create asset
                asset = model_class(**row_data)
                db.session.add(asset)
                db.session.commit()
                success_count += 1
                
            except Exception as e:
                db.session.rollback()
                errors.append(f"Dòng {row_num}: Lỗi khi tạo tài sản - {str(e)}")
                skipped_count += 1
        
        # Combine header errors with row errors
        all_errors = header_errors + errors
        
        return {
            'success': True,
            'errors': all_errors,
            'success_count': success_count,
            'skipped_count': skipped_count
        }
    
    def create_import_template(self, asset_type):
        """Create Excel template for import"""
        from services.import_service import ImportService
        
        import_service = ImportService()
        filepath = import_service.create_template(asset_type)
        
        return filepath
