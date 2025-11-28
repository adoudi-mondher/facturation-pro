"""
Routes API
Fournit des données JSON pour les formulaires dynamiques
"""
from flask import Blueprint, jsonify
from app.models.produit import Produit
from app.models.client import Client

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/produits')
def get_produits():
    """Liste des produits pour le formulaire de facture"""
    produits = Produit.query.filter_by(actif=True).order_by(Produit.designation).all()
    
    return jsonify([{
        'id': p.id,
        'reference': p.reference,
        'designation': p.designation,
        'prix_ht': float(p.prix_ht),
        'taux_tva': float(p.taux_tva),
        'gerer_stock': p.gerer_stock,
        'stock_actuel': p.stock_actuel if p.gerer_stock else None
    } for p in produits])

@bp.route('/clients')
def get_clients():
    """Liste des clients pour le formulaire de facture"""
    clients = Client.query.filter_by(actif=True).order_by(Client.nom).all()
    
    return jsonify([{
        'id': c.id,
        'nom_complet': c.nom_complet,
        'email': c.email,
        'adresse': c.adresse,
        'code_postal': c.code_postal,
        'ville': c.ville
    } for c in clients])
