"""Services qui interrogent les API publiques (ipify et ipinfo.io)."""
from .api_client import ApiClient
from .exceptions import ApiError, IPNotAvailableError
from .models import IPAddressInfo


class PublicIPService(ApiClient):
    """Récupère l'adresse IP publique (IPv4 ou IPv6) via ipify."""

    def __init__(self):
        super().__init__("https://api.ipify.org")

    def get_ipv4(self):
        data = self._get_json(params={"format": "json"})
        return data["ip"]

    def get_ipv6(self):
        # api6.ipify.org ne répond que si la machine a une connectivité IPv6
        client = ApiClient("https://api6.ipify.org")
        try:
            return client._get_json(params={"format": "json"})["ip"]
        except ApiError as err:
            raise IPNotAvailableError("Pas d'IPv6 public détecté.") from err
        finally:
            self.last_url = client.last_url
            self.last_elapsed = client.last_elapsed


class GeoLocationService(ApiClient):
    """Enrichit une adresse avec ville, pays, opérateur (ipinfo.io)."""

    def __init__(self):
        super().__init__("https://ipinfo.io")

    def get_info(self, address):
        data = self._get_json(path=f"/{address}/json")
        return IPAddressInfo(
            address,
            city=data.get("city"),       # .get() gère les clés absentes
            region=data.get("region"),   # (leçon de l'étape 9 du lab)
            country=data.get("country"),
            org=data.get("org"),
            timezone=data.get("timezone"),
        )
