# Architecture de la Passerelle de Paiement Stripe - Easy Facture

## 📋 Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Spécifications](#spécifications)
3. [Architecture technique](#architecture-technique)
4. [Infrastructure et DNS](#infrastructure-et-dns)
5. [Intégration Stripe](#intégration-stripe)
6. [Schéma de base de données](#schéma-de-base-de-données)
7. [Implémentation détaillée](#implémentation-détaillée)
8. [Sécurité](#sécurité)
9. [Plan d'implémentation](#plan-dimplémentation)

---

## Vue d'ensemble

### Objectif
Permettre aux utilisateurs d'Easy Facture d'acheter une licence lifetime à **199€** directement depuis l'application desktop, avec activation automatique après paiement via Stripe.

### Contexte actuel
- **Application desktop**: Windows .exe (PyInstaller + Inno Setup)
- **Système de licence existant**: API trial sur `api.easyfacture.mondher.ch`
- **Base de données**: PostgreSQL sur VPS OVH
- **DNS**: Géré par Infomaniak

---

## Spécifications

### Prix et devises
- **Prix de base**: 199€ (EUR)
- **Multi-devises**: Support prévu pour EUR, USD, CHF, GBP
- **Type de licence**: Lifetime (à vie)
- **Mode de paiement**: Carte bancaire via Stripe Checkout

### Expérience utilisateur
1. L'utilisateur utilise l'application en mode trial
2. Clic sur un bouton "Obtenir licence - 199€"
3. Redirection vers Stripe Checkout (page hébergée par Stripe)
4. Paiement sécurisé
5. Redirection vers page de confirmation sur `easyfacture.mondher.ch`
6. Email de confirmation automatique
7. Activation automatique de la licence (via webhook)

---

## Architecture technique

### Flux de paiement complet

```
┌─────────────────────────────────────────────────────────────────┐
│                    DESKTOP APP (Windows)                        │
│                                                                 │
│  [Mode Trial] → [Bouton "Obtenir licence - 199€"]             │
│                          ↓                                      │
│              POST /api/create-checkout-session                 │
│              Body: {machine_id, email}                         │
└────────────────────────────┬────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│              LICENSE SERVER (VPS OVH)                           │
│              api.easyfacture.mondher.ch                         │
│                                                                 │
│  1. Vérifier que machine_id n'a pas déjà de licence lifetime  │
│  2. Créer session Stripe Checkout avec metadata:              │
│     - machine_id                                                │
│     - email                                                     │
│     - price_id (199€)                                          │
│  3. Retourner checkout_url                                     │
└────────────────────────────┬────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                    STRIPE CHECKOUT                              │
│              (Page hébergée par Stripe)                         │
│                                                                 │
│  - Formulaire de paiement sécurisé (PCI-DSS compliant)        │
│  - Cartes bancaires supportées                                 │
│  - 3D Secure automatique                                       │
│  - Multi-devises                                                │
└────────────────────────────┬────────────────────────────────────┘
                             ↓
              ┌──────────────┴───────────────┐
              ↓                              ↓
┌─────────────────────────┐    ┌────────────────────────────────┐
│   SUCCESS_URL           │    │   WEBHOOK (backend)            │
│   (UX immédiate)        │    │   (activation licence)         │
│                         │    │                                │
│ easyfacture.mondher.ch/ │    │ api.easyfacture.mondher.ch/    │
│ payment/success         │    │ stripe/webhook                 │
│                         │    │                                │
│ ✅ Affichage:          │    │ 1. Vérifier signature Stripe  │
│ - Confirmation visuelle │    │ 2. Extraire metadata          │
│ - Remerciement          │    │ 3. UPDATE licenses SET:       │
│ - Instructions          │    │    - type = 'lifetime'        │
│ - Relancer l'app        │    │    - stripe_payment_id        │
│                         │    │    - activated_at = NOW()     │
│                         │    │ 4. Envoyer email confirmation │
└─────────────────────────┘    └────────────────────────────────┘
```

### Points clés de l'architecture

#### 1. **success_url** (expérience utilisateur)
- **URL**: `https://easyfacture.mondher.ch/payment/success?session_id={CHECKOUT_SESSION_ID}`
- **Rôle**: Affichage immédiat d'une confirmation à l'utilisateur
- **Contenu**: Page statique HTML/CSS professionnelle
- **Ne fait PAS l'activation** (risque si l'utilisateur n'arrive pas sur la page)

#### 2. **webhook** (activation réelle)
- **URL**: `https://api.easyfacture.mondher.ch/stripe/webhook`
- **Rôle**: Activation fiable de la licence côté serveur
- **Événement Stripe**: `checkout.session.completed`
- **Sécurité**: Vérification de signature Stripe obligatoire
- **C'est LA source de vérité** pour l'activation

---

## Infrastructure et DNS

### Architecture recommandée: Sous-domaine dédié

#### Option retenue: `easyfacture.mondher.ch`

**Avantages:**
- ✅ Professionnel et cohérent avec le branding
- ✅ Site statique ultra-rapide (pas de WordPress)
- ✅ SSL Let's Encrypt gratuit
- ✅ Aucune dépendance WordPress
- ✅ Hébergement sur VPS OVH existant
- ✅ Contrôle total sur le contenu

**Alternative rejetée:** `mondher.ch/easy-facture-success-payment`
- ❌ Moins professionnel
- ❌ Dépendance à WordPress
- ❌ Potentiellement plus lent
- ❌ Moins de contrôle

### Configuration DNS (Infomaniak)

```dns
Type: A
Nom: easyfacture
Valeur: [IP_VPS_OVH]
TTL: 3600
```

**Résultat:** `easyfacture.mondher.ch` → VPS OVH

---

## Intégration Stripe

### Configuration Stripe

#### 1. Créer un produit "Easy Facture Lifetime License"
```bash
# Via Dashboard Stripe ou API
Product Name: Easy Facture - Licence Lifetime
Description: Licence à vie pour Easy Facture
```

#### 2. Créer les prix par devise
```python
# Prix EUR (principal)
price_eur = stripe.Price.create(
    product="prod_XXXXXX",
    unit_amount=19900,  # 199.00 EUR en centimes
    currency="eur",
)

# Prix USD
price_usd = stripe.Price.create(
    product="prod_XXXXXX",
    unit_amount=21900,  # 219.00 USD
    currency="usd",
)

# Prix CHF
price_chf = stripe.Price.create(
    product="prod_XXXXXX",
    unit_amount=19900,  # 199.00 CHF
    currency="chf",
)
```

### Endpoint: Créer une session Checkout

**Route Flask:** `POST /api/create-checkout-session`

```python
from flask import Blueprint, request, jsonify
import stripe
import os

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

bp = Blueprint('payment', __name__)

@bp.route('/api/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """
    Crée une session Stripe Checkout pour l'achat d'une licence
    """
    data = request.json
    machine_id = data.get('machine_id')
    email = data.get('email')
    currency = data.get('currency', 'eur').lower()

    # Validation
    if not machine_id or not email:
        return jsonify({'error': 'machine_id et email requis'}), 400

    # Vérifier si la machine a déjà une licence lifetime
    existing_license = License.query.filter_by(
        machine_id=machine_id,
        type='lifetime'
    ).first()

    if existing_license:
        return jsonify({'error': 'Cette machine possède déjà une licence lifetime'}), 400

    # Prix selon la devise
    price_ids = {
        'eur': 'price_XXXXXX_EUR',
        'usd': 'price_XXXXXX_USD',
        'chf': 'price_XXXXXX_CHF',
    }

    price_id = price_ids.get(currency, price_ids['eur'])

    try:
        # Créer la session Checkout
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://easyfacture.mondher.ch/payment/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://easyfacture.mondher.ch/payment/cancel',
            customer_email=email,
            metadata={
                'machine_id': machine_id,
                'email': email,
                'product': 'easy_facture_lifetime'
            }
        )

        return jsonify({
            'checkout_url': session.url,
            'session_id': session.id
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### Endpoint: Webhook Stripe

**Route Flask:** `POST /stripe/webhook`

```python
import stripe
from flask import request, jsonify
from app.models import License
from app.extensions import db
from datetime import datetime

@bp.route('/stripe/webhook', methods=['POST'])
def stripe_webhook():
    """
    Webhook Stripe pour activer les licences après paiement
    """
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')

    try:
        # Vérifier la signature Stripe (CRITIQUE pour la sécurité)
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError:
        return jsonify({'error': 'Invalid signature'}), 400

    # Gérer l'événement checkout.session.completed
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Extraire les métadonnées
        machine_id = session['metadata'].get('machine_id')
        email = session['metadata'].get('email')

        if not machine_id or not email:
            return jsonify({'error': 'Missing metadata'}), 400

        # Activer la licence
        license_record = License.query.filter_by(machine_id=machine_id).first()

        if license_record:
            # Mettre à jour la licence existante (trial → lifetime)
            license_record.type = 'lifetime'
            license_record.email = email
            license_record.stripe_customer_id = session.get('customer')
            license_record.stripe_payment_intent_id = session.get('payment_intent')
            license_record.amount_paid = session['amount_total']
            license_record.currency = session['currency']
            license_record.activated_at = datetime.utcnow()
        else:
            # Créer une nouvelle licence (rare, mais possible)
            license_record = License(
                machine_id=machine_id,
                email=email,
                type='lifetime',
                stripe_customer_id=session.get('customer'),
                stripe_payment_intent_id=session.get('payment_intent'),
                amount_paid=session['amount_total'],
                currency=session['currency'],
                activated_at=datetime.utcnow()
            )
            db.session.add(license_record)

        db.session.commit()

        # TODO: Envoyer email de confirmation
        # send_license_confirmation_email(email, machine_id)

        return jsonify({'status': 'success'}), 200

    return jsonify({'status': 'ignored'}), 200
```

---

## Schéma de base de données

### Table `licenses` (PostgreSQL)

**Modifications à apporter:**

```sql
-- Ajouter colonnes Stripe
ALTER TABLE licenses ADD COLUMN stripe_customer_id VARCHAR(255);
ALTER TABLE licenses ADD COLUMN stripe_payment_intent_id VARCHAR(255);
ALTER TABLE licenses ADD COLUMN amount_paid INTEGER; -- en centimes
ALTER TABLE licenses ADD COLUMN currency VARCHAR(3) DEFAULT 'EUR';

-- Index pour recherche rapide
CREATE INDEX idx_licenses_stripe_customer ON licenses(stripe_customer_id);
CREATE INDEX idx_licenses_stripe_payment ON licenses(stripe_payment_intent_id);
```

**Schéma complet:**

```sql
CREATE TABLE licenses (
    id SERIAL PRIMARY KEY,
    machine_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    type VARCHAR(20) DEFAULT 'trial', -- 'trial' ou 'lifetime'

    -- Colonnes Stripe
    stripe_customer_id VARCHAR(255),
    stripe_payment_intent_id VARCHAR(255),
    amount_paid INTEGER, -- Montant en centimes (19900 = 199.00€)
    currency VARCHAR(3) DEFAULT 'EUR',

    -- Dates
    activated_at TIMESTAMP, -- Date d'activation lifetime
    created_at TIMESTAMP DEFAULT NOW(),

    -- Index
    CONSTRAINT check_type CHECK (type IN ('trial', 'lifetime'))
);

CREATE INDEX idx_licenses_machine_id ON licenses(machine_id);
CREATE INDEX idx_licenses_email ON licenses(email);
CREATE INDEX idx_licenses_type ON licenses(type);
CREATE INDEX idx_licenses_stripe_customer ON licenses(stripe_customer_id);
```

---

## Implémentation détaillée

### 1. Configuration Nginx sur VPS OVH

**Fichier:** `/etc/nginx/sites-available/easyfacture.mondher.ch`

```nginx
server {
    listen 80;
    server_name easyfacture.mondher.ch;

    # Redirection HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name easyfacture.mondher.ch;

    # SSL Let's Encrypt
    ssl_certificate /etc/letsencrypt/live/easyfacture.mondher.ch/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/easyfacture.mondher.ch/privkey.pem;

    # Sécurité SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Root du site statique
    root /var/www/easyfacture-website;
    index index.html;

    # Logs
    access_log /var/log/nginx/easyfacture.access.log;
    error_log /var/log/nginx/easyfacture.error.log;

    # Servir les fichiers statiques
    location / {
        try_files $uri $uri/ =404;
    }

    # Headers sécurité
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

**Activation:**
```bash
sudo ln -s /etc/nginx/sites-available/easyfacture.mondher.ch /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 2. SSL avec Let's Encrypt

```bash
# Installer Certbot
sudo apt update
sudo apt install certbot python3-certbot-nginx

# Obtenir certificat SSL
sudo certbot --nginx -d easyfacture.mondher.ch

# Renouvellement automatique (déjà configuré par Certbot)
sudo certbot renew --dry-run
```

### 3. Structure du site statique

**Arborescence:**
```
/var/www/easyfacture-website/
├── index.html              # Landing page
├── payment/
│   ├── success.html        # Page de succès après paiement
│   └── cancel.html         # Page si annulation
├── assets/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
│       ├── logo.png
│       └── screenshots/
└── legal/
    ├── mentions-legales.html
    ├── cgv.html
    └── politique-confidentialite.html
```

### 4. Page de succès (success.html)

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Paiement validé - Easy Facture</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            background: white;
            border-radius: 20px;
            padding: 60px 40px;
            max-width: 600px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }

        .checkmark {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: #28a745;
            margin: 0 auto 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: scaleIn 0.5s ease-out;
        }

        .checkmark svg {
            width: 50px;
            height: 50px;
            stroke: white;
            stroke-width: 3;
            fill: none;
            stroke-dasharray: 50;
            stroke-dashoffset: 50;
            animation: drawCheck 0.5s ease-out 0.3s forwards;
        }

        @keyframes scaleIn {
            from { transform: scale(0); }
            to { transform: scale(1); }
        }

        @keyframes drawCheck {
            to { stroke-dashoffset: 0; }
        }

        h1 {
            color: #28a745;
            font-size: 2.5rem;
            margin-bottom: 20px;
        }

        p {
            color: #666;
            font-size: 1.1rem;
            line-height: 1.8;
            margin-bottom: 30px;
        }

        .info-box {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin: 30px 0;
            text-align: left;
        }

        .info-box h3 {
            color: #333;
            margin-bottom: 15px;
            font-size: 1.2rem;
        }

        .info-box ul {
            list-style: none;
            padding-left: 0;
        }

        .info-box li {
            padding: 8px 0;
            color: #555;
        }

        .info-box li:before {
            content: "✓ ";
            color: #28a745;
            font-weight: bold;
            margin-right: 10px;
        }

        .btn {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 40px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.1rem;
            transition: transform 0.3s, box-shadow 0.3s;
            margin-top: 20px;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }

        .email-notice {
            background: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 10px;
            padding: 15px;
            margin-top: 30px;
            color: #856404;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="checkmark">
            <svg viewBox="0 0 52 52">
                <polyline points="14 27 22 35 38 17"/>
            </svg>
        </div>

        <h1>Paiement validé !</h1>

        <p>
            Merci pour votre achat ! Votre licence <strong>Easy Facture Lifetime</strong>
            sera activée automatiquement dans les prochaines minutes.
        </p>

        <div class="info-box">
            <h3>📋 Prochaines étapes :</h3>
            <ul>
                <li>Relancez l'application Easy Facture</li>
                <li>Votre licence sera automatiquement détectée</li>
                <li>Vous recevrez un email de confirmation sous peu</li>
                <li>Profitez de toutes les fonctionnalités sans limitation !</li>
            </ul>
        </div>

        <div class="email-notice">
            📧 Un email de confirmation a été envoyé à votre adresse.
            Pensez à vérifier vos spams si vous ne le recevez pas.
        </div>

        <a href="#" class="btn" onclick="alert('Fermez cette page et relancez Easy Facture'); return false;">
            Compris, merci !
        </a>

        <p style="margin-top: 30px; font-size: 0.9rem; color: #999;">
            Besoin d'aide ? Contactez-nous à
            <a href="mailto:support@easyfacture.mondher.ch" style="color: #667eea;">
                support@easyfacture.mondher.ch
            </a>
        </p>
    </div>
</body>
</html>
```

### 5. Code côté application desktop (Python)

**Fonction pour initier le paiement:**

```python
import requests
import webbrowser
from app.utils.license import get_machine_id

def purchase_lifetime_license(email):
    """
    Démarre le processus d'achat de licence lifetime
    """
    machine_id = get_machine_id()

    # Appeler l'API pour créer une session Checkout
    response = requests.post(
        'https://api.easyfacture.mondher.ch/api/create-checkout-session',
        json={
            'machine_id': machine_id,
            'email': email,
            'currency': 'eur'
        }
    )

    if response.status_code == 200:
        data = response.json()
        checkout_url = data['checkout_url']

        # Ouvrir le navigateur sur la page de paiement Stripe
        webbrowser.open(checkout_url)

        return True
    else:
        error = response.json().get('error', 'Erreur inconnue')
        raise Exception(f"Erreur lors de la création de la session: {error}")
```

**Interface utilisateur (bouton dans l'app):**

```python
# Dans votre interface Tkinter/Qt
def on_purchase_click():
    """
    Gérer le clic sur le bouton "Obtenir licence"
    """
    email = email_entry.get()

    if not email or '@' not in email:
        messagebox.showerror("Erreur", "Veuillez entrer une adresse email valide")
        return

    try:
        purchase_lifetime_license(email)
        messagebox.showinfo(
            "Redirection",
            "Votre navigateur va s'ouvrir pour finaliser le paiement.\n\n"
            "Une fois le paiement effectué, relancez l'application."
        )
    except Exception as e:
        messagebox.showerror("Erreur", str(e))
```

---

## Sécurité

### Points critiques

#### 1. Vérification signature webhook Stripe
```python
# TOUJOURS vérifier la signature
event = stripe.Webhook.construct_event(
    payload, sig_header, webhook_secret
)
# NE JAMAIS faire confiance au payload sans vérification
```

#### 2. Variables d'environnement
```bash
# .env sur le serveur (NE JAMAIS commiter)
STRIPE_SECRET_KEY=sk_live_XXXXXXXXXX
STRIPE_WEBHOOK_SECRET=whsec_XXXXXXXXXX
STRIPE_PUBLISHABLE_KEY=pk_live_XXXXXXXXXX
```

#### 3. HTTPS obligatoire partout
- `api.easyfacture.mondher.ch` → SSL Let's Encrypt
- `easyfacture.mondher.ch` → SSL Let's Encrypt
- Stripe webhook REFUSE les URLs HTTP

#### 4. Validation des données
```python
# Vérifier que machine_id n'a pas déjà une licence
# Vérifier format email
# Vérifier que le paiement est bien completed
# Logger tous les événements webhook
```

#### 5. Idempotence du webhook
```python
# Stripe peut renvoyer le même événement plusieurs fois
# Utiliser stripe_payment_intent_id comme clé unique
if License.query.filter_by(stripe_payment_intent_id=payment_intent_id).first():
    return jsonify({'status': 'already_processed'}), 200
```

---

## Plan d'implémentation

### Phase 1: Infrastructure (2-3 heures)
1. ✅ Configurer DNS Infomaniak (`easyfacture.mondher.ch` → VPS OVH)
2. ✅ Créer dossier `/var/www/easyfacture-website`
3. ✅ Configurer Nginx
4. ✅ Obtenir certificat SSL Let's Encrypt
5. ✅ Créer pages statiques (success, cancel, landing)

### Phase 2: Backend License Server (3-4 heures)
1. ✅ Modifier schéma BDD (ajouter colonnes Stripe)
2. ✅ Créer route `/api/create-checkout-session`
3. ✅ Créer route `/stripe/webhook`
4. ✅ Configurer variables d'environnement Stripe
5. ✅ Tester en mode test Stripe

### Phase 3: Stripe Configuration (1-2 heures)
1. ✅ Créer produit "Easy Facture Lifetime" dans Dashboard Stripe
2. ✅ Créer prix pour EUR, USD, CHF
3. ✅ Configurer webhook endpoint dans Stripe Dashboard
4. ✅ Récupérer clés API et webhook secret

### Phase 4: Application Desktop (2-3 heures)
1. ✅ Ajouter bouton "Obtenir licence - 199€" dans l'interface
2. ✅ Implémenter fonction `purchase_lifetime_license()`
3. ✅ Tester ouverture navigateur vers Stripe
4. ✅ Vérifier détection automatique licence après activation

### Phase 5: Tests (2-3 heures)
1. ✅ Test complet en mode Stripe Test
2. ✅ Vérifier webhook reçu et traité
3. ✅ Vérifier activation licence en BDD
4. ✅ Vérifier email confirmation (si implémenté)
5. ✅ Vérifier détection dans l'app desktop

### Phase 6: Production (1 heure)
1. ✅ Passer en mode Stripe Live
2. ✅ Mettre à jour clés API en production
3. ✅ Tester un paiement réel (puis rembourser)
4. ✅ Monitoring des logs webhook

**Temps total estimé: 11-16 heures** (sur plusieurs jours)

---

## Ressources

### Documentation Stripe
- [Stripe Checkout](https://stripe.com/docs/payments/checkout)
- [Webhooks](https://stripe.com/docs/webhooks)
- [Testing](https://stripe.com/docs/testing)

### Cartes de test Stripe
```
Succès: 4242 4242 4242 4242
3D Secure: 4000 0027 6000 3184
Refusée: 4000 0000 0000 0002
```

### Variables d'environnement
```bash
# Mode Test
STRIPE_SECRET_KEY=sk_test_XXXXXXXXXX
STRIPE_PUBLISHABLE_KEY=pk_test_XXXXXXXXXX
STRIPE_WEBHOOK_SECRET=whsec_XXXXXXXXXX

# Mode Production
STRIPE_SECRET_KEY=sk_live_XXXXXXXXXX
STRIPE_PUBLISHABLE_KEY=pk_live_XXXXXXXXXX
STRIPE_WEBHOOK_SECRET=whsec_XXXXXXXXXX
```

---

## Questions fréquentes (FAQ)

### Pourquoi success_url ET webhook ?
- **success_url**: UX immédiate pour l'utilisateur (visuel)
- **webhook**: Activation réelle et fiable (serveur-to-serveur)
- Le webhook est LA source de vérité, success_url est juste de l'affichage

### Que se passe-t-il si l'utilisateur ferme le navigateur avant success_url ?
- Aucun problème ! Le webhook activera quand même la licence
- L'utilisateur recevra l'email de confirmation
- À la prochaine ouverture de l'app, la licence sera détectée

### Peut-on activer plusieurs machines avec la même licence ?
- Non, le `machine_id` est unique
- Une licence = une machine
- Pour changer de machine, il faudra une fonction de transfert (future feature)

### Remboursements ?
- Gérer via Dashboard Stripe (manuel)
- Le webhook `charge.refunded` peut être écouté pour désactiver auto

---

## Notes importantes

- 🔒 **Sécurité**: TOUJOURS vérifier signature webhook
- 📧 **Email**: Implémenter confirmation email (SendGrid, Mailgun, ou SMTP)
- 📊 **Logs**: Logger tous les événements webhook pour debug
- 🧪 **Tests**: Tester abondamment en mode test avant production
- 💰 **Prix**: 199€ est le prix initial, ajustable dans Stripe Dashboard
- 🌍 **Multi-devises**: Créer un prix par devise dans Stripe
- 🔄 **Webhook retry**: Stripe retry automatiquement si timeout/erreur

---

**Document créé le:** 2026-01-03
**Dernière mise à jour:** 2026-01-03
**Version:** 1.0
**Auteur:** Mondher

