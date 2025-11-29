"""
Routes Documents (Factures et Devis)
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, current_app
from app.models.document import Document
from app.models.client import Client
from app.models.ligne_document import LigneDocument
from app.models.produit import Produit
from app.models.mouvement_stock import MouvementStock
from app.models.entreprise import Entreprise
from app.services.pdf_service import PDFService
from app.forms.facture_form import FactureForm
from app.forms.devis_form import DevisForm
from app.extensions import db
from datetime import datetime, timedelta
import os

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

@bp.route('/factures/edit/<int:id>', methods=['GET', 'POST'])
def edit_facture(id):
    """Modifier une facture (brouillon ou envoyée uniquement)"""
    facture = Document.query.get_or_404(id)
    
    # Vérifier le statut - payée = non modifiable
    if facture.statut == 'payee':
        flash('⚠️ Cette facture est payée. Pour la modifier, créez un avoir.', 'error')
        return redirect(url_for('documents.view', id=id))
    
    # Avertissement si envoyée
    if facture.statut == 'envoyee':
        flash('⚠️ Attention : cette facture a déjà été envoyée au client.', 'warning')
    
    form = FactureForm(obj=facture)
    
    # Charger les clients pour le select
    clients = Client.query.filter_by(actif=True).order_by(Client.nom).all()
    form.client_id.choices = [(0, '-- Sélectionner un client --')] + [(c.id, c.nom_complet) for c in clients]
    
    if form.validate_on_submit():
        try:
            # Annuler les mouvements de stock existants si facture n'était pas brouillon
            if facture.statut != 'brouillon':
                for ligne in facture.lignes:
                    if ligne.produit.gerer_stock:
                        # Remettre le stock
                        ligne.produit.stock_actuel += ligne.quantite
            
            # Supprimer les anciennes lignes
            LigneDocument.query.filter_by(document_id=facture.id).delete()
            MouvementStock.query.filter_by(reference_document_id=facture.id).delete()
            
            # Mettre à jour les infos de base
            facture.client_id = form.client_id.data
            facture.date_emission = form.date_emission.data
            facture.date_echeance = form.date_echeance.data
            facture.statut = form.statut.data
            facture.conditions_paiement = form.conditions_paiement.data
            facture.notes = form.notes.data
            
            # Récupérer les nouvelles lignes depuis le formulaire
            lignes_data = {}
            remise_globale = float(request.form.get('remise_globale', 0))
            
            for key, value in request.form.items():
                if key.startswith('lignes[') and value:
                    parts = key.split('[')
                    ligne_id = parts[1].rstrip(']')
                    field_name = parts[2].rstrip(']')
                    
                    if ligne_id not in lignes_data:
                        lignes_data[ligne_id] = {}
                    
                    lignes_data[ligne_id][field_name] = value
            
            # Créer les nouvelles lignes
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
                            commentaire=f"Facture {facture.numero} (modifiée)"
                        )
                        db.session.add(mouvement)
                    
                    ordre += 1
            
            # Appliquer la remise globale et calculer les totaux
            facture.remise_globale = remise_globale
            facture.calculer_totaux()
            
            db.session.commit()
            
            flash(f'✅ Facture {facture.numero} modifiée avec succès', 'success')
            return redirect(url_for('documents.view', id=facture.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Erreur lors de la modification : {str(e)}', 'error')
            return redirect(url_for('documents.edit_facture', id=id))
    
    # Pré-remplir le formulaire avec les données existantes
    if request.method == 'GET':
        form.client_id.data = facture.client_id
        form.date_emission.data = facture.date_emission
        form.date_echeance.data = facture.date_echeance
        form.statut.data = facture.statut
        form.conditions_paiement.data = facture.conditions_paiement
        form.notes.data = facture.notes
    
    return render_template('documents/edit_facture.html', 
                         form=form, 
                         facture=facture)

@bp.route('/devis')
def devis_list():
    """Liste des devis"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    statut = request.args.get('statut', '')  # ← AJOUTER
    
    query = Document.query.filter_by(type='devis')
    
    if search:
        query = query.join(Document.client).filter(
            db.or_(
                Document.numero.ilike(f'%{search}%'),
                Document.client.has(Client.nom.ilike(f'%{search}%'))  # ← Chercher aussi dans le nom du client
            )
        )
    
    if statut:  # ← AJOUTER
        query = query.filter_by(statut=statut)
    
    devis = query.order_by(Document.date_emission.desc())\
        .paginate(page=page, per_page=20, error_out=False)
    
    return render_template('documents/devis_list.html', 
                         devis=devis, 
                         search=search,
                         statut=statut)  # ← AJOUTER

@bp.route('/devis/create', methods=['GET', 'POST'])
def create_devis():
    """Créer un nouveau devis"""
    form = DevisForm()
    
    # Charger les clients pour le select
    clients = Client.query.filter_by(actif=True).order_by(Client.nom).all()
    form.client_id.choices = [(0, '-- Sélectionner un client --')] + [(c.id, c.nom_complet) for c in clients]
    
    if form.validate_on_submit():
        try:
            # Créer le devis
            devis = Document(
                type='devis',
                client_id=form.client_id.data,
                date_emission=form.date_emission.data,
                date_echeance=form.date_validite.data,  # date_validite pour devis
                statut=form.statut.data,
                notes=form.notes.data
            )
            
            # Générer le numéro
            devis.generate_numero()
            
            db.session.add(devis)
            db.session.flush()
            
            # Récupérer les lignes (identique aux factures)
            lignes_data = {}
            remise_globale = float(request.form.get('remise_globale', 0))
            
            for key, value in request.form.items():
                if key.startswith('lignes[') and value:
                    parts = key.split('[')
                    ligne_id = parts[1].rstrip(']')
                    field_name = parts[2].rstrip(']')
                    
                    if ligne_id not in lignes_data:
                        lignes_data[ligne_id] = {}
                    
                    lignes_data[ligne_id][field_name] = value
            
            # Créer les lignes (PAS de mouvement de stock pour les devis !)
            ordre = 0
            for ligne_id, ligne_info in lignes_data.items():
                if 'produit_id' in ligne_info and ligne_info['produit_id']:
                    produit = Produit.query.get(int(ligne_info['produit_id']))
                    
                    if not produit:
                        continue
                    
                    ligne = LigneDocument(
                        document_id=devis.id,
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
                    ordre += 1
            
            # Appliquer la remise globale et calculer les totaux
            devis.remise_globale = remise_globale
            devis.calculer_totaux()
            
            db.session.commit()
            
            flash(f'Devis {devis.numero} créé avec succès', 'success')
            return redirect(url_for('documents.devis_list'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la création du devis : {str(e)}', 'error')
            return redirect(url_for('documents.create_devis'))
    
    return render_template('documents/create_devis.html', form=form)

@bp.route('/devis/edit/<int:id>', methods=['GET', 'POST'])
def edit_devis(id):
    """Modifier un devis (brouillon ou envoyé uniquement)"""
    devis = Document.query.get_or_404(id)
    
    # Vérifier le statut - accepté/refusé = non modifiable
    if devis.statut in ['accepte', 'refuse']:
        flash(f'⚠️ Ce devis est {devis.statut}. Impossible de le modifier.', 'error')
        return redirect(url_for('documents.view', id=id))
    
    # Avertissement si envoyé
    if devis.statut == 'envoye':
        flash('⚠️ Attention : ce devis a déjà été envoyé au client.', 'warning')
    
    form = DevisForm(obj=devis)
    
    # Charger les clients
    clients = Client.query.filter_by(actif=True).order_by(Client.nom).all()
    form.client_id.choices = [(0, '-- Sélectionner un client --')] + [(c.id, c.nom_complet) for c in clients]
    
    if form.validate_on_submit():
        try:
            # Supprimer les anciennes lignes
            LigneDocument.query.filter_by(document_id=devis.id).delete()
            
            # Mettre à jour
            devis.client_id = form.client_id.data
            devis.date_emission = form.date_emission.data
            devis.date_echeance = form.date_validite.data
            devis.statut = form.statut.data
            devis.notes = form.notes.data
            
            # Récupérer les nouvelles lignes
            lignes_data = {}
            remise_globale = float(request.form.get('remise_globale', 0))
            
            for key, value in request.form.items():
                if key.startswith('lignes[') and value:
                    parts = key.split('[')
                    ligne_id = parts[1].rstrip(']')
                    field_name = parts[2].rstrip(']')
                    
                    if ligne_id not in lignes_data:
                        lignes_data[ligne_id] = {}
                    
                    lignes_data[ligne_id][field_name] = value
            
            # Créer les nouvelles lignes
            ordre = 0
            for ligne_id, ligne_info in lignes_data.items():
                if 'produit_id' in ligne_info and ligne_info['produit_id']:
                    produit = Produit.query.get(int(ligne_info['produit_id']))
                    
                    if not produit:
                        continue
                    
                    ligne = LigneDocument(
                        document_id=devis.id,
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
                    ordre += 1
            
            # Appliquer la remise globale et calculer les totaux
            devis.remise_globale = remise_globale
            devis.calculer_totaux()
            
            db.session.commit()
            
            flash(f'✅ Devis {devis.numero} modifié avec succès', 'success')
            return redirect(url_for('documents.view', id=devis.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Erreur lors de la modification : {str(e)}', 'error')
            return redirect(url_for('documents.edit_devis', id=id))
    
    # Pré-remplir
    if request.method == 'GET':
        form.client_id.data = devis.client_id
        form.date_emission.data = devis.date_emission
        form.date_validite.data = devis.date_echeance
        form.statut.data = devis.statut
        form.notes.data = devis.notes
    
    return render_template('documents/edit_devis.html', 
                         form=form, 
                         devis=devis)

@bp.route('/factures/<int:id>/pdf')
def facture_pdf(id):
    """Générer le PDF d'une facture"""
    facture = Document.query.get_or_404(id)
    
    if facture.type != 'facture':
        flash('❌ Ce document n\'est pas une facture', 'error')
        return redirect(url_for('documents.view', id=id))
    
    try:
       # Récupérer les infos entreprise
        ent = Entreprise.get_instance()
        entreprise = {
            'nom_entreprise': ent.nom or 'Mon Entreprise',
            'adresse': ent.adresse or '',
            'code_postal': ent.code_postal or '',
            'ville': ent.ville or '',
            'telephone': ent.telephone or '',
            'email': ent.email or '',
            'siret': ent.siret or '',
            'tva_intra': ent.tva_intra or '',
            'mentions_legales': ent.mentions_legales or '',
            'logo_path': ent.logo_path or ''
        }
        
        # Générer le PDF
        pdf_service = PDFService(facture, entreprise)
        
        # Chemin du PDF (chemin absolu depuis la racine du projet)
        pdf_dir = os.path.join(os.path.dirname(current_app.root_path), 'data', 'pdf')
        os.makedirs(pdf_dir, exist_ok=True)
        pdf_filename = f"facture_{facture.numero.replace('/', '_')}.pdf"
        pdf_path = os.path.join(pdf_dir, pdf_filename)
        
        # Générer
        pdf_service.generate(pdf_path)
        
        # Sauvegarder le chemin en BDD
        facture.pdf_path = pdf_path
        db.session.commit()
        
        # Envoyer le fichier
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=pdf_filename
        )
        
    except Exception as e:
        flash(f'❌ Erreur lors de la génération du PDF : {str(e)}', 'error')
        return redirect(url_for('documents.view', id=id))

@bp.route('/devis/<int:id>/pdf')
def devis_pdf(id):
    """Générer le PDF d'un devis"""
    devis = Document.query.get_or_404(id)
    
    if devis.type != 'devis':
        flash('❌ Ce document n\'est pas un devis', 'error')
        return redirect(url_for('documents.view', id=id))
    
    try:
        # Récupérer les infos entreprise
        ent = Entreprise.get_instance()
        entreprise = {
            'nom_entreprise': ent.nom or 'Mon Entreprise',
            'adresse': ent.adresse or '',
            'code_postal': ent.code_postal or '',
            'ville': ent.ville or '',
            'telephone': ent.telephone or '',
            'email': ent.email or '',
            'siret': ent.siret or '',
            'tva_intra': ent.tva_intra or '',
            'mentions_legales': ent.mentions_legales or '',
            'logo_path': ent.logo_path or ''
        }
        
        # Générer le PDF
        pdf_service = PDFService(devis, entreprise)
        
        # Chemin du PDF (chemin absolu depuis la racine du projet)
        pdf_dir = os.path.join(os.path.dirname(current_app.root_path), 'data', 'pdf')
        os.makedirs(pdf_dir, exist_ok=True)
        pdf_filename = f"devis_{devis.numero.replace('/', '_')}.pdf"
        pdf_path = os.path.join(pdf_dir, pdf_filename)
        
        # Générer
        pdf_service.generate(pdf_path)
        
        # Sauvegarder le chemin en BDD
        devis.pdf_path = pdf_path
        db.session.commit()
        
        # Envoyer le fichier
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=pdf_filename
        )
        
    except Exception as e:
        flash(f'❌ Erreur lors de la génération du PDF : {str(e)}', 'error')
        return redirect(url_for('documents.view', id=id))

@bp.route('/view/<int:id>')
def view(id):
    """Voir un document"""
    document = Document.query.get_or_404(id)
    return render_template('documents/view.html', document=document)

@bp.route('/devis/<int:id>/convert-to-facture', methods=['POST'])
def convert_devis_to_facture(id):
    """Convertir un devis en facture"""
    devis = Document.query.get_or_404(id)
    
    # Vérifier que c'est bien un devis
    if devis.type != 'devis':
        flash('❌ Ce document n\'est pas un devis', 'error')
        return redirect(url_for('documents.view', id=id))
    
    # Vérifier le statut
    if devis.statut == 'refuse':
        flash('❌ Impossible de convertir un devis refusé', 'error')
        return redirect(url_for('documents.view', id=id))
    
    try:
        # Créer la facture
        facture = Document(
            type='facture',
            client_id=devis.client_id,
            date_emission=datetime.now().date(),
            date_echeance=(datetime.now() + timedelta(days=30)).date(),
            statut='brouillon',
            conditions_paiement='Paiement à 30 jours',
            notes=f"Facture créée depuis le devis {devis.numero}\n\n{devis.notes or ''}",
            remise_globale=devis.remise_globale
        )
        
        # Générer le numéro
        facture.generate_numero()
        db.session.add(facture)
        db.session.flush()
        
        # Copier les lignes
        for ligne_devis in devis.lignes:
            ligne_facture = LigneDocument(
                document_id=facture.id,
                produit_id=ligne_devis.produit_id,
                designation=ligne_devis.designation,
                quantite=ligne_devis.quantite,
                prix_unitaire_ht=ligne_devis.prix_unitaire_ht,
                taux_tva=ligne_devis.taux_tva,
                remise_ligne=ligne_devis.remise_ligne,
                ordre=ligne_devis.ordre
            )
            ligne_facture.calculer_total()
            db.session.add(ligne_facture)
            
            # Gérer le stock (la facture est en brouillon, donc pas de mouvement pour l'instant)
            # Le stock sera impacté quand on changera le statut en "envoyée" ou "payée"
        
        # Calculer les totaux
        facture.calculer_totaux()
        
        # Marquer le devis comme accepté
        devis.statut = 'accepte'
        
        db.session.commit()
        
        flash(f'✅ Facture {facture.numero} créée depuis le devis {devis.numero}', 'success')
        return redirect(url_for('documents.view', id=facture.id))
        
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Erreur lors de la conversion : {str(e)}', 'error')
        return redirect(url_for('documents.view', id=id))
