"""Classe de base pour appeler une API REST.

Reprend les techniques du lab 4.9.2 :
- urllib.parse.urlencode pour construire l'URL (étape 3)
- requests.get(...) puis .json() et .status_code (étapes 3 et 4)
- affichage du message d'erreur renvoyé par l'API (étape 14)
"""
import urllib.parse

import requests

from .exceptions import ApiError


class ApiClient:
    """Envoie des requêtes GET et vérifie les réponses."""

    def __init__(self, base_url, timeout=5):
        self._base_url = base_url  # attribut protégé (encapsulation)
        self._timeout = timeout
        self.last_url = None       # dernière URL demandée (pour la vérifier dans le navigateur)
        self.last_elapsed = None   # durée de la dernière requête (secondes)

    def _build_url(self, path="", params=None):
        """Construit l'URL complète avec urlencode, comme dans le lab."""
        url = self._base_url + path
        if params:
            url += "?" + urllib.parse.urlencode(params)
        return url

    def _get_json(self, path="", params=None):
        """Appelle l'API et renvoie le JSON sous forme de dict/list Python.

        Lève ApiError si la connexion échoue, si le statut HTTP n'est pas 200
        ou si la réponse n'est pas du JSON valide.
        """
        url = self._build_url(path, params)
        self.last_url = url
        try:
            response = requests.get(url, timeout=self._timeout)
        except requests.exceptions.RequestException as err:
            raise ApiError(f"Connexion impossible à {url} : {err}") from err

        self.last_elapsed = response.elapsed.total_seconds()
        json_status = response.status_code

        if json_status != 200:
            # Message d'erreur de l'API s'il existe (étape 14 du lab)
            message = ""
            try:
                body = response.json()
                if isinstance(body, dict):
                    message = str(body.get("message") or body.get("error") or "")
            except ValueError:
                pass
            raise ApiError(f"Statut HTTP {json_status} pour {url}. {message}".strip())

        try:
            return response.json()
        except ValueError as err:
            raise ApiError("Réponse non JSON") from err
