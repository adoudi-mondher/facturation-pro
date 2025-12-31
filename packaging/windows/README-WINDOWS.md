# 🪟 EASY FACTURE - VERSION WINDOWS

**Version :** 1.6.0 (avec système de licence)
**Par :** Mondher ADOUDI - Sidr Valley AI
**Contact :** adoudi@mondher.ch

---

## 🚀 BUILD DE L'APPLICATION

### ⚠️ IMPORTANT : 2 types de build

| Script | Pour | Vos données |
|--------|------|-------------|
| `build.bat` / `build.sh` | VOUS (dev) | ✅ Préservées |
| `build_for_client.bat` / `build_for_client.sh` | CLIENTS | ❌ Propre |

### 🏠 Build PERSONNEL (garde vos données)

**PowerShell/CMD :**
```cmd
cd packaging\windows
build.bat
```

**Git Bash :**
```bash
bash packaging/windows/build.sh
```

### 📦 Build CLIENT (propre pour distribution)

**PowerShell/CMD :**
```cmd
cd packaging\windows
build_for_client.bat
```

**Git Bash :**
```bash
bash packaging/windows/build_for_client.sh
```

---

Le script va :
1. ✅ Vérifier Python 3.14+
2. ✅ Créer un environnement virtuel dédié (`venv_build`)
3. ✅ Installer PyInstaller et toutes les dépendances
4. ✅ Compiler l'application avec tous les modules (cryptography, PIL, etc.)
5. ✅ Créer `packaging/windows/dist/EasyFacture/`

**Temps :** 2-5 minutes
**Résultat :**
- **EasyFacture.exe** : 13 MB
- **Package complet** : 53 MB (219 fichiers)

---

## 📦 DISTRIBUTION

### Créer le package utilisateur :

```
EasyFacture-Windows/
├── EasyFacture.exe          ← Double-clic pour lancer
├── data/                    ← Base de données
├── _internal/               ← Fichiers système (ne pas toucher)
├── Guide-Utilisateur.pdf
└── LISEZMOI.txt
```

**Compresser en ZIP :**
```
EasyFacture-Windows-v1.5.0.zip
```

---

## 👤 GUIDE UTILISATEUR

### Installation :
1. Extraire le ZIP
2. Double-cliquer sur `EasyFacture.exe`
3. ✅ Le navigateur s'ouvre automatiquement !

### Utilisation :
- **Lancer :** Double-clic sur `EasyFacture.exe`
- **Arrêter :** Fermer la fenêtre console
- **Données :** Dossier `data/`

---

## 🔧 CONFIGURATION

### Port personnalisé :

Modifier dans `launcher.py` :
```python
port = find_free_port(start_port=8000)  # Changer 5000 en 8000
```

Puis rebuild.

---

## 🐛 DÉPANNAGE

### L'exe ne démarre pas :
- Vérifier l'antivirus (peut bloquer)
- Exécuter en tant qu'administrateur

### Le navigateur ne s'ouvre pas :
- Attendre 5 secondes
- Ouvrir manuellement : `http://localhost:5000`

### Erreur "Port déjà utilisé" :
- Fermer les autres instances
- Redémarrer le PC

---

## 📊 TAILLE

**Exécutable compilé :** 13 MB (EasyFacture.exe)
**Package complet :** 53 MB (219 fichiers)
**Avec données utilisateur :** ~60-100 MB

## 🔐 SYSTÈME DE LICENCE (v1.6.0)

L'application inclut maintenant un système de protection par licence :
- Basé sur l'empreinte matérielle de la machine
- Chiffrement AES-128 (cryptography/Fernet)
- Licence stockée dans `%APPDATA%\FacturationPro\license.dat`
- Activation possible via interface graphique (tkinter) ou console

Pour désactiver en développement, modifier dans [run.py:18](../../run.py#L18) :
```python
ENABLE_LICENSE_CHECK = False
```

---

## ✅ TESTÉ SUR

- ✅ Windows 11
- ✅ Windows 10
- ✅ Windows Server 2019

---

**Support :** adoudi@mondher.ch  
**© 2025 Sidr Valley AI - Tous droits réservés**
