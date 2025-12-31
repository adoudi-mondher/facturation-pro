# EasyFacture - Application de Facturation Professionnelle

Application desktop de facturation complète pour petites et moyennes entreprises.

Version actuelle : **1.7.0**

---

## Installation

### Prérequis

- Python 3.11 ou supérieur
- pip (gestionnaire de paquets Python)
- Git (optionnel)

### Installation rapide

```bash
# Cloner le projet (si depuis Git)
git clone https://github.com/adoudi-mondher/facturation-pro.git
cd facturation-pro

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Copier la configuration
cp .env.example .env

# Lancer l'application
python run.py
```

L'application démarrera automatiquement sur http://127.0.0.1:5000

---

## Fonctionnalités

### Gestion commerciale
- Gestion des clients (création, modification, suppression)
- Gestion des produits et services
- Gestion de stock (optionnelle)
- Catégories de produits
- Pricing flexible

### Facturation
- Création de factures
- Création de devis
- Numérotation automatique
- Calculs TVA automatiques
- Multi-devises
- Statuts de paiement (payée, en attente, annulée)

### Documents
- Génération PDF professionnelle
- Logo personnalisable
- Informations entreprise complètes
- Export Excel (.xlsx)
- Export CSV
- Export FEC (Fichier des Écritures Comptables)

### Communication
- Envoi de factures par email
- Templates d'emails personnalisables
- Pièces jointes PDF automatiques

### Paramètres entreprise
- Configuration complète des informations
- Logo personnalisé
- Conditions générales de vente
- Mentions légales

### Sécurité
- Système de licence avec protection hardware
- Activation en ligne ou manuelle
- Essai gratuit 30 jours disponible
- Validation périodique

### Tableau de bord
- Vue d'ensemble des activités
- Statistiques de vente
- Factures récentes
- Alertes stock bas

---

## Structure du projet

```
facturation-app/
├── run.py                      # Point d'entrée principal
├── config.py                   # Configuration Flask
├── requirements.txt            # Dépendances Python
├── .env.example               # Template de configuration
│
├── app/                        # Application Flask
│   ├── __init__.py            # Factory pattern
│   ├── extensions.py          # Extensions (SQLAlchemy, etc.)
│   │
│   ├── models/                # Modèles de données
│   │   ├── client.py
│   │   ├── produit.py
│   │   ├── facture.py
│   │   ├── devis.py
│   │   └── entreprise.py
│   │
│   ├── routes/                # Contrôleurs
│   │   ├── main.py
│   │   ├── clients.py
│   │   ├── produits.py
│   │   ├── factures.py
│   │   ├── devis.py
│   │   └── entreprise.py
│   │
│   ├── templates/             # Templates HTML (Jinja2)
│   ├── static/                # Assets (CSS, JS, images)
│   │
│   └── utils/                 # Utilitaires
│       ├── license.py         # Gestion des licences
│       ├── trial_client.py    # Client API trial
│       ├── pdf_generator.py   # Génération PDF
│       └── email_sender.py    # Envoi emails
│
├── data/                      # Données runtime
│   ├── facturation.db         # Base de données SQLite
│   ├── uploads/               # Fichiers uploadés
│   └── license.key            # Licence (si activée)
│
├── packaging/                 # Scripts de packaging
│   └── windows/
│       ├── EasyFacture.spec   # Configuration PyInstaller
│       ├── build.sh           # Build développement
│       └── build_for_client.sh # Build client
│
└── tests/                     # Tests unitaires
```

---

## Utilisation

### Premier lancement

1. L'application vérifie la licence au démarrage
2. Options d'activation:
   - **Essai gratuit** : 30 jours automatique (nécessite email)
   - **Activation manuelle** : si vous avez une clé de licence
3. Configuration entreprise (nom, adresse, logo, etc.)
4. Commencer à créer vos factures

### Workflow typique

1. **Paramètres entreprise** : Remplir vos informations
2. **Clients** : Ajouter vos clients
3. **Produits** : Créer votre catalogue
4. **Factures/Devis** : Créer vos documents
5. **PDF** : Générer et envoyer par email

---

## Configuration

### Fichier .env

```bash
# Flask
SECRET_KEY=votre-cle-secrete-ici
FLASK_ENV=production
PORT=5000

# Base de données
DATABASE_URL=sqlite:///data/facturation.db

# Email (optionnel)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=votre-email@gmail.com
MAIL_PASSWORD=votre-mot-de-passe-app

# Licence
LICENSE_SERVER_URL=https://api.mondher.ch/api/v1
```

### Email avec Gmail

1. Activer l'authentification à 2 facteurs
2. Générer un mot de passe d'application
3. Utiliser ce mot de passe dans MAIL_PASSWORD

---

## Développement

### Lancer en mode développement

```bash
# Dans .env, définir:
FLASK_ENV=development

# Lancer avec debug
python run.py
```

### Base de données

```bash
# Créer une migration (après modification modèles)
flask db migrate -m "Description de la modification"

# Appliquer la migration
flask db upgrade

# Revenir en arrière
flask db downgrade
```

### Tests

```bash
# Installer les dépendances de test
pip install pytest pytest-cov

# Lancer tous les tests
pytest

# Avec couverture
pytest --cov=app tests/
```

---

## Build et distribution

### Créer un exécutable Windows

```bash
cd packaging/windows

# Build pour développement (conserve vos données)
bash build.sh

# Build pour client (sans données personnelles)
bash build_for_client.sh
```

L'exécutable sera dans `dist/EasyFacture.exe` (environ 53 MB)

### Build pour autres OS

```bash
# macOS
pyinstaller packaging/macos/EasyFacture.spec

# Linux
pyinstaller packaging/linux/EasyFacture.spec
```

---

## API de licence (pour développeurs)

### Endpoints disponibles

**POST** `/api/v1/licenses/trial`
```json
{
  "email": "client@example.com",
  "machine_id": "abc123..."
}
```

**POST** `/api/v1/licenses/validate`
```json
{
  "license_key": "...",
  "machine_id": "abc123..."
}
```

### Obtenir le Machine ID

```bash
python -c "from app.utils.license import LicenseManager; print(LicenseManager().get_machine_id())"
```

---

## Problèmes courants

### Le navigateur ne s'ouvre pas

Ouvrez manuellement : http://127.0.0.1:5000

### Port déjà utilisé

```bash
# Changer le port dans .env
PORT=5001
```

### Base de données verrouillée

```bash
# Fermer toutes les instances de l'application
# Si le problème persiste, sauvegarder puis supprimer:
# data/facturation.db
```

### Erreur d'import cryptography

```bash
pip install --upgrade cryptography
```

### Erreur PIL/Pillow

```bash
pip install --upgrade Pillow
```

---

## Sécurité

- Les clés de chiffrement sont stockées de manière sécurisée
- Les mots de passe ne sont jamais stockés en clair dans le code
- Utilisez `.env` pour les informations sensibles
- Ne commitez jamais `.env` dans Git

---

## Technologies utilisées

- **Backend**: Flask 3.0
- **Base de données**: SQLAlchemy + SQLite
- **PDF**: ReportLab
- **Email**: Flask-Mail
- **Excel**: openpyxl
- **Interface**: Bootstrap 5 + JavaScript
- **Build**: PyInstaller

---

## Roadmap

### Version 1.7 (Actuelle)
- Système de licence avec essai gratuit 30 jours
- Activation en ligne automatique
- Validation périodique des licences
- Client API pour communication serveur

### Version 1.8 (À venir)
- Dashboard amélioré avec graphiques
- Gestion des fournisseurs
- Bons de commande
- Relances automatiques

### Version 2.0 (Futur)
- Multi-utilisateurs avec permissions
- API REST complète
- Application mobile (iOS/Android)
- Mode SaaS (cloud)
- Synchronisation multi-appareils

---

## Support

Pour toute question ou problème:
- Documentation complète dans le dossier `/docs`
- Issues GitHub: https://github.com/adoudi-mondher/facturation-pro/issues

---

## Licence

Open Source - Pour les développeurs

Copyright (c) 2025 Mondher Adoudi

---

## Auteur

**Mondher Adoudi**
- GitHub: [@adoudi-mondher](https://github.com/adoudi-mondher)
- Email: adoudi@mondher.ch

---

Dernière mise à jour : 31 décembre 2025
