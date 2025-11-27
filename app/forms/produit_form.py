"""
Formulaire Produit
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, SelectField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Optional, Length, NumberRange

class ProduitForm(FlaskForm):
    """Formulaire de création/édition de produit"""
    
    reference = StringField(
        'Référence',
        validators=[Optional(), Length(max=50)]
    )
    
    designation = StringField(
        'Désignation *',
        validators=[DataRequired(message="La désignation est obligatoire"), Length(max=200)]
    )
    
    description = TextAreaField(
        'Description',
        validators=[Optional()]
    )
    
    prix_ht = DecimalField(
        'Prix HT *',
        validators=[DataRequired(message="Le prix HT est obligatoire"), NumberRange(min=0)],
        places=2
    )
    
    taux_tva = DecimalField(
        'Taux TVA (%) *',
        default=20.00,
        validators=[DataRequired(), NumberRange(min=0, max=100)],
        places=2
    )
    
    unite = SelectField(
        'Unité',
        choices=[
            ('piece', 'Pièce'),
            ('kg', 'Kilogramme'),
            ('heure', 'Heure'),
            ('forfait', 'Forfait'),
            ('litre', 'Litre'),
            ('m2', 'Mètre carré')
        ],
        default='piece'
    )
    
    categorie = StringField(
        'Catégorie',
        validators=[Optional(), Length(max=100)]
    )
    
    # Gestion de stock
    gerer_stock = BooleanField(
        'Gérer le stock pour ce produit'
    )
    
    stock_actuel = IntegerField(
        'Stock actuel',
        validators=[Optional(), NumberRange(min=0)],
        default=0
    )
    
    stock_minimum = IntegerField(
        'Stock minimum (seuil d\'alerte)',
        validators=[Optional(), NumberRange(min=0)],
        default=0
    )
