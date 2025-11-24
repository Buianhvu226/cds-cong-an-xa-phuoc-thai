from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def calculate_next_inspection_date(ngay_kiem_tra_gan_nhat, dinh_ky_kiem_tra):
    """
    Calculate next inspection date based on last inspection and period
    BR-002: Auto-calculate ngay_kiem_tra_tiep_theo
    """
    if not ngay_kiem_tra_gan_nhat or not dinh_ky_kiem_tra:
        return None
    
    # Parse date if string
    if isinstance(ngay_kiem_tra_gan_nhat, str):
        ngay_kiem_tra_gan_nhat = datetime.fromisoformat(ngay_kiem_tra_gan_nhat).date()
    
    # Map period string to months
    period_map = {
        '1 tháng': 1,
        '3 tháng': 3,
        '6 tháng': 6,
        '12 tháng': 12
    }
    
    months = period_map.get(dinh_ky_kiem_tra, 0)
    if months == 0:
        return None
    
    # Calculate next date
    next_date = ngay_kiem_tra_gan_nhat + relativedelta(months=months)
    return next_date.isoformat()

def get_inspection_status(ngay_kiem_tra_tiep_theo, today=None):
    """
    Get inspection status: overdue, due_soon, or normal
    BR-003: Trạng thái kiểm tra
    """
    if today is None:
        today = datetime.now().date()
    
    # Parse date if string
    if isinstance(ngay_kiem_tra_tiep_theo, str):
        ngay_kiem_tra_tiep_theo = datetime.fromisoformat(ngay_kiem_tra_tiep_theo).date()
    
    days_until = (ngay_kiem_tra_tiep_theo - today).days
    
    if days_until < 0:
        return 'overdue'  # Quá hạn
    elif days_until <= 15:
        return 'due_soon'  # Sắp hết hạn
    else:
        return 'normal'  # Bình thường

# Note: generate_asset_code is now handled in AssetService._generate_asset_code
# This function is kept for backward compatibility but not used
def generate_asset_code(prefix, db_model=None, table_name=None):
    """
    Generate unique asset code: [Prefix][YY][MM][XXX]
    BR-001: Auto-generate mã tài sản
    Note: This is now handled in AssetService
    """
    pass

