"""
Formulaire Facture
"""
from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, TextAreaField, HiddenField
from wtforms.validators import DataRequired
from datetime import datetime, timedelta

class FactureForm(FlaskForm):
    """Formulaire de création/édition de facture"""
    
    client_id = SelectField(
        'Client *',
        coerce=int,
        validators=[DataRequired(message="Veuillez sélectionner un client")]
    )
    
    date_emission = DateField(
        'Date d\'émission *',
        default=datetime.now().date(),
        validators=[DataRequired()]
    )
    
    date_echeance = DateField(
        'Date d\'échéance',
        default=lambda: (datetime.now() + timedelta(days=30)).date()
    )
    
    statut = SelectField(
        'Statut',
        choices=[
            ('brouillon', 'Brouillon'),
            ('envoyee', 'Envoyée'),
            ('payee', 'Payée')
        ],
        default='brouillon'
    )
    
    conditions_paiement = SelectField(
        'Conditions de paiement',
        choices=[
            ('Paiement à réception', 'Paiement à réception'),
            ('Paiement à 15 jours', 'Paiement à 15 jours'),
            ('Paiement à 30 jours', 'Paiement à 30 jours'),
            ('Paiement à 45 jours', 'Paiement à 45 jours'),
            ('Paiement à 60 jours', 'Paiement à 60 jours')
        ],
        default='Paiement à 30 jours'
    )
    
    notes = TextAreaField('Notes')
    
    # Les lignes seront gérées dynamiquement en JavaScript
