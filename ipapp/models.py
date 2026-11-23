"""Modèle de données : une adresse IP et ses informations."""
import ipaddress


class IPAddressInfo:
    """Représente une adresse IP (v4 ou v6) et ses informations associées."""

    def __init__(self, address, city=None, region=None,
                 country=None, org=None, timezone=None):
        # ip_address() lève ValueError si l'adresse est invalide
        self.__ip = ipaddress.ip_address(address)  # attribut privé
        self.city = city
        self.region = region
        self.country = country
        self.org = org
        self.timezone = timezone

    @property
    def address(self):
        return str(self.__ip)

    @property
    def version(self):
        """4 ou 6."""
        return self.__ip.version

    @property
    def is_private(self):
        return self.__ip.is_private

    def to_dict(self):
        return {"address": self.address, "version": self.version,
                "city": self.city, "region": self.region,
                "country": self.country, "org": self.org,
                "timezone": self.timezone}

    def __str__(self):
        lines = [f"Adresse IPv{self.version} : {self.address}"]
        for label, value in (("Ville", self.city), ("Région", self.region),
                             ("Pays", self.country), ("Opérateur", self.org),
                             ("Fuseau", self.timezone)):
            if value:
                lines.append(f"  {label} : {value}")
        return "\n".join(lines)
