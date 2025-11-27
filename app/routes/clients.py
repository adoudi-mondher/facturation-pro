"""
Routes Clients
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models.client import Client
from app.forms.client_form import ClientForm
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

@bp.route('/create', methods=['GET', 'POST'])
def create():
    """Créer un nouveau client"""
    form = ClientForm()
    
    if form.validate_on_submit():
        client = Client()
        form.populate_obj(client)
        
        db.session.add(client)
        db.session.commit()
        
        flash(f'Client {client.nom_complet} créé avec succès', 'success')
        return redirect(url_for('clients.view', id=client.id))
    
    return render_template('clients/create.html', form=form)

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

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    """Modifier un client"""
    client = Client.query.get_or_404(id)
    form = ClientForm(obj=client)
    
    if form.validate_on_submit():
        form.populate_obj(client)
        db.session.commit()
        
        flash(f'Client {client.nom_complet} modifié avec succès', 'success')
        return redirect(url_for('clients.view', id=client.id))
    
    return render_template('clients/edit.html', form=form, client=client)

@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    """Supprimer un client (soft delete)"""
    client = Client.query.get_or_404(id)
    
    # Vérifier qu'il n'a pas de factures
    if client.documents.count() > 0:
        flash('Impossible de supprimer un client avec des factures/devis', 'error')
        return redirect(url_for('clients.view', id=id))
    
    # Soft delete : on désactive juste
    client.actif = False
    db.session.commit()
    
    flash(f'Client {client.nom_complet} désactivé', 'success')
    return redirect(url_for('clients.list'))
