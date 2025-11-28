"""
Formulaire Devis
"""
from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired
from datetime import datetime, timedelta

class DevisForm(FlaskForm):
    """Formulaire de création/édition de devis"""
    
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
    
    date_validite = DateField(
        'Date de validité',
        default=lambda: (datetime.now() + timedelta(days=30)).date()
    )
    
    statut = SelectField(
        'Statut',
        choices=[
            ('brouillon', 'Brouillon'),
            ('envoye', 'Envoyé'),
            ('accepte', 'Accepté'),
            ('refuse', 'Refusé')
        ],
        default='brouillon'
    )
    
    notes = TextAreaField('Notes')
    
    # Les lignes seront gérées dynamiquement en JavaScript
