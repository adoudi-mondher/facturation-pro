# 🌐 Guide de déploiement à distance - EasyFacture v1.6.0

**Version avec système de licence lié à la machine**

---

## 🎯 Problématique

Votre application est protégée par une licence liée au **Machine ID** (empreinte matérielle). Comment déployer chez un client **sans être sur place** ?

---

## ✅ Solution : 3 méthodes professionnelles

### 📋 **Méthode 1 : Récupération du Machine ID (RECOMMANDÉE)**

**Principe :** Le client vous envoie son Machine ID, vous générez sa licence à distance.

#### **Étape 1 : Préparer l'utilitaire pour le client**

Créez un petit exécutable autonome avec le script [get_machine_id.py](get_machine_id.py) :

```bash
# Compiler get_machine_id.py en .exe
pyinstaller --onefile --name "GetMachineID" get_machine_id.py
```

Résultat : `dist/GetMachineID.exe` (~10 MB)

#### **Étape 2 : Envoyer au client**

Package à envoyer :
```
📦 EasyFacture-Setup-Client.zip
├── GetMachineID.exe         ← Utilitaire simple
├── Instructions.txt         ← Guide client
└── EasyFacture-v1.6.0.zip   ← Application complète
```

**Instructions.txt** :
```
ETAPE 1 : OBTENIR VOTRE MACHINE ID
===================================
1. Double-cliquez sur "GetMachineID.exe"
2. Un fichier "machine_id_NOMPC.txt" sera créé
3. Envoyez ce fichier à : adoudi@mondher.ch

ETAPE 2 : RECEVOIR VOTRE LICENCE
=================================
Vous recevrez par email un fichier "license_votre_email.txt"
contenant votre clé de licence.

ETAPE 3 : INSTALLER L'APPLICATION
==================================
1. Décompressez "EasyFacture-v1.6.0.zip"
2. Double-cliquez sur "EasyFacture.exe"
3. Entrez la clé de licence reçue par email
4. L'application se lance automatiquement

Support : adoudi@mondher.ch
```

#### **Étape 3 : Client vous envoie son Machine ID**

Le client exécute `GetMachineID.exe` et vous envoie :
```
machine_id_CLIENTPC.txt
----------------------
Machine ID : a1b2c3d4e5f6...
```

#### **Étape 4 : Vous générez la licence**

Sur votre machine de développement :

```bash
# Lancer le générateur
python generate_customer_license.py

# Choisir option 2 : "Generer avec Machine ID (client distant)"
# Entrer le Machine ID reçu
# Entrer les infos client (email, nom, entreprise)
# Choisir type de licence (Trial, Annuelle, etc.)
```

Résultat : Un fichier `license_client_email_20251212.txt` est généré avec :
- La clé de licence chiffrée
- Les infos client
- Les instructions d'activation

#### **Étape 5 : Envoyer la licence au client**

Email au client :
```
Objet : Votre licence Facturation Pro

Bonjour,

Voici votre clé de licence Facturation Pro :

----------------------------------------------------------------------
gAAAAABnWxY2...votre_cle_complete_ici...
----------------------------------------------------------------------

Valable jusqu'au : 12/12/2026
Machine autorisée : PC-CLIENT-001

Instructions :
1. Lancez EasyFacture.exe
2. Copiez-collez la clé ci-dessus
3. Cliquez sur "Activer"

Support : adoudi@mondher.ch
Cordialement,
Mondher ADOUDI
```

---

### 🌐 **Méthode 2 : Version Trial + Activation en ligne (AVANCÉ)**

**Principe :** Distribution d'une version "trial" qui s'active via un serveur web.

#### **Architecture :**

```
Client                          Serveur Web (votre side)
┌─────────────┐                ┌──────────────────┐
│EasyFacture  │                │  License API     │
│  - Trial 30j│───── GET ────>│  - Génération    │
│  - Machine  │    MachineID  │  - Validation    │
│    ID auto  │<──── POST ─── │  - Base clients  │
└─────────────┘    License    └──────────────────┘
```

#### **Implémentation :**

**Créer une API Flask simple** (exemple) :

```python
# server_license_api.py
from flask import Flask, request, jsonify
from app.utils.license import LicenseManager

app = Flask(__name__)

@app.route('/api/request-license', methods=['POST'])
def request_license():
    """Client demande une licence"""
    data = request.json
    machine_id = data.get('machine_id')
    email = data.get('email')

    # TODO: Validation + Enregistrement en base
    # TODO: Envoyer email à l'admin pour approbation

    return jsonify({'status': 'pending', 'message': 'Demande enregistrée'})

@app.route('/api/activate', methods=['POST'])
def activate():
    """Admin approuve et client récupère la licence"""
    data = request.json
    token = data.get('activation_token')

    # TODO: Vérifier token d'activation
    # TODO: Générer licence

    return jsonify({'license_key': 'gAAAAABn...'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, ssl_context='adhoc')
```

**Avantages :**
- ✅ Activation automatique via internet
- ✅ Pas de Machine ID à copier-coller
- ✅ Statistiques clients en temps réel

**Inconvénients :**
- ❌ Nécessite un serveur web public
- ❌ Plus complexe à mettre en place

---

### 📧 **Méthode 3 : Licence générique + Activation manuelle**

**Principe :** Version démo illimitée mais avec watermark, activation payante après.

#### **Implémentation :**

Modifier [run.py:18](run.py#L18) :

```python
# Mode demo : désactiver la vérification stricte
ENABLE_LICENSE_CHECK = False  # Demo illimitée
# Ou
DEMO_MODE = True  # Afficher watermark "VERSION DEMO"
```

**Distribution :**
1. Client télécharge version "demo" sans licence
2. Application fonctionne avec limitations visuelles :
   - Watermark "VERSION DEMO" sur les PDFs
   - Message "Acheter licence" dans l'interface
3. Client achète → Vous générez licence → Client active

---

## 📊 Comparaison des méthodes

| Critère | Méthode 1<br>Machine ID | Méthode 2<br>API en ligne | Méthode 3<br>Demo |
|---------|------------------------|---------------------------|-------------------|
| **Simplicité** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **Sécurité** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Pas besoin serveur** | ✅ | ❌ | ✅ |
| **Expérience client** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Coût** | Gratuit | Hébergement | Gratuit |

**👉 Recommandation : Méthode 1 (Machine ID) pour commencer**

---

## 🛠️ Outils fournis

### ✅ Scripts disponibles

| Fichier | Usage | Qui l'utilise |
|---------|-------|---------------|
| [get_machine_id.py](get_machine_id.py) | Récupère Machine ID | **CLIENT** |
| [generate_customer_license.py](generate_customer_license.py) | Génère licences | **VOUS (admin)** |
| [test_license.py](test_license.py) | Test du système | Développement |

### 📦 Compiler get_machine_id.py en .exe

Pour envoyer au client un exécutable simple :

```bash
# Option 1 : Avec PyInstaller (fichier unique)
pyinstaller --onefile --name "GetMachineID" --icon icons/icon.ico get_machine_id.py

# Option 2 : Avec console visible (debug)
pyinstaller --onefile --console --name "GetMachineID" get_machine_id.py

# Résultat : dist/GetMachineID.exe (~10-15 MB)
```

---

## 🎬 Scénario complet : Déploiement client distant

### 📅 **Jour 1 : Préparation**

Vous (administrateur) :
```bash
# 1. Builder l'application VERSION CLIENT (propre, sans vos données)
bash packaging/windows/build_for_client.sh
# OU
packaging\windows\build_for_client.bat

# 2. Compiler l'utilitaire Machine ID
build_machine_id_tool.bat
# OU
pyinstaller --onefile get_machine_id.py

# 3. Créer le package client
mkdir EasyFacture-Setup-Client
cp dist/GetMachineID.exe EasyFacture-Setup-Client/
cp -r packaging/windows/dist/EasyFacture EasyFacture-Setup-Client/EasyFacture-v1.6.0/
echo "Instructions..." > EasyFacture-Setup-Client/Instructions.txt

# Vérifier que le package est PROPRE (sans vos données)
ls -la EasyFacture-Setup-Client/EasyFacture-v1.6.0/data/
# Devrait être VIDE (sauf dossiers uploads/ et backups/)

# 4. Compresser
zip -r EasyFacture-Setup-Client.zip EasyFacture-Setup-Client/

# 5. Envoyer au client
# Email avec lien Google Drive / Dropbox / WeTransfer
```

**⚠️ IMPORTANT** : Utilisez `build_for_client.sh` et NON `build.sh` pour distribuer aux clients !
- `build.sh` → Préserve VOS données (pour vous)
- `build_for_client.sh` → Version PROPRE (pour clients)

### 📧 **Jour 2 : Client récupère son Machine ID**

Client :
1. Reçoit `EasyFacture-Setup-Client.zip`
2. Décompresse
3. Double-clic sur `GetMachineID.exe`
4. Envoie `machine_id_CLIENTPC.txt` par email

### 🔑 **Jour 3 : Vous générez la licence**

Vous :
```bash
# 1. Ouvrir le générateur
python generate_customer_license.py

# 2. Option "2" (Machine ID distant)
# 3. Coller le Machine ID reçu : a1b2c3d4e5f6...
# 4. Entrer : client@entreprise.com
# 5. Choisir : "5" (Licence annuelle)

# Résultat : license_client_entreprise.com_20251212.txt généré
```

### ✉️ **Jour 4 : Envoi de la licence**

Vous envoyez le fichier de licence par email sécurisé.

### ✅ **Jour 5 : Client active**

Client :
1. Lance `EasyFacture.exe`
2. Dialogue d'activation apparaît
3. Colle la clé reçue
4. Clique "Activer"
5. ✅ Application activée !

---

## 🔒 Sécurité

### ✅ Points forts

- **Chiffrement AES-128** : Clés chiffrées avec Fernet (cryptography)
- **Liaison hardware** : Machine ID basé sur MAC + système + hostname
- **Expiration** : Licences avec date de validité
- **Pas de serveur** : Pas de point de défaillance unique

### ⚠️ Limitations

- **Changement de matériel** : Nouvelle licence nécessaire si changement de carte réseau
- **Clonage VM** : Si client clone la VM, Machine ID identique
- **Transfert de clé** : Un client pourrait partager sa clé (mais limitée à sa machine)

### 🛡️ Améliorations possibles

1. **Anti-tamper** : Détecter modification du code
2. **Vérification périodique** : Check-in toutes les 30 jours
3. **Blacklist** : Système de révocation de licences
4. **Telemetry** : Statistiques d'usage anonymes

---

## 📞 Support client

### Questions fréquentes

**Q : "Mon Machine ID a changé après mise à jour Windows"**
R : Windows Update peut changer hostname. → Regénérer licence gratuite

**Q : "J'ai changé de PC, ma licence ne fonctionne plus"**
R : Normal, licence liée au hardware. → Acheter nouvelle licence ou transfert payant

**Q : "L'application dit 'Licence expirée'"**
R : Renouveler la licence annuelle. → Contacter pour renouvellement

### Templates d'emails

**Email 1 : Envoi du setup**
```
Objet : Setup Facturation Pro

Bonjour,

Voici le lien de téléchargement :
[Lien Google Drive]

Etapes :
1. Télécharger et décompresser
2. Exécuter GetMachineID.exe
3. M'envoyer le fichier machine_id_xxx.txt

Je vous enverrai votre licence sous 24h.

Cordialement,
```

**Email 2 : Envoi de la licence**
```
Objet : Votre licence Facturation Pro

Bonjour,

Votre licence est prête ! (voir pièce jointe)

Clé :
gAAAAABnWxY2...

Valable jusqu'au : [DATE]

Activez en lançant l'application.

Support : adoudi@mondher.ch
```

---

## ✨ Conclusion

La **Méthode 1 (Machine ID)** est idéale pour démarrer :
- ✅ Simple
- ✅ Sécurisé
- ✅ Pas de serveur
- ✅ Contrôle total

**Workflow optimal :**
1. Client télécharge → 2. Envoie Machine ID → 3. Reçoit licence → 4. Active → ✅ Prêt !

**Support :** adoudi@mondher.ch
