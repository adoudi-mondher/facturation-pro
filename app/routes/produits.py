"""
Routes Produits
"""
from flask import Blueprint, render_template, request
from app.models.produit import Produit
from app.extensions import db

bp = Blueprint('produits', __name__, url_prefix='/produits')

@bp.route('/')
def list():
    """Liste des produits"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Produit.query
    
    if search:
        query = query.filter(
            db.or_(
                Produit.designation.ilike(f'%{search}%'),
                Produit.reference.ilike(f'%{search}%'),
                Produit.categorie.ilike(f'%{search}%')
            )
        )
    
    produits = query.filter_by(actif=True)\
        .order_by(Produit.designation)\
        .paginate(page=page, per_page=20, error_out=False)
    
    return render_template('produits/list.html', 
                         produits=produits, 
                         search=search)

@bp.route('/view/<int:id>')
def view(id):
    """Voir un produit"""
    produit = Produit.query.get_or_404(id)
    
    # Historique stock si géré
    mouvements = []
    if produit.gerer_stock:
        mouvements = produit.mouvements_stock[:20]  # 20 derniers mouvements
    
    return render_template('produits/view.html', 
                         produit=produit,
                         mouvements=mouvements)
