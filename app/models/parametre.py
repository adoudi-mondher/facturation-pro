"""
Modèle Paramètre (système clé-valeur)
"""
from app.extensions import db
from app.models import TimestampMixin

class Parametre(db.Model, TimestampMixin):
    """Paramètres de configuration (clé-valeur)"""
    __tablename__ = 'parametres'
    
    id = db.Column(db.Integer, primary_key=True)
    cle = db.Column(db.String(100), unique=True, nullable=False)
    valeur = db.Column(db.Text)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Parametre {self.cle}={self.valeur}>'
    
    @staticmethod
    def get_valeur(cle, defaut=None):
        """Récupère la valeur d'un paramètre"""
        param = Parametre.query.filter_by(cle=cle).first()
        return param.valeur if param else defaut
    
    @staticmethod
    def set_valeur(cle, valeur, description=None):
        """Définit la valeur d'un paramètre"""
        param = Parametre.query.filter_by(cle=cle).first()
        if param:
            param.valeur = valeur
            if description:
                param.description = description
        else:
            param = Parametre(cle=cle, valeur=valeur, description=description)
            db.session.add(param)
        db.session.commit()
        return param
