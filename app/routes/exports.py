"""
Routes Exports (FEC, Excel, CSV)
À AJOUTER dans app/routes/__init__.py ou créer un nouveau fichier app/routes/exports.py
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, make_response
from app.models.document import Document
from app.models.entreprise import Entreprise
from app.services.fec_service import FECService
from app.services.excel_service import ExcelService
from app.services.csv_service import CSVService
from datetime import datetime, timedelta
from io import BytesIO

bp = Blueprint('exports', __name__, url_prefix='/exports')


@bp.route('/')
def index():
    """Page d'accueil des exports"""
    return render_template('exports/index.html')


@bp.route('/fec', methods=['GET', 'POST'])
def export_fec():
    """Export FEC (Fichier des Écritures Comptables)"""
    
    if request.method == 'GET':
        # Afficher le formulaire avec dates par défaut
        date_debut_default = datetime.now().replace(month=1, day=1).strftime('%Y-%m-%d')
        date_fin_default = datetime.now().strftime('%Y-%m-%d')
        return render_template('exports/fec.html', 
                             date_debut_default=date_debut_default,
                             date_fin_default=date_fin_default)
    
    # POST : Générer le FEC
    try:
        # Récupérer les dates
        date_debut_str = request.form.get('date_debut')
        date_fin_str = request.form.get('date_fin')
        
        date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d').date() if date_debut_str else None
        date_fin = datetime.strptime(date_fin_str, '%Y-%m-%d').date() if date_fin_str else None
        
        # Récupérer les factures
        factures = Document.query.filter_by(type='facture').all()
        
        # Récupérer infos entreprise
        entreprise = Entreprise.get_instance()
        
        # Générer le FEC
        fec_content = FECService.generate_fec(
            documents=factures,
            date_debut=date_debut,
            date_fin=date_fin,
            entreprise=entreprise
        )
        
        # Nom du fichier
        filename = FECService.get_fec_filename(entreprise, date_debut, date_fin)
        
        # Créer la réponse
        response = make_response(fec_content)
        response.headers['Content-Type'] = 'text/plain; charset=utf-8'
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        
        flash(f'✅ Export FEC généré : {filename}', 'success')
        return response
        
    except Exception as e:
        flash(f'❌ Erreur lors de l\'export FEC : {str(e)}', 'error')
        return redirect(url_for('exports.export_fec'))


@bp.route('/excel', methods=['GET', 'POST'])
def export_excel():
    """Export Excel"""
    
    if request.method == 'GET':
        # Afficher le formulaire avec dates par défaut
        date_debut_default = datetime.now().replace(month=1, day=1).strftime('%Y-%m-%d')
        date_fin_default = datetime.now().strftime('%Y-%m-%d')
        return render_template('exports/excel.html',
                             date_debut_default=date_debut_default,
                             date_fin_default=date_fin_default)
    
    # POST : Générer l'Excel
    try:
        # Récupérer les dates
        date_debut_str = request.form.get('date_debut')
        date_fin_str = request.form.get('date_fin')
        
        date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d').date() if date_debut_str else None
        date_fin = datetime.strptime(date_fin_str, '%Y-%m-%d').date() if date_fin_str else None
        
        # Récupérer les factures
        factures = Document.query.filter_by(type='facture').all()
        
        # Récupérer infos entreprise
        entreprise = Entreprise.get_instance()
        
        # Générer l'Excel
        wb = ExcelService.generate_factures_excel(
            documents=factures,
            date_debut=date_debut,
            date_fin=date_fin,
            entreprise=entreprise
        )
        
        # Sauvegarder dans un buffer
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        
        # Nom du fichier
        filename = ExcelService.get_excel_filename(date_debut, date_fin)
        
        # Envoyer le fichier
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        flash(f'❌ Erreur lors de l\'export Excel : {str(e)}', 'error')
        return redirect(url_for('exports.export_excel'))


@bp.route('/csv', methods=['GET', 'POST'])
def export_csv():
    """Export CSV"""
    
    if request.method == 'GET':
        # Afficher le formulaire avec dates par défaut
        date_debut_default = datetime.now().replace(month=1, day=1).strftime('%Y-%m-%d')
        date_fin_default = datetime.now().strftime('%Y-%m-%d')
        return render_template('exports/csv.html',
                             date_debut_default=date_debut_default,
                             date_fin_default=date_fin_default)
    
    # POST : Générer le CSV
    try:
        # Récupérer les dates
        date_debut_str = request.form.get('date_debut')
        date_fin_str = request.form.get('date_fin')
        
        date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d').date() if date_debut_str else None
        date_fin = datetime.strptime(date_fin_str, '%Y-%m-%d').date() if date_fin_str else None
        
        # Récupérer les factures
        factures = Document.query.filter_by(type='facture').all()
        
        # Générer le CSV
        csv_content = CSVService.generate_factures_csv(
            documents=factures,
            date_debut=date_debut,
            date_fin=date_fin
        )
        
        # Nom du fichier
        filename = CSVService.get_csv_filename(date_debut, date_fin)
        
        # Créer la réponse
        response = make_response(csv_content)
        response.headers['Content-Type'] = 'text/csv; charset=utf-8'
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        
        flash(f'✅ Export CSV généré : {filename}', 'success')
        return response
        
    except Exception as e:
        flash(f'❌ Erreur lors de l\'export CSV : {str(e)}', 'error')
        return redirect(url_for('exports.export_csv'))
