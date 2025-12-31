"""
Système de gestion des licences pour Facturation Pro
Version sécurisée - N'affecte PAS le fonctionnement normal si désactivé
"""

import hashlib
import uuid
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

class LicenseManager:
    """
    Gestionnaire de licences avec protection hardware
    Mode gracieux : l'app fonctionne même si ce module a un problème
    """
    
    # ⚠️ IMPORTANT : Générer votre propre clé avec :
    # python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key())"
    SECRET_KEY = b'QvS9Dy6SjhpVPFf-nsu2NZ-xPfS3-Xaom--vwvdeH6w='
    
    def __init__(self):
        self.license_file = self._get_license_path()
        self._cipher = None
        self._init_cipher()
    
    def _init_cipher(self):
        """Initialise le chiffrement (avec fallback gracieux)"""
        try:
            from cryptography.fernet import Fernet
            self._cipher = Fernet(self.SECRET_KEY)
        except Exception as e:
            print(f"⚠️  Avertissement chiffrement: {e}")
            self._cipher = None
    
    def _get_license_path(self):
        """Détermine le chemin du fichier de licence"""
        try:
            # Essayer APPDATA (Windows)
            if os.getenv('APPDATA'):
                base_path = Path(os.getenv('APPDATA')) / 'FacturationPro'
            # Sinon HOME directory
            else:
                base_path = Path.home() / '.facturationpro'
            
            base_path.mkdir(parents=True, exist_ok=True)
            return base_path / 'license.dat'
            
        except Exception as e:
            # Fallback : dossier courant
            print(f"⚠️  Utilisation dossier courant pour licence: {e}")
            return Path('./license.dat')
    
    def get_machine_id(self):
        """
        Génère un identifiant unique basé sur le hardware
        Méthode robuste avec plusieurs fallbacks
        """
        try:
            import platform
            
            # MAC Address
            mac = uuid.getnode()
            mac_str = f"{mac:012x}"
            
            # Infos système
            system = platform.system()
            machine = platform.machine()
            node = platform.node()
            
            # Combinaison unique
            unique_str = f"{mac_str}-{system}-{machine}-{node}"
            
            # Hash SHA256 (32 caractères)
            return hashlib.sha256(unique_str.encode()).hexdigest()[:32]
            
        except Exception as e:
            print(f"⚠️  Erreur génération Machine ID: {e}")
            # Fallback minimal
            return hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()[:32]
    
    def generate_license(self, customer_email, days=365):
        """
        Génère une clé de licence pour un client
        ⚠️  À utiliser UNIQUEMENT côté administrateur
        
        Args:
            customer_email: Email du client
            days: Durée de validité en jours
        
        Returns:
            str: Clé de licence chiffrée (hex)
        """
        if not self._cipher:
            raise Exception("Chiffrement non initialisé")
        
        machine_id = self.get_machine_id()
        expiry = (datetime.now() + timedelta(days=days)).isoformat()
        
        license_data = {
            'email': customer_email,
            'machine_id': machine_id,
            'expiry': expiry,
            'version': '1.6.0',
            'generated': datetime.now().isoformat()
        }
        
        # Chiffrement
        json_data = json.dumps(license_data)
        encrypted = self._cipher.encrypt(json_data.encode())
        
        return encrypted.hex()
    
    def validate_license(self, license_key=None):
        """
        Valide une clé de licence
        Mode gracieux : retourne False en cas d'erreur, ne plante pas
        
        Args:
            license_key: Clé à valider (ou None pour charger depuis fichier)
        
        Returns:
            tuple: (bool: valide, str: message)
        """
        try:
            # Charger la licence
            if license_key is None:
                license_key = self.load_license()
            
            if not license_key:
                return False, "Aucune licence trouvée"
            
            if not self._cipher:
                return False, "Système de chiffrement non disponible"
            
            # Déchiffrer
            encrypted = bytes.fromhex(license_key)
            decrypted = self._cipher.decrypt(encrypted)
            license_data = json.loads(decrypted.decode())
            
            # Vérifier machine ID
            current_machine_id = self.get_machine_id()
            if license_data.get('machine_id') != current_machine_id:
                return False, "Licence non valide pour cette machine"
            
            # Vérifier expiration
            expiry_str = license_data.get('expiry')
            if expiry_str:
                expiry = datetime.fromisoformat(expiry_str)
                if datetime.now() > expiry:
                    days_expired = (datetime.now() - expiry).days
                    return False, f"Licence expirée depuis {days_expired} jour(s)"
                
                # Jours restants
                days_left = (expiry - datetime.now()).days
                return True, f"Licence valide ({days_left} jours restants)"
            
            return True, "Licence valide"
            
        except Exception as e:
            return False, f"Erreur validation: {str(e)}"
    
    def save_license(self, license_key):
        """
        Sauvegarde une clé de licence
        
        Args:
            license_key: Clé à sauvegarder
        
        Returns:
            bool: Succès
        """
        try:
            with open(self.license_file, 'w') as f:
                f.write(license_key.strip())
            return True
        except Exception as e:
            print(f"❌ Erreur sauvegarde licence: {e}")
            return False
    
    def load_license(self):
        """
        Charge la licence existante
        
        Returns:
            str or None: Clé de licence ou None
        """
        try:
            if self.license_file.exists():
                with open(self.license_file, 'r') as f:
                    content = f.read().strip()
                    return content if content else None
        except Exception as e:
            print(f"⚠️  Impossible de charger la licence: {e}")
        
        return None
    
    def delete_license(self):
        """
        Supprime la licence (désactivation)
        
        Returns:
            bool: Succès
        """
        try:
            if self.license_file.exists():
                self.license_file.unlink()
            return True
        except Exception as e:
            print(f"❌ Erreur suppression licence: {e}")
            return False
    
    def get_license_info(self):
        """
        Récupère les informations de la licence actuelle
        
        Returns:
            dict or None: Informations de licence déchiffrées
        """
        try:
            license_key = self.load_license()
            if not license_key or not self._cipher:
                return None
            
            encrypted = bytes.fromhex(license_key)
            decrypted = self._cipher.decrypt(encrypted)
            return json.loads(decrypted.decode())
            
        except Exception:
            return None


# Fonction utilitaire pour générer une clé secrète
def generate_secret_key():
    """
    Génère une nouvelle clé secrète Fernet
    Utiliser pour créer votre propre SECRET_KEY
    """
    try:
        from cryptography.fernet import Fernet
        return Fernet.generate_key()
    except ImportError:
        print("❌ Module cryptography non installé")
        print("   pip install cryptography")
        return None


# Mode test si exécuté directement
if __name__ == '__main__':
    print("="*60)
    print("  TEST DU SYSTÈME DE LICENCE")
    print("="*60 + "\n")
    
    # 1. Générer une clé secrète
    print("1️⃣  Génération d'une clé secrète:")
    secret = generate_secret_key()
    if secret:
        print(f"   {secret}")
        print("   ⚠️  Copiez cette clé dans SECRET_KEY de ce fichier\n")
    
    # 2. Test du manager
    print("2️⃣  Test du LicenseManager:")
    manager = LicenseManager()
    print(f"   Machine ID: {manager.get_machine_id()}")
    print(f"   Fichier licence: {manager.license_file}\n")
    
    # 3. Génération d'une licence de test
    print("3️⃣  Génération d'une licence de test (30 jours):")
    try:
        test_license = manager.generate_license("test@example.com", days=30)
        print(f"   Licence: {test_license[:50]}...\n")
        
        # 4. Sauvegarde
        print("4️⃣  Sauvegarde de la licence:")
        if manager.save_license(test_license):
            print("   ✅ Licence sauvegardée\n")
        
        # 5. Validation
        print("5️⃣  Validation de la licence:")
        valid, message = manager.validate_license()
        print(f"   Résultat: {valid}")
        print(f"   Message: {message}\n")
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}\n")
    
    print("="*60)
    print("✅ Test terminé")
    print("="*60)
