#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de génération de données de démonstration réalistes
Pour créer des screenshots professionnels pour la landing page

Usage:
    python seed_demo_data.py

ATTENTION: Ce script va RÉINITIALISER la base de données!
"""

import os
import sys
from datetime import datetime, timedelta
from decimal import Decimal
import random

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models.entreprise import Entreprise
from app.models.client import Client
from app.models.produit import Produit
from app.models.document import Document
from app.models.ligne_document import LigneDocument
from app.models.parametre import Parametre


def clear_database():
    """Supprime toutes les données (sauf configuration entreprise)"""
    print("🗑️  Suppression des données existantes...")

    # Supprimer dans l'ordre des dépendances
    LigneDocument.query.delete()
    Document.query.delete()
    Client.query.delete()
    Produit.query.delete()

    db.session.commit()
    print("✅ Données supprimées\n")


def create_entreprise():
    """Configure les informations de l'entreprise"""
    print("🏢 Configuration de l'entreprise...")

    entreprise = Entreprise.get_instance()
    entreprise.nom = "Sidr Valley AI"
    entreprise.adresse = "42 Avenue de l'Innovation"
    entreprise.code_postal = "75001"
    entreprise.ville = "Paris"
    entreprise.pays = "France"
    entreprise.siret = "123 456 789 00012"
    entreprise.tva_intra = "FR12 123456789"
    entreprise.telephone = "+33 1 23 45 67 89"
    entreprise.email = "contact@sidrvalley.fr"
    entreprise.site_web = "https://sidrvalley.fr"
    entreprise.taux_tva_defaut = Decimal("20.0")  # TVA France
    entreprise.mentions_legales = "Sidr Valley AI - SARL au capital de 10 000 €\nSiège social: 42 Avenue de l'Innovation, 75001 Paris, France\nSIRET: 123 456 789 00012"

    db.session.commit()
    print(f"✅ Entreprise configurée: {entreprise.nom}\n")

    return entreprise


def create_produits():
    """Crée une liste de produits/services réalistes"""
    print("📦 Création des produits et services...")

    produits_data = [
        {
            'reference': 'CONS-001',
            'designation': 'Consultation stratégique IA',
            'description': 'Consultation d\'expert en intelligence artificielle et stratégie digitale',
            'prix_ht': Decimal('150.00'),
            'taux_tva': Decimal('7.7'),
            'unite': 'heure',
            'categorie': 'Conseil',
        },
        {
            'reference': 'DEV-001',
            'designation': 'Développement application web',
            'description': 'Développement d\'application web sur mesure (Python/Flask)',
            'prix_ht': Decimal('120.00'),
            'taux_tva': Decimal('7.7'),
            'unite': 'heure',
            'categorie': 'Développement',
        },
        {
            'reference': 'DEV-002',
            'designation': 'Développement chatbot IA',
            'description': 'Création et intégration de chatbot intelligent basé sur l\'IA',
            'prix_ht': Decimal('3500.00'),
            'taux_tva': Decimal('7.7'),
            'unite': 'forfait',
            'categorie': 'Développement',
        },
        {
            'reference': 'FORM-001',
            'designation': 'Formation ChatGPT & IA',
            'description': 'Formation complète à l\'utilisation de ChatGPT et outils IA pour entreprises',
            'prix_ht': Decimal('800.00'),
            'taux_tva': Decimal('7.7'),
            'unite': 'journee',
            'categorie': 'Formation',
        },
        {
            'reference': 'FORM-002',
            'designation': 'Workshop automatisation',
            'description': 'Atelier pratique sur l\'automatisation des processus avec l\'IA',
            'prix_ht': Decimal('450.00'),
            'taux_tva': Decimal('7.7'),
            'unite': 'demi-journee',
            'categorie': 'Formation',
        },
        {
            'reference': 'MAINT-001',
            'designation': 'Support technique mensuel',
            'description': 'Support technique et maintenance d\'application (10h/mois)',
            'prix_ht': Decimal('1200.00'),
            'taux_tva': Decimal('7.7'),
            'unite': 'mois',
            'categorie': 'Support',
        },
        {
            'reference': 'AUDIT-001',
            'designation': 'Audit système IA',
            'description': 'Audit complet de vos processus et recommandations d\'intégration IA',
            'prix_ht': Decimal('2500.00'),
            'taux_tva': Decimal('7.7'),
            'unite': 'forfait',
            'categorie': 'Conseil',
        },
        {
            'reference': 'HOST-001',
            'designation': 'Hébergement cloud annuel',
            'description': 'Hébergement cloud sécurisé avec backups quotidiens',
            'prix_ht': Decimal('1800.00'),
            'taux_tva': Decimal('7.7'),
            'unite': 'annee',
            'categorie': 'Infrastructure',
        },
    ]

    produits = []
    for data in produits_data:
        produit = Produit(**data, actif=True)
        db.session.add(produit)
        produits.append(produit)

    db.session.commit()
    print(f"✅ {len(produits)} produits créés\n")

    return produits


def create_clients():
    """Crée des clients variés et réalistes"""
    print("👥 Création des clients...")

    clients_data = [
        {
            'type': 'entreprise',
            'nom': 'TechStart',
            'raison_sociale': 'TechStart Innovation SAS',
            'email': 'contact@techstart.fr',
            'telephone': '+33 1 45 67 89 01',
            'adresse': '15 Rue de l\'Innovation',
            'code_postal': '75002',
            'ville': 'Paris',
            'pays': 'France',
            'notes': 'Startup prometteuse dans la fintech. Très intéressés par l\'IA.',
            'actif': True,
        },
        {
            'type': 'entreprise',
            'nom': 'Dubois',
            'raison_sociale': 'Cabinet Dubois & Associés',
            'email': 'info@cabinet-dubois.fr',
            'telephone': '+33 4 78 90 12 34',
            'adresse': '28 Avenue de la République',
            'code_postal': '69003',
            'ville': 'Lyon',
            'pays': 'France',
            'notes': 'Client fidèle depuis 2 ans. Demandes régulières d\'automatisation.',
            'actif': True,
        },
        {
            'type': 'particulier',
            'nom': 'Martin',
            'prenom': 'Sophie',
            'email': 'sophie.martin@gmail.com',
            'telephone': '+33 6 12 34 56 78',
            'adresse': '8 Chemin des Roses',
            'code_postal': '06000',
            'ville': 'Nice',
            'pays': 'France',
            'notes': 'Consultante indépendante. Besoin de formation continue.',
            'actif': True,
        },
        {
            'type': 'entreprise',
            'nom': 'FormaPro',
            'raison_sociale': 'Association FormaPro',
            'email': 'contact@formapro.fr',
            'telephone': '+33 1 98 76 54 32',
            'adresse': '3 Place de la Formation',
            'code_postal': '92100',
            'ville': 'Boulogne-Billancourt',
            'pays': 'France',
            'notes': 'Association de formation continue. Organise régulièrement des workshops.',
            'actif': True,
        },
        {
            'type': 'entreprise',
            'nom': 'RetailTech',
            'raison_sociale': 'RetailTech Solutions SAS',
            'email': 'direction@retailtech.fr',
            'telephone': '+33 3 23 45 67 89',
            'adresse': '45 Boulevard du Commerce',
            'code_postal': '33000',
            'ville': 'Bordeaux',
            'pays': 'France',
            'notes': 'PME dans le retail. Projet d\'intégration chatbot en cours.',
            'actif': True,
        },
    ]

    clients = []
    for data in clients_data:
        client = Client(**data)
        db.session.add(client)
        clients.append(client)

    db.session.commit()
    print(f"✅ {len(clients)} clients créés\n")

    return clients


def add_ligne(document_id, produit_id, designation, quantite, prix_ht, taux_tva, ordre, remise=0):
    """Helper pour créer une ligne de document avec total calculé"""
    ligne = LigneDocument(
        document_id=document_id,
        produit_id=produit_id,
        designation=designation,
        quantite=quantite,
        prix_unitaire_ht=prix_ht,
        taux_tva=taux_tva,
        remise_ligne=remise,
        ordre=ordre
    )
    ligne.calculer_total()
    db.session.add(ligne)
    return ligne


def create_devis(clients, produits):
    """Crée des devis variés"""
    print("📝 Création des devis...")

    devis_list = []

    # Devis 1: TechStart - Accepté (converti en facture)
    devis1 = Document(
        type='devis',
        client_id=clients[0].id,  # TechStart
        date_emission=datetime.now() - timedelta(days=45),
        date_echeance=datetime.now() - timedelta(days=15),
        statut='accepte',
        conditions_paiement='Paiement à 30 jours fin de mois',
        notes='Merci pour votre confiance. Le projet débutera dès réception de votre accord.',
    )
    devis1.generate_numero()
    db.session.add(devis1)
    db.session.flush()

    # Lignes du devis 1
    add_ligne(
        document_id=devis1.id,
        produit_id=produits[2].id,  # Chatbot IA
        designation='Développement chatbot IA personnalisé',
        quantite=1,
        prix_ht=Decimal('3500.00'),
        taux_tva=Decimal('20.0'),
        ordre=1
    )
    add_ligne(
        document_id=devis1.id,
        produit_id=produits[0].id,  # Consultation
        designation='Consultation stratégique IA (analyse besoins)',
        quantite=8,
        prix_ht=Decimal('150.00'),
        taux_tva=Decimal('20.0'),
        ordre=2
    )

    devis1.calculer_totaux()
    devis_list.append(devis1)

    # Devis 2: Fiduciaire Dubois - En attente
    devis2 = Document(
        type='devis',
        client_id=clients[1].id,  # Fiduciaire Dubois
        date_emission=datetime.now() - timedelta(days=10),
        date_echeance=datetime.now() + timedelta(days=20),
        statut='envoye',
        conditions_paiement='Paiement à 30 jours',
        notes='Devis valable 30 jours. N\'hésitez pas à me contacter pour toute question.',
    )
    devis2.generate_numero()
    db.session.add(devis2)
    db.session.flush()

    add_ligne(
        document_id=devis2.id,
        produit_id=produits[6].id,  # Audit IA
        designation='Audit système IA et automatisation',
        quantite=1,
        prix_ht=Decimal('2500.00'),
        taux_tva=Decimal('20.0'),
        ordre=1
    )
    add_ligne(
        document_id=devis2.id,
        produit_id=produits[0].id,  # Consultation
        designation='Suivi et accompagnement (5h)',
        quantite=5,
        prix_ht=Decimal('150.00'),
        taux_tva=Decimal('20.0'),
        ordre=2
    )

    devis2.calculer_totaux()
    devis_list.append(devis2)

    # Devis 3: Helvetia Formation - Refusé
    devis3 = Document(
        type='devis',
        client_id=clients[3].id,  # Helvetia Formation
        date_emission=datetime.now() - timedelta(days=60),
        date_echeance=datetime.now() - timedelta(days=30),
        statut='refuse',
        conditions_paiement='Paiement à réception',
        notes='Formation collective pour vos membres.',
    )
    devis3.generate_numero()
    db.session.add(devis3)
    db.session.flush()

    add_ligne(
        document_id=devis3.id,
        produit_id=produits[3].id,  # Formation ChatGPT
        designation='Formation ChatGPT & IA (groupe de 12)',
        quantite=2,
        prix_ht=Decimal('800.00'),
        taux_tva=Decimal('20.0'),
        remise=Decimal('10.00'),  # 10% de remise
        ordre=1
    )

    devis3.calculer_totaux()
    devis_list.append(devis3)

    db.session.commit()
    print(f"✅ {len(devis_list)} devis créés\n")

    return devis_list


def create_factures(clients, produits):
    """Crée des factures variées avec différents statuts"""
    print("💰 Création des factures...")

    factures_list = []

    # Facture 1: TechStart - PAYÉE (suite du devis accepté)
    facture1 = Document(
        type='facture',
        client_id=clients[0].id,  # TechStart
        date_emission=datetime.now() - timedelta(days=35),
        date_echeance=datetime.now() - timedelta(days=5),
        statut='payee',
        date_paiement=datetime.now() - timedelta(days=10),
        conditions_paiement='Paiement à 30 jours fin de mois',
        notes='Merci pour votre paiement rapide !',
    )
    facture1.generate_numero()
    db.session.add(facture1)
    db.session.flush()

    add_ligne(
        document_id=facture1.id,
        produit_id=produits[2].id,
        designation='Développement chatbot IA personnalisé',
        quantite=1,
        prix_ht=Decimal('3500.00'),
        taux_tva=Decimal('20.0'),
        ordre=1
    )
    add_ligne(
        document_id=facture1.id,
        produit_id=produits[0].id,
        designation='Consultation stratégique IA (8h)',
        quantite=8,
        prix_ht=Decimal('150.00'),
        taux_tva=Decimal('20.0'),
        ordre=2
    )

    facture1.calculer_totaux()
    factures_list.append(facture1)

    # Facture 2: Fiduciaire Dubois - PAYÉE
    facture2 = Document(
        type='facture',
        client_id=clients[1].id,
        date_emission=datetime.now() - timedelta(days=50),
        date_echeance=datetime.now() - timedelta(days=20),
        statut='payee',
        date_paiement=datetime.now() - timedelta(days=22),
        conditions_paiement='Paiement à 30 jours',
    )
    facture2.generate_numero()
    db.session.add(facture2)
    db.session.flush()

    add_ligne(
        document_id=facture2.id,
        produit_id=produits[1].id,
        designation='Développement module automatisation comptable',
        quantite=24,
        prix_ht=Decimal('120.00'),
        taux_tva=Decimal('20.0'),
        ordre=1
    )

    facture2.calculer_totaux()
    factures_list.append(facture2)

    # Facture 3: Sophie Martin - PAYÉE
    facture3 = Document(
        type='facture',
        client_id=clients[2].id,  # Sophie Martin
        date_emission=datetime.now() - timedelta(days=40),
        date_echeance=datetime.now() - timedelta(days=10),
        statut='payee',
        date_paiement=datetime.now() - timedelta(days=12),
        conditions_paiement='Paiement immédiat',
    )
    facture3.generate_numero()
    db.session.add(facture3)
    db.session.flush()

    add_ligne(
        document_id=facture3.id,
        produit_id=produits[3].id,
        designation='Formation ChatGPT & IA individuelle',
        quantite=1,
        prix_ht=Decimal('800.00'),
        taux_tva=Decimal('20.0'),
        ordre=1
    )

    facture3.calculer_totaux()
    factures_list.append(facture3)

    # Facture 4: Helvetia Formation - PAYÉE
    facture4 = Document(
        type='facture',
        client_id=clients[3].id,
        date_emission=datetime.now() - timedelta(days=25),
        date_echeance=datetime.now() + timedelta(days=5),
        statut='payee',
        date_paiement=datetime.now() - timedelta(days=2),
        conditions_paiement='Paiement à 30 jours',
    )
    facture4.generate_numero()
    db.session.add(facture4)
    db.session.flush()

    add_ligne(
        document_id=facture4.id,
        produit_id=produits[4].id,
        designation='Workshop automatisation (2 sessions)',
        quantite=2,
        prix_ht=Decimal('450.00'),
        taux_tva=Decimal('20.0'),
        ordre=1
    )

    facture4.calculer_totaux()
    factures_list.append(facture4)

    # Facture 5: SwissRetail - EN ATTENTE (récente)
    facture5 = Document(
        type='facture',
        client_id=clients[4].id,  # SwissRetail
        date_emission=datetime.now() - timedelta(days=15),
        date_echeance=datetime.now() + timedelta(days=15),
        statut='envoyee',
        conditions_paiement='Paiement à 30 jours fin de mois',
        notes='Merci de procéder au paiement dans les délais indiqués.',
    )
    facture5.generate_numero()
    db.session.add(facture5)
    db.session.flush()

    add_ligne(
        document_id=facture5.id,
        produit_id=produits[0].id,
        designation='Consultation stratégique e-commerce & IA',
        quantite=12,
        prix_ht=Decimal('150.00'),
        taux_tva=Decimal('20.0'),
        ordre=1
    )
    add_ligne(
        document_id=facture5.id,
        produit_id=produits[4].id,
        designation='Workshop automatisation',
        quantite=1,
        prix_ht=Decimal('450.00'),
        taux_tva=Decimal('20.0'),
        ordre=2
    )

    facture5.calculer_totaux()
    factures_list.append(facture5)

    # Facture 6: Fiduciaire Dubois - Support mensuel PAYÉE
    facture6 = Document(
        type='facture',
        client_id=clients[1].id,
        date_emission=datetime.now() - timedelta(days=30),
        date_echeance=datetime.now(),
        statut='payee',
        date_paiement=datetime.now() - timedelta(days=5),
        conditions_paiement='Paiement mensuel',
    )
    facture6.generate_numero()
    db.session.add(facture6)
    db.session.flush()

    add_ligne(
        document_id=facture6.id,
        produit_id=produits[5].id,
        designation='Support technique mensuel - Décembre 2025',
        quantite=1,
        prix_ht=Decimal('1200.00'),
        taux_tva=Decimal('20.0'),
        ordre=1
    )

    facture6.calculer_totaux()
    factures_list.append(facture6)

    # Facture 7: TechStart - Hébergement PAYÉE
    facture7 = Document(
        type='facture',
        client_id=clients[0].id,
        date_emission=datetime.now() - timedelta(days=20),
        date_echeance=datetime.now() + timedelta(days=10),
        statut='payee',
        date_paiement=datetime.now() - timedelta(days=1),
        conditions_paiement='Paiement annuel anticipé',
    )
    facture7.generate_numero()
    db.session.add(facture7)
    db.session.flush()

    add_ligne(
        document_id=facture7.id,
        produit_id=produits[7].id,
        designation='Hébergement cloud annuel - 2026',
        quantite=1,
        prix_ht=Decimal('1800.00'),
        taux_tva=Decimal('20.0'),
        ordre=1
    )

    facture7.calculer_totaux()
    factures_list.append(facture7)

    # Facture 8: SwissRetail - EN RETARD
    facture8 = Document(
        type='facture',
        client_id=clients[4].id,
        date_emission=datetime.now() - timedelta(days=75),
        date_echeance=datetime.now() - timedelta(days=45),
        statut='envoyee',  # En retard de paiement
        conditions_paiement='Paiement à 30 jours',
        notes='RAPPEL: Cette facture est en attente de paiement depuis plus de 30 jours.',
    )
    facture8.generate_numero()
    db.session.add(facture8)
    db.session.flush()

    add_ligne(
        document_id=facture8.id,
        produit_id=produits[1].id,
        designation='Développement interface backoffice',
        quantite=32,
        prix_ht=Decimal('120.00'),
        taux_tva=Decimal('20.0'),
        ordre=1
    )

    facture8.calculer_totaux()
    factures_list.append(facture8)

    # Facture 9: Sophie Martin - EN ATTENTE
    facture9 = Document(
        type='facture',
        client_id=clients[2].id,
        date_emission=datetime.now() - timedelta(days=5),
        date_echeance=datetime.now() + timedelta(days=25),
        statut='envoyee',
        conditions_paiement='Paiement à 30 jours',
    )
    facture9.generate_numero()
    db.session.add(facture9)
    db.session.flush()

    add_ligne(
        document_id=facture9.id,
        produit_id=produits[0].id,
        designation='Consultation stratégie marketing IA',
        quantite=4,
        prix_ht=Decimal('150.00'),
        taux_tva=Decimal('20.0'),
        ordre=1
    )

    facture9.calculer_totaux()
    factures_list.append(facture9)

    # Facture 10: TechStart - Support mensuel EN ATTENTE
    facture10 = Document(
        type='facture',
        client_id=clients[0].id,
        date_emission=datetime.now() - timedelta(days=2),
        date_echeance=datetime.now() + timedelta(days=28),
        statut='envoyee',
        conditions_paiement='Paiement mensuel à 30 jours',
    )
    facture10.generate_numero()
    db.session.add(facture10)
    db.session.flush()

    add_ligne(
        document_id=facture10.id,
        produit_id=produits[5].id,
        designation='Support technique mensuel - Janvier 2026',
        quantite=1,
        prix_ht=Decimal('1200.00'),
        taux_tva=Decimal('20.0'),
        ordre=1
    )

    facture10.calculer_totaux()
    factures_list.append(facture10)

    # === FACTURES JANVIER 2026 (pour screenshots) ===

    # Facture 11: RetailTech - Formation équipe PAYÉE (début janvier)
    facture11 = Document(
        type='facture',
        client_id=clients[4].id,  # RetailTech
        date_emission=datetime(2026, 1, 8),
        date_echeance=datetime(2026, 2, 7),
        statut='payee',
        date_paiement=datetime(2026, 1, 15),
        conditions_paiement='Paiement à 30 jours',
        notes='Formation équipe de 8 personnes - Merci !',
    )
    facture11.generate_numero()
    db.session.add(facture11)
    db.session.flush()

    add_ligne(
        document_id=facture11.id,
        produit_id=produits[3].id,  # Formation ChatGPT
        designation='Formation ChatGPT & IA pour équipe (8 personnes)',
        quantite=1,
        prix_ht=Decimal('800.00'),
        taux_tva=Decimal('20.0'),
        ordre=1
    )
    add_ligne(
        document_id=facture11.id,
        produit_id=produits[0].id,  # Consultation
        designation='Consultation post-formation (3h)',
        quantite=3,
        prix_ht=Decimal('150.00'),
        taux_tva=Decimal('20.0'),
        ordre=2
    )

    facture11.calculer_totaux()
    factures_list.append(facture11)

    # Facture 12: TechStart - Développement module PAYÉE
    facture12 = Document(
        type='facture',
        client_id=clients[0].id,  # TechStart
        date_emission=datetime(2026, 1, 12),
        date_echeance=datetime(2026, 2, 11),
        statut='payee',
        date_paiement=datetime(2026, 1, 20),
        conditions_paiement='Paiement à 30 jours',
    )
    facture12.generate_numero()
    db.session.add(facture12)
    db.session.flush()

    add_ligne(
        document_id=facture12.id,
        produit_id=produits[1].id,  # Dev Python
        designation='Développement module d\'analyse prédictive',
        quantite=40,
        prix_ht=Decimal('120.00'),
        taux_tva=Decimal('20.0'),
        ordre=1
    )

    facture12.calculer_totaux()
    factures_list.append(facture12)

    # Facture 13: Cabinet Dubois - Audit + Formation PAYÉE
    facture13 = Document(
        type='facture',
        client_id=clients[1].id,  # Cabinet Dubois
        date_emission=datetime(2026, 1, 15),
        date_echeance=datetime(2026, 2, 14),
        statut='payee',
        date_paiement=datetime(2026, 1, 28),
        conditions_paiement='Paiement à 30 jours',
    )
    facture13.generate_numero()
    db.session.add(facture13)
    db.session.flush()

    add_ligne(
        document_id=facture13.id,
        produit_id=produits[6].id,  # Audit IA
        designation='Audit système IA et processus',
        quantite=1,
        prix_ht=Decimal('2500.00'),
        taux_tva=Decimal('20.0'),
        ordre=1
    )
    add_ligne(
        document_id=facture13.id,
        produit_id=produits[4].id,  # Workshop
        designation='Workshop automatisation workflows',
        quantite=1,
        prix_ht=Decimal('450.00'),
        taux_tva=Decimal('20.0'),
        ordre=2
    )

    facture13.calculer_totaux()
    factures_list.append(facture13)

    # Facture 14: FormaPro - Workshop + Consultation EN ATTENTE (récente)
    facture14 = Document(
        type='facture',
        client_id=clients[3].id,  # FormaPro
        date_emission=datetime(2026, 1, 25),
        date_echeance=datetime(2026, 2, 24),
        statut='envoyee',
        conditions_paiement='Paiement à 30 jours',
        notes='Workshop animé le 20 janvier 2026',
    )
    facture14.generate_numero()
    db.session.add(facture14)
    db.session.flush()

    add_ligne(
        document_id=facture14.id,
        produit_id=produits[4].id,  # Workshop
        designation='Workshop IA pour formateurs (2 sessions)',
        quantite=2,
        prix_ht=Decimal('450.00'),
        taux_tva=Decimal('20.0'),
        ordre=1
    )
    add_ligne(
        document_id=facture14.id,
        produit_id=produits[0].id,  # Consultation
        designation='Consultation stratégie pédagogique IA',
        quantite=5,
        prix_ht=Decimal('150.00'),
        taux_tva=Decimal('20.0'),
        ordre=2
    )

    facture14.calculer_totaux()
    factures_list.append(facture14)

    db.session.commit()
    print(f"✅ {len(factures_list)} factures créées (dont 4 en janvier 2026)\n")

    return factures_list


def print_summary(clients, produits, devis, factures):
    """Affiche un résumé des données créées"""
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES DONNÉES DE DÉMONSTRATION")
    print("="*60)

    print(f"\n👥 Clients: {len(clients)}")
    for client in clients:
        print(f"   - {client.nom_complet} ({client.type})")

    print(f"\n📦 Produits/Services: {len(produits)}")
    for produit in produits:
        print(f"   - {produit.designation} ({produit.prix_ht} EUR HT)")

    print(f"\n📝 Devis: {len(devis)}")
    statuts_devis = {}
    for d in devis:
        statuts_devis[d.statut] = statuts_devis.get(d.statut, 0) + 1
    for statut, count in statuts_devis.items():
        print(f"   - {statut}: {count}")

    print(f"\n💰 Factures: {len(factures)}")
    statuts_factures = {}
    total_ca = Decimal('0.00')
    total_attente = Decimal('0.00')
    for f in factures:
        statuts_factures[f.statut] = statuts_factures.get(f.statut, 0) + 1
        if f.statut == 'payee':
            total_ca += f.total_ttc
        elif f.statut == 'envoyee':
            total_attente += f.total_ttc

    for statut, count in statuts_factures.items():
        print(f"   - {statut}: {count}")

    print(f"\n💵 Chiffre d'affaires:")
    print(f"   - Total payé: {total_ca:.2f} EUR TTC")
    print(f"   - En attente: {total_attente:.2f} EUR TTC")
    print(f"   - TOTAL: {total_ca + total_attente:.2f} EUR TTC")

    print("\n" + "="*60)
    print("✅ DONNÉES DE DÉMONSTRATION PRÊTES !")
    print("="*60)
    print("\n🎯 Vous pouvez maintenant:")
    print("   1. Lancer l'application: python run.py")
    print("   2. Prendre des screenshots pour votre landing page")
    print("   3. Les données sont réalistes et professionnelles\n")


def main():
    """Fonction principale"""
    print("\n" + "="*60)
    print("🌱 GÉNÉRATION DE DONNÉES DE DÉMONSTRATION")
    print("="*60)
    print("\n⚠️  ATTENTION: Ce script va RÉINITIALISER votre base de données!")
    print("   Toutes les données actuelles seront supprimées.\n")

    response = input("Voulez-vous continuer ? (oui/non): ").lower().strip()
    if response not in ['oui', 'o', 'yes', 'y']:
        print("\n❌ Opération annulée.\n")
        return

    print("\n🚀 Démarrage de la génération...\n")

    # Créer l'application Flask
    app = create_app('development')

    with app.app_context():
        # Nettoyer la base
        clear_database()

        # Créer les données
        entreprise = create_entreprise()
        produits = create_produits()
        clients = create_clients()
        devis = create_devis(clients, produits)
        factures = create_factures(clients, produits)

        # Afficher le résumé
        print_summary(clients, produits, devis, factures)


if __name__ == '__main__':
    main()
