"""
Service d'export CSV simple
"""
import csv
from io import StringIO
from datetime import datetime


class CSVService:
    """Service d'export CSV universel"""
    
    @staticmethod
    def generate_factures_csv(documents, date_debut=None, date_fin=None):
        """
        Génère un fichier CSV avec la liste des factures
        
        Args:
            documents: Liste de Documents (factures)
            date_debut: Date de début (optionnel)
            date_fin: Date de fin (optionnel)
            
        Returns:
            str: Contenu CSV
        """
        output = StringIO()
        writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        
        # En-têtes
        headers = [
            "Numéro",
            "Date émission",
            "Client",
            "Email client",
            "Téléphone client",
            "Statut",
            "Total HT",
            "Total TVA",
            "Total TTC",
            "Date échéance",
            "Conditions paiement",
            "Notes"
        ]
        writer.writerow(headers)
        
        # Filtrer par date
        filtered_docs = documents
        if date_debut:
            filtered_docs = [d for d in filtered_docs if d.date_emission >= date_debut]
        if date_fin:
            filtered_docs = [d for d in filtered_docs if d.date_emission <= date_fin]
        
        # Trier par date
        filtered_docs = sorted(filtered_docs, key=lambda d: d.date_emission, reverse=True)
        
        # Mapping statuts
        statut_map = {
            'brouillon': 'Brouillon',
            'envoyee': 'Envoyée',
            'payee': 'Payée'
        }
        
        # Données
        for doc in filtered_docs:
            row = [
                doc.numero,
                doc.date_emission.strftime('%d/%m/%Y'),
                doc.client.nom_complet,
                doc.client.email or "",
                doc.client.telephone or "",
                statut_map.get(doc.statut, doc.statut.capitalize()),
                f"{float(doc.total_ht):.2f}",
                f"{float(doc.total_tva):.2f}",
                f"{float(doc.total_ttc):.2f}",
                doc.date_echeance.strftime('%d/%m/%Y') if doc.date_echeance else "",
                doc.conditions_paiement or "",
                (doc.notes or "").replace('\n', ' ')  # Enlever retours ligne
            ]
            writer.writerow(row)
        
        return output.getvalue()
    
    @staticmethod
    def get_csv_filename(date_debut=None, date_fin=None):
        """Génère le nom du fichier CSV"""
        if date_debut and date_fin:
            return f"factures_{date_debut.strftime('%Y%m%d')}_{date_fin.strftime('%Y%m%d')}.csv"
        else:
            return f"factures_{datetime.now().strftime('%Y%m%d')}.csv"
