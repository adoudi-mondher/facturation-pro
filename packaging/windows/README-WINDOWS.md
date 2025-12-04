# 🪟 EASY FACTURE - VERSION WINDOWS

**Version :** 1.5.0  
**Par :** Mondher ADOUDI - Sidr Valley AI  
**Contact :** adoudi@mondher.ch

---

## 🚀 INSTALLATION

### Étape 1 : Build de l'exécutable

```cmd
cd windows
build.bat
```

Le script va :
1. ✅ Vérifier Python
2. ✅ Installer PyInstaller si nécessaire
3. ✅ Compiler l'application
4. ✅ Créer `dist\EasyFacture\`

**Temps :** 2-5 minutes

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

**Exécutable compilé :** ~80-150 MB  
**Avec données :** ~100-200 MB

---

## ✅ TESTÉ SUR

- ✅ Windows 11
- ✅ Windows 10
- ✅ Windows Server 2019

---

**Support :** adoudi@mondher.ch  
**© 2025 Sidr Valley AI - Tous droits réservés**
