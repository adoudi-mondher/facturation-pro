# 🔒 Analyse de sécurité - Facturation Pro v1.6.0

**Date** : 12 décembre 2025
**Analysé par** : Claude Code Assistant

---

## 📊 Résumé exécutif

| Aspect | Statut | Risque | Action requise |
|--------|--------|--------|----------------|
| Base de données | ✅ Bon | 🟢 Faible | Aucune (SQLite local) |
| Secrets en clair | ⚠️ Attention | 🟡 Moyen | Recommandations |
| Clé de licence | ⚠️ Attention | 🟡 Moyen | Rotation conseillée |
| Secret key Flask | ⚠️ Attention | 🟠 Élevé | **URGENT** en production |
| Mots de passe SMTP | ✅ Bon | 🟢 Faible | Config utilisateur |
| Fichiers sensibles | ✅ Bon | 🟢 Faible | .gitignore OK |

---

## 🔍 Détail de l'analyse

### 1. Base de données (SQLite)

#### Configuration actuelle

**Fichier** : [config.py:25-26](config.py#L25-L26)
```python
DB_PATH = DATA_DIR / 'facturation.db'
SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
```

#### ✅ Points positifs

1. **SQLite local** - Pas d'exposition réseau
   - Fichier local : `data/facturation.db`
   - Pas de serveur de BDD distant à sécuriser
   - Pas de port ouvert

2. **Fichier protégé par .gitignore**
   - Pattern `*.db` ligne 18
   - Pattern `data/facturation.db` ligne 21
   - ✅ Ne sera jamais commité

3. **Pas de mot de passe requis**
   - SQLite = fichier local, pas d'auth
   - Sécurité = permissions du système de fichiers
   - Sur Windows : ACL (Access Control Lists)

#### ⚠️ Points d'attention

1. **Pas de chiffrement du fichier DB**
   - Le fichier `facturation.db` est en clair sur le disque
   - N'importe qui avec accès au fichier peut le lire

2. **Permissions Windows**
   - Par défaut, le propriétaire du fichier peut le lire
   - Autres utilisateurs Windows peuvent potentiellement y accéder

#### 💡 Recommandations

**Pour l'instant (0-50 clients)** : ✅ OK tel quel
- SQLite local est suffisant
- Application desktop mono-utilisateur
- Fichier dans `data/` du dossier application

**Si vous passez multi-utilisateurs** :
```python
# Option 1 : SQLite chiffré (SQLCipher)
SQLALCHEMY_DATABASE_URI = 'sqlite+pysqlcipher:///:memory:?cipher=aes-256-cfb&kdf_iter=64000'

# Option 2 : PostgreSQL avec auth
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/facturation'
```

---

### 2. SECRET_KEY Flask

#### Configuration actuelle

**Fichier** : [config.py:19](config.py#L19)
```python
SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
```

**Fichier** : [.env:2](.env#L2)
```bash
SECRET_KEY=changez-cette-cle-secrete-en-production
```

#### ⚠️ PROBLÈME CRITIQUE

**Valeur par défaut faible** : `'dev-secret-key-change-in-production'`
- ❌ Clé prévisible
- ❌ Pas assez longue (32 caractères minimum recommandé)
- ❌ Pas aléatoire

**Fichier .env avec valeur faible** : `changez-cette-cle-secrete-en-production`
- ❌ Clé d'exemple non changée
- ❌ Présente dans le code source

#### 🔥 Risque

Si un attaquant obtient la SECRET_KEY :
- Peut forger des cookies de session
- Peut usurper l'identité de n'importe quel utilisateur
- Peut contourner CSRF protection

#### ✅ Solution URGENTE

**Étape 1** : Générer une vraie clé forte
```bash
# Méthode 1 : Python
python -c "import secrets; print(secrets.token_hex(32))"

# Méthode 2 : OpenSSL
openssl rand -hex 32

# Exemple de sortie (64 caractères) :
# 8f3b2a9c7d6e1f4b5a0c8e2d9f7a3b6c1e4d8a2f5b9c0e3d7a1f6b4c8e2d9f5a3
```

**Étape 2** : Mettre à jour .env
```bash
# .env (NE PAS COMMITER)
SECRET_KEY=8f3b2a9c7d6e1f4b5a0c8e2d9f7a3b6c1e4d8a2f5b9c0e3d7a1f6b4c8e2d9f5a3
```

**Étape 3** : Améliorer config.py
```python
# config.py
import secrets

class Config:
    # Générer une clé aléatoire si .env non configuré
    _default_key = secrets.token_hex(32)
    SECRET_KEY = os.environ.get('SECRET_KEY') or _default_key

    # Avertir si clé par défaut utilisée
    if SECRET_KEY == _default_key:
        import warnings
        warnings.warn(
            "⚠️  SECRET_KEY non configurée ! Définissez SECRET_KEY dans .env",
            UserWarning
        )
```

---

### 3. Clé de chiffrement des licences

#### Configuration actuelle

**Fichier** : [app/utils/license.py:21](app/utils/license.py#L21)
```python
SECRET_KEY = b'PyJ-ejNAc-rrtIY8gYeawRCNQzoB39GnbQCUISOpIXM='
```

#### ⚠️ PROBLÈME MOYEN

**Clé hardcodée dans le code** :
- ❌ Présente dans tous les builds
- ❌ Visible dans le code source
- ❌ Même clé pour tous les déploiements

**Impact si compromise** :
- Un attaquant peut générer des licences valides
- Peut décrypter les licences existantes
- Peut contourner le système de licence

#### ✅ Solution recommandée

**Option 1** : Déplacer dans .env (simple)
```python
# app/utils/license.py
class LicenseManager:
    def __init__(self):
        # Lire depuis .env
        key = os.environ.get('LICENSE_SECRET_KEY')

        if not key:
            # Générer une clé unique au premier lancement
            key = Fernet.generate_key().decode()

            # Sauvegarder dans un fichier local caché
            key_file = Path.home() / '.facturationpro' / 'license.key'
            key_file.parent.mkdir(exist_ok=True)
            key_file.write_text(key)

            print(f"⚠️  Clé de licence générée et sauvegardée dans {key_file}")
            print(f"⚠️  Ajoutez dans votre .env : LICENSE_SECRET_KEY={key}")

        self._cipher = Fernet(key.encode())
```

**Option 2** : Clé par déploiement (avancé)
```python
# Générer une clé différente pour chaque installation
# Stockée dans un fichier protégé hors du code source
```

**Option 3** : Garder tel quel (acceptable pour commencer)
- ✅ OK pour les 10-50 premiers clients
- ⚠️ À changer avant passage en production large échelle
- 💡 Documenter que c'est un point d'amélioration v2.0

---

### 4. Mots de passe SMTP

#### Configuration actuelle

**Fichier** : [config.py:52-56](config.py#L52-L56)
```python
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USER = os.environ.get('SMTP_USER', '')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
```

**Fichier** : [.env:11-14](.env#L11-L14)
```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
```

#### ✅ Points positifs

1. **Lecture depuis .env**
   - Pas hardcodé dans le code
   - Fichier .env dans .gitignore
   - ✅ Ne sera jamais commité

2. **Valeurs par défaut vides**
   - Pas de mot de passe par défaut
   - L'utilisateur doit configurer

3. **Stockage en BDD chiffré ?**
   **Fichier** : [app/models/entreprise.py](app/models/entreprise.py)
   ```python
   smtp_password = db.Column(db.String(500))
   ```
   - ⚠️ Stocké en CLAIR dans la BDD !

#### ⚠️ Points d'attention

**Mot de passe SMTP en clair dans SQLite** :
- Table `entreprise`, colonne `smtp_password`
- ❌ Stocké en texte brut
- ❌ Visible si quelqu'un ouvre le fichier .db

#### 💡 Recommandations

**Option 1** : Chiffrement dans la BDD (recommandé)
```python
# app/models/entreprise.py
from cryptography.fernet import Fernet
import base64

class Entreprise(db.Model):
    _smtp_password_encrypted = db.Column('smtp_password', db.String(500))

    @property
    def smtp_password(self):
        """Décrypte le mot de passe"""
        if not self._smtp_password_encrypted:
            return ''

        cipher = Fernet(app.config['ENCRYPTION_KEY'])
        return cipher.decrypt(self._smtp_password_encrypted.encode()).decode()

    @smtp_password.setter
    def smtp_password(self, value):
        """Chiffre le mot de passe avant stockage"""
        if not value:
            self._smtp_password_encrypted = ''
            return

        cipher = Fernet(app.config['ENCRYPTION_KEY'])
        encrypted = cipher.encrypt(value.encode())
        self._smtp_password_encrypted = encrypted.decode()
```

**Option 2** : Ne pas stocker, demander à chaque envoi (simple)
```python
# Lors de l'envoi d'email, demander le mot de passe via formulaire
# Ne jamais le sauvegarder
```

**Option 3** : Utiliser OAuth2 au lieu de mot de passe
```python
# Gmail supporte OAuth2 (plus sécurisé que mot de passe)
# https://developers.google.com/gmail/api/auth/about-auth
```

---

### 5. Fichiers sensibles

#### Configuration actuelle

**Fichier** : [.gitignore](.gitignore)
```gitignore
# Database
*.db
data/facturation.db

# Environment
.env

# License files
license_*.txt
.personal_backup/

# Uploads
data/uploads/*
data/pdf/*.pdf
```

#### ✅ Points positifs

1. **Base de données protégée**
   - `*.db` exclu
   - `data/facturation.db` exclu explicitement

2. **Fichier .env protégé**
   - Ne sera jamais commité
   - Contient les secrets

3. **Licences personnelles protégées**
   - `license_*.txt` exclu
   - `.personal_backup/` exclu

4. **Documents clients protégés**
   - `data/pdf/*.pdf` exclu
   - Pas de fuite de factures clients

#### ⚠️ Vérification recommandée

Vérifier qu'aucun secret n'a déjà été commité :
```bash
# Chercher dans l'historique Git
git log --all --full-history -- .env
git log --all --full-history -- "*.db"
git log --all --full-history -- "license_*.txt"

# Si trouvé, nettoyer l'historique (DANGEREUX)
# git filter-branch --force --index-filter \
#   'git rm --cached --ignore-unmatch .env' \
#   --prune-empty --tag-name-filter cat -- --all
```

---

## 🎯 Plan d'action recommandé

### 🔴 PRIORITÉ 1 - URGENT (avant distribution)

1. **Générer une SECRET_KEY forte**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   # Copier dans .env
   ```

2. **Documenter dans README**
   - Ajouter section "Configuration sécurisée"
   - Expliquer importance de SECRET_KEY

### 🟠 PRIORITÉ 2 - Important (avant 10 clients)

3. **Chiffrer les mots de passe SMTP en BDD**
   - Implémenter property avec Fernet
   - Migration des données existantes

4. **Rotation de la clé de licence**
   - Générer nouvelle clé
   - Documenter le processus

### 🟡 PRIORITÉ 3 - Améliorations (version 2.0)

5. **Ajouter chiffrement SQLite**
   - SQLCipher ou équivalent
   - Si données très sensibles

6. **Implémenter OAuth2 pour email**
   - Plus sécurisé que mot de passe SMTP
   - Gmail, Outlook supportent OAuth2

7. **Audit de sécurité complet**
   - Test d'intrusion
   - Revue de code par expert sécurité

---

## 📝 Checklist de sécurité

### Avant chaque déploiement

- [ ] SECRET_KEY unique et forte (64 caractères)
- [ ] Fichier .env configuré et NON commité
- [ ] Base de données .db NON commitée
- [ ] Licences personnelles NON commitées
- [ ] Mots de passe SMTP chiffrés (ou OAuth2)
- [ ] Clé de licence unique (ou accepter le risque)
- [ ] Permissions du dossier `data/` restrictives
- [ ] Logs ne contiennent pas de secrets
- [ ] HTTPS si déploiement web (futur)

### Documentation utilisateur

- [ ] Expliquer importance de SECRET_KEY
- [ ] Guide de configuration .env sécurisé
- [ ] Recommandations mots de passe SMTP
- [ ] Procédure de backup sécurisé de la BDD

---

## 🛡️ Recommandations générales

### Pour l'instant (Application desktop locale)

**Niveau de risque actuel** : 🟢 ACCEPTABLE

Votre application est une **application desktop** avec :
- SQLite local (pas d'exposition réseau)
- Utilisateur unique par installation
- Pas d'accès web distant

**Sécurité actuelle** : ✅ Suffisante pour :
- Usage personnel
- Déploiement chez clients (1 PC = 1 installation)
- <100 installations

### Si vous passez en mode web/multi-utilisateurs

**Niveau de risque** : 🔴 CRITIQUE

Il faudra alors :
- Passer à PostgreSQL avec auth forte
- Implémenter HTTPS obligatoire
- Ajouter authentification utilisateur
- Chiffrer TOUTES les données sensibles
- Audits de sécurité réguliers
- RGPD compliance

---

## 📚 Ressources

### Génération de secrets
```bash
# SECRET_KEY (64 chars)
python -c "import secrets; print(secrets.token_hex(32))"

# Clé Fernet pour chiffrement
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key())"

# UUID unique
python -c "import uuid; print(str(uuid.uuid4()))"
```

### Outils de sécurité Python
- `python-dotenv` - Variables d'environnement ✅ Déjà utilisé
- `cryptography` - Chiffrement ✅ Déjà utilisé
- `bandit` - Analyse statique de sécurité (à installer)
- `safety` - Check vulnérabilités dépendances (à installer)

### Commandes de vérification
```bash
# Installer outils de sécurité
pip install bandit safety

# Analyser le code
bandit -r app/

# Vérifier les dépendances
safety check

# Chercher secrets hardcodés
grep -r "password\|secret\|key" --include="*.py" app/ | grep "="
```

---

**Conclusion** : Votre application est **sécurisée pour une utilisation desktop locale**, mais nécessite quelques ajustements avant une distribution large échelle ou un passage en mode web.

**Actions critiques** :
1. ✅ Générer SECRET_KEY forte
2. ✅ Documenter configuration sécurisée
3. ⚠️ Envisager chiffrement SMTP passwords

**Version** : 1.6.0
**Date** : 12 décembre 2025
