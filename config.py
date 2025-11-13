import os

class Config:
    """Configuration de base de l'application"""
    
    # Clé secrète pour les sessions
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configuration de la base de données
    # En prod : PostgreSQL via DATABASE_URL
    # En dev : SQLite local
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///tasks.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False