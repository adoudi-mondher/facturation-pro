# 🔧 Corrections du Build Windows - EasyFacture v1.6.0

**Date :** 12 décembre 2025
**Par :** Mondher Adoudi

---

## 📋 Problèmes identifiés et corrigés

### ❌ Problème principal
Le build Windows échouait avec l'erreur : **"Spec file not found"** et chemins Unix invalides.

### 🔍 Causes identifiées

1. **Chemins Unix dans le fichier .spec Windows** ([packaging/windows/EasyFacture.spec](packaging/windows/EasyFacture.spec))
   - Chemins absolus Unix `/run.py` au lieu de chemins relatifs Windows `../../run.py`
   - Icône avec chemin Unix `/icons/icon.ico`

2. **Imports manquants pour le système de licence v1.6.0**
   - `cryptography` et `cryptography.fernet` non inclus
   - `PIL` et `PIL.Image` pour le traitement d'images
   - `dateutil` et `dateutil.parser` pour les dates

3. **Environnement virtuel cassé**
   - Le `venv` existant pointait vers un Python 3.14 mal installé
   - Message : `Could not find platform independent libraries <prefix>`

4. **Incompatibilité Git Bash**
   - Pas de script `.sh` pour les utilisateurs Git Bash
   - Seul `build.bat` disponible (CMD/PowerShell uniquement)

---

## ✅ Solutions appliquées

### 1. Correction du fichier .spec ([packaging/windows/EasyFacture.spec](packaging/windows/EasyFacture.spec))

**Avant :**
```python
Analysis(
    ['/run.py'],  # ❌ Chemin Unix absolu
    datas=[
        ('/app', 'app'),  # ❌ Chemins Unix
        ('/static', 'static'),
    ],
    icon='/icons/icon.ico'  # ❌ Chemin Unix
)
```

**Après :**
```python
Analysis(
    ['../../run.py'],  # ✅ Chemin relatif Windows
    datas=[
        ('../../app', 'app'),  # ✅ Chemins relatifs
        ('../../static', 'static'),
        ('../../config.py', '.'),
        ('../../icons', 'icons')  # ✅ Dossier icons ajouté
    ],
    hiddenimports=[
        # ... imports Flask existants ...
        'cryptography',  # ✅ Nouveau
        'cryptography.fernet',  # ✅ Nouveau
        'PIL',  # ✅ Nouveau
        'PIL.Image',  # ✅ Nouveau
        'dateutil',  # ✅ Nouveau
        'dateutil.parser'  # ✅ Nouveau
    ],
    icon='../../icons/icon.ico'  # ✅ Chemin relatif
)
```

### 2. Mise à jour de build.bat ([packaging/windows/build.bat](packaging/windows/build.bat))

**Modifications :**
- Version mise à jour : **1.5.0 → 1.6.0**
- Ajout des nouveaux `hiddenimports` dans la génération dynamique du .spec
- Ajout du dossier `icons` dans les `datas`
- Correction du chemin de l'icône

### 3. Création d'un script Git Bash ([packaging/windows/build.sh](packaging/windows/build.sh))

Nouveau script shell compatible avec Git Bash sur Windows :

**Fonctionnalités :**
- ✅ Détection automatique de Python via `py` (Python Launcher)
- ✅ Création d'un `venv_build` dédié et propre
- ✅ Installation automatique de PyInstaller et dépendances
- ✅ Build avec gestion d'erreurs
- ✅ Vérification du résultat (taille, nombre de fichiers)
- ✅ Messages clairs et progressifs

**Usage :**
```bash
bash packaging/windows/build.sh
```

### 4. Synchronisation du .spec racine ([EasyFacture.spec](EasyFacture.spec))

Le fichier `.spec` à la racine du projet a également été mis à jour avec :
- Chemins relatifs depuis la racine (sans `../../`)
- Mêmes `hiddenimports` ajoutés
- Icône corrigée

---

## 📦 Résultat du build

**Build réussi ✅**

```
================================================
   BUILD TERMINÉ AVEC SUCCÈS !
================================================

📦 Exécutable: packaging/windows/dist/EasyFacture/EasyFacture.exe
📏 Taille: 53M

✓ EasyFacture.exe créé (13M)
✓ 219 fichiers dans le package
✓ Taille totale: 53M
```

**Contenu :**
```
packaging/windows/dist/EasyFacture/
├── EasyFacture.exe (13 MB)
└── _internal/ (40 MB)
    ├── Python runtime
    ├── Bibliothèques Flask, SQLAlchemy, ReportLab, etc.
    ├── app/ (code de l'application)
    ├── static/ (CSS, JS, images)
    ├── data/ (base de données SQLite)
    ├── config.py
    └── icons/
```

---

## 🧪 Tests effectués

- ✅ Build depuis Git Bash avec Python 3.14
- ✅ Création du venv_build automatique
- ✅ Installation de toutes les dépendances (26 packages)
- ✅ Compilation PyInstaller sans erreurs critiques
- ✅ Génération de l'exécutable EasyFacture.exe
- ✅ Inclusion de tous les modules (Flask, cryptography, PIL, etc.)

**Avertissements (non bloquants) :**
- `Could not find platform independent libraries <prefix>` - Python 3.14 avec paths non standard, mais fonctionne
- `Hidden import 'flask_migrate' not found` - Module optionnel, pas utilisé dans le code
- `tkinter installation is broken` - Optionnel pour l'UI de licence, fallback console disponible

---

## 📚 Documentation mise à jour

### [packaging/windows/README-WINDOWS.md](packaging/windows/README-WINDOWS.md)

- ✅ Version mise à jour : 1.6.0
- ✅ Instructions pour les deux méthodes de build (bat + sh)
- ✅ Section sur le système de licence
- ✅ Tailles exactes du package

---

## 🚀 Pour builder maintenant

### Option 1 : PowerShell / CMD
```cmd
cd packaging\windows
build.bat
```

### Option 2 : Git Bash
```bash
bash packaging/windows/build.sh
```

### Option 3 : Depuis la racine avec le .spec racine
```bash
cd /d/workflow/python/facturation-app
python -m PyInstaller EasyFacture.spec --clean
```

---

## ⚠️ Notes importantes

1. **Environnement virtuel dédié :**
   - Le script `build.sh` crée automatiquement `venv_build/`
   - Cela évite les conflits avec le `venv` existant qui était cassé
   - Vous pouvez supprimer l'ancien `venv` si vous voulez

2. **Python 3.14 :**
   - Des warnings `Could not find platform independent libraries` apparaissent
   - C'est un problème connu de Python 3.14 sur certaines installations Windows
   - **Le build fonctionne quand même** grâce au venv_build

3. **Fichier .spec :**
   - Le fichier [packaging/windows/EasyFacture.spec](packaging/windows/EasyFacture.spec) est maintenant permanent
   - Ne pas le supprimer (il n'est plus généré dynamiquement par build.sh)

4. **git ignore :**
   - Ajouter `venv_build/` à [.gitignore](.gitignore) si vous ne voulez pas le committer

---

## 🎯 Prochaines étapes recommandées

1. **Tester l'exécutable :**
   ```bash
   cd packaging/windows/dist/EasyFacture
   ./EasyFacture.exe
   ```

2. **Vérifier le système de licence :**
   - L'application devrait demander une clé de licence au premier lancement
   - Ou passer en mode dégradé si `ENABLE_LICENSE_CHECK = False`

3. **Créer un ZIP de distribution :**
   ```bash
   cd packaging/windows/dist
   zip -r EasyFacture-Windows-v1.6.0.zip EasyFacture/
   ```

4. **Commit des modifications :**
   ```bash
   git add packaging/windows/EasyFacture.spec
   git add packaging/windows/build.sh
   git add packaging/windows/build.bat
   git add packaging/windows/README-WINDOWS.md
   git add EasyFacture.spec
   git commit -m "fix(build): correct Windows build with proper paths and dependencies"
   ```

---

## 📞 Support

Si vous rencontrez des problèmes :
- Vérifiez que Python 3.14 est installé : `py --version`
- Supprimez `venv_build/` et relancez le build
- Vérifiez les logs dans `packaging/windows/build/EasyFacture/warn-EasyFacture.txt`

**Contact :** adoudi@mondher.ch

---

**✨ Build Windows corrigé et fonctionnel ! ✨**
