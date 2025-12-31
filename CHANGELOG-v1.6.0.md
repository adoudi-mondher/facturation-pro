# Changelog - Version 1.6.0 (Décembre 2025)

## 🎉 Nouveautés majeures

### 🔐 Système de licence matérielle
- **Nouveau module** : `app/utils/license.py` (581 lignes)
  - Protection basée sur Machine ID (MAC + hostname + système)
  - Chiffrement AES-128 avec cryptography/Fernet
  - Génération et validation de licences
  - Stockage sécurisé dans `%APPDATA%\FacturationPro\license.dat`
  - Graceful degradation (app fonctionne même si problème de licence)

- **Outils de gestion de licences** :
  - `generate_customer_license.py` : Générateur de licences
    - Option 1 : Sur place (client présent)
    - Option 2 : À distance (avec Machine ID)
  - `get_machine_id.py` : Utilitaire pour clients distants
  - `build_machine_id_tool.bat` : Compiler GetMachineID.exe
  - `test_license.py` : Tests du système de licence

### 🏗️ Build Windows amélioré

#### Correction des bugs de build
- **Fichiers .spec corrigés** :
  - Chemins Unix (`/app`, `/run.py`) → Chemins Windows relatifs (`../../app`)
  - Ajout des imports manquants : `cryptography`, `PIL`, `dateutil`
  - Icône corrigée : `../../icons/icon.ico`

- **Nouveaux scripts de build** :
  - `packaging/windows/build.sh` : Build personnel (Git Bash)
  - `packaging/windows/build.bat` : Build personnel (CMD/PowerShell)
  - `packaging/windows/build_for_client.sh` : Build client propre (Git Bash) ✨ **NOUVEAU**
  - `packaging/windows/build_for_client.bat` : Build client propre (CMD) ✨ **NOUVEAU**

#### Protection automatique des données
- **Sauvegarde/restauration automatique** lors du build personnel
- Préserve votre licence, base de données, uploads
- Dossier temporaire `.backup_personal_data/` (auto-nettoyé)

#### Deux types de build distincts
- **Build personnel** (`build.sh`) : Préserve vos données de test
- **Build client** (`build_for_client.sh`) : Version propre sans données

### 📦 Déploiement à distance

#### 3 méthodes documentées
1. **Machine ID par email** (simple, gratuite) ✅ Implémentée
2. **Serveur d'activation en ligne** (avancée, documentée)
3. **Version demo + activation manuelle** (alternative)

#### Workflow optimisé
- Client télécharge → Exécute GetMachineID.exe → Envoie Machine ID
- Admin génère licence → Envoie au client
- Client active → Application fonctionnelle

---

## 📝 Modifications des fichiers

### Fichiers modifiés

| Fichier | Type | Description |
|---------|------|-------------|
| `.gitignore` | Modifié | Ajout : `venv_build/`, `license_*.txt`, `.personal_backup/`, `.backup_personal_data/` |
| `config.py` | Modifié | `LICENSE_ENABLED = True`, version 1.6.0 |
| `run.py` | Modifié | Intégration du check de licence au démarrage |
| `packaging/windows/build.bat` | Modifié | Protection données + imports manquants |
| `packaging/windows/README-WINDOWS.md` | Modifié | Documentation des 2 types de build |

### Nouveaux fichiers

#### 🔐 Système de licence
- `app/utils/license.py` - Gestionnaire de licences
- `generate_customer_license.py` - Générateur admin
- `get_machine_id.py` - Utilitaire client
- `build_machine_id_tool.bat` - Compilateur GetMachineID
- `test_license.py` - Tests

#### 🏗️ Build Windows
- `packaging/windows/build.sh` - Build personnel (Git Bash)
- `packaging/windows/build_for_client.sh` - Build client (Git Bash)
- `packaging/windows/build_for_client.bat` - Build client (CMD)
- `packaging/windows/EasyFacture.spec` - Spec PyInstaller corrigé
- `EasyFacture.spec` - Spec racine

#### 📚 Documentation
- `BUILD-PERSONNEL-VS-CLIENT.md` - Différence entre builds
- `GUIDE-DEPLOIEMENT-DISTANT.md` - Guide complet déploiement (11 KB)
- `DEPLOIEMENT-CLIENT-README.md` - Aide-mémoire rapide
- `PROTECTION-DONNEES-BUILD.md` - Protection automatique des données
- `CHANGELOG-v1.6.0.md` - Ce fichier

#### 🧹 Maintenance
- `cleanup.sh` - Script de nettoyage du projet

### Fichiers archivés
- `docs/archive/CORRECTIONS-BUILD-WINDOWS.md` - Historique des corrections (obsolète)

### Fichiers supprimés
- `venv/` - Environnement virtuel (421 MB libérés)
- `venv_build/` - Environnement de build
- `build/`, `dist/` - Artefacts temporaires
- `packaging/windows/build/`, `packaging/windows/dist/`
- `__pycache__/` - Caches Python (8 dossiers)
- `.pytest_cache/`, `htmlcov/` - Caches de tests
- `config.py.backup`, `run.py.backup` - Backups manuels
- `license_adoudi_at_mondher.ch_20251207.txt` - Licence perso (→ `.personal_backup/`)

---

## 🔧 Améliorations techniques

### Dépendances ajoutées
- `cryptography >= 41.0.0` - Chiffrement des licences
- Déjà présent : `pillow`, `python-dateutil`

### Build PyInstaller
- **Taille** : 53 MB (219 fichiers)
- **Exécutable** : 13 MB (EasyFacture.exe)
- **Temps de build** : 2-5 minutes
- **Plateforme** : Windows 10/11

### Compatibilité
- Python 3.14+
- Windows 10/11
- Git Bash / CMD / PowerShell

---

## 📊 Statistiques

- **Lignes de code ajoutées** : ~2000+
- **Fichiers créés** : 16
- **Documentation** : 5 guides (30+ KB)
- **Espace libéré** : 421 MB
- **Build fonctionnel** : ✅ Testé et validé

---

## 🎯 Prochaines étapes recommandées

### Immédiat
1. ✅ Recréer venv : `py -m venv venv`
2. ✅ Installer dépendances : `pip install -r requirements.txt`
3. ✅ Tester le build : `bash packaging/windows/build.sh`
4. ✅ Commit : `git add . && git commit -m "feat: add license system v1.6.0"`

### Court terme (0-10 clients)
- Utiliser la méthode 1 (Machine ID par email)
- Tester le déploiement sur 2-3 clients
- Collecter les retours

### Moyen terme (10-50 clients)
- Envisager serveur d'activation en ligne
- Ajouter dashboard admin
- Intégration paiement (Stripe/PayPal)

---

## ⚠️ Notes importantes

### Sécurité
- ✅ Licence personnelle protégée (`.personal_backup/`)
- ✅ Pattern `license_*.txt` dans .gitignore
- ✅ Base de données exclue du versioning
- ✅ Fichier `.env` protégé

### Build
- ⚠️ Toujours utiliser `build_for_client.sh` pour distribution
- ⚠️ Ne jamais distribuer un build fait avec `build.sh` (contient vos données)
- ✅ Vérifier que `data/` est vide avant d'envoyer au client

### Licence
- 🔑 Machine ID : 32 caractères (SHA256)
- 🔑 Clé de licence : ~368 caractères (hex)
- 🔑 Expiration : Configurable (Trial/Mensuel/Annuel/Vie)
- 🔑 Révocation : Pas encore implémentée (v2.0)

---

**Version** : 1.6.0
**Date** : 12 décembre 2025
**Auteur** : Mondher ADOUDI - Sidr Valley AI
**Assistant** : Claude Code (Anthropic)

**Statut** : ✅ Production Ready
