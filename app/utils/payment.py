#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de gestion des paiements Stripe pour licences lifetime
"""

import requests
import webbrowser
from typing import Tuple, Optional


class PaymentManager:
    """Gestionnaire des paiements Stripe pour Easy Facture"""

    def __init__(self, api_url: str = "https://api.easyfacture.mondher.ch"):
        """
        Initialise le gestionnaire de paiements

        Args:
            api_url: URL de l'API license-server (par défaut: production)
        """
        self.api_url = api_url.rstrip('/')

    def purchase_lifetime_license(
        self,
        email: str,
        machine_id: str,
        currency: str = 'eur'
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Démarre le processus d'achat d'une licence lifetime

        Args:
            email: Email de l'utilisateur
            machine_id: ID unique de la machine
            currency: Devise (eur, usd, chf, gbp)

        Returns:
            Tuple[bool, str, Optional[str]]: (succès, message, checkout_url)

        Raises:
            Exception: Si erreur lors de la création de la session
        """

        # Valider l'email
        if not email or '@' not in email:
            return False, "Adresse email invalide", None

        # Valider le machine_id
        if not machine_id or len(machine_id) < 32:
            return False, "Machine ID invalide", None

        # Préparer la requête
        payload = {
            "machine_id": machine_id,
            "email": email,
            "currency": currency.lower()
        }

        try:
            # Appeler l'API pour créer la session Stripe Checkout
            response = requests.post(
                f"{self.api_url}/api/create-checkout-session",
                json=payload,
                timeout=10
            )

            # Vérifier le statut de la réponse
            if response.status_code == 200:
                data = response.json()

                if data.get('success'):
                    checkout_url = data.get('checkout_url')

                    if checkout_url:
                        # Ouvrir le navigateur sur la page de paiement Stripe
                        webbrowser.open(checkout_url)
                        return True, "Redirection vers Stripe...", checkout_url
                    else:
                        return False, "URL de paiement manquante", None
                else:
                    return False, "Erreur lors de la création de la session", None

            elif response.status_code == 400:
                # Erreur client (machine déjà avec licence, etc.)
                error_detail = response.json().get('detail', 'Erreur inconnue')
                return False, error_detail, None

            elif response.status_code == 429:
                # Rate limit dépassé
                return False, "Trop de tentatives. Veuillez réessayer dans 1 heure.", None

            else:
                # Autre erreur serveur
                return False, f"Erreur serveur (code {response.status_code})", None

        except requests.exceptions.Timeout:
            return False, "Délai d'attente dépassé. Vérifiez votre connexion internet.", None

        except requests.exceptions.ConnectionError:
            return False, "Impossible de se connecter au serveur de licences.", None

        except requests.exceptions.RequestException as e:
            return False, f"Erreur réseau: {str(e)}", None

        except Exception as e:
            return False, f"Erreur inattendue: {str(e)}", None

    def open_checkout_url(self, checkout_url: str) -> bool:
        """
        Ouvre l'URL de checkout dans le navigateur

        Args:
            checkout_url: URL de la page Stripe Checkout

        Returns:
            bool: True si succès, False sinon
        """
        try:
            webbrowser.open(checkout_url)
            return True
        except Exception:
            return False


# Instance globale pour faciliter l'utilisation
payment_manager = PaymentManager()
