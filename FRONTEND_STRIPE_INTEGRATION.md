# Intégration Stripe Frontend - facturation-app

Guide d'implémentation du frontend pour l'achat de licences lifetime Easy Facture.

**Date**: 2026-01-03
**Version**: 1.0
**Status**: ✅ Implémentation frontend complète

---

## 📋 Modifications apportées

### 1. Module Payment (app/utils/payment.py)

**Nouveau fichier** avec la classe `PaymentManager`:

```python
class PaymentManager:
    def purchase_lifetime_license(email, machine_id, currency='eur'):
        """
        Démarre le processus d'achat d'une licence lifetime

        Returns:
            Tuple[bool, str, Optional[str]]: (succès, message, checkout_url)
        """
```

**Fonctionnalités:**
- Validation email et machine_id
- Appel API `/api/create-checkout-session`
- Ouverture automatique du navigateur sur Stripe Checkout
- Gestion des erreurs (réseau, rate limit, etc.)

### 2. Route Flask (app/routes/parametres.py)

**Nouvelle route ajoutée:**

```python
@bp.route('/purchase-license', methods=['POST'])
def purchase_license():
    """Initier l'achat d'une licence lifetime"""
```

**Comportement:**
- Reçoit l'email en POST (JSON)
- Récupère le machine_id via LicenseManager
- Appelle payment_manager.purchase_lifetime_license()
- Retourne JSON avec checkout_url

### 3. Template Paramètres (app/templates/parametres/index.html)

**Ajouts:**

#### Section Licence (après le formulaire de paramètres)
```html
<div class="card mt-4">
    <div class="card-header bg-primary text-white">
        <h5>Licence Easy Facture</h5>
    </div>
    <div class="card-body">
        <!-- Présentation de l'offre -->
        <button data-bs-toggle="modal" data-bs-target="#purchaseModal">
            Obtenir la licence
        </button>
    </div>
</div>
```

#### Modal Bootstrap
- Formulaire avec champ email
- Bouton "Procéder au paiement"
- Affichage des erreurs
- Spinner de chargement

#### Script JavaScript
- Validation email côté client
- Appel AJAX à `/parametres/purchase-license`
- Redirection automatique vers Stripe Checkout
- Gestion des erreurs

---

## 🎯 Flux utilisateur

```
1. Utilisateur va dans Paramètres
   ↓
2. Voit la section "Licence Easy Facture - 199€"
   ↓
3. Clique sur "Obtenir la licence"
   ↓
4. Modal s'ouvre avec formulaire email
   ↓
5. Remplit son email et clique "Procéder au paiement"
   ↓
6. JavaScript appelle /parametres/purchase-license (AJAX)
   ↓
7. Backend appelle /api/create-checkout-session
   ↓
8. Backend retourne checkout_url
   ↓
9. JavaScript redirige vers Stripe Checkout
   ↓
10. Utilisateur paie sur Stripe
    ↓
11. Stripe redirige vers easyfacture.mondher.ch/payment/success
    ↓
12. Webhook active la licence en arrière-plan
    ↓
13. Utilisateur relance l'app → Licence détectée
```

---

## 🧪 Tests

### Test 1: Interface utilisateur

1. Lancer l'application
```bash
python run.py
```

2. Aller dans **Paramètres**

3. Vérifier que la section "Licence Easy Facture" s'affiche

4. Cliquer sur "Obtenir la licence"

5. Vérifier que le modal s'ouvre

**Attendu:**
- Section licence visible
- Modal fonctionnel
- Email pré-rempli si configuré

### Test 2: Validation email

1. Dans le modal, laisser l'email vide

2. Cliquer "Procéder au paiement"

**Attendu:**
- Message d'erreur: "Veuillez entrer une adresse email valide"
- Modal reste ouvert

### Test 3: Appel API (backend requis)

**Prérequis:**
- License-server déployé et configuré
- Clés Stripe test configurées

1. Entrer un email valide: `test@mondher.ch`

2. Cliquer "Procéder au paiement"

**Attendu:**
- Bouton affiche "Redirection..."
- Navigateur s'ouvre sur Stripe Checkout
- URL commence par `https://checkout.stripe.com/`

### Test 4: Flux complet (E2E)

1. Dans le modal, entrer `test@mondher.ch`

2. Cliquer "Procéder au paiement"

3. Sur Stripe Checkout, utiliser carte de test:
   - Numéro: `4242 4242 4242 4242`
   - Date: n'importe quelle date future
   - CVC: n'importe quel 3 chiffres

4. Compléter le paiement

**Attendu:**
- Redirection vers `easyfacture.mondher.ch/payment/success`
- Message de confirmation
- Webhook appelé (vérifier logs backend)
- Licence activée en BDD
- Relancer l'app → Détection licence lifetime

---

## 🔧 Configuration requise

### Variables d'environnement

Aucune variable spécifique côté frontend.
L'URL de l'API est codée en dur dans `payment.py`:

```python
api_url = "https://api.easyfacture.mondher.ch"
```

**Pour tester en local**, modifier temporairement:
```python
api_url = "http://localhost:8000"  # License-server local
```

### Dépendances Python

Aucune nouvelle dépendance.
Utilise `requests` (déjà présent).

---

## 📱 Interface utilisateur

### Section Licence

**Emplacement:** Paramètres (après le formulaire SMTP)

**Design:**
- Card avec header bleu
- 2 colonnes:
  - Gauche: Description (4 avantages)
  - Droite: Prix + Bouton
- Bouton vert "Obtenir la licence"

### Modal d'achat

**Éléments:**
- Header bleu avec icône
- Alerte info (redirection Stripe)
- Champ email requis
- Alerte succès (prix 199€)
- Zone d'erreur (masquée par défaut)
- 2 boutons: Annuler / Procéder

**États du bouton:**
- Normal: "🔒 Procéder au paiement"
- Chargement: "⏳ Redirection..."
- Erreur: Retour à normal

---

## 🐛 Gestion des erreurs

### Erreurs frontend

| Cas | Message | Action |
|-----|---------|--------|
| Email vide | "Veuillez entrer une adresse email valide" | Modal reste ouvert |
| Email invalide | "Veuillez entrer une adresse email valide" | Modal reste ouvert |
| Erreur réseau | "Erreur réseau: [détail]" | Modal reste ouvert |

### Erreurs backend

| Cas | Message | HTTP |
|-----|---------|------|
| Machine déjà avec licence | "Cette machine possède déjà une licence lifetime active" | 400 |
| Rate limit dépassé | "Trop de tentatives..." | 429 |
| Config Stripe manquante | "Configuration Stripe manquante..." | 500 |
| Erreur Stripe API | "Erreur Stripe: [détail]" | 500 |

---

## 💡 Améliorations futures

### Phase 2 (optionnel)

- [ ] **Badge de statut** : Afficher "Trial" ou "Lifetime" dans le header
- [ ] **Countdown trial** : "Il vous reste X jours"
- [ ] **Multi-devises** : Sélecteur EUR/USD/CHF
- [ ] **Page dédiée** : `/license` au lieu de Paramètres
- [ ] **Historique achats** : Afficher date d'achat et montant

### Phase 3 (futur)

- [ ] **Transfert licence** : Bouton pour changer de machine
- [ ] **Invoice download** : Télécharger facture Stripe
- [ ] **Upgrade reminder** : Popup au démarrage si trial proche expiration

---

## 📝 Code snippets

### Appel manuel depuis Python

```python
from app.utils.payment import payment_manager
from app.utils.license import LicenseManager

# Récupérer machine_id
license_mgr = LicenseManager()
machine_id = license_mgr.get_machine_id()

# Initier l'achat
success, message, url = payment_manager.purchase_lifetime_license(
    email="test@example.com",
    machine_id=machine_id,
    currency="eur"
)

if success:
    print(f"Checkout URL: {url}")
else:
    print(f"Erreur: {message}")
```

### Test AJAX avec curl

```bash
# Simuler la requête du frontend
curl -X POST http://localhost:5000/parametres/purchase-license \
  -H "Content-Type: application/json" \
  -d '{"email":"test@mondher.ch"}'
```

**Réponse attendue:**
```json
{
  "success": true,
  "message": "Redirection vers Stripe...",
  "checkout_url": "https://checkout.stripe.com/c/pay/cs_test_..."
}
```

---

## 🔗 Liens utiles

- **Stripe Checkout Docs**: https://stripe.com/docs/payments/checkout
- **Bootstrap 5 Modals**: https://getbootstrap.com/docs/5.0/components/modal/
- **Flask AJAX**: https://flask.palletsprojects.com/en/2.3.x/patterns/jquery/

---

## ✅ Checklist d'implémentation

- [x] Créer `app/utils/payment.py`
- [x] Ajouter route `/parametres/purchase-license`
- [x] Modifier template `parametres/index.html`
- [x] Ajouter section Licence
- [x] Créer modal Bootstrap
- [x] Implémenter JavaScript AJAX
- [x] Gestion des erreurs
- [x] Documentation

---

**Prochaines étapes:**
1. Tester l'interface en local
2. Déployer le backend (license-server)
3. Configurer Stripe en mode test
4. Test E2E complet
5. Passage en production

---

**Créé le:** 2026-01-03
**Auteur:** Claude & Mondher
