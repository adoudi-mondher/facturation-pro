"""
Modèle Entreprise (Singleton)
"""
from app.extensions import db
from app.models import TimestampMixin

class Entreprise(db.Model, TimestampMixin):
    """Informations de l'entreprise (singleton)"""
    __tablename__ = 'entreprise'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    logo_path = db.Column(db.String(500))
    adresse = db.Column(db.Text)
    code_postal = db.Column(db.String(10))
    ville = db.Column(db.String(100))
    pays = db.Column(db.String(100), default='France')
    siret = db.Column(db.String(20))
    tva_intra = db.Column(db.String(20))
    telephone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    site_web = db.Column(db.String(200))
    taux_tva_defaut = db.Column(db.Numeric(5, 2), default=20.00)
    mentions_legales = db.Column(db.Text)
    cgv = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Entreprise {self.nom}>'
    
    @staticmethod
    def get_instance():
        """Récupère l'instance unique de l'entreprise"""
        entreprise = Entreprise.query.first()
        if not entreprise:
            # Créer une instance par défaut si elle n'existe pas
            entreprise = Entreprise(nom="Mon Entreprise", taux_tva_defaut=20.00)
            db.session.add(entreprise)
            db.session.commit()
        return entreprise
