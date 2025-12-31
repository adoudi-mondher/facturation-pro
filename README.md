# 📊 Easy Facture

Application desktop de facturation professionnelle - Version 1.6

## Installation

### 1. Prérequis
- Python 3.11 ou supérieur
- pip (gestionnaire de paquets Python)

### 2. Installation des dépendances

```bash
# Créer un environnement virtuel (recommandé)
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows:
venv\Scripts\activate
# Sur macOS/Linux:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer .env si nécessaire (optionnel pour démarrer)
```

## Lancement de l'application

```bash
python run.py
```

L'application va :
1. Démarrer le serveur Flask en local (http://127.0.0.1:5000)
2. Créer automatiquement la base de données si elle n'existe pas
3. Ouvrir votre navigateur par défaut

**⚠️ Ne fermez pas la fenêtre de console !**

Pour arrêter l'application : `Ctrl+C` dans la console

## Structure du projet

```
facturation-app/
├── run.py                  # Point d'entrée
├── config.py               # Configuration
├── requirements.txt        # Dépendances
├── .env                    # Configuration locale
│
├── app/                    # Application Flask
│   ├── __init__.py        # Factory
│   ├── extensions.py      # SQLAlchemy
│   ├── models/            # Modèles BDD
│   ├── routes/            # Controllers
│   ├── templates/         # Templates HTML
│   └── static/            # CSS/JS/Images
│
└── data/                   # Données runtime
    ├── facturation.db     # Base de données SQLite
    └── uploads/           # Fichiers uploadés
```

## Fonctionnalités

### Version 1.6 (Actuelle)
- [x] Gestion des clients
- [x] Gestion des produits/services
- [x] Gestion de stock (optionnelle)
- [x] Création de factures
- [x] Création de devis
- [x] Tableau de bord
- [x] Paramètres entreprise
- [x] Génération PDF
- [x] Envoi par email
- [x] Export Excel/CSV

### Prochaines versions
- Multi-utilisateurs
- Paiements en ligne
- Statistiques avancées
- Mode cloud

## Développement

### Lancer en mode développement
```bash
python run.py
```

### Créer de nouvelles migrations (si modifications BDD)
```bash
flask db migrate -m "Description"
flask db upgrade
```

### Tests
```bash
pytest
```

## Packaging (PyInstaller)

Pour créer un exécutable autonome :

```bash
# Installer PyInstaller
pip install pyinstaller

# Créer l'exécutable
pyinstaller --onefile --windowed --name="FacturationPro" run.py

# L'exécutable sera dans : dist/FacturationPro.exe (Windows)
```

## Problèmes courants

### Le navigateur ne s'ouvre pas automatiquement
- Ouvrez manuellement : http://127.0.0.1:5000

### Port déjà utilisé
- Modifiez le port dans `.env` : `PORT=5001`

### Base de données verrouillée
- Fermez toutes les instances de l'application
- Supprimez `data/facturation.db` (⚠️ perte de données)

## License

Propriétaire - Tous droits réservés

## Auteur

Mondher
