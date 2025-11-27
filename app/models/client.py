"""
Modèle Client
"""
from app.extensions import db
from app.models import TimestampMixin

class Client(db.Model, TimestampMixin):
    """Client (particulier ou entreprise)"""
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), default='particulier')  # particulier, entreprise
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100))
    raison_sociale = db.Column(db.String(200))
    email = db.Column(db.String(100))
    telephone = db.Column(db.String(20))
    adresse = db.Column(db.Text)
    code_postal = db.Column(db.String(10))
    ville = db.Column(db.String(100))
    pays = db.Column(db.String(100), default='France')
    notes = db.Column(db.Text)
    actif = db.Column(db.Boolean, default=True)
    
    # Relations
    documents = db.relationship('Document', back_populates='client', lazy='dynamic')
    
    def __repr__(self):
        return f'<Client {self.nom_complet}>'
    
    @property
    def nom_complet(self):
        """Retourne le nom complet du client"""
        if self.type == 'entreprise':
            return self.raison_sociale or self.nom
        else:
            parts = []
            if self.prenom:
                parts.append(self.prenom)
            parts.append(self.nom)
            return ' '.join(parts)
    
    @property
    def nb_factures(self):
        """Nombre de factures du client"""
        return self.documents.filter_by(type='facture').count()
    
    @property
    def total_ca(self):
        """Chiffre d'affaires total du client"""
        from app.models.document import Document
        total = db.session.query(db.func.sum(Document.total_ttc))\
            .filter(Document.client_id == self.id)\
            .filter(Document.type == 'facture')\
            .filter(Document.statut.in_(['envoyee', 'payee']))\
            .scalar()
        return float(total) if total else 0.0
