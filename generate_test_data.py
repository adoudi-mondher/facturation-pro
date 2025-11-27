#!/usr/bin/env python3
"""
Script pour générer des données de test
Remplit la base de données avec des clients, produits et factures fictifs
"""

from app import create_app
from app.extensions import db
from app.models.entreprise import Entreprise
from app.models.client import Client
from app.models.produit import Produit
from app.models.document import Document
from app.models.ligne_document import LigneDocument
from app.models.mouvement_stock import MouvementStock
from datetime import datetime, timedelta
import random

def create_test_data():
    """Crée des données de test"""
    
    print("🚀 Génération des données de test...")
    print("=" * 60)
    
    # 1. Mettre à jour l'entreprise
    print("\n1️⃣  Configuration de l'entreprise...")
    entreprise = Entreprise.get_instance()
    entreprise.nom = "Saveurs Méditerranéennes"
    entreprise.adresse = "12 Rue de la République"
    entreprise.code_postal = "13001"
    entreprise.ville = "Marseille"
    entreprise.pays = "France"
    entreprise.siret = "12345678901234"
    entreprise.tva_intra = "FR12345678901"
    entreprise.telephone = "04 91 00 00 00"
    entreprise.email = "contact@saveurs-med.fr"
    entreprise.site_web = "https://saveurs-mediterraneennes.fr"
    entreprise.taux_tva_defaut = 10.0
    entreprise.mentions_legales = "SARL au capital de 10 000 € - RCS Marseille"
    db.session.commit()
    print("   ✅ Entreprise configurée")
    
    # 2. Créer des clients
    print("\n2️⃣  Création de 10 clients...")
    clients_data = [
        {"type": "particulier", "nom": "Dupont", "prenom": "Jean", "email": "jean.dupont@email.fr", "telephone": "06 12 34 56 78", "ville": "Marseille"},
        {"type": "particulier", "nom": "Martin", "prenom": "Sophie", "email": "sophie.martin@email.fr", "telephone": "06 23 45 67 89", "ville": "Aix-en-Provence"},
        {"type": "entreprise", "nom": "TechCorp", "raison_sociale": "TechCorp SARL", "email": "contact@techcorp.fr", "telephone": "04 91 11 22 33", "ville": "Marseille"},
        {"type": "particulier", "nom": "Bernard", "prenom": "Marie", "email": "marie.bernard@email.fr", "telephone": "06 34 56 78 90", "ville": "Cassis"},
        {"type": "entreprise", "nom": "Restaurant Le Panier", "raison_sociale": "Le Panier SAS", "email": "resto@lepanier.fr", "telephone": "04 91 22 33 44", "ville": "Marseille"},
        {"type": "particulier", "nom": "Dubois", "prenom": "Pierre", "email": "pierre.dubois@email.fr", "telephone": "06 45 67 89 01", "ville": "Aubagne"},
        {"type": "entreprise", "nom": "Hôtel Vieux Port", "raison_sociale": "Hôtel VP SAS", "email": "contact@hotelvp.fr", "telephone": "04 91 33 44 55", "ville": "Marseille"},
        {"type": "particulier", "nom": "Moreau", "prenom": "Claire", "email": "claire.moreau@email.fr", "telephone": "06 56 78 90 12", "ville": "La Ciotat"},
        {"type": "particulier", "nom": "Petit", "prenom": "Luc", "email": "luc.petit@email.fr", "telephone": "06 67 89 01 23", "ville": "Marseille"},
        {"type": "entreprise", "nom": "Traiteur Provence", "raison_sociale": "Traiteur Provence SARL", "email": "contact@traiteur-provence.fr", "telephone": "04 91 44 55 66", "ville": "Aix-en-Provence"},
    ]
    
    clients = []
    for data in clients_data:
        client = Client(**data)
        db.session.add(client)
        clients.append(client)
    
    db.session.commit()
    print(f"   ✅ {len(clients)} clients créés")
    
    # 3. Créer des produits
    print("\n3️⃣  Création de 20 produits...")
    produits_data = [
        # Plateaux
        {"reference": "PLT-001", "designation": "Plateau Mezze", "prix_ht": 45.00, "taux_tva": 10.0, "unite": "piece", "categorie": "Plateaux", "gerer_stock": True, "stock_actuel": 15, "stock_minimum": 5},
        {"reference": "PLT-002", "designation": "Plateau Tapas", "prix_ht": 38.00, "taux_tva": 10.0, "unite": "piece", "categorie": "Plateaux", "gerer_stock": True, "stock_actuel": 12, "stock_minimum": 5},
        {"reference": "PLT-003", "designation": "Plateau Fromages", "prix_ht": 42.00, "taux_tva": 10.0, "unite": "piece", "categorie": "Plateaux", "gerer_stock": True, "stock_actuel": 8, "stock_minimum": 3},
        {"reference": "PLT-004", "designation": "Plateau Fruits de Mer", "prix_ht": 65.00, "taux_tva": 10.0, "unite": "piece", "categorie": "Plateaux", "gerer_stock": True, "stock_actuel": 3, "stock_minimum": 2},
        
        # Plats
        {"reference": "PLAT-001", "designation": "Couscous Royal (10 pers)", "prix_ht": 120.00, "taux_tva": 10.0, "unite": "forfait", "categorie": "Plats", "gerer_stock": False},
        {"reference": "PLAT-002", "designation": "Paella Valenciana (10 pers)", "prix_ht": 110.00, "taux_tva": 10.0, "unite": "forfait", "categorie": "Plats", "gerer_stock": False},
        {"reference": "PLAT-003", "designation": "Tajine Poulet Citron", "prix_ht": 12.00, "taux_tva": 10.0, "unite": "piece", "categorie": "Plats", "gerer_stock": False},
        {"reference": "PLAT-004", "designation": "Moussaka Maison", "prix_ht": 11.00, "taux_tva": 10.0, "unite": "piece", "categorie": "Plats", "gerer_stock": False},
        
        # Entrées
        {"reference": "ENT-001", "designation": "Houmous Maison", "prix_ht": 8.50, "taux_tva": 10.0, "unite": "piece", "categorie": "Entrées", "gerer_stock": True, "stock_actuel": 25, "stock_minimum": 10},
        {"reference": "ENT-002", "designation": "Caviar d'Aubergine", "prix_ht": 7.50, "taux_tva": 10.0, "unite": "piece", "categorie": "Entrées", "gerer_stock": True, "stock_actuel": 20, "stock_minimum": 10},
        {"reference": "ENT-003", "designation": "Tzatziki", "prix_ht": 6.50, "taux_tva": 10.0, "unite": "piece", "categorie": "Entrées", "gerer_stock": True, "stock_actuel": 18, "stock_minimum": 8},
        {"reference": "ENT-004", "designation": "Taboulé Libanais", "prix_ht": 8.00, "taux_tva": 10.0, "unite": "piece", "categorie": "Entrées", "gerer_stock": True, "stock_actuel": 0, "stock_minimum": 10},
        
        # Desserts
        {"reference": "DES-001", "designation": "Baklava (6 pièces)", "prix_ht": 9.00, "taux_tva": 10.0, "unite": "piece", "categorie": "Desserts", "gerer_stock": True, "stock_actuel": 30, "stock_minimum": 15},
        {"reference": "DES-002", "designation": "Cornes de Gazelle (6 pièces)", "prix_ht": 8.50, "taux_tva": 10.0, "unite": "piece", "categorie": "Desserts", "gerer_stock": True, "stock_actuel": 25, "stock_minimum": 15},
        {"reference": "DES-003", "designation": "Loukoums Assortis", "prix_ht": 12.00, "taux_tva": 10.0, "unite": "piece", "categorie": "Desserts", "gerer_stock": True, "stock_actuel": 2, "stock_minimum": 5},
        
        # Boissons
        {"reference": "BOIS-001", "designation": "Thé à la Menthe (1L)", "prix_ht": 5.00, "taux_tva": 10.0, "unite": "litre", "categorie": "Boissons", "gerer_stock": True, "stock_actuel": 40, "stock_minimum": 20},
        {"reference": "BOIS-002", "designation": "Limonade Maison (1L)", "prix_ht": 6.00, "taux_tva": 10.0, "unite": "litre", "categorie": "Boissons", "gerer_stock": True, "stock_actuel": 35, "stock_minimum": 15},
        
        # Services
        {"reference": "SERV-001", "designation": "Service Traiteur (par personne)", "prix_ht": 25.00, "taux_tva": 10.0, "unite": "piece", "categorie": "Services", "gerer_stock": False},
        {"reference": "SERV-002", "designation": "Location Vaisselle (service complet)", "prix_ht": 15.00, "taux_tva": 20.0, "unite": "forfait", "categorie": "Services", "gerer_stock": False},
        {"reference": "SERV-003", "designation": "Livraison Marseille", "prix_ht": 10.00, "taux_tva": 20.0, "unite": "forfait", "categorie": "Services", "gerer_stock": False},
    ]
    
    produits = []
    for data in produits_data:
        produit = Produit(**data)
        db.session.add(produit)
        produits.append(produit)
    
    db.session.commit()
    print(f"   ✅ {len(produits)} produits créés")
    
    # 4. Créer des factures
    print("\n4️⃣  Création de 15 factures...")
    
    statuts_facture = ['brouillon', 'envoyee', 'payee']
    factures_created = 0
    
    for i in range(15):
        # Choisir un client aléatoire
        client = random.choice(clients)
        
        # Date aléatoire dans les 60 derniers jours
        date_emission = datetime.now().date() - timedelta(days=random.randint(0, 60))
        
        # Créer la facture
        facture = Document(
            type='facture',
            client_id=client.id,
            date_emission=date_emission,
            statut=random.choice(statuts_facture),
            conditions_paiement="Paiement à 30 jours",
            notes="Merci pour votre commande !"
        )
        
        # Générer le numéro
        facture.generate_numero()
        
        db.session.add(facture)
        db.session.flush()  # Pour avoir l'ID
        
        # Ajouter 2-5 lignes de produits
        nb_lignes = random.randint(2, 5)
        ordre = 0
        
        for _ in range(nb_lignes):
            produit = random.choice(produits)
            quantite = random.randint(1, 5)
            
            ligne = LigneDocument(
                document_id=facture.id,
                produit_id=produit.id,
                designation=produit.designation,
                quantite=quantite,
                prix_unitaire_ht=produit.prix_ht,
                taux_tva=produit.taux_tva,
                ordre=ordre
            )
            ligne.calculer_total()
            db.session.add(ligne)
            
            # Si produit géré en stock, créer mouvement
            if produit.gerer_stock and produit.stock_actuel is not None:
                stock_avant = produit.stock_actuel
                produit.stock_actuel -= int(quantite)
                stock_apres = produit.stock_actuel
                
                mouvement = MouvementStock(
                    produit_id=produit.id,
                    type_mouvement='facture',
                    quantite=-quantite,
                    stock_avant=stock_avant,
                    stock_apres=stock_apres,
                    reference_document_id=facture.id,
                    commentaire=f"Facture {facture.numero}"
                )
                db.session.add(mouvement)
            
            ordre += 1
        
        # Calculer les totaux
        facture.calculer_totaux()
        
        factures_created += 1
    
    db.session.commit()
    print(f"   ✅ {factures_created} factures créées")
    
    # 5. Créer quelques devis
    print("\n5️⃣  Création de 5 devis...")
    
    statuts_devis = ['brouillon', 'envoye', 'accepte', 'refuse']
    devis_created = 0
    
    for i in range(5):
        client = random.choice(clients)
        date_emission = datetime.now().date() - timedelta(days=random.randint(0, 30))
        
        devis = Document(
            type='devis',
            client_id=client.id,
            date_emission=date_emission,
            statut=random.choice(statuts_devis),
            notes="Devis valable 30 jours"
        )
        
        devis.generate_numero()
        db.session.add(devis)
        db.session.flush()
        
        # Ajouter 2-4 lignes
        nb_lignes = random.randint(2, 4)
        
        for j in range(nb_lignes):
            produit = random.choice(produits)
            quantite = random.randint(1, 3)
            
            ligne = LigneDocument(
                document_id=devis.id,
                produit_id=produit.id,
                designation=produit.designation,
                quantite=quantite,
                prix_unitaire_ht=produit.prix_ht,
                taux_tva=produit.taux_tva,
                ordre=j
            )
            ligne.calculer_total()
            db.session.add(ligne)
        
        devis.calculer_totaux()
        devis_created += 1
    
    db.session.commit()
    print(f"   ✅ {devis_created} devis créés")
    
    # 6. Statistiques finales
    print("\n" + "=" * 60)
    print("✅ GÉNÉRATION TERMINÉE !")
    print("=" * 60)
    print(f"\n📊 Récapitulatif :")
    print(f"   • Entreprise : {entreprise.nom}")
    print(f"   • Clients : {len(clients)}")
    print(f"   • Produits : {len(produits)}")
    print(f"   • Factures : {factures_created}")
    print(f"   • Devis : {devis_created}")
    print(f"\n🎯 Tu peux maintenant tester l'application avec des données réelles !")
    print(f"   Ouvre : http://127.0.0.1:5000\n")

if __name__ == '__main__':
    app = create_app('development')
    with app.app_context():
        # Demander confirmation
        print("\n⚠️  ATTENTION : Ce script va remplir la base de données avec des données de test.")
        print("   Si tu as déjà des données, elles seront conservées.")
        response = input("\n   Continuer ? (oui/non) : ")
        
        if response.lower() in ['oui', 'o', 'yes', 'y']:
            create_test_data()
        else:
            print("\n❌ Annulé.")
