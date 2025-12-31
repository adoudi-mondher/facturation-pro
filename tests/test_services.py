"""
Tests des services - Easy Facture
"""
import pytest
from app.services.pdf_service import PDFService
from app.services.fec_service import FECService
from app.services.excel_service import ExcelService
from app.services.csv_service import CSVService
from app.models.document import Document
from app.models.client import Client
from app.models.entreprise import Entreprise
from app.extensions import db
from datetime import datetime
import os

class TestPDFService:
    """Tests du service PDF"""
    
    def test_generate_pdf_facture(self, app, sample_client):
        """Test génération PDF facture"""
        with app.app_context():
            client = Client.query.get(sample_client.id)
            entreprise = Entreprise.get_instance()
            
            # Créer une facture
            facture = Document(
                type='facture',
                numero='FAC-TEST-001',
                client_id=client.id,
                total_ht=100.00,
                total_tva=20.00,
                total_ttc=120.00,
                statut='brouillon'
            )
            db.session.add(facture)
            db.session.commit()
            
            # Générer le PDF
            pdf_path = PDFService.generate_facture_pdf(facture, entreprise)
            
            # Vérifier que le fichier existe
            assert pdf_path is not None
            assert os.path.exists(pdf_path)
            assert pdf_path.endswith('.pdf')
            
            # Nettoyer
            if os.path.exists(pdf_path):
                os.remove(pdf_path)

class TestFECService:
    """Tests du service FEC"""
    
    def test_generate_fec(self, app, sample_client):
        """Test génération FEC"""
        with app.app_context():
            client = Client.query.get(sample_client.id)
            entreprise = Entreprise.get_instance()
            
            # Créer une facture
            facture = Document(
                type='facture',
                numero='FAC-2025-00001',
                client_id=client.id,
                date_emission=datetime.now().date(),
                total_ht=100.00,
                total_tva=20.00,
                total_ttc=120.00,
                statut='envoyee'
            )
            db.session.add(facture)
            db.session.commit()
            
            # Générer le FEC
            fec_content = FECService.generate_fec([facture], entreprise=entreprise)
            
            # Vérifications
            assert fec_content is not None
            assert 'JournalCode' in fec_content  # Header
            assert 'FAC-2025-00001' in fec_content  # Numéro facture
            assert '|' in fec_content  # Séparateur pipe
    
    def test_fec_filename(self, app):
        """Test génération nom fichier FEC"""
        with app.app_context():
            entreprise = Entreprise.get_instance()
            entreprise.siret = "12345678900000"
            
            filename = FECService.get_fec_filename(entreprise)
            
            assert filename.startswith("12345678900000FEC")
            assert filename.endswith(".txt")

class TestExcelService:
    """Tests du service Excel"""
    
    def test_generate_excel(self, app, sample_client):
        """Test génération Excel"""
        with app.app_context():
            client = Client.query.get(sample_client.id)
            entreprise = Entreprise.get_instance()
            
            # Créer des factures
            factures = []
            for i in range(3):
                facture = Document(
                    type='facture',
                    numero=f'FAC-2025-{i:05d}',
                    client_id=client.id,
                    total_ht=100.00 + i * 10,
                    total_tva=20.00 + i * 2,
                    total_ttc=120.00 + i * 12,
                    statut='envoyee'
                )
                factures.append(facture)
            
            db.session.add_all(factures)
            db.session.commit()
            
            # Générer l'Excel
            wb = ExcelService.generate_factures_excel(factures, entreprise=entreprise)
            
            # Vérifications
            assert wb is not None
            assert 'Factures' in wb.sheetnames
            assert 'Statistiques' in wb.sheetnames

class TestCSVService:
    """Tests du service CSV"""
    
    def test_generate_csv(self, app, sample_client):
        """Test génération CSV"""
        with app.app_context():
            client = Client.query.get(sample_client.id)
            
            # Créer des factures
            factures = []
            for i in range(3):
                facture = Document(
                    type='facture',
                    numero=f'FAC-2025-{i:05d}',
                    client_id=client.id,
                    date_emission=datetime.now().date(),
                    total_ht=100.00,
                    total_tva=20.00,
                    total_ttc=120.00,
                    statut='envoyee'
                )
                factures.append(facture)
            
            db.session.add_all(factures)
            db.session.commit()
            
            # Générer le CSV
            csv_content = CSVService.generate_factures_csv(factures)
            
            # Vérifications
            assert csv_content is not None
            assert 'Numéro;Date' in csv_content or 'Numéro' in csv_content
            assert ';' in csv_content  # Séparateur point-virgule
            assert 'FAC-2025' in csv_content
