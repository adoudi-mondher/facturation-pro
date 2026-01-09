"""
Configuration de l'application Flask
Version 1.7 - Easy Facture avec rapports CA
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Répertoire de base
BASE_DIR = Path(__file__).parent

# Fonction pour déterminer le dossier de données
def get_data_dir():
    """Retourne le dossier de données approprié selon l'environnement"""
    # Si on est en mode développement (script Python direct)
    if not getattr(sys, 'frozen', False):
        return BASE_DIR / 'data'

    # Si on est en mode exécutable PyInstaller
    # Utiliser AppData\Local pour stocker les données utilisateur
    appdata = os.environ.get('LOCALAPPDATA')
    if appdata:
        data_dir = Path(appdata) / 'EasyFacture' / 'data'
    else:
        # Fallback si LOCALAPPDATA n'existe pas
        data_dir = Path.home() / '.easyfacture' / 'data'

    return data_dir

class Config:
    """Configuration de base"""

    # Secret key pour les sessions
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Générer une clé automatiquement si non configurée
    if not SECRET_KEY:
        import secrets
        SECRET_KEY = secrets.token_hex(32)

    # Base de données
    DATA_DIR = get_data_dir()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    DB_PATH = DATA_DIR / 'facturation.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Dossiers
    UPLOAD_FOLDER = DATA_DIR / 'uploads'
    BACKUP_FOLDER = DATA_DIR / 'backups'
    # Logs dans le même emplacement que les données
    LOG_FOLDER = DATA_DIR.parent / 'logs'
    
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
    APP_VERSION = '1.7.0'  # Version avec rapports CA + données françaises
    
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