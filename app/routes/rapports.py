"""
Routes pour les rapports et statistiques
"""
from flask import Blueprint, render_template, request
from datetime import datetime, timedelta
from sqlalchemy import func, extract
from app.extensions import db
from app.models.document import Document

bp = Blueprint('rapports', __name__, url_prefix='/rapports')

@bp.route('/ca')
def chiffre_affaires():
    """
    Rapport du chiffre d'affaires par mois
    Affiche les 12 derniers mois avec CA HT et TTC
    """
    # Paramètres de la requête
    periode = request.args.get('periode', '12')  # Nombre de mois à afficher
    try:
        nb_mois = int(periode)
        nb_mois = max(1, min(nb_mois, 24))  # Entre 1 et 24 mois
    except ValueError:
        nb_mois = 12

    # Date de début (nb_mois en arrière)
    date_fin = datetime.now()
    date_debut = date_fin - timedelta(days=nb_mois * 30)

    # Requête SQL pour agréger le CA par mois
    # On récupère uniquement les factures payées et envoyées
    resultats = db.session.query(
        extract('year', Document.date_emission).label('annee'),
        extract('month', Document.date_emission).label('mois'),
        func.sum(Document.total_ht).label('ca_ht'),
        func.sum(Document.total_tva).label('ca_tva'),
        func.sum(Document.total_ttc).label('ca_ttc'),
        func.count(Document.id).label('nb_factures')
    ).filter(
        Document.type == 'facture',
        Document.statut.in_(['envoyee', 'payee']),
        Document.date_emission >= date_debut
    ).group_by(
        extract('year', Document.date_emission),
        extract('month', Document.date_emission)
    ).order_by(
        extract('year', Document.date_emission).desc(),
        extract('month', Document.date_emission).desc()
    ).all()

    # Convertir en liste de dictionnaires pour le template
    donnees_ca = []
    total_ht = 0
    total_tva = 0
    total_ttc = 0
    total_factures = 0

    for row in resultats:
        annee = int(row.annee)
        mois = int(row.mois)
        ca_ht = float(row.ca_ht or 0)
        ca_tva = float(row.ca_tva or 0)
        ca_ttc = float(row.ca_ttc or 0)
        nb_factures = int(row.nb_factures or 0)

        # Nom du mois en français
        mois_noms = ['', 'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
                     'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
        mois_nom = mois_noms[mois]

        donnees_ca.append({
            'annee': annee,
            'mois': mois,
            'mois_nom': mois_nom,
            'periode': f"{mois_nom} {annee}",
            'ca_ht': ca_ht,
            'ca_tva': ca_tva,
            'ca_ttc': ca_ttc,
            'nb_factures': nb_factures
        })

        total_ht += ca_ht
        total_tva += ca_tva
        total_ttc += ca_ttc
        total_factures += nb_factures

    # Inverser pour avoir du plus ancien au plus récent dans le graphique
    donnees_ca_graph = list(reversed(donnees_ca))

    return render_template('rapports/ca.html',
                         donnees_ca=donnees_ca,
                         donnees_ca_graph=donnees_ca_graph,
                         total_ht=total_ht,
                         total_tva=total_tva,
                         total_ttc=total_ttc,
                         total_factures=total_factures,
                         periode=nb_mois)
