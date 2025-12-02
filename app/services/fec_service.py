"""
Service d'export FEC (Fichier des Écritures Comptables)
Conforme à la réglementation française
"""
from datetime import datetime
from decimal import Decimal
import os


class FECService:
    """Service d'export au format FEC"""
    
    # Plan comptable français standard
    COMPTE_CLIENT = "411"  # Clients
    COMPTE_TVA = "44571"   # TVA collectée
    COMPTE_VENTES = "707000"  # Ventes de marchandises
    
    JOURNAL_CODE = "VE"    # Journal des ventes
    JOURNAL_LIB = "Ventes"
    
    def __init__(self, entreprise):
        """
        Initialise le service FEC
        
        Args:
            entreprise: Instance Entreprise pour les infos SIRET
        """
        self.entreprise = entreprise
    
    @staticmethod
    def generate_fec(documents, date_debut=None, date_fin=None, entreprise=None):
        """
        Génère un fichier FEC pour une liste de documents
        
        Args:
            documents: Liste de Documents (factures)
            date_debut: Date de début de période (optionnel)
            date_fin: Date de fin de période (optionnel)
            entreprise: Instance Entreprise
            
        Returns:
            str: Contenu du fichier FEC
        """
        service = FECService(entreprise)
        
        # En-tête FEC (18 colonnes obligatoires)
        header = "JournalCode|JournalLib|EcritureNum|EcritureDate|CompteNum|CompteLib|CompAuxNum|CompAuxLib|PieceRef|PieceDate|EcritureLib|Debit|Credit|EcritureLet|DateLet|ValidDate|Montantdevise|Idevise\n"
        
        lines = [header]
        
        # Filtrer par date si nécessaire
        filtered_docs = documents
        if date_debut:
            filtered_docs = [d for d in filtered_docs if d.date_emission >= date_debut]
        if date_fin:
            filtered_docs = [d for d in filtered_docs if d.date_emission <= date_fin]
        
        # Trier par date
        filtered_docs = sorted(filtered_docs, key=lambda d: d.date_emission)
        
        # Générer les écritures pour chaque document
        for doc in filtered_docs:
            # Ignorer les brouillons
            if doc.statut == 'brouillon':
                continue
            
            lines.extend(service._generate_document_lines(doc))
        
        return "".join(lines)
    
    def _generate_document_lines(self, document):
        """
        Génère les 3 lignes FEC pour un document (facture)
        
        Args:
            document: Document (facture)
            
        Returns:
            list: Liste des lignes FEC
        """
        lines = []
        
        # Infos communes
        journal_code = self.JOURNAL_CODE
        journal_lib = self.JOURNAL_LIB
        ecriture_num = document.numero.replace('/', '')  # Enlever les /
        ecriture_date = document.date_emission.strftime('%Y%m%d')
        piece_ref = document.numero
        piece_date = document.date_emission.strftime('%Y%m%d')
        valid_date = document.date_emission.strftime('%Y%m%d')
        
        # Client - Code auxiliaire (max 13 caractères)
        client_code = self._generate_client_code(document.client)
        client_lib = document.client.nom_complet[:100]  # Max 100 car
        
        # Montants
        montant_ttc = float(document.total_ttc)
        montant_tva = float(document.total_tva)
        montant_ht = float(document.total_ht)
        
        # LIGNE 1 : Débit Client (411xxx)
        line1 = self._format_line(
            journal_code=journal_code,
            journal_lib=journal_lib,
            ecriture_num=ecriture_num,
            ecriture_date=ecriture_date,
            compte_num=self.COMPTE_CLIENT + client_code[:10],  # 411 + code client
            compte_lib="Clients",
            comp_aux_num=client_code,
            comp_aux_lib=client_lib,
            piece_ref=piece_ref,
            piece_date=piece_date,
            ecriture_lib=f"Facture {document.numero} - {client_lib[:50]}",
            debit=montant_ttc,
            credit=0.0,
            valid_date=valid_date
        )
        lines.append(line1)
        
        # LIGNE 2 : Crédit TVA (44571)
        if montant_tva > 0:
            line2 = self._format_line(
                journal_code=journal_code,
                journal_lib=journal_lib,
                ecriture_num=ecriture_num,
                ecriture_date=ecriture_date,
                compte_num=self.COMPTE_TVA,
                compte_lib="TVA collectée",
                comp_aux_num="",
                comp_aux_lib="",
                piece_ref=piece_ref,
                piece_date=piece_date,
                ecriture_lib=f"TVA collectée - Facture {document.numero}",
                debit=0.0,
                credit=montant_tva,
                valid_date=valid_date
            )
            lines.append(line2)
        
        # LIGNE 3 : Crédit Ventes (707000)
        line3 = self._format_line(
            journal_code=journal_code,
            journal_lib=journal_lib,
            ecriture_num=ecriture_num,
            ecriture_date=ecriture_date,
            compte_num=self.COMPTE_VENTES,
            compte_lib="Ventes de marchandises",
            comp_aux_num="",
            comp_aux_lib="",
            piece_ref=piece_ref,
            piece_date=piece_date,
            ecriture_lib=f"Ventes - Facture {document.numero}",
            debit=0.0,
            credit=montant_ht,
            valid_date=valid_date
        )
        lines.append(line3)
        
        return lines
    
    def _format_line(self, journal_code, journal_lib, ecriture_num, ecriture_date,
                     compte_num, compte_lib, comp_aux_num, comp_aux_lib,
                     piece_ref, piece_date, ecriture_lib, debit, credit, valid_date):
        """
        Formate une ligne FEC
        
        Returns:
            str: Ligne FEC avec séparateur |
        """
        # Format des montants : 2 décimales, virgule comme séparateur
        debit_str = f"{debit:.2f}".replace('.', ',')
        credit_str = f"{credit:.2f}".replace('.', ',')
        
        # Colonnes FEC (18 colonnes obligatoires)
        columns = [
            journal_code,           # 1. JournalCode
            journal_lib,            # 2. JournalLib
            ecriture_num,           # 3. EcritureNum
            ecriture_date,          # 4. EcritureDate (YYYYMMDD)
            compte_num,             # 5. CompteNum
            compte_lib,             # 6. CompteLib
            comp_aux_num,           # 7. CompAuxNum (code client)
            comp_aux_lib,           # 8. CompAuxLib (nom client)
            piece_ref,              # 9. PieceRef
            piece_date,             # 10. PieceDate (YYYYMMDD)
            ecriture_lib,           # 11. EcritureLib
            debit_str,              # 12. Debit
            credit_str,             # 13. Credit
            "",                     # 14. EcritureLet (lettrage)
            "",                     # 15. DateLet
            valid_date,             # 16. ValidDate (YYYYMMDD)
            debit_str if debit > 0 else credit_str,  # 17. Montantdevise
            "EUR"                   # 18. Idevise
        ]
        
        return "|".join(columns) + "\n"
    
    def _generate_client_code(self, client):
        """
        Génère un code client pour le FEC (max 13 caractères)
        
        Args:
            client: Instance Client
            
        Returns:
            str: Code client
        """
        # Utiliser les 4 premières lettres du nom + ID
        nom_clean = ''.join(c for c in client.nom.upper() if c.isalnum())[:4]
        return f"{nom_clean}{client.id}"
    
    @staticmethod
    def get_fec_filename(entreprise, date_debut=None, date_fin=None):
        """
        Génère le nom du fichier FEC selon la norme
        Format: SIRET + FEC + YYYYMMDD (début exercice) + YYYYMMDD (fin exercice)
        
        Args:
            entreprise: Instance Entreprise
            date_debut: Date de début
            date_fin: Date de fin
            
        Returns:
            str: Nom du fichier
        """
        siret = (entreprise.siret or "00000000000000").replace(' ', '')[:14]
        
        if not date_debut:
            date_debut = datetime(datetime.now().year, 1, 1).date()
        if not date_fin:
            date_fin = datetime.now().date()
        
        debut_str = date_debut.strftime('%Y%m%d')
        fin_str = date_fin.strftime('%Y%m%d')
        
        return f"{siret}FEC{debut_str}{fin_str}.txt"
