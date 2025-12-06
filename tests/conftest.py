"""
Configuration PyTest - Easy Facture
"""
import pytest
import os
import tempfile
from app import create_app
from app.extensions import db
from app.models.client import Client
from app.models.produit import Produit
from app.models.document import Document
from app.models.entreprise import Entreprise

@pytest.fixture
def app():
    """Crée une instance de test de l'application"""
    # Créer un fichier temporaire pour la BDD de test
    db_fd, db_path = tempfile.mkstemp()
    
    # Configuration de test
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key'
    })
    
    # Créer les tables
    with app.app_context():
        db.create_all()
        
        # Créer des données de test
        entreprise = Entreprise(
            nom="Test Entreprise",
            siret="12345678900000",
            adresse="1 rue Test",
            code_postal="75001",
            ville="Paris",
            email="test@test.com"
        )
        db.session.add(entreprise)
        db.session.commit()
    
    yield app
    
    # Nettoyage
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """Client de test Flask"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """CLI runner de test"""
    return app.test_cli_runner()

@pytest.fixture
def sample_client(app):
    """Client exemple pour les tests"""
    with app.app_context():
        client = Client(
            nom="Dupont",
            prenom="Jean",
            email="jean.dupont@test.com",
            telephone="0123456789",
            adresse="1 rue Client",
            code_postal="75002",
            ville="Paris"
        )
        db.session.add(client)
        db.session.commit()
        
        # Stocker l'ID avant de quitter le contexte
        client_id = client.id
    
    # Retourner l'ID au lieu de l'objet
    return client_id

@pytest.fixture
def sample_produit(app):
    """Produit exemple pour les tests"""
    with app.app_context():
        produit = Produit(
            nom="Produit Test",
            description="Description test",
            prix_unitaire=10.00,
            unite="unité",
            stock=100
        )
        db.session.add(produit)
        db.session.commit()
        return produit
