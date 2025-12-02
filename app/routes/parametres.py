"""
Routes Paramètres
"""
import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from werkzeug.utils import secure_filename
from app.models.entreprise import Entreprise
from app.extensions import db

bp = Blueprint('parametres', __name__, url_prefix='/parametres')

def allowed_file(filename):
    """Vérifie si l'extension du fichier est autorisée"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

    # Configuration SMTP
    entreprise.smtp_server = request.form.get('smtp_server', '')
    entreprise.smtp_port = int(request.form.get('smtp_port', 587))
    entreprise.smtp_user = request.form.get('smtp_user', '')
    smtp_password = request.form.get('smtp_password', '')
    if smtp_password:
        entreprise.smtp_password = smtp_password
    entreprise.smtp_use_tls = request.form.get('smtp_use_tls') == 'on'
    
    # Gérer l'upload du logo
    if 'logo' in request.files:
        file = request.files['logo']
        if file and file.filename and allowed_file(file.filename):
            # Sécuriser le nom du fichier
            filename = secure_filename(file.filename)
            # Ajouter un timestamp pour éviter les conflits
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            
            # Chemin de sauvegarde
            upload_folder = current_app.config['LOGOS_FOLDER']
            filepath = upload_folder / filename
            
            # Sauvegarder le fichier
            file.save(str(filepath))
            
            # Supprimer l'ancien logo si existe
            if entreprise.logo_path and os.path.exists(entreprise.logo_path):
                try:
                    os.remove(entreprise.logo_path)
                except:
                    pass
            
            # Enregistrer le nouveau chemin
            entreprise.logo_path = str(filepath)
            flash('Logo uploadé avec succès', 'success')
    
    db.session.commit()
    
    flash('Paramètres sauvegardés avec succès', 'success')
    return redirect(url_for('parametres.index'))

@bp.route('/delete_logo')
def delete_logo():
    """Supprimer le logo"""
    entreprise = Entreprise.get_instance()
    
    if entreprise.logo_path and os.path.exists(entreprise.logo_path):
        try:
            os.remove(entreprise.logo_path)
            entreprise.logo_path = None
            db.session.commit()
            flash('Logo supprimé', 'success')
        except Exception as e:
            flash(f'Erreur lors de la suppression : {str(e)}', 'error')
    
    return redirect(url_for('parametres.index'))
