"""
Routes Documents (Factures et Devis)
"""
from flask import Blueprint, render_template, request
from app.models.document import Document
from app.extensions import db

bp = Blueprint('documents', __name__, url_prefix='/documents')

@bp.route('/factures')
def factures_list():
    """Liste des factures"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    statut = request.args.get('statut', '')
    
    query = Document.query.filter_by(type='facture')
    
    if search:
        query = query.join(Document.client).filter(
            db.or_(
                Document.numero.ilike(f'%{search}%'),
                Document.client.has(Client.nom.ilike(f'%{search}%'))
            )
        )
    
    if statut:
        query = query.filter_by(statut=statut)
    
    factures = query.order_by(Document.date_emission.desc())\
        .paginate(page=page, per_page=20, error_out=False)
    
    return render_template('documents/factures_list.html', 
                         factures=factures, 
                         search=search,
                         statut=statut)

@bp.route('/devis')
def devis_list():
    """Liste des devis"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Document.query.filter_by(type='devis')
    
    if search:
        query = query.filter(
            db.or_(
                Document.numero.ilike(f'%{search}%')
            )
        )
    
    devis = query.order_by(Document.date_emission.desc())\
        .paginate(page=page, per_page=20, error_out=False)
    
    return render_template('documents/devis_list.html', 
                         devis=devis, 
                         search=search)

@bp.route('/view/<int:id>')
def view(id):
    """Voir un document"""
    document = Document.query.get_or_404(id)
    return render_template('documents/view.html', document=document)
