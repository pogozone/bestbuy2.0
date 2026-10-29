"""Rabattaktionen"""

from abc import ABC, abstractmethod


class Promotion(ABC):
    """Schnittstelle für Rabattaktionen."""
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity: int):
        """Berechnet den Aktionspreis für die angegebene Menge."""
        raise NotImplementedError

    def __repr__(self) -> str:
        return self.name


class SecondHalfPrice(Promotion):
    """Berechnet jedes zweite Stück zum halben Preis."""
    def apply_promotion(self, product, quantity: int):

        # Beispiel-Logik: Jedes zweite Produkt zum halben Preis
        """Berechnet den Aktionspreis für die angegebene Menge."""
        normal_price = product.price * quantity

        if quantity < 2:
            return normal_price

        # Wie viele Paare bekommen 50% Rabatt auf das zweite Stück?
        pairs = quantity // 2
        discount = pairs * (product.price * 0.5)

        return normal_price - discount

    def __repr__(self) -> str:
        return "SecondHalfPrice"


class ThirdOneFree(Promotion):

    """Berechnet jedes dritte Stück kostenlos."""
    def apply_promotion(self, product, quantity: int):
        """Berechnet den Aktionspreis für die angegebene Menge."""
        return (quantity - quantity // 3) * product.price

    def __repr__(self) -> str:
        return "ThirdOneFree"


class PercentDiscount(Promotion):
    """Reduziert den Gesamtpreis um einen festen Prozentsatz."""
    def __init__(self, name, percent):
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity: int):
        """Berechnet den Aktionspreis für die angegebene Menge."""
        price = product.price * quantity
        return price * (1 - self.percent / 100)

    def __repr__(self) -> str:
        return f"PercentDiscount ({self.percent}%)"
