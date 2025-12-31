"""
Tests des routes - Easy Facture
"""
import pytest
from flask import url_for

class TestMainRoutes:
    """Tests des routes principales"""
    
    def test_dashboard(self, client):
        """Test page tableau de bord"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Tableau de bord' in response.data or b'Dashboard' in response.data
    
    def test_dashboard_redirect(self, client):
        """Test redirection vers dashboard"""
        response = client.get('/')
        # Si redirection vers /dashboard
        assert response.status_code in [200, 302]

class TestClientRoutes:
    """Tests des routes clients"""
    
    def test_clients_list(self, client):
        """Test liste des clients"""
        response = client.get('/clients/')
        assert response.status_code == 200
    
    def test_client_create_get(self, client):
        """Test affichage formulaire création client"""
        response = client.get('/clients/create')
        assert response.status_code == 200
        assert b'form' in response.data.lower()
    
    def test_client_create_post(self, client):
        """Test création d'un client via POST"""
        response = client.post('/clients/create', data={
            'nom': 'TestNom',
            'prenom': 'TestPrenom',
            'email': 'test@test.com',
            'telephone': '0123456789'
        }, follow_redirects=True)
        
        assert response.status_code == 200

class TestProduitRoutes:
    """Tests des routes produits"""
    
    def test_produits_list(self, client):
        """Test liste des produits"""
        response = client.get('/produits/')
        assert response.status_code == 200
    
    def test_produit_create_get(self, client):
        """Test affichage formulaire création produit"""
        response = client.get('/produits/create')
        assert response.status_code == 200

class TestDocumentRoutes:
    """Tests des routes documents"""
    
    def test_factures_list(self, client):
        """Test liste des factures"""
        response = client.get('/documents/factures')
        assert response.status_code == 200
    
    def test_devis_list(self, client):
        """Test liste des devis"""
        response = client.get('/documents/devis')
        assert response.status_code == 200
    
    def test_facture_create_get(self, client, sample_client):
        """Test affichage formulaire création facture"""
        response = client.get('/documents/facture/create')
        assert response.status_code == 200

class TestExportRoutes:
    """Tests des routes d'export"""
    
    def test_exports_index(self, client):
        """Test page exports"""
        response = client.get('/exports/')
        assert response.status_code == 200
    
    def test_export_fec_get(self, client):
        """Test affichage formulaire export FEC"""
        response = client.get('/exports/fec')
        assert response.status_code == 200
    
    def test_export_excel_get(self, client):
        """Test affichage formulaire export Excel"""
        response = client.get('/exports/excel')
        assert response.status_code == 200
    
    def test_export_csv_get(self, client):
        """Test affichage formulaire export CSV"""
        response = client.get('/exports/csv')
        assert response.status_code == 200

class TestParametresRoutes:
    """Tests des routes paramètres"""
    
    def test_parametres_index(self, client):
        """Test page paramètres"""
        response = client.get('/parametres/')
        assert response.status_code == 200
