from datetime import datetime

def validate_asset_data(asset_type, data, is_update=False):
    """
    Validate asset data according to business rules
    BR-004: Validation rules
    """
    errors = []
    
    # Required fields
    if not is_update:
        if asset_type == 'weapons':
            required_fields = ['ten_tai_san', 'ma_danh_muc', 'don_vi_tinh', 'so_luong']
        elif asset_type == 'vehicles':
            required_fields = ['ten_phuong_tien', 'danh_muc_phuong_tien', 'don_vi_tinh', 'so_luong']
        elif asset_type == 'water':
            required_fields = ['ten_trang_bi', 'danh_muc_trang_thiet_bi', 'don_vi_tinh', 'so_luong']
        else:
            required_fields = ['ten_tai_san', 'so_luong']
        
        for field in required_fields:
            if not data.get(field):
                errors.append(f"{field} is required")
    
    # Validate ten_tai_san length (min 3 chars)
    if asset_type == 'vehicles':
        ten_field = 'ten_phuong_tien'
    elif asset_type == 'water':
        ten_field = 'ten_trang_bi'
    else:
        ten_field = 'ten_tai_san'
    
    if data.get(ten_field):
        if len(data[ten_field]) < 3:
            errors.append(f"{ten_field} must be at least 3 characters")
    
    # Validate so_luong (min 1)
    if data.get('so_luong') is not None:
        if data['so_luong'] < 1:
            errors.append("so_luong must be at least 1")
    
    # Validate gia_tri_con_lai <= nguyen_gia
    if data.get('gia_tri_con_lai') and data.get('nguyen_gia'):
        if float(data['gia_tri_con_lai']) > float(data['nguyen_gia']):
            errors.append("gia_tri_con_lai must be <= nguyen_gia")
    
    # Validate ngay_kiem_tra_tiep_theo >= ngay_kiem_tra_gan_nhat
    if data.get('ngay_kiem_tra_tiep_theo') and data.get('ngay_kiem_tra_gan_nhat'):
        ngay_gan_nhat = data['ngay_kiem_tra_gan_nhat']
        ngay_tiep_theo = data['ngay_kiem_tra_tiep_theo']
        
        if isinstance(ngay_gan_nhat, str):
            ngay_gan_nhat = datetime.fromisoformat(ngay_gan_nhat).date()
        if isinstance(ngay_tiep_theo, str):
            ngay_tiep_theo = datetime.fromisoformat(ngay_tiep_theo).date()
        
        if ngay_tiep_theo < ngay_gan_nhat:
            errors.append("ngay_kiem_tra_tiep_theo must be >= ngay_kiem_tra_gan_nhat")
    
    if errors:
        return '; '.join(errors)
    return None

