#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour l'intégration API Trial
Simule le flux utilisateur complet
"""

import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent))

from app.utils.trial_client import trial_client
from app.utils.license import LicenseManager

def test_full_workflow():
    """Test complet du flux trial"""

    print("=" * 70)
    print("TEST D'INTEGRATION - LICENCE TRIAL")
    print("=" * 70)
    print()

    # Simulation d'un nouveau client
    email = "demo@example.com"
    manager = LicenseManager()
    machine_id = manager.get_machine_id()

    print(f"1. Machine ID: {machine_id}")
    print()

    # Étape 1: Demander une licence trial
    print("2. Demande de licence d'essai à l'API...")
    success, message, license_key = trial_client.request_trial_license(
        email=email,
        machine_id=machine_id,
        customer_name="Test User",
        company_name="Demo Company"
    )

    if not success:
        print(f"   ❌ ERREUR: {message}")
        return False

    print(f"   ✅ SUCCES: {message}")
    print(f"   Clé de licence reçue (tronquée): {license_key[:50]}...")
    print()

    # Étape 2: Sauvegarder la licence
    print("3. Sauvegarde de la licence...")
    if manager.save_license(license_key):
        print("   ✅ Licence sauvegardée dans data/license.key")
    else:
        print("   ❌ Échec de la sauvegarde")
        return False
    print()

    # Étape 3: Validation locale
    print("4. Validation LOCALE de la licence...")
    valid_local, msg_local = manager.validate_license()

    if valid_local:
        print(f"   ✅ {msg_local}")
    else:
        print(f"   ❌ {msg_local}")
        return False
    print()

    # Étape 4: Validation API
    print("5. Validation API (en ligne)...")
    valid_api, msg_api, data_api = trial_client.validate_license_online(
        license_key=license_key,
        machine_id=machine_id
    )

    if valid_api:
        print(f"   ✅ {msg_api}")
        print(f"   Type: {data_api.get('license_type')}")
        print(f"   Expire dans: {data_api.get('days_remaining')} jours")
    else:
        print(f"   ❌ {msg_api}")
        return False
    print()

    # Résumé
    print("=" * 70)
    print("RÉSULTAT: TOUS LES TESTS RÉUSSIS ✅")
    print("=" * 70)
    print()
    print("Flux complet validé:")
    print("  1. ✅ Demande de licence trial (API)")
    print("  2. ✅ Sauvegarde de la licence (local)")
    print("  3. ✅ Validation locale (offline)")
    print("  4. ✅ Validation API (online)")
    print()
    print("L'intégration facturation-app ↔ license-server fonctionne parfaitement!")
    print()

    return True


if __name__ == '__main__':
    try:
        success = test_full_workflow()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
