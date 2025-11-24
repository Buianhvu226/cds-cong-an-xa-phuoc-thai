"""
Script to create admin user
Usage: python create_admin.py
"""
from app import app
from database import db
from models import User
from utils.auth import hash_password

def create_admin():
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(username='admin', is_deleted=False).first()
        if admin:
            print('Admin user already exists!')
            return
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@phuocthai.local',
            password_hash=hash_password('admin123'),
            full_name='Quản trị viên',
            role='admin',
            is_active=True
        )
        
        db.session.add(admin)
        db.session.commit()
        print('Admin user created successfully!')
        print('Username: admin')
        print('Password: admin123')
        print('Please change the password after first login!')

if __name__ == '__main__':
    create_admin()

