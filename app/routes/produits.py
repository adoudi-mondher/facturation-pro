"""
Routes Produits
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.produit import Produit
from app.forms.produit_form import ProduitForm
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

@bp.route('/create', methods=['GET', 'POST'])
def create():
    """Créer un nouveau produit"""
    form = ProduitForm()
    
    if form.validate_on_submit():
        produit = Produit()
        form.populate_obj(produit)
        
        db.session.add(produit)
        db.session.commit()
        
        flash(f'Produit {produit.designation} créé avec succès', 'success')
        return redirect(url_for('produits.view', id=produit.id))
    
    return render_template('produits/create.html', form=form)

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

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    """Modifier un produit"""
    produit = Produit.query.get_or_404(id)
    form = ProduitForm(obj=produit)
    
    if form.validate_on_submit():
        form.populate_obj(produit)
        db.session.commit()
        
        flash(f'Produit {produit.designation} modifié avec succès', 'success')
        return redirect(url_for('produits.view', id=produit.id))
    
    return render_template('produits/edit.html', form=form, produit=produit)

@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    """Supprimer un produit (soft delete)"""
    produit = Produit.query.get_or_404(id)
    
    # Soft delete : on désactive juste
    produit.actif = False
    db.session.commit()
    
    flash(f'Produit {produit.designation} désactivé', 'success')
    return redirect(url_for('produits.list'))
