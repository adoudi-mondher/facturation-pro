"""
Modèle Produit
"""
from app.extensions import db
from app.models import TimestampMixin

class Produit(db.Model, TimestampMixin):
    """Produit ou service"""
    __tablename__ = 'produits'
    
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(50), unique=True)
    designation = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    prix_ht = db.Column(db.Numeric(10, 2), nullable=False)
    taux_tva = db.Column(db.Numeric(5, 2), default=20.00)
    unite = db.Column(db.String(20), default='piece')  # piece, kg, heure, forfait, m2, litre
    categorie = db.Column(db.String(100))
    gerer_stock = db.Column(db.Boolean, default=False)
    stock_actuel = db.Column(db.Integer)
    stock_minimum = db.Column(db.Integer)
    actif = db.Column(db.Boolean, default=True)
    
    # Relations
    lignes_document = db.relationship('LigneDocument', back_populates='produit')
    mouvements_stock = db.relationship('MouvementStock', back_populates='produit', 
                                      order_by='MouvementStock.created_at.desc()')
    
    def __repr__(self):
        return f'<Produit {self.designation}>'
    
    @property
    def prix_ttc(self):
        """Calcule le prix TTC"""
        return float(self.prix_ht) * (1 + float(self.taux_tva) / 100)
    
    @property
    def stock_statut(self):
        """Statut du stock : non_gere, ok, alerte, rupture"""
        if not self.gerer_stock:
            return 'non_gere'
        if self.stock_actuel is None or self.stock_actuel == 0:
            return 'rupture'
        if self.stock_minimum and self.stock_actuel <= self.stock_minimum:
            return 'alerte'
        return 'ok'
    
    @property
    def stock_disponible(self):
        """Vérifie si le stock est disponible"""
        if not self.gerer_stock:
            return True
        return self.stock_actuel and self.stock_actuel > 0
    
    def verifier_stock(self, quantite):
        """Vérifie si la quantité demandée est disponible"""
        if not self.gerer_stock:
            return True
        if self.stock_actuel is None:
            return False
        return self.stock_actuel >= quantite
