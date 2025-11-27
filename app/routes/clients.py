"""
Routes Clients
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models.client import Client
from app.extensions import db

bp = Blueprint('clients', __name__, url_prefix='/clients')

@bp.route('/')
def list():
    """Liste des clients"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Client.query
    
    if search:
        query = query.filter(
            db.or_(
                Client.nom.ilike(f'%{search}%'),
                Client.prenom.ilike(f'%{search}%'),
                Client.email.ilike(f'%{search}%'),
                Client.raison_sociale.ilike(f'%{search}%')
            )
        )
    
    clients = query.filter_by(actif=True)\
        .order_by(Client.nom)\
        .paginate(page=page, per_page=20, error_out=False)
    
    return render_template('clients/list.html', 
                         clients=clients, 
                         search=search)

@bp.route('/view/<int:id>')
def view(id):
    """Voir un client"""
    client = Client.query.get_or_404(id)
    
    # Historique des factures
    from app.models.document import Document
    factures = Document.query.filter_by(client_id=id, type='facture')\
        .order_by(Document.date_emission.desc())\
        .limit(10)\
        .all()
    
    return render_template('clients/view.html', 
                         client=client,
                         factures=factures)

# Les routes create, edit, delete seront ajoutées avec les forms
