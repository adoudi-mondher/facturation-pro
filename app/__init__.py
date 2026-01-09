"""
Factory Flask - Création de l'application
"""
from flask import Flask
from config import config

def create_app(config_name='default'):
    """
    Factory pour créer l'application Flask
    
    Args:
        config_name: Nom de la configuration ('development', 'production', 'default')
    
    Returns:
        Application Flask configurée
    """
    app = Flask(__name__, static_folder='../static')
    
    # Charger la configuration
    app.config.from_object(config[config_name])

    # Initialiser les extensions
    from app.extensions import db
    db.init_app(app)

    # Filtres Jinja2 personnalisés (AVANT blueprints)
    register_template_filters(app)

    # Before request handler pour injecter license_status dans flask.g
    @app.before_request
    def load_license_status():
        """Charge le statut de licence avant chaque requête"""
        from flask import g
        try:
            from app.utils.license import LicenseManager
            license_manager = LicenseManager()
            g.license_status = license_manager.get_license_status()
        except Exception as e:
            # Fallback gracieux si erreur
            g.license_status = {
                'is_valid': True,
                'license_type': 'trial',
                'days_left': 15,
                'message': 'Mode développement (erreur)',
                'should_show_cta': True,
                'email': ''
            }

    # Context processor pour injecter g.license_status dans les templates
    @app.context_processor
    def inject_license_status():
        """Injecte le statut de licence dans tous les templates"""
        from flask import g
        return {'license_status': getattr(g, 'license_status', None)}

    # Enregistrer les blueprints (routes)
    from app.routes import main, clients, produits, documents, parametres, api, rapports
    app.register_blueprint(main.bp)
    app.register_blueprint(clients.bp)
    app.register_blueprint(produits.bp)
    app.register_blueprint(documents.bp)
    app.register_blueprint(parametres.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(rapports.bp)
    from app.routes import exports
    app.register_blueprint(exports.bp)

    # Route pour servir les fichiers uploadés
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        """Servir les fichiers uploadés"""
        import os
        from flask import send_from_directory
        upload_folder = app.config['UPLOAD_FOLDER']
        return send_from_directory(upload_folder, filename)

    # Créer les tables et initialiser les données
    with app.app_context():
        db.create_all()
        init_default_data()

    return app

def init_default_data():
    """Initialise les données par défaut"""
    from app.extensions import db
    from app.models.entreprise import Entreprise
    from app.models.parametre import Parametre
    
    # Créer l'entreprise par défaut si elle n'existe pas
    if not Entreprise.query.first():
        entreprise = Entreprise(
            nom="Mon Entreprise",
            taux_tva_defaut=20.00,
            pays="France"
        )
        db.session.add(entreprise)
    
    # Paramètres par défaut
    params_defaut = [
        ('numero_facture_compteur', '1', 'Compteur auto-incrémenté factures'),
        ('numero_devis_compteur', '1', 'Compteur auto-incrémenté devis'),
        ('prefix_facture', 'FAC', 'Préfixe numéros de facture'),
        ('prefix_devis', 'DEV', 'Préfixe numéros de devis'),
    ]
    
    for cle, valeur, desc in params_defaut:
        if not Parametre.query.filter_by(cle=cle).first():
            param = Parametre(cle=cle, valeur=valeur, description=desc)
            db.session.add(param)
    
    db.session.commit()

def register_template_filters(app):
    """Enregistre les filtres Jinja2 personnalisés"""
    
    @app.template_filter('currency')
    def currency_filter(value):
        """Formate un nombre en devise EUR"""
        if value is None:
            return "0,00 €"
        return f"{float(value):,.2f} €".replace(',', ' ').replace('.', ',')
    
    @app.template_filter('date_fr')
    def date_fr_filter(value):
        """Formate une date au format français"""
        if value is None:
            return ""
        if hasattr(value, 'strftime'):
            return value.strftime('%d/%m/%Y')
        return str(value)
    
    @app.template_filter('datetime_fr')
    def datetime_fr_filter(value):
        """Formate une datetime au format français"""
        if value is None:
            return ""
        if hasattr(value, 'strftime'):
            return value.strftime('%d/%m/%Y %H:%M')
        return str(value)

