"""Produkte mit Bestand, Mengenlimit und optionaler Rabattaktion."""

class Product:

    """Ein Produkt mit Preis, Lagerbestand und optionaler Rabattaktion."""
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = quantity > 0
        self.promotion = None

    @property
    def price(self) -> float:
        """Gibt den Produktpreis zurück."""
        return self._price

    @price.setter
    def price(self, value: float):
        """Setzt den Produktpreis."""
        if value < 0:
            raise ValueError("Der Preis darf nicht negativ sein.")
        self._price = value

    def get_quantity(self) -> int:
        """Gibt den Lagerbestand zurück."""
        return self.quantity

    def get_price(self) -> float:
        """Gibt den Stückpreis zurück."""
        return self.price

    def set_quantity(self, quantity: int):
        """Aktualisiert den Lagerbestand."""
        if quantity < 0:
            raise ValueError("Der Bestand darf nicht negativ sein.")

        self.quantity = quantity
        self.active = quantity > 0

    def is_active(self) -> bool:
        """Meldet, ob das Produkt angeboten wird."""
        return self.active

    def deactivate(self):
        """Deaktiviert ein Produkt."""
        self.active = False

    def set_promotion(self, promotion):
        """Setzt eine Rabattaktion."""
        self.promotion = promotion

    def remove_promotion(self, promotion):
        """Entfernt die Rabattaktion."""
        if self.promotion is promotion:
            self.promotion = None

    def get_total_price(self, quantity: int) -> float:
        """Berechnet den Gesamtpreis inklusive einer Rabattaktion."""
        if self.promotion is not None:
            return self.promotion.apply_promotion(self, quantity)
        return quantity * self.price

    def buy(self, quantity: int) -> float:
        """Prüft die Kaufmenge und berechnet den Preis."""
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError(
                "Die Kaufmenge muss eine positive ganze Zahl sein."
            )

        if not self.active:
            raise ValueError(
                f"Es tut uns leid, aber {self.name} "
                "haben wir nicht mehr im Sortiment."
            )

        if quantity > self.quantity:
            raise ValueError(
                f"Du kannst maximal {self.quantity} "
                f"von {self.name} bestellen."
            )

        price_total = self.get_total_price(quantity)

        self.quantity -= quantity

        if self.quantity == 0:
            self.deactivate()

        return price_total

    def __str__(self) -> str:
        quantity = (
            "Unlimited" if isinstance(self, NonStockedProduct)
            else self.quantity
        )
        limit = (
            f" | Max per order: {self.maximum}"
            if isinstance(self, LimitedProduct) else ""
        )
        promotion = (
            repr(self.promotion) if self.promotion is not None else "None"
        )
        return (
            f"Name: {self.name} | Price: {self.price:.2f} | "
            f"Quantity: {quantity}{limit} | Promotion: {promotion}"
        )

    def __gt__(self, other):
        return self.quantity > other.quantity

    def __lt__(self, other):
        return self.quantity < other.quantity


class NonStockedProduct(Product):

    """Ein unbegrenzt verfügbares Produkt ohne Lagerbestand."""
    def __init__(self, name, price):
        super().__init__(name, price, 0)
        self.active = True

    def set_quantity(self, quantity):
        """Ignoriert Mengenänderungen, da kein Lagerbestand geführt wird."""

    def buy(self, quantity):

        """Prüft die Kaufmenge und berechnet den Preis."""
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError(
                "Die Kaufmenge muss eine positive ganze Zahl sein."
            )

        if not self.active:
            raise ValueError(
                f"Es tut uns leid, aber {self.name} "
                "haben wir nicht mehr im Sortiment."
            )

        return self.get_total_price(quantity)


class LimitedProduct(Product):
    """Ein Lagerprodukt mit Höchstmenge pro Bestellung."""
    def __init__(self, name, price, quantity, maximum=1):
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def buy(self, quantity: int) -> float:
        """Prüft die Kaufmenge und berechnet den Preis."""
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError(
                "Die Kaufmenge muss eine positive ganze Zahl sein."
            )

        if quantity > self.maximum:
            raise ValueError(
                f"Du kannst von '{self.name}' maximal "
                f"{self.maximum} Stück pro Bestellung kaufen!"
            )

        return super().buy(quantity)
