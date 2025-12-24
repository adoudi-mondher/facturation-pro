# 🏠 Build Personnel vs 📦 Build Client

## ⚠️ QUESTION IMPORTANTE

**"Le build pour un nouveau client est-il propre sans données de test ?"**

### ❌ Réponse : NON (avec `build.sh` normal)

Si vous utilisez le script standard `build.sh` ou `build.bat`, le build **contient VOS données personnelles** car le système de protection **restaure** automatiquement votre dossier `data/` après le build.

### ✅ Solution : 2 scripts différents

---

## 📋 Comparaison des scripts

| Critère | `build.sh` / `build.bat` | `build_for_client.sh` / `.bat` |
|---------|--------------------------|-------------------------------|
| **Usage** | Développement personnel | Distribution aux clients |
| **Vos données** | ✅ PRÉSERVÉES | ❌ NON INCLUSES |
| **Votre licence** | ✅ Activée | ❌ Absente |
| **Base de données** | ✅ Vos factures/clients | ❌ Pas de BDD |
| **Uploads** | ✅ Vos logos/fichiers | ❌ Dossier vide |
| **Backups** | ✅ Vos sauvegardes | ❌ Dossier vide |
| **Prêt pour envoi** | ❌ NON (contient vos données) | ✅ OUI (propre) |

---

## 🏠 Script 1 : Build PERSONNEL (avec protection)

### Fichiers
- [packaging/windows/build.sh](packaging/windows/build.sh)
- [packaging/windows/build.bat](packaging/windows/build.bat)

### Utilisation

```bash
# Git Bash
bash packaging/windows/build.sh

# CMD / PowerShell
packaging\windows\build.bat
```

### Comportement

1. **Sauvegarde** automatique de `dist/EasyFacture/data/`
2. **Build** de l'application
3. **Restauration** automatique de vos données

### Résultat

```
dist/EasyFacture/
├── EasyFacture.exe
├── _internal/
└── data/                          ← VOS DONNÉES RESTAURÉES
    ├── facturation.db             ← Votre base de données
    ├── uploads/
    │   ├── logos/
    │   │   └── votre_logo.png     ← Vos fichiers
    │   └── factures/
    └── backups/
```

### ✅ Utiliser pour
- Votre usage personnel
- Tests et développement
- Garder votre environnement de travail intact

### ❌ NE PAS utiliser pour
- Distribuer aux clients (contient vos données !)
- Créer un package de distribution

---

## 📦 Script 2 : Build CLIENT (propre)

### Fichiers
- [packaging/windows/build_for_client.sh](packaging/windows/build_for_client.sh) ✨ NOUVEAU
- [packaging/windows/build_for_client.bat](packaging/windows/build_for_client.bat) ✨ NOUVEAU

### Utilisation

```bash
# Git Bash
bash packaging/windows/build_for_client.sh

# CMD / PowerShell
packaging\windows\build_for_client.bat
```

### Comportement

1. ⚠️ **Confirmation** : Demande si vous voulez vraiment un build propre
2. **Nettoyage complet** SANS sauvegarde
3. **Build** de l'application
4. **Création** d'un dossier `data/` vide structuré

### Résultat

```
dist/EasyFacture/
├── EasyFacture.exe
├── _internal/
└── data/                          ← DOSSIER VIDE (PROPRE)
    ├── uploads/                   ← Dossier vide
    │   └── .gitkeep
    └── backups/                   ← Dossier vide
        └── .gitkeep
```

### ✅ Utiliser pour
- **Distribuer aux clients**
- Créer un package de distribution
- Envoi par email/téléchargement

### ❌ NE PAS utiliser pour
- Votre usage personnel (efface vos données !)

---

## 🎬 Workflow recommandé

### Développement quotidien

```bash
# Utilisez le build normal (préserve vos données)
bash packaging/windows/build.sh

# Testez votre application
cd packaging/windows/dist/EasyFacture
./EasyFacture.exe

# Vos données sont intactes ✓
```

### Distribution client

```bash
# 1. Utilisez le build CLIENT (propre)
bash packaging/windows/build_for_client.sh

# 2. Vérifiez qu'il est propre
ls -la packaging/windows/dist/EasyFacture/data/
# → Doit être VIDE (sauf dossiers uploads/, backups/)

# 3. Compressez
cd packaging/windows/dist
zip -r EasyFacture-v1.6.0-Client.zip EasyFacture/

# 4. Envoyez au client
```

---

## 🔍 Comment vérifier si un build est "propre" ?

### Après le build, vérifiez :

```bash
# Vérifier l'absence de base de données
ls packaging/windows/dist/EasyFacture/data/facturation.db
# → Devrait dire "No such file" ✓

# Vérifier que uploads/ est vide
ls packaging/windows/dist/EasyFacture/data/uploads/
# → Devrait contenir seulement .gitkeep ✓

# Vérifier la taille du package
du -sh packaging/windows/dist/EasyFacture/
# → ~53M (si plus, contient probablement des données)
```

### Indicateurs d'un build "sale" (avec vos données)

❌ Fichier `data/facturation.db` existe (plusieurs MB)
❌ Dossier `data/uploads/` contient des fichiers
❌ Package fait >60 MB

### Indicateurs d'un build "propre"

✅ Pas de `data/facturation.db`
✅ `data/uploads/` vide (sauf .gitkeep)
✅ Package fait ~53 MB

---

## ⚡ Commandes rapides

```bash
# Build pour MOI (préserve mes données)
bash packaging/windows/build.sh

# Build pour CLIENT (propre, sans données)
bash packaging/windows/build_for_client.sh

# Vérifier qu'un build est propre
[ -f packaging/windows/dist/EasyFacture/data/facturation.db ] && echo "❌ PAS PROPRE" || echo "✅ PROPRE"
```

---

## 📝 Messages de confirmation

### build_for_client.sh affiche :

```
================================================
   EASY FACTURE - BUILD VERSION CLIENT
   Version 1.6.0 (Distribution propre)
================================================

⚠️  ATTENTION: Ce build sera SANS vos données de test
   Utiliser pour: Distribution aux clients
   Ne PAS utiliser pour: Votre version perso

Continuer? (o/n): _
```

→ Tapez `o` seulement si vous voulez un build PROPRE pour client

### build.sh affiche :

```
[4/6] Nettoyage des builds précédents...
     ⚠️  Sauvegarde des données personnelles détectée...
     ✓ Données sauvegardées temporairement
```

→ Vos données sont protégées

---

## 🎯 Récapitulatif

### Pour VOUS (développement)
```bash
bash packaging/windows/build.sh
```
✅ Garde votre licence
✅ Garde vos données de test
✅ Environnement de travail préservé

### Pour CLIENTS (distribution)
```bash
bash packaging/windows/build_for_client.sh
```
✅ Aucune donnée personnelle
✅ Prêt à envoyer immédiatement
✅ Le client créera sa propre base vierge

---

## 📚 Documentation associée

- [PROTECTION-DONNEES-BUILD.md](PROTECTION-DONNEES-BUILD.md) - Détails sur la protection des données
- [GUIDE-DEPLOIEMENT-DISTANT.md](GUIDE-DEPLOIEMENT-DISTANT.md) - Guide de déploiement complet
- [DEPLOIEMENT-CLIENT-README.md](DEPLOIEMENT-CLIENT-README.md) - Aide-mémoire rapide

---

**Version :** 1.6.0
**Date :** Décembre 2025
**Par :** Claude Code Assistant + Mondher ADOUDI

**⚠️ RÈGLE D'OR** : Utilisez TOUJOURS `build_for_client` pour distribuer !
