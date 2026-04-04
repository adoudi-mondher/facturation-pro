# 🛡️ Protection des données personnelles lors du build

## 🎯 Problème résolu

Lorsque vous faites un nouveau build de l'application pour distribuer aux clients, le script **supprime le dossier `dist/`**, ce qui **efface vos données personnelles** :
- Votre base de données SQLite (`data/facturation.db`)
- Vos factures/devis créés
- Vos uploads (logos, etc.)
- **Votre licence activée** sur votre machine de développement

## ✅ Solution implémentée

Les scripts de build ont été **modifiés pour préserver automatiquement vos données** :

### 🔄 Processus automatique

1. **Avant nettoyage** : Sauvegarde automatique de `dist/EasyFacture/data/` vers `.backup_personal_data/`
2. **Build** : Compilation propre de l'application
3. **Après build** : Restauration automatique des données dans `dist/EasyFacture/data/`

### 📁 Ce qui est préservé

✅ **Base de données** : `data/facturation.db` (toutes vos factures/clients/produits)
✅ **Uploads** : `data/uploads/` (logos, pièces jointes)
✅ **Backups** : `data/backups/` (sauvegardes automatiques)
✅ **Licence** : Votre clé de licence activée reste fonctionnelle

### 🚫 Ce qui est nettoyé

❌ **build/** : Fichiers temporaires PyInstaller
❌ **dist/** (sauf data/) : Nouvelle version de l'application
❌ **EasyFacture.spec** (build.bat) : Régénéré à chaque fois

---

## 🎬 Exemple d'utilisation

### Avant (❌ problématique)

```bash
# Build 1
bash packaging/windows/build.sh
# → Vous activez la licence sur dist/EasyFacture
# → Vous créez des factures de test

# Build 2 (quelques jours plus tard)
bash packaging/windows/build.sh
# → ❌ Tout est effacé ! Licence perdue, factures perdues !
```

### Après (✅ avec protection)

```bash
# Build 1
bash packaging/windows/build.sh
# → Vous activez la licence
# → Vous créez des factures

# Build 2
bash packaging/windows/build.sh
# Sortie :
# [4/6] Nettoyage des builds précédents...
#      ⚠️  Sauvegarde des données personnelles détectée...
#      ✓ Données sauvegardées temporairement
#      - build/ supprimé
#      - dist/ supprimé
# ...
# [6/6] Vérification du résultat...
#      🔄 Restauration des données personnelles...
#      ✓ Données personnelles restaurées
#      ✓ EasyFacture.exe créé (13M)

# → ✅ Vos données sont intactes !
# → ✅ Votre licence fonctionne toujours !
```

---

## 📊 Logs de protection

Pendant le build, vous verrez ces messages :

### Si des données existent
```
[4/6] Nettoyage des builds précédents...
     ⚠️  Sauvegarde des données personnelles détectée...
     ✓ Données sauvegardées temporairement
     - build/ supprimé
     - dist/ supprimé
     Nettoyage: OK
     (EasyFacture.spec et données personnelles conservés)
```

### Après le build réussi
```
[6/6] Vérification du résultat...
     ✓ EasyFacture.exe créé (13M)
     🔄 Restauration des données personnelles...
     ✓ Données personnelles restaurées
     ✓ 219 fichiers dans le package
```

### En cas d'échec du build
```
ERROR: Le build a échoué (code: 1)

     🔄 Tentative de restauration des données...
     ✓ Données restaurées malgré l'échec
```

---

## 🔍 Détails techniques

### Scripts modifiés

#### 1. [packaging/windows/build.sh](packaging/windows/build.sh#L59-L77) (Git Bash)

```bash
# Sauvegarde avant nettoyage
BACKUP_NEEDED=false
if [ -d "dist/EasyFacture/data" ]; then
    echo "     ⚠️  Sauvegarde des données personnelles..."
    mkdir -p .backup_personal_data
    cp -r dist/EasyFacture/data .backup_personal_data/
    BACKUP_NEEDED=true
fi

# Nettoyage
rm -rf build dist

# Restauration après build
if [ "$BACKUP_NEEDED" = true ]; then
    echo "     🔄 Restauration des données personnelles..."
    cp -r .backup_personal_data/data dist/EasyFacture/
    rm -rf .backup_personal_data
fi
```

#### 2. [packaging/windows/build.bat](packaging/windows/build.bat#L35-L52) (CMD/PowerShell)

```batch
REM Sauvegarde
set BACKUP_NEEDED=0
if exist dist\EasyFacture\data (
    xcopy /E /I /Q /Y dist\EasyFacture\data .backup_personal_data\data >nul
    set BACKUP_NEEDED=1
)

REM Nettoyage
rmdir /s /q build
rmdir /s /q dist

REM Restauration
if %BACKUP_NEEDED%==1 (
    xcopy /E /I /Q /Y .backup_personal_data\data dist\EasyFacture\data >nul
    rmdir /s /q .backup_personal_data
)
```

---

## ⚙️ Configuration

### Build pour VOUS (avec vos données) vs Build pour CLIENT (propre)

#### 🏠 **Build personnel** (avec protection des données)

```bash
# Pour votre usage personnel - PRÉSERVE vos données
bash packaging/windows/build.sh
# OU
packaging\windows\build.bat
```
✅ Garde votre licence activée
✅ Garde vos factures de test
✅ Idéal pour développement/tests

#### 📦 **Build client** (version propre SANS vos données)

```bash
# Pour distribuer aux clients - SANS vos données
bash packaging/windows/build_for_client.sh
# OU
packaging\windows\build_for_client.bat
```
✅ Aucune donnée personnelle
✅ Dossier `data/` vide mais structuré
✅ Prêt pour distribution immédiate

### Comparaison

| Aspect | `build.sh` | `build_for_client.sh` |
|--------|------------|----------------------|
| Vos données | ✅ Préservées | ❌ Non incluses |
| Usage | Dev/Tests | Distribution client |
| Licence activée | ✅ Oui | ❌ Non (vide) |
| Base de données | ✅ Votre BDD | ❌ Pas de BDD |
| Uploads | ✅ Vos fichiers | ❌ Dossier vide |

### Forcer la restauration manuelle

Si le script échoue pour une raison quelconque :

```bash
# Vérifier si backup existe
ls -la packaging/windows/.backup_personal_data/

# Restaurer manuellement
cp -r packaging/windows/.backup_personal_data/data \
      packaging/windows/dist/EasyFacture/

# Nettoyer le backup
rm -rf packaging/windows/.backup_personal_data/
```

---

## 🎯 Cas d'usage

### Workflow développeur (vous)

1. **Développement** : Travaillez dans votre `dist/EasyFacture/` personnel
2. **Activation** : Licence activée sur votre machine
3. **Tests** : Créez des factures/clients de test
4. **Nouveau build** : Lancez `build.sh` → Vos données sont préservées ✅
5. **Distribution** : Copiez `dist/EasyFacture/` pour envoyer aux clients

### Workflow distribution client

Pour créer un package "clean" sans vos données de dev :

```bash
# Option 1 : Copier sans le dossier data
cp -r packaging/windows/dist/EasyFacture /tmp/EasyFacture-Client
rm -rf /tmp/EasyFacture-Client/data
zip -r EasyFacture-Client.zip /tmp/EasyFacture-Client

# Option 2 : Garder le dossier data vide (pour que l'app le crée)
mkdir /tmp/EasyFacture-Client/data
touch /tmp/EasyFacture-Client/data/.gitkeep
```

---

## 🚨 Important

### ⚠️ Le dossier `.backup_personal_data/` est temporaire

- Créé **uniquement pendant le build**
- Supprimé **automatiquement après restauration**
- Si vous voyez ce dossier après un build, c'est qu'il y a eu un problème

### ⚠️ Ajoutez à .gitignore

Assurez-vous que ces dossiers ne sont PAS commités :

```gitignore
# .gitignore
packaging/windows/dist/
packaging/windows/build/
packaging/windows/.backup_personal_data/
venv_build/
*.spec
```

---

## ✨ Avantages

✅ **Sécurité** : Vos données ne sont jamais perdues
✅ **Automatique** : Aucune manipulation manuelle
✅ **Transparent** : Vous voyez les messages de sauvegarde/restauration
✅ **Robuste** : Même en cas d'échec du build, restauration garantie
✅ **Développement fluide** : Builds multiples sans risque

---

## 📞 En cas de problème

Si vos données sont quand même perdues :

1. **Vérifier le backup** : `ls packaging/windows/.backup_personal_data/`
2. **Restaurer manuellement** : Commandes ci-dessus
3. **Vérifier les logs** : Messages pendant le build
4. **Derniers recours** : Sauvegardes automatiques dans `data/backups/`

**Support :** adoudi@mondher.ch

---

**Version :** 1.6.0
**Date :** Décembre 2025
**Par :** Mondher ADOUDI
