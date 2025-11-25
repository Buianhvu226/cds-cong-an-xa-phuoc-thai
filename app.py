from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from database import db
from routes import assets, notifications, maintenance, reports, dashboard, auth, tin_bao, vu_an, bi_can, tam_giam
# Import models to ensure they're registered with SQLAlchemy
from models import (
    DanhSachVuKhiCongCuHoTro,
    DanhSachPhuongTien,
    DanhSachThietBiKyThuatNghiepVu,
    DanhSachThietBiVanPhongDoanhTrai,
    DanhSachTrangThietBiThuy,
    LichSuKiemTraBaoTri,
    DanhMucLoaiTaiSan,
    User,
    # Phase 2 models
    TinBao,
    VuAn,
    BiCan,
    LichSuChuyenDoi,
    TamGiam
)

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# CORS configuration
CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)

# Register blueprints
app.register_blueprint(auth.bp, url_prefix='/api/auth')
app.register_blueprint(assets.bp, url_prefix='/api/assets')
app.register_blueprint(notifications.bp, url_prefix='/api/notifications')
app.register_blueprint(maintenance.bp, url_prefix='/api/maintenance')
app.register_blueprint(reports.bp, url_prefix='/api/reports')
app.register_blueprint(dashboard.bp, url_prefix='/api/dashboard')
# Phase 2 blueprints
app.register_blueprint(tin_bao.bp, url_prefix='/api/tin-bao')
app.register_blueprint(vu_an.bp, url_prefix='/api/vu-an')
app.register_blueprint(bi_can.bp, url_prefix='/api')
app.register_blueprint(tam_giam.bp, url_prefix='/api/tam-giam')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {'status': 'ok', 'message': 'Asset Management System API is running'}, 200

if __name__ == '__main__':
    print(f"🚀 Starting server on http://localhost:{app.config['FLASK_PORT']}")
    print("📝 Note: Database migrations are managed by Flask-Migrate")
    print("   Run 'flask db upgrade' to apply migrations")
    app.run(debug=app.config['FLASK_DEBUG'], port=app.config['FLASK_PORT'], host='0.0.0.0')

