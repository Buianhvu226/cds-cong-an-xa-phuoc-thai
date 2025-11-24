import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
from models import User
from database import db
from werkzeug.security import check_password_hash, generate_password_hash

def generate_token(user):
    """Generate JWT token for user"""
    payload = {
        'user_id': user.id,
        'username': user.username,
        'role': user.role,
        'exp': datetime.utcnow() + timedelta(seconds=current_app.config['JWT_EXPIRATION_DELTA'])
    }
    token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm=current_app.config['JWT_ALGORITHM'])
    return token

def verify_token(token):
    """Verify JWT token and return user"""
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=[current_app.config['JWT_ALGORITHM']])
        user_id = payload.get('user_id')
        user = User.query.filter_by(id=user_id, is_active=True, is_deleted=False).first()
        return user
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_current_user():
    """Get current user from request token"""
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    
    try:
        token = auth_header.split(' ')[1]  # Bearer <token>
        return verify_token(token)
    except (IndexError, AttributeError):
        return None

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Unauthorized. Please login.'}), 401
        return f(*args, **kwargs)
    return decorated_function

def require_admin(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Unauthorized. Please login.'}), 401
        if not user.is_admin():
            return jsonify({'error': 'Forbidden. Admin access required.'}), 403
        return f(*args, **kwargs)
    return decorated_function

def hash_password(password):
    """Hash password using werkzeug"""
    return generate_password_hash(password)

def check_password(password_hash, password):
    """Check password against hash"""
    return check_password_hash(password_hash, password)

