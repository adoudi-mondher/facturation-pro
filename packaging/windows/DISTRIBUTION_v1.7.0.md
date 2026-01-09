# Easy Facture v1.7.0 - Guide de Distribution

**Date de build:** 2026-01-09
**Version:** 1.7.0
**Build:** Production Clean Build

---

## 🎯 Nouveautés de la version 1.7.0

### ✨ Fonctionnalités principales

1. **Intégration Stripe pour licences Lifetime**
   - Badge CTA rouge (#ff2c55) dans le sidebar
   - Modal de paiement intégré avec Stripe Checkout
   - Email auto-rempli depuis la base de données
   - Redirection vers checkout sécurisé Stripe

2. **Système de licence amélioré**
   - Support des licences trial (30 jours)
   - Support des licences lifetime (achat unique 199€)
   - Validation locale + validation API en ligne
   - Bannière de compte à rebours (< 7 jours restants)

3. **Rapports de chiffre d'affaires**
   - Visualisation par mois/année
   - Export des données
   - Graphiques interactifs

4. **Données de démonstration françaises**
   - Script `seed_demo_data.py` inclus
   - Données en EUR et localisation française

---

## 📦 Contenu du package

```
EasyFacture/
├── EasyFacture.exe          (11 MB - Executable principal)
├── python311.dll            (DLL Python)
├── _internal/              (1088 fichiers - Dépendances)
│   ├── base_library.zip
│   ├── certifi/
│   ├── flask/
│   ├── sqlalchemy/
│   ├── stripe/
│   └── ...
├── icons/
│   └── icon.ico
└── static/
    └── (ressources web)
```

**Taille totale:** ~59 MB

---

## 🚀 Distribution aux clients

### Option 1 : ZIP (Recommandée)

```bash
cd packaging/windows/dist
zip -r EasyFacture-v1.7.0-Windows.zip EasyFacture/
```

**Envoyer :** `EasyFacture-v1.7.0-Windows.zip` (~25 MB compressé)

### Option 2 : Installateur (À venir)

Utiliser Inno Setup pour créer un installateur `.exe` avec :
- Installation automatique dans Program Files
- Création de raccourcis bureau/menu démarrer
- Désinstallation propre

---

## 📝 Instructions pour les clients

### Installation

1. **Télécharger** le fichier `EasyFacture-v1.7.0-Windows.zip`
2. **Extraire** le contenu dans un dossier de votre choix (ex: `C:\Program Files\EasyFacture`)
3. **Lancer** `EasyFacture.exe`

### Premier lancement (Mode Trial)

Au premier démarrage :
1. Une fenêtre demande votre **Machine ID**
2. Cliquez sur "**OUI : Essai GRATUIT 30 jours**"
3. Entrez votre **email**
4. Cliquez sur "**OK**"

➡️ Vous recevez instantanément une licence trial de 30 jours valide !

### Passer en Lifetime

**Option 1 : Depuis l'application**
1. Cliquez sur le **badge rouge** dans le sidebar
2. Remplissez vos informations (email pré-rempli)
3. **Paiement sécurisé** via Stripe (199€)
4. Vous recevez votre **clé lifetime par email**
5. L'app se met à jour automatiquement

**Option 2 : Depuis le site web**
1. Allez sur https://easyfacture.mondher.ch
2. Cliquez sur "**Acheter**"
3. Complétez le paiement
4. Vous recevez votre **clé par email**
5. Dans l'app : **Paramètres** > **Activer une licence** > Collez la clé

---

## 🔧 Configuration technique

### Prérequis système

- **OS:** Windows 10/11 (64-bit)
- **RAM:** 512 MB minimum, 1 GB recommandé
- **Disque:** 200 MB libres
- **Connexion Internet:** Recommandée (validation licence)

### Emplacements des données

**En mode développement :**
```
facturation-app/
├── data/
│   ├── facturation.db
│   ├── backups/
│   └── uploads/
└── logs/
```

**En mode production (executable) :**
```
C:\Users\<USERNAME>\AppData\Local\EasyFacture\
├── data/
│   ├── facturation.db
│   ├── backups/
│   └── uploads/
└── logs/
```

---

## 🔒 Sécurité et licence

### Système de protection

1. **Validation locale** (cryptographie)
   - Vérification de la clé de licence
   - Binding au machine_id unique

2. **Validation en ligne** (API)
   - Une fois par jour si connexion Internet
   - Détection de révocation
   - API: `https://api.easyfacture.mondher.ch`

3. **Mode gracieux**
   - En cas de panne API, l'app continue de fonctionner
   - Pas de blocage intempestif

### Stripe Integration

- **Paiement sécurisé:** Stripe Checkout
- **PCI-DSS compliant:** Aucune donnée bancaire stockée
- **Prix:** 199€ (paiement unique)
- **Devises supportées:** EUR, USD, CHF, GBP

---

## 🐛 Résolution de problèmes

### L'app ne démarre pas

**Vérification:**
```bash
# Tester en mode console pour voir les erreurs
EasyFacture.exe
```

**Solutions courantes:**
- Vérifier les droits d'écriture dans AppData
- Désactiver temporairement l'antivirus
- Exécuter en tant qu'administrateur

### Licence non activée

**Si le trial ne fonctionne pas:**
1. Vérifier la connexion Internet
2. Vérifier que l'API `api.easyfacture.mondher.ch` est accessible
3. Contacter le support avec le **Machine ID**

### Badge CTA ne s'affiche pas

**Vérifications:**
1. Vider le cache du navigateur (Ctrl+Shift+R)
2. Vérifier que la licence est bien en mode trial
3. Redémarrer l'application

---

## 📊 Fichiers de configuration

### .env (Variables d'environnement)

**Non inclus dans le build** (créé automatiquement au premier lancement)

```bash
# Licence
LICENSE_ENABLED=True

# Base de données
ITEMS_PER_PAGE=20
MAX_UPLOAD_SIZE=5

# SMTP (optionnel)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
```

---

## 📞 Support

**Email:** contact@mondher.ch
**Site web:** https://easyfacture.mondher.ch
**API Status:** https://api.easyfacture.mondher.ch/health

---

## 📜 Changelog v1.7.0

### Ajouts
- ✅ Intégration Stripe pour licences lifetime
- ✅ Badge CTA rouge dans sidebar (#ff2c55)
- ✅ Modal de paiement avec email auto-fill
- ✅ Bannière de compte à rebours (< 7 jours)
- ✅ Rapports CA par mois/année
- ✅ Données de démo françaises (EUR)

### Améliorations
- ✅ Validation de licence en ligne périodique
- ✅ Meilleure gestion des erreurs réseau
- ✅ Performance optimisée (temps de démarrage réduit)

### Corrections
- ✅ Correction du rechargement du context processor
- ✅ Fix de l'email auto-fill depuis tous les CTA
- ✅ Correction de la détection d'email placeholder

---

## 🔐 Licence et légal

**Copyright © 2026 Mondher Adoudi**
**Tous droits réservés.**

Cette application est protégée par un système de licence.
Utilisation commerciale interdite sans licence valide.

**Powered by:**
- Python 3.11
- Flask 3.0
- SQLAlchemy 2.0
- Stripe API
- PyInstaller 6.17

---

**Build généré le:** 2026-01-09
**Build ID:** v1.7.0-clean-production
**Environnement:** Windows 64-bit

✨ **Prêt pour distribution !**
