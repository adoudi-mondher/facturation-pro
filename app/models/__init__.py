"""
Models SQLAlchemy
"""
from datetime import datetime
from app.extensions import db

class TimestampMixin:
    """Mixin pour ajouter created_at et updated_at automatiquement"""
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

# Importer tous les modèles pour qu'ils soient disponibles
from app.models.entreprise import Entreprise
from app.models.client import Client
from app.models.produit import Produit
from app.models.document import Document
from app.models.ligne_document import LigneDocument
from app.models.mouvement_stock import MouvementStock
from app.models.parametre import Parametre

__all__ = [
    'TimestampMixin',
    'Entreprise',
    'Client',
    'Produit',
    'Document',
    'LigneDocument',
    'MouvementStock',
    'Parametre'
]
