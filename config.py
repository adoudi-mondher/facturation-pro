"""
Configuration de l'application Flask
Version 1.7 - Avec support licence
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Répertoire de base
BASE_DIR = Path(__file__).parent

class Config:
    """Configuration de base"""

    # Secret key pour les sessions
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Vérifier que la SECRET_KEY est configurée
    if not SECRET_KEY:
        import warnings
        warnings.warn(
            "⚠️  SECRET_KEY non configurée dans .env ! "
            "Exécutez: python generate_secret_key.py",
            UserWarning,
            stacklevel=2
        )
        # Générer une clé temporaire (différente à chaque démarrage)
        import secrets
        SECRET_KEY = secrets.token_hex(32)
        print("⚠️  SECRET_KEY temporaire générée (sera perdue au redémarrage)")
        print("⚠️  Configurez SECRET_KEY dans .env pour la persistance")
    
    # Base de données
    DATA_DIR = BASE_DIR / 'data'
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    DB_PATH = DATA_DIR / 'facturation.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Dossiers
    UPLOAD_FOLDER = BASE_DIR / (os.environ.get('UPLOAD_FOLDER') or 'data/uploads')
    BACKUP_FOLDER = BASE_DIR / (os.environ.get('BACKUP_FOLDER') or 'data/backups')
    LOG_FOLDER = BASE_DIR / (os.environ.get('LOG_FOLDER') or 'logs')
    
    # Créer les dossiers s'ils n'existent pas
    for folder in [UPLOAD_FOLDER, BACKUP_FOLDER, LOG_FOLDER]:
        folder.mkdir(parents=True, exist_ok=True)
    
    # Sous-dossiers uploads
    LOGOS_FOLDER = UPLOAD_FOLDER / 'logos'
    FACTURES_FOLDER = UPLOAD_FOLDER / 'factures'
    LOGOS_FOLDER.mkdir(exist_ok=True)
    FACTURES_FOLDER.mkdir(exist_ok=True)
    
    # Upload
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_UPLOAD_SIZE', 5)) * 1024 * 1024  # Mo
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Pagination
    ITEMS_PER_PAGE = int(os.environ.get('ITEMS_PER_PAGE', 20))
    
    # Email
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
    SMTP_USER = os.environ.get('SMTP_USER', '')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
    SMTP_USE_TLS = os.environ.get('SMTP_USE_TLS', 'True').lower() == 'true'
    
    # Application
    APP_NAME = 'Easy Facture'
    APP_VERSION = '1.7.0'  # ⬆️ Mise à jour version
    
    # 🆕 Licence (nouveau)
    LICENSE_ENABLED = os.environ.get('LICENSE_ENABLED', 'True').lower() == 'true'

class DevelopmentConfig(Config):
    """Configuration développement"""
    DEBUG = True
    TESTING = False
    # En dev, on peut désactiver la licence
    LICENSE_ENABLED = os.environ.get('LICENSE_ENABLED', 'False').lower() == 'true'

class ProductionConfig(Config):
    """Configuration production"""
    DEBUG = False
    TESTING = False
    # En prod, licence obligatoire
    LICENSE_ENABLED = True

# Configuration par défaut
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}