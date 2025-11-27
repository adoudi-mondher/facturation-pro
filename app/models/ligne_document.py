"""
Modèle Ligne de document
"""
from app.extensions import db

class LigneDocument(db.Model):
    """Ligne de document (facture ou devis)"""
    __tablename__ = 'lignes_document'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produits.id'))
    designation = db.Column(db.Text, nullable=False)
    quantite = db.Column(db.Numeric(10, 2), default=1.00)
    prix_unitaire_ht = db.Column(db.Numeric(10, 2), nullable=False)
    taux_tva = db.Column(db.Numeric(5, 2), default=20.00)
    remise_ligne = db.Column(db.Numeric(10, 2), default=0.00)
    type_remise_ligne = db.Column(db.String(15), default='pourcentage')
    total_ht = db.Column(db.Numeric(10, 2), nullable=False)
    ordre = db.Column(db.Integer, default=0)
    
    # Relations
    document = db.relationship('Document', back_populates='lignes')
    produit = db.relationship('Produit', back_populates='lignes_document')
    
    def __repr__(self):
        return f'<LigneDocument {self.designation}>'
    
    def calculer_total(self):
        """Calcule le total HT de la ligne"""
        subtotal = float(self.quantite) * float(self.prix_unitaire_ht)
        
        if self.type_remise_ligne == 'pourcentage':
            montant_remise = subtotal * (float(self.remise_ligne) / 100)
        else:
            montant_remise = float(self.remise_ligne)
        
        self.total_ht = subtotal - montant_remise
        return self.total_ht
