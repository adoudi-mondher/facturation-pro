# ❓ FAQ - EASY FACTURE v1.5.0

**Questions fréquemment posées**

---

## 📦 INSTALLATION

### Q: Quel système d'exploitation est supporté ?
**R:** Windows 10+, macOS 11+, Linux (Ubuntu, Debian, Raspberry Pi OS)

### Q: Ai-je besoin d'installer Python ?
**R:** 
- **Windows .exe** : NON
- **Mac/Linux** : Le script l'installe automatiquement

### Q: Combien d'espace disque requis ?
**R:** 
- Windows : ~150 MB
- Mac/Linux : ~300 MB (avec environnement)
- Raspberry Pi : ~500 MB

### Q: Fonctionne sur Raspberry Pi 3 ?
**R:** OUI ! Optimisé pour Pi 3B+ et Pi 4 (4GB recommandé)

---

## 🚀 UTILISATION

### Q: Comment démarrer l'application ?
**R:**
- **Windows** : Double-clic `EasyFacture.exe`
- **Mac** : Double-clic `EasyFacture.command`
- **Linux** : Commande `easy-facture`

### Q: Comment arrêter l'application ?
**R:** Fermer la fenêtre console/terminal

### Q: L'application nécessite Internet ?
**R:** NON ! Fonctionne 100% hors ligne. Internet requis uniquement pour :
- Envoi d'emails
- Mises à jour (optionnel)

### Q: Puis-je utiliser sur plusieurs ordinateurs ?
**R:** OUI ! Copiez tout le dossier sur une clé USB

---

## 💾 DONNÉES

### Q: Où sont stockées mes données ?
**R:** Dossier `data/facturation.db` (SQLite)

### Q: Comment sauvegarder ?
**R:** Copiez le dossier `data/` régulièrement

### Q: Comment restaurer ?
**R:** Remplacez le dossier `data/` par votre sauvegarde

### Q: Mes données sont sécurisées ?
**R:** OUI ! Stockées localement, jamais sur le cloud

### Q: Puis-je exporter mes données ?
**R:** OUI ! 
- Export FEC (comptable)
- Export Excel
- Export CSV

---

## 📧 EMAIL

### Q: Comment configurer l'envoi d'emails ?
**R:** Paramètres → Configuration SMTP → Remplir les infos

### Q: Quel SMTP utiliser ?
**R:**
- **Gmail** : smtp.gmail.com (port 587) + mot de passe d'application
- **Outlook** : smtp-mail.outlook.com (port 587)

### Q: Erreur "Authentification failed" ?
**R:** 
- Gmail : Utilisez un mot de passe d'application (pas votre mot de passe Gmail)
- Activez la validation en 2 étapes d'abord

### Q: Le PDF s'attache automatiquement ?
**R:** OUI ! Dès que vous envoyez par email

---

## 📄 PDF

### Q: Comment personnaliser le PDF ?
**R:** 
- Paramètres → Logo (upload votre logo)
- Paramètres → Infos entreprise
- Les PDFs sont générés automatiquement

### Q: Puis-je changer les couleurs du PDF ?
**R:** Oui, dans `app/services/pdf_service.py` (lignes 18-23)

### Q: Le PDF n'inclut pas mon logo ?
**R:** Vérifiez :
1. Logo uploadé dans Paramètres
2. Format : PNG ou JPG
3. Taille max : 5 MB

---

## 💰 COMPTABILITÉ

### Q: Qu'est-ce que le FEC ?
**R:** Fichier des Écritures Comptables (obligatoire France pour contrôles fiscaux)

### Q: Je dois donner le FEC à mon comptable ?
**R:** OUI, si vous êtes en France et soumis aux contrôles

### Q: Le FEC est conforme ?
**R:** OUI, format officiel avec 18 colonnes réglementaires

---

## 🔧 TECHNIQUE

### Q: Quel port utilise l'application ?
**R:** 5000 par défaut (trouve automatiquement un port libre si occupé)

### Q: Comment changer le port ?
**R:** 
- Windows : Modifier `launcher.py` ligne 27
- Mac/Linux : Modifier le script de lancement

### Q: Puis-je accéder depuis un autre PC ?
**R:** OUI ! Remplacez `127.0.0.1` par votre IP locale

### Q: Antivirus bloque le .exe ?
**R:** Ajoutez une exception (faux positif classique avec PyInstaller)

---

## 🍓 RASPBERRY PI

### Q: Quelle version de Raspberry Pi ?
**R:** Pi 3B+ minimum, Pi 4 (4GB) recommandé

### Q: Démarre automatiquement ?
**R:** OUI ! Configuré avec systemd

### Q: Comment connecter une imprimante ?
**R:** Menu → Préférences → Print Settings

### Q: Fonctionne avec écran tactile ?
**R:** OUI ! Support natif

### Q: Performances ?
**R:** 
- RAM : 200-300 MB
- CPU : 5-10%
- Très fluide sur Pi 4

---

## 🐳 DOCKER

### Q: Pourquoi utiliser Docker ?
**R:** 
- Installation universelle
- Isolation complète
- Parfait pour serveur

### Q: Comment démarrer avec Docker ?
**R:** `docker-compose up -d`

### Q: Accès depuis un autre PC ?
**R:** `http://[IP-SERVEUR]:5000`

---

## 💸 COMMERCIAL

### Q: Quel est le prix ?
**R:** 
- Logiciel seul : 49€ (licence unique)
- Kit Raspberry Pi : 299€ (inclut licence)

### Q: C'est un abonnement ?
**R:** NON ! Paiement unique, pas d'abonnement

### Q: Les mises à jour sont payantes ?
**R:** 
- Mises à jour v1.x : GRATUITES
- Support 1 an : Inclus
- Années suivantes : 19€/an (optionnel)

---

## 🆘 PROBLÈMES COURANTS

### "Port déjà utilisé"
**Solution :** Fermer les autres instances ou redémarrer

### "Base de données corrompue"
**Solution :** Restaurer depuis sauvegarde

### "Erreur au démarrage"
**Solution :** 
1. Vérifier les logs
2. Réinstaller l'environnement
3. Contacter le support

### "PDF ne se génère pas"
**Solution :**
1. Vérifier le dossier `data/pdf/` existe
2. Permissions en écriture
3. Vérifier les logs

---

## 📞 SUPPORT

**Email :** adoudi@mondher.ch  
**Délai :** 24-48h  
**Support premium :** 99€/an (réponse prioritaire)

---

## 🚀 ASTUCES PRO

### Sauvegarder automatiquement
Créer un script de sauvegarde automatique du dossier `data/`

### Utiliser un NAS
Stocker le dossier `data/` sur un NAS pour partage réseau

### Imprimer directement
Configurer l'impression PDF automatique

### Multi-utilisateurs
Installer sur un serveur, accès depuis tous les postes

---

**Dernière mise à jour :** Décembre 2025  
**Version :** 1.5.0
