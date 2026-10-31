import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory is Subscription_Management_System
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env
load_dotenv(BASE_DIR / '.env')

class Config:
    """Base Application Configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'brightloop_super_secret_development_key_9921_x')
    
    # Database Configuration
    DATABASE_PATH = BASE_DIR / os.getenv('DATABASE_PATH', 'database/brightloop.db')
    SCHEMA_PATH = BASE_DIR / 'database' / 'schema.sql'
    SEED_PATH = BASE_DIR / 'database' / 'seed_data.sql'
    
    # Frontend Paths
    TEMPLATE_FOLDER = str(BASE_DIR / 'frontend' / 'templates')
    STATIC_FOLDER = str(BASE_DIR / 'frontend' / 'static')
    
    # Financial & Localization Settings
    DEFAULT_CURRENCY = os.getenv('DEFAULT_CURRENCY', 'USD')
    DEFAULT_TAX_RATE = float(os.getenv('TAX_RATE', '0.08')) # 8% standard tax
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('FLASK_DEBUG', '1') == '1'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = DevelopmentConfig()

