"""
Tests des modèles - Easy Facture
CORRIGÉ pour correspondre aux vrais modèles
"""
import pytest
from app.models.client import Client
from app.models.produit import Produit
from app.models.document import Document
from app.extensions import db

class TestClient:
    """Tests du modèle Client"""
    
    def test_create_client(self, app):
        """Test création d'un client"""
        with app.app_context():
            client = Client(
                nom="Test",
                prenom="User",
                email="test@example.com"
            )
            db.session.add(client)
            db.session.commit()
            
            assert client.id is not None
            assert client.nom == "Test"
    
    def test_client_nom_complet(self, app):
        """Test propriété nom_complet"""
        with app.app_context():
            client = Client(nom="Dupont", prenom="Jean")
            db.session.add(client)
            db.session.commit()
            
            assert client.nom_complet == "Jean Dupont"
    
    def test_client_validation_email(self, app):
        """Test validation email"""
        with app.app_context():
            client = Client(nom="Test", email="valid@email.com")
            db.session.add(client)
            db.session.commit()
            assert client.email == "valid@email.com"


class TestProduit:
    """Tests du modèle Produit"""
    
    def test_create_produit(self, app):
        """Test création d'un produit"""
        with app.app_context():
            import uuid
            ref = f"TEST-{uuid.uuid4().hex[:8].upper()}"
            
            produit = Produit(
                reference=ref,
                designation="Test Product",
                prix_ht=19.99,
                stock_actuel=50
            )
            db.session.add(produit)
            db.session.commit()
            
            assert produit.id is not None
            assert produit.reference == ref
            assert produit.designation == "Test Product"
            assert float(produit.prix_ht) == 19.99
    
    def test_produit_stock(self, app):
        """Test gestion du stock"""
        with app.app_context():
            import uuid
            ref = f"TEST-{uuid.uuid4().hex[:8].upper()}"
            
            produit = Produit(
                reference=ref,
                designation="Test",
                prix_ht=10.00,
                gerer_stock=True,
                stock_actuel=100
            )
            db.session.add(produit)
            db.session.commit()
            
            assert produit.stock_actuel == 100
            
            # Réduire le stock
            produit.stock_actuel -= 10
            db.session.commit()
            assert produit.stock_actuel == 90
    
    def test_produit_prix_ttc(self, app):
        """Test calcul prix TTC"""
        with app.app_context():
            import uuid
            ref = f"TEST-{uuid.uuid4().hex[:8].upper()}"
            
            produit = Produit(
                reference=ref,
                designation="Test TTC",
                prix_ht=100.00,
                taux_tva=20.00
            )
            db.session.add(produit)
            db.session.commit()
            
            # Prix TTC = 100 * 1.20 = 120
            assert produit.prix_ttc == 120.00


class TestDocument:
    """Tests du modèle Document"""
    
    def test_create_facture(self, app, sample_client):
        """Test création d'une facture"""
        with app.app_context():
            import uuid
            numero = f"FAC-TEST-{uuid.uuid4().hex[:8].upper()}"
            
            # Utiliser l'ID directement
            facture = Document(
                type='facture',
                numero=numero,
                client_id=sample_client,
                total_ht=100.00,
                total_tva=20.00,
                total_ttc=120.00,
                statut='brouillon'
            )
            db.session.add(facture)
            db.session.commit()
            
            assert facture.id is not None
            assert facture.type == 'facture'
            assert facture.numero == numero
    
    def test_document_statut(self, app, sample_client):
        """Test changement de statut"""
        with app.app_context():
            import uuid
            numero = f"FAC-TEST-{uuid.uuid4().hex[:8].upper()}"
            
            doc = Document(
                type='facture',
                numero=numero,
                client_id=sample_client,
                statut='brouillon'
            )
            db.session.add(doc)
            db.session.commit()
            
            assert doc.statut == 'brouillon'
            
            # Changer le statut
            doc.statut = 'envoyee'
            db.session.commit()
            assert doc.statut == 'envoyee'