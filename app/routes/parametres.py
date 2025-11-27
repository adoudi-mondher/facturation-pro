"""
Routes Paramètres
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models.entreprise import Entreprise
from app.extensions import db

bp = Blueprint('parametres', __name__, url_prefix='/parametres')

@bp.route('/')
def index():
    """Page des paramètres"""
    entreprise = Entreprise.get_instance()
    return render_template('parametres/index.html', entreprise=entreprise)

@bp.route('/save', methods=['POST'])
def save():
    """Sauvegarder les paramètres"""
    entreprise = Entreprise.get_instance()
    
    # Récupérer les données du formulaire
    entreprise.nom = request.form.get('nom', '')
    entreprise.adresse = request.form.get('adresse', '')
    entreprise.code_postal = request.form.get('code_postal', '')
    entreprise.ville = request.form.get('ville', '')
    entreprise.telephone = request.form.get('telephone', '')
    entreprise.email = request.form.get('email', '')
    entreprise.siret = request.form.get('siret', '')
    entreprise.tva_intra = request.form.get('tva_intra', '')
    entreprise.site_web = request.form.get('site_web', '')
    entreprise.taux_tva_defaut = float(request.form.get('taux_tva_defaut', 20.0))
    entreprise.mentions_legales = request.form.get('mentions_legales', '')
    
    db.session.commit()
    
    flash('Paramètres sauvegardés avec succès', 'success')
    return redirect(url_for('parametres.index'))
