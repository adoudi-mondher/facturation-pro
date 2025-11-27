"""
Routes principales - Dashboard
"""
from flask import Blueprint, render_template
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from app.models.document import Document
from app.models.client import Client
from app.models.produit import Produit
from app.extensions import db

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/dashboard')
def dashboard():
    """Page d'accueil / Tableau de bord"""
    
    # Statistiques générales
    nb_clients = Client.query.filter_by(actif=True).count()
    nb_produits = Produit.query.filter_by(actif=True).count()
    
    # Factures du mois en cours
    debut_mois = datetime.now().replace(day=1)
    nb_factures_mois = Document.query.filter(
        Document.type == 'facture',
        Document.date_emission >= debut_mois
    ).count()
    
    # CA du mois en cours
    ca_mois = db.session.query(func.sum(Document.total_ttc)).filter(
        Document.type == 'facture',
        Document.statut.in_(['envoyee', 'payee']),
        Document.date_emission >= debut_mois
    ).scalar() or 0
    
    # Factures récentes (5 dernières)
    factures_recentes = Document.query\
        .filter_by(type='facture')\
        .order_by(Document.created_at.desc())\
        .limit(5)\
        .all()
    
    # Alertes stock
    produits_rupture = Produit.query\
        .filter(Produit.gerer_stock == True)\
        .filter(Produit.stock_actuel == 0)\
        .count()
    
    produits_alerte = Produit.query\
        .filter(Produit.gerer_stock == True)\
        .filter(Produit.stock_actuel > 0)\
        .filter(Produit.stock_actuel <= Produit.stock_minimum)\
        .count()
    
    stats = {
        'nb_clients': nb_clients,
        'nb_produits': nb_produits,
        'nb_factures_mois': nb_factures_mois,
        'ca_mois': float(ca_mois),
        'produits_rupture': produits_rupture,
        'produits_alerte': produits_alerte
    }
    
    return render_template('dashboard/index.html',
                         stats=stats,
                         factures_recentes=factures_recentes)
