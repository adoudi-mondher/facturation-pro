"""
Modèle Mouvement de stock
"""
from app.extensions import db
from datetime import datetime

class MouvementStock(db.Model):
    """Mouvement de stock (entrée/sortie)"""
    __tablename__ = 'mouvements_stock'
    
    id = db.Column(db.Integer, primary_key=True)
    produit_id = db.Column(db.Integer, db.ForeignKey('produits.id'), nullable=False)
    type_mouvement = db.Column(db.String(20), nullable=False)  # entree, sortie, ajustement, facture
    quantite = db.Column(db.Numeric(10, 2), nullable=False)
    stock_avant = db.Column(db.Numeric(10, 2))
    stock_apres = db.Column(db.Numeric(10, 2))
    reference_document_id = db.Column(db.Integer, db.ForeignKey('documents.id'))
    commentaire = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relations
    produit = db.relationship('Produit', back_populates='mouvements_stock')
    document = db.relationship('Document', back_populates='mouvements_stock')
    
    def __repr__(self):
        return f'<MouvementStock {self.type_mouvement} {self.quantite}>'
