from app import app
from services.report_service import ReportService

with app.app_context():
    svc = ReportService()
    data = svc._generate_expiring_report()
    print('Expiring count:', len(data['data']))
    print('Types:', sorted({item['asset_type'] for item in data['data']}))
