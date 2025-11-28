"""
Routes Documents (Factures et Devis)
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.document import Document
from app.models.client import Client
from app.models.ligne_document import LigneDocument
from app.models.produit import Produit
from app.models.mouvement_stock import MouvementStock
from app.forms.facture_form import FactureForm
from app.extensions import db
from datetime import datetime

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

@bp.route('/factures/create', methods=['GET', 'POST'])
def create_facture():
    """Créer une nouvelle facture"""
    form = FactureForm()
    
    # Charger les clients pour le select
    clients = Client.query.filter_by(actif=True).order_by(Client.nom).all()
    form.client_id.choices = [(0, '-- Sélectionner un client --')] + [(c.id, c.nom_complet) for c in clients]
    
    if form.validate_on_submit():
        try:
            # Créer la facture
            facture = Document(
                type='facture',
                client_id=form.client_id.data,
                date_emission=form.date_emission.data,
                date_echeance=form.date_echeance.data,
                statut=form.statut.data,
                conditions_paiement=form.conditions_paiement.data,
                notes=form.notes.data
            )
            
            # Générer le numéro
            facture.generate_numero()
            
            db.session.add(facture)
            db.session.flush()  # Pour avoir l'ID
            
            # Récupérer les lignes depuis le formulaire
            lignes_data = {}
            remise_globale = float(request.form.get('remise_globale', 0))
            
            # Parser les lignes (format: lignes[1][produit_id], lignes[1][quantite], etc.)
            for key, value in request.form.items():
                if key.startswith('lignes[') and value:
                    # Extraire l'index de la ligne et le champ
                    parts = key.split('[')
                    ligne_id = parts[1].rstrip(']')
                    field_name = parts[2].rstrip(']')
                    
                    if ligne_id not in lignes_data:
                        lignes_data[ligne_id] = {}
                    
                    lignes_data[ligne_id][field_name] = value
            
            # Créer les lignes
            ordre = 0
            for ligne_id, ligne_info in lignes_data.items():
                if 'produit_id' in ligne_info and ligne_info['produit_id']:
                    produit = Produit.query.get(int(ligne_info['produit_id']))
                    
                    if not produit:
                        continue
                    
                    ligne = LigneDocument(
                        document_id=facture.id,
                        produit_id=produit.id,
                        designation=ligne_info.get('designation', produit.designation),
                        quantite=float(ligne_info.get('quantite', 1)),
                        prix_unitaire_ht=float(ligne_info.get('prix_unitaire_ht', produit.prix_ht)),
                        taux_tva=float(ligne_info.get('taux_tva', produit.taux_tva)),
                        remise_ligne=float(ligne_info.get('remise_ligne', 0)),
                        ordre=ordre
                    )
                    ligne.calculer_total()
                    db.session.add(ligne)
                    
                    # Gérer le stock si le statut n'est pas brouillon
                    if facture.statut != 'brouillon' and produit.gerer_stock:
                        stock_avant = produit.stock_actuel or 0
                        produit.stock_actuel = stock_avant - int(ligne.quantite)
                        stock_apres = produit.stock_actuel
                        
                        # Créer le mouvement de stock
                        mouvement = MouvementStock(
                            produit_id=produit.id,
                            type_mouvement='facture',
                            quantite=-ligne.quantite,
                            stock_avant=stock_avant,
                            stock_apres=stock_apres,
                            reference_document_id=facture.id,
                            commentaire=f"Facture {facture.numero}"
                        )
                        db.session.add(mouvement)
                    
                    ordre += 1
            
            # Appliquer la remise globale et calculer les totaux
            facture.remise_globale = remise_globale
            facture.calculer_totaux()
            
            db.session.commit()
            
            flash(f'Facture {facture.numero} créée avec succès', 'success')
            return redirect(url_for('documents.view', id=facture.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la création de la facture : {str(e)}', 'error')
            return redirect(url_for('documents.create_facture'))
    
    return render_template('documents/create_facture.html', form=form)

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
