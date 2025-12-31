#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Client API pour les licences trial (essai gratuit)
Communique avec le License Server pour obtenir automatiquement des licences d'essai
"""

import requests
from pathlib import Path
from datetime import datetime, timedelta
from typing import Tuple


# Configuration API
# API_BASE_URL = "https://api.mondher.ch/api/v1"  # Production
API_BASE_URL = "http://127.0.0.1:8000/api/v1"  # Développement local

REQUEST_TIMEOUT = 10  # secondes


class TrialAPIClient:
    """Client pour communiquer avec le License Server"""

    def __init__(self):
        self.api_url = API_BASE_URL

    def request_trial_license(
        self,
        email: str,
        machine_id: str,
        customer_name: str = None,
        company_name: str = None
    ) -> Tuple[bool, str, str]:
        """
        Demande une licence d'essai au serveur

        Args:
            email: Email du client
            machine_id: Identifiant unique de la machine
            customer_name: Nom du client (optionnel)
            company_name: Nom de l'entreprise (optionnel)

        Returns:
            tuple: (success, message, license_key)
                - success: True si licence obtenue
                - message: Message de succès ou d'erreur
                - license_key: Clé de licence (None si échec)
        """
        try:
            # Préparer la requête
            payload = {
                "email": email,
                "machine_id": machine_id,
                "customer_name": customer_name,
                "company_name": company_name
            }

            # Appeler l'API
            response = requests.post(
                f"{self.api_url}/licenses/trial",
                json=payload,
                timeout=REQUEST_TIMEOUT
            )

            # Analyser la réponse
            if response.status_code == 200:
                data = response.json()
                license_key = data.get("license_key")
                message = data.get("message", "Licence d'essai obtenue avec succès")

                return True, message, license_key

            elif response.status_code == 400:
                # Erreur client (déjà une trial, etc.)
                data = response.json()
                error_msg = data.get("detail", "Une erreur est survenue")
                return False, error_msg, None

            elif response.status_code == 429:
                # Rate limit dépassé
                return False, "Trop de requêtes. Veuillez réessayer dans 1 heure.", None

            else:
                # Autre erreur serveur
                return False, f"Erreur serveur ({response.status_code})", None

        except requests.exceptions.Timeout:
            return False, "Délai d'attente dépassé. Vérifiez votre connexion internet.", None

        except requests.exceptions.ConnectionError:
            return False, "Impossible de se connecter au serveur. Vérifiez votre connexion internet.", None

        except requests.exceptions.RequestException as e:
            return False, f"Erreur de connexion: {str(e)}", None

        except Exception as e:
            return False, f"Erreur inattendue: {str(e)}", None

    def validate_license_online(
        self,
        license_key: str,
        machine_id: str
    ) -> Tuple[bool, str, dict]:
        """
        Valide une licence auprès du serveur

        Args:
            license_key: Clé de licence à valider
            machine_id: Identifiant de la machine

        Returns:
            tuple: (is_valid, message, data)
                - is_valid: True si licence valide
                - message: Message de validation
                - data: Données de la licence (None si invalide)
        """
        try:
            # Appeler l'API
            response = requests.post(
                f"{self.api_url}/licenses/validate",
                json={
                    "license_key": license_key,
                    "machine_id": machine_id
                },
                timeout=REQUEST_TIMEOUT
            )

            if response.status_code == 200:
                data = response.json()
                is_valid = data.get("valid", False)
                message = data.get("message", "")

                if is_valid:
                    return True, message, data
                else:
                    return False, message, None

            else:
                return False, f"Erreur serveur ({response.status_code})", None

        except requests.exceptions.RequestException:
            # En cas d'erreur réseau, on ne peut pas valider en ligne
            # L'appelant doit utiliser la validation locale
            return None, "Validation en ligne impossible (pas de connexion)", None

        except Exception as e:
            return None, f"Erreur: {str(e)}", None

    def should_check_online(self, last_check_file: Path) -> bool:
        """
        Détermine si on doit vérifier en ligne (une fois par jour)

        Args:
            last_check_file: Fichier contenant le timestamp du dernier check

        Returns:
            bool: True si on doit vérifier
        """
        if not last_check_file.exists():
            return True

        try:
            last_check = datetime.fromtimestamp(last_check_file.stat().st_mtime)
            time_since_check = datetime.now() - last_check

            # Vérifier si plus de 24h depuis le dernier check
            return time_since_check > timedelta(days=1)

        except Exception:
            return True

    def mark_checked(self, last_check_file: Path):
        """
        Marque qu'on a vérifié en ligne maintenant

        Args:
            last_check_file: Fichier à mettre à jour
        """
        try:
            last_check_file.parent.mkdir(parents=True, exist_ok=True)
            last_check_file.touch()
        except Exception:
            pass  # Pas critique si ça échoue


# Instance globale
trial_client = TrialAPIClient()
