from database import db
from models import (
    DanhSachVuKhiCongCuHoTro,
    DanhSachPhuongTien,
    DanhSachThietBiKyThuatNghiepVu,
    DanhSachThietBiVanPhongDoanhTrai,
    DanhSachTrangThietBiThuy
)
from services.notification_service import NotificationService
from sqlalchemy import func

class DashboardService:
    def __init__(self):
        self.models = {
            'weapons': DanhSachVuKhiCongCuHoTro,
            'vehicles': DanhSachPhuongTien,
            'water': DanhSachTrangThietBiThuy,
            'technical': DanhSachThietBiKyThuatNghiepVu,
            'office': DanhSachThietBiVanPhongDoanhTrai
        }
    
    def get_stats(self):
        """Get dashboard statistics"""
        from sqlalchemy import inspect
        
        stats = {
            'total_assets': 0,
            'by_type': {
                'weapons': 0,
                'vehicles': 0,
                'water': 0,
                'technical': 0,
                'office': 0
            },
            'total_value': {
                'nguyen_gia': 0,
                'gia_tri_con_lai': 0
            }
        }
        
        # Check if database tables exist
        try:
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
        except Exception as e:
            raise Exception(f"Database connection error: {str(e)}. Please run 'python init_db.py' to initialize the database.")
        
        try:
            for asset_type, model_class in self.models.items():
                table_name = model_class.__tablename__
                
                # Check if table exists
                if table_name not in existing_tables:
                    print(f"Warning: Table {table_name} does not exist")
                    continue
                
                try:
                    count = model_class.query.filter_by(is_deleted=False).count()
                    stats['by_type'][asset_type] = count
                    stats['total_assets'] += count
                except Exception as e:
                    print(f"Warning: Could not count {asset_type}: {str(e)}")
                    continue
                
                # Sum values - handle NULL values and missing columns
                try:
                    # Check if columns exist
                    columns = [col.name for col in inspector.get_columns(table_name)]
                    
                    if 'nguyen_gia' in columns and 'gia_tri_con_lai' in columns:
                        result = db.session.query(
                            func.sum(model_class.nguyen_gia).label('total_nguyen_gia'),
                            func.sum(model_class.gia_tri_con_lai).label('total_gia_tri_con_lai')
                        ).filter_by(is_deleted=False).first()
                        
                        if result:
                            if result.total_nguyen_gia is not None:
                                stats['total_value']['nguyen_gia'] += float(result.total_nguyen_gia)
                            if result.total_gia_tri_con_lai is not None:
                                stats['total_value']['gia_tri_con_lai'] += float(result.total_gia_tri_con_lai)
                except Exception as e:
                    # If there's an error (e.g., column doesn't exist), skip value calculation
                    print(f"Warning: Could not calculate values for {asset_type}: {str(e)}")
                    pass
        except Exception as e:
            print(f"Error in get_stats: {str(e)}")
            raise
        
        return stats
    
    def get_top_alerts(self, limit=5):
        """Get top priority alerts"""
        notification_service = NotificationService()
        notifications = notification_service.get_notifications(limit=limit)
        return notifications
