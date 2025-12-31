# 🔄 Intégration API Trial - EasyFacture v1.7

**Date**: Janvier 2025
**Objectif**: Permettre aux clients d'obtenir automatiquement une licence d'essai de 30 jours

---

## 📋 Modifications apportées

### 1. **Nouvelle dépendance**

Ajout de `requests==2.31.0` dans [requirements.txt](requirements.txt:27)

```bash
pip install requests==2.31.0
```

---

### 2. **Nouveau module: `app/utils/trial_client.py`**

Client API pour communiquer avec le License Server.

**Fonctionnalités** :
- `request_trial_license()` - Demande une licence d'essai au serveur
- `validate_license_online()` - Valide une licence auprès du serveur
- `should_check_online()` - Détermine si on doit vérifier (1x/jour)
- `mark_checked()` - Marque qu'on a vérifié

**Configuration** :
```python
# Production
API_BASE_URL = "https://api.mondher.ch/api/v1"

# Développement local
# API_BASE_URL = "http://127.0.0.1:8000/api/v1"
```

---

### 3. **Modifications dans `run.py`**

#### A. Fonction `check_license()` - Validation en 2 étapes

**Avant** : Validation 100% locale

**Maintenant** :
1. **Validation LOCALE** (toujours) - Fonctionne offline
2. **Validation API** (1x/jour si connexion internet) - Détecte révocation

**Comportement** :
- ✅ **Avec internet** : Vérifie l'API une fois par jour
- ✅ **Sans internet** : Continue avec validation locale uniquement
- ⚠️ **Licence révoquée** : Bloque le démarrage

**Fichier de tracking** : `data/.last_api_check` (timestamp du dernier check)

#### B. Fonction `attempt_activation()` - Interface Essai Gratuit

**Avant** : Une seule option
```
┌─────────────────────────────────┐
│  Entrez votre clé de licence    │
└─────────────────────────────────┘
```

**Maintenant** : Trois options
```
┌──────────────────────────────────────┐
│  Que souhaitez-vous faire ?          │
│                                      │
│  OUI : Essai GRATUIT 30 jours       │
│  NON : J'ai déjà une licence        │
│  ANNULER : Quitter                   │
└──────────────────────────────────────┘
```

**Flux "Essai Gratuit"** :
1. Utilisateur clique "OUI"
2. Demande son email
3. Appelle l'API : `POST /api/v1/licenses/trial`
4. Reçoit la licence chiffrée
5. Sauvegarde dans `data/license.key`
6. Valide localement
7. ✅ Application activée pour 30 jours

**Gestion d'erreurs** :
- Pas de connexion internet → Message clair
- Trial déjà existante → Informe l'utilisateur
- Rate limit dépassé → "Réessayez dans 1 heure"

---

### 4. **Modifications dans `EasyFacture.spec`**

Ajout des imports pour `requests` :
```python
hiddenimports=[
    # ... autres imports ...
    'requests',
    'requests.adapters',
    'requests.auth',
    'urllib3'
],
```

---

## 🔄 Flux utilisateur complet

### Scénario 1: Nouveau client (Essai gratuit)

```
1. Client télécharge EasyFacture.zip depuis mondher.ch/easyfacture
2. Extrait et lance EasyFacture.exe
3. Première popup : "Votre Machine ID : abc123..."
4. Deuxième popup : "Que souhaitez-vous faire ?"
5. Clique "OUI - Essai GRATUIT"
6. Entre son email : "client@example.com"
7. API génère la licence automatiquement
8. Popup : "Succès ! Vous pouvez utiliser EasyFacture pendant 30 jours"
9. Application se lance normalement
```

**Durée totale** : < 1 minute (vs. 24-48h avec processus manuel)

---

### Scénario 2: Client avec licence payante

```
1. Client lance EasyFacture.exe
2. Première popup : "Votre Machine ID : abc123..."
3. Deuxième popup : "Que souhaitez-vous faire ?"
4. Clique "NON - J'ai déjà une licence"
5. Colle la licence reçue par email
6. Popup : "Succès ! Licence activée"
7. Application se lance normalement
```

**Processus inchangé** : Comme avant (génération manuelle côté vendeur)

---

### Scénario 3: Validation périodique (utilisateur existant)

```
1. Client lance EasyFacture.exe (jour N+10)
2. Validation LOCALE : ✅ OK (expiration dans 20 jours)
3. Dernier check API : Il y a 2 jours → Pas besoin de re-vérifier
4. Application démarre immédiatement

---

1. Client lance EasyFacture.exe (jour N+11)
2. Validation LOCALE : ✅ OK (expiration dans 19 jours)
3. Dernier check API : Il y a 3 jours → Pas besoin de re-vérifier
4. Application démarre immédiatement

---

1. Client lance EasyFacture.exe (jour N+12)
2. Validation LOCALE : ✅ OK (expiration dans 18 jours)
3. Dernier check API : Il y a 1 jours → Pas besoin de re-vérifier
4. Application démarre immédiatement

---

1. Client lance EasyFacture.exe (jour N+13)
2. Validation LOCALE : ✅ OK (expiration dans 17 jours)
3. Dernier check API : Il y a 2 jours → Pas besoin de re-vérifier
4. Application démarre immédiatement

---

1. Client lance EasyFacture.exe (jour N+14)
2. Validation LOCALE : ✅ OK (expiration dans 16 jours)
3. Dernier check API : Il y a 3 jours → Pas besoin de re-vérifier
4. Application démarre immédiatement

---

1. Client lance EasyFacture.exe (jour N+15)
2. Validation LOCALE : ✅ OK (expiration dans 15 jours)
3. Dernier check API : Il y a 4 jours → ⏰ PLUS DE 24H, ON VÉRIFIE
4. Appel API : POST /api/v1/licenses/validate
5. Réponse API : ✅ Licence valide
6. Mise à jour fichier .last_api_check
7. Application démarre normalement
```

**Fréquence** : Check API tous les 1-2 jours (pas à chaque lancement)

---

## 🔐 Sécurité

### Points de sécurité maintenus

✅ **Chiffrement** : Licence toujours chiffrée avec Fernet (AES-128)
✅ **Machine ID** : Liaison machine toujours vérifiée
✅ **Validation locale** : Fonctionne sans internet (voyage, avion, etc.)
✅ **Pas de stockage de credentials** : API publique (pas d'auth pour trial)

### Nouveaux contrôles

✅ **Rate limiting** : 3 trials/heure par IP (anti-abus)
✅ **Révocation** : Licence peut être désactivée à distance
✅ **Unicité** : 1 seul trial par email ET par machine
✅ **Timeout** : Requêtes API limitées à 10 secondes

---

## 🧪 Tests à effectuer

### Tests avant déploiement

- [ ] **Test offline** : Lancer sans connexion internet → Validation locale OK
- [ ] **Test trial** : Obtenir une licence d'essai via l'interface
- [ ] **Test validation API** : Vérifier que le check quotidien fonctionne
- [ ] **Test révocation** : Révoquer une licence côté serveur → Blocage client
- [ ] **Test rate limit** : Demander 4 trials en 1h → Blocage à la 4ème
- [ ] **Test unicité email** : 2ème trial avec même email → Refus
- [ ] **Test unicité machine** : 2ème trial avec même machine → Refus
- [ ] **Test build Windows** : PyInstaller inclut bien `requests`

---

## 📦 Déploiement

### Étape 1: Mettre à jour l'environnement local

```bash
cd /d/workflow/python/facturation-app
pip install -r requirements.txt
```

### Étape 2: Tester en développement

```bash
# Modifier trial_client.py pour pointer vers dev
API_BASE_URL = "http://127.0.0.1:8000/api/v1"

# Lancer l'application
python run.py
```

### Étape 3: Builder le package client

```bash
cd packaging/windows
bash build_for_client.sh
```

**Vérifications** :
- `dist/EasyFacture/EasyFacture.exe` existe
- Taille : ~55-60 MB (vs. 53 MB avant, +requests)
- Fichier `_internal/app/utils/trial_client.py` présent

### Étape 4: Tester le build

1. Copier `dist/EasyFacture/` sur machine de test
2. Lancer `EasyFacture.exe`
3. Tester le flux "Essai Gratuit"

### Étape 5: Déployer l'API (voir license-server)

Avant de distribuer aux clients, déployer le License Server sur VPS.

### Étape 6: Switcher en production

Dans `app/utils/trial_client.py` :
```python
API_BASE_URL = "https://api.mondher.ch/api/v1"  # Production
```

Rebuilder et distribuer.

---

## 🎯 Configuration pour distribution

### Pour builds CLIENT (distribution publique)

**Dans `trial_client.py`** :
```python
API_BASE_URL = "https://api.mondher.ch/api/v1"  # Production
```

### Pour builds DÉVELOPPEUR (votre usage)

**Dans `run.py`** :
```python
ENABLE_LICENSE_CHECK = False  # Désactiver le check
```

---

## 📊 Métriques disponibles (côté serveur)

Une fois l'API déployée, vous pourrez suivre :

- **Nombre de trials demandés** (table `licenses` où `license_type='trial'`)
- **Taux de conversion** (trials → licences payantes)
- **Validations quotidiennes** (table `activations`)
- **Clients actifs** (dernière validation < 7 jours)
- **Taux d'expiration** (trials expirés non convertis)

---

## ❓ FAQ

### L'application fonctionne-t-elle sans internet ?

**OUI** ! La validation locale suffit. Le check API est optionnel (1x/jour).

### Que se passe-t-il si l'API est hors ligne ?

Validation locale continue de fonctionner. L'utilisateur ne voit aucune erreur.

### Peut-on révoquer une licence à distance ?

**OUI** ! Via le dashboard admin (Phase 2), vous marquez `is_revoked=True`. Au prochain check API (< 24h), le client sera bloqué.

### Combien de trials par machine ?

**1 seul**. L'API refuse les demandes suivantes pour la même machine OU le même email.

### Comment tester sans consommer son unique trial ?

Utilisez plusieurs machines virtuelles OU changez de Machine ID en modifiant le code temporairement.

---

## 🔜 Prochaines étapes

1. **Phase 1** : Déployer le License Server sur VPS
2. **Phase 2** : Créer le dashboard admin
3. **Phase 3** : Ajouter le système heartbeat (statistiques)
4. **Phase 4** : Email automatique (trial expiré, upgrade)

---

**Version**: 1.7.0
**Date**: Janvier 2025
**Statut**: ✅ Prêt pour tests
