#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test du systeme de licence
A executer AVANT d'integrer dans l'app principale
"""

import sys
import os

# Ajouter le dossier parent au path pour importer app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_import():
    """Test 1: Import du module"""
    print("="*60)
    print("TEST 1: Import du module de licence")
    print("="*60)
    
    try:
        from app.utils.license import LicenseManager, generate_secret_key
        print("OK Import reussi\n")
        return True
    except ImportError as e:
        print(f"ERREUR import: {e}")
        print("   Verifiez que app/utils/__init__.py existe\n")
        return False
    except Exception as e:
        print(f"ERREUR: {e}\n")
        return False


def test_dependencies():
    """Test 2: Dependencies"""
    print("="*60)
    print("TEST 2: Verification des dependances")
    print("="*60)
    
    try:
        import cryptography
        print(f"OK cryptography installe (version {cryptography.__version__})\n")
        return True
    except ImportError:
        print("ERREUR cryptography NON installe")
        print("   Installation: pip install cryptography\n")
        return False


def test_secret_key_generation():
    """Test 3: Generation de cle secrete"""
    print("="*60)
    print("TEST 3: Generation de cle secrete")
    print("="*60)
    
    try:
        from app.utils.license import generate_secret_key
        
        key = generate_secret_key()
        if key:
            print(f"OK Cle generee: {key}")
            print("\nIMPORTANT:")
            print("   Copiez cette cle dans app/utils/license.py")
            print("   Remplacez SECRET_KEY par cette valeur\n")
            return True, key
        else:
            print("ERREUR Echec generation\n")
            return False, None
    except Exception as e:
        print(f"ERREUR: {e}\n")
        return False, None


def test_machine_id():
    """Test 4: Machine ID"""
    print("="*60)
    print("TEST 4: Generation Machine ID")
    print("="*60)
    
    try:
        from app.utils.license import LicenseManager
        
        manager = LicenseManager()
        machine_id = manager.get_machine_id()
        
        print(f"OK Machine ID: {machine_id}")
        print(f"   Longueur: {len(machine_id)} caracteres")
        print(f"   Fichier licence: {manager.license_file}\n")
        return True, manager
    except Exception as e:
        print(f"ERREUR: {e}\n")
        return False, None


def test_license_generation(manager):
    """Test 5: Generation de licence"""
    print("="*60)
    print("TEST 5: Generation d'une licence de test")
    print("="*60)
    
    try:
        license_key = manager.generate_license("test@example.com", days=30)
        print(f"OK Licence generee:")
        print(f"   {license_key[:60]}...")
        print(f"   Longueur: {len(license_key)} caracteres\n")
        return True, license_key
    except Exception as e:
        print(f"ERREUR: {e}\n")
        return False, None


def test_license_save_load(manager, license_key):
    """Test 6: Sauvegarde et chargement"""
    print("="*60)
    print("TEST 6: Sauvegarde et chargement de licence")
    print("="*60)
    
    try:
        if manager.save_license(license_key):
            print("OK Licence sauvegardee")
        else:
            print("ERREUR Echec sauvegarde")
            return False
        
        loaded = manager.load_license()
        if loaded:
            print(f"OK Licence chargee")
            print(f"   Match: {loaded == license_key}")
        else:
            print("ERREUR Echec chargement")
            return False
        
        print()
        return True
    except Exception as e:
        print(f"ERREUR: {e}\n")
        return False


def test_license_validation(manager):
    """Test 7: Validation"""
    print("="*60)
    print("TEST 7: Validation de la licence")
    print("="*60)
    
    try:
        valid, message = manager.validate_license()
        
        if valid:
            print(f"OK Licence VALIDE")
            print(f"   Message: {message}\n")
        else:
            print(f"ERREUR Licence INVALIDE")
            print(f"   Message: {message}\n")
        
        return valid
    except Exception as e:
        print(f"ERREUR: {e}\n")
        return False


def test_cleanup(manager):
    """Test 8: Nettoyage"""
    print("="*60)
    print("TEST 8: Nettoyage des fichiers de test")
    print("="*60)
    
    try:
        if manager.delete_license():
            print("OK Fichier de test supprime\n")
        else:
            print("ATTENTION Impossible de supprimer\n")
    except Exception as e:
        print(f"ATTENTION Erreur nettoyage: {e}\n")


def main():
    """Execute tous les tests"""
    print("\n" + "="*60)
    print("  SUITE DE TESTS - SYSTEME DE LICENCE")
    print("  Facturation Pro v1.6")
    print("="*60 + "\n")
    
    results = []
    
    # Test 1
    if not test_import():
        print("\nECHEC CRITIQUE: Import impossible")
        return
    results.append(True)
    
    # Test 2
    if not test_dependencies():
        print("\nECHEC CRITIQUE: pip install cryptography")
        return
    results.append(True)
    
    # Test 3
    success, secret_key = test_secret_key_generation()
    results.append(success)
    if not success:
        return
    
    # Test 4
    success, manager = test_machine_id()
    results.append(success)
    if not success or not manager:
        return
    
    # Test 5
    success, license_key = test_license_generation(manager)
    results.append(success)
    if not success or not license_key:
        return
    
    # Test 6
    success = test_license_save_load(manager, license_key)
    results.append(success)
    if not success:
        return
    
    # Test 7
    success = test_license_validation(manager)
    results.append(success)
    
    # Test 8
    test_cleanup(manager)
    
    # Resume
    print("="*60)
    print("  RESUME DES TESTS")
    print("="*60)
    total = len(results)
    passed = sum(results)
    print(f"Tests reussis: {passed}/{total}")
    
    if passed == total:
        print("\nOK TOUS LES TESTS PASSES!")
        print("\nPROCHAINES ETAPES:")
        print("   1. Copier la cle dans app/utils/license.py")
        print("   2. Tester: python run.py")
        print("   3. Builder si OK")
    else:
        print(f"\nATTENTION {total - passed} echec(s)")
    
    print("="*60 + "\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrompu")
    except Exception as e:
        print(f"\nERREUR: {e}")
        import traceback
        traceback.print_exc()