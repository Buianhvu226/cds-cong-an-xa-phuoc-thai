import os
from dotenv import load_dotenv

load_dotenv()

# Get base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    """Application configuration"""
    
    # Database - SQLite
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        f'sqlite:///{os.path.join(BASE_DIR, "database.db")}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    
    # CORS
    # Cho phép nhiều origins, phân cách bởi dấu phẩy
    # Ví dụ: 'http://localhost:5173,https://phuocthai.hctech.com.vn'
    cors_origins_str = os.getenv('CORS_ORIGINS', 'http://localhost:5173')
    CORS_ORIGINS = [origin.strip() for origin in cors_origins_str.split(',') if origin.strip()]
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION_DELTA = 86400  # 24 hours

