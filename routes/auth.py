from flask import Blueprint, request, jsonify
from models import User
from database import db
from utils.auth import generate_token, hash_password, check_password, require_auth, require_admin, get_current_user
from datetime import datetime

bp = Blueprint('auth', __name__)

@bp.route('/users', methods=['GET'])
@require_admin
def get_users():
    """Get list of all users (admin only)"""
    try:
        users = User.query.filter_by(is_deleted=False).order_by(User.created_at.desc()).all()
        return jsonify({
            'users': [user.to_dict() for user in users]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/users', methods=['POST'])
@require_admin
def create_user():
    """Create new user (admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('username') or not data.get('email') or not data.get('password') or not data.get('full_name'):
            return jsonify({'error': 'Vui lòng điền đầy đủ thông tin'}), 400
        
        # Check if username exists
        if User.query.filter_by(username=data['username'], is_deleted=False).first():
            return jsonify({'error': 'Tên đăng nhập đã tồn tại'}), 400
        
        # Check if email exists
        if User.query.filter_by(email=data['email'], is_deleted=False).first():
            return jsonify({'error': 'Email đã tồn tại'}), 400
        
        # Validate password length
        if len(data['password']) < 6:
            return jsonify({'error': 'Mật khẩu phải có ít nhất 6 ký tự'}), 400
        
        # Create user
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=hash_password(data['password']),
            full_name=data['full_name'],
            role=data.get('role', 'chuyen_vien')  # Default to chuyen_vien
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Tạo tài khoản thành công',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/register', methods=['POST'])
@require_admin
def register():
    """Register new user (only admin can create users) - deprecated, use /users"""
    return create_user()

@bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        if not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Vui lòng nhập tên đăng nhập và mật khẩu'}), 400
        
        # Find user
        user = User.query.filter_by(username=data['username'], is_deleted=False).first()
        
        if not user or not check_password(user.password_hash, data['password']):
            return jsonify({'error': 'Tên đăng nhập hoặc mật khẩu không đúng'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Tài khoản đã bị vô hiệu hóa'}), 403
        
        # Generate token
        token = generate_token(user)
        
        return jsonify({
            'message': 'Đăng nhập thành công',
            'token': token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/me', methods=['GET'])
@require_auth
def get_current_user_info():
    """Get current user information"""
    try:
        user = get_current_user()
        return jsonify({
            'user': user.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/change-password', methods=['POST'])
@require_auth
def change_password():
    """Change user password"""
    try:
        user = get_current_user()
        data = request.get_json()
        
        if not data.get('old_password') or not data.get('new_password'):
            return jsonify({'error': 'Vui lòng nhập mật khẩu cũ và mật khẩu mới'}), 400
        
        # Verify old password
        if not check_password(user.password_hash, data['old_password']):
            return jsonify({'error': 'Mật khẩu cũ không đúng'}), 400
        
        # Update password
        user.password_hash = hash_password(data['new_password'])
        user.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({'message': 'Đổi mật khẩu thành công'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

