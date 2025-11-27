"""
Formulaire Client
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, EmailField, TelField
from wtforms.validators import DataRequired, Email, Optional, Length

class ClientForm(FlaskForm):
    """Formulaire de création/édition de client"""
    
    type = SelectField(
        'Type de client',
        choices=[('particulier', 'Particulier'), ('entreprise', 'Entreprise')],
        default='particulier'
    )
    
    # Champs particulier
    prenom = StringField(
        'Prénom',
        validators=[Optional(), Length(max=100)]
    )
    
    nom = StringField(
        'Nom *',
        validators=[DataRequired(message="Le nom est obligatoire"), Length(max=100)]
    )
    
    # Champ entreprise
    raison_sociale = StringField(
        'Raison sociale',
        validators=[Optional(), Length(max=200)]
    )
    
    # Contact
    email = EmailField(
        'Email',
        validators=[Optional(), Email(message="Email invalide")]
    )
    
    telephone = StringField(
        'Téléphone',
        validators=[Optional(), Length(max=20)]
    )
    
    # Adresse
    adresse = TextAreaField(
        'Adresse',
        validators=[Optional()]
    )
    
    code_postal = StringField(
        'Code postal',
        validators=[Optional(), Length(max=10)]
    )
    
    ville = StringField(
        'Ville',
        validators=[Optional(), Length(max=100)]
    )
    
    pays = StringField(
        'Pays',
        default='France',
        validators=[Optional(), Length(max=100)]
    )
    
    # Notes
    notes = TextAreaField(
        'Notes internes',
        validators=[Optional()]
    )
