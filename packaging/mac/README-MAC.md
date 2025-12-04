# 🍎 EASY FACTURE - VERSION MAC

**Version :** 1.5.0  
**Par :** Mondher ADOUDI - Sidr Valley AI  
**Contact :** adoudi@mondher.ch

---

## 🚀 INSTALLATION

### Étape 1 : Préparer le package

```bash
cd mac
chmod +x install.sh
./install.sh
```

---

## 📦 DISTRIBUTION

### Structure du package :

```
EasyFacture-Mac/
├── EasyFacture.command     ← Double-clic pour lancer
├── requirements.txt
├── run.py
├── app/
├── data/
├── config.py
├── Guide-Utilisateur.pdf
└── LISEZMOI.txt
```

**Compresser en ZIP :**
```bash
zip -r EasyFacture-Mac-v1.5.0.zip EasyFacture-Mac/
```

---

## 👤 GUIDE UTILISATEUR

### Installation :
1. Extraire le ZIP
2. **Double-cliquer sur `EasyFacture.command`**
3. Si "Non identifié" :
   - Clic droit → Ouvrir
   - Confirmer "Ouvrir"
4. ✅ Le navigateur s'ouvre automatiquement !

### Première utilisation :
Le script va :
- ✅ Créer l'environnement Python
- ✅ Installer les dépendances (1-2 min)
- ✅ Lancer l'application

**Les fois suivantes = instantané !**

---

## 🔧 CONFIGURATION

### Autoriser l'exécution :

```bash
cd EasyFacture-Mac
chmod +x EasyFacture.command
```

### Terminal au lieu de double-clic :

```bash
./EasyFacture.command
```

---

## 🐛 DÉPANNAGE

### "Impossible d'ouvrir" :
1. Clic droit sur `EasyFacture.command`
2. Ouvrir
3. Confirmer

### Python non trouvé :
```bash
# Installer Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Installer Python
brew install python3
```

### Port occupé :
- Le script trouve automatiquement un port libre
- Vérifier avec : `lsof -i :5000`

---

## 📊 ESPACE DISQUE

**Application :** ~50 MB  
**Avec environnement :** ~200-300 MB  
**Avec données :** Variable

---

## ✅ TESTÉ SUR

- ✅ macOS Sonoma (14.x)
- ✅ macOS Ventura (13.x)
- ✅ macOS Monterey (12.x)
- ✅ macOS Big Sur (11.x)

**Architectures :**
- ✅ Intel (x86_64)
- ✅ Apple Silicon (M1/M2/M3)

---

## 💡 ASTUCE

**Créer une icône Dock :**
1. Glisser `EasyFacture.command` dans le Dock
2. Lancer depuis le Dock

---

**Support :** adoudi@mondher.ch  
**© 2025 Sidr Valley AI - Tous droits réservés**
