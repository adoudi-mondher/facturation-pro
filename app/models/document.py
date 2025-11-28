"""
Modèle Document (Facture et Devis)
"""
from app.extensions import db
from app.models import TimestampMixin
from datetime import datetime

class Document(db.Model, TimestampMixin):
    """Document (facture ou devis)"""
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), nullable=False)  # facture, devis
    numero = db.Column(db.String(50), unique=True, nullable=False)
    prefix = db.Column(db.String(10), default='FAC')
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    date_emission = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    date_echeance = db.Column(db.Date)
    statut = db.Column(db.String(20), default='brouillon')
    total_ht = db.Column(db.Numeric(10, 2), default=0.00)
    total_tva = db.Column(db.Numeric(10, 2), default=0.00)
    total_ttc = db.Column(db.Numeric(10, 2), default=0.00)
    remise_globale = db.Column(db.Numeric(10, 2), default=0.00)
    type_remise = db.Column(db.String(15), default='pourcentage')
    conditions_paiement = db.Column(db.Text)
    notes = db.Column(db.Text)
    envoi_email_date = db.Column(db.DateTime)
    date_paiement = db.Column(db.Date)
    pdf_path = db.Column(db.String(500))
    
    # Relations
    client = db.relationship('Client', back_populates='documents')
    lignes = db.relationship('LigneDocument', back_populates='document', 
                            cascade='all, delete-orphan', 
                            order_by='LigneDocument.ordre')
    mouvements_stock = db.relationship('MouvementStock', back_populates='document')
    
    def __repr__(self):
        return f'<Document {self.numero}>'
    
    def calculer_totaux(self):
        """Recalcule les totaux du document"""
        # Somme des lignes HT
        total_ht_lignes = sum(float(ligne.total_ht) for ligne in self.lignes)
        
        # Appliquer remise globale
        if self.type_remise == 'pourcentage':
            montant_remise = total_ht_lignes * (float(self.remise_globale) / 100)
        else:
            montant_remise = float(self.remise_globale)
        
        self.total_ht = total_ht_lignes - montant_remise
        
        # Calculer TVA (somme par taux)
        total_tva_lignes = sum(
            float(ligne.total_ht) * (float(ligne.taux_tva) / 100) 
            for ligne in self.lignes
        )
        
        # Si remise globale, recalculer TVA proportionnellement
        if montant_remise > 0 and total_ht_lignes > 0:
            ratio = float(self.total_ht) / total_ht_lignes
            self.total_tva = total_tva_lignes * ratio
        else:
            self.total_tva = total_tva_lignes
        
        self.total_ttc = float(self.total_ht) + float(self.total_tva)
    
    @property
    def is_editable(self):
        """Vérifie si le document est modifiable"""
        return self.statut == 'brouillon'
    
    @property
    def is_payee(self):
        """Vérifie si la facture est payée"""
        return self.statut == 'payee'
    
    def generate_numero(self):
        """Génère le numéro de document automatiquement"""
        from app.models.parametre import Parametre
        
        if self.type == 'facture':
            prefix = Parametre.get_valeur('prefix_facture', 'FAC')
            compteur = int(Parametre.get_valeur('numero_facture_compteur', '1'))
        else:
            prefix = Parametre.get_valeur('prefix_devis', 'DEV')
            compteur = int(Parametre.get_valeur('numero_devis_compteur', '1'))
        
        # Format: PREFIX-ANNÉE-XXXXX
        annee = datetime.now().year
        self.numero = f"{prefix}-{annee}-{compteur:05d}"
        self.prefix = prefix
        
        # Incrémenter le compteur
        if self.type == 'facture':
            Parametre.set_valeur('numero_facture_compteur', str(compteur + 1))
        else:
            Parametre.set_valeur('numero_devis_compteur', str(compteur + 1))

    @property
    def lignes_json(self):
        """Retourne les lignes au format JSON pour le JavaScript"""
        import json
        return json.dumps([{
            'produit_id': ligne.produit_id,
            'designation': ligne.designation,
            'quantite': float(ligne.quantite),
            'prix_unitaire_ht': float(ligne.prix_unitaire_ht),
            'taux_tva': float(ligne.taux_tva),
            'remise_ligne': float(ligne.remise_ligne) if ligne.remise_ligne else 0
        } for ligne in self.lignes])
