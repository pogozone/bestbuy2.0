class Product:
    quantity = 0
    active = True

    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def get_quantity(self):
        return self.quantity

    def set_quantity(self, quantity):
        if quantity < 0:
            raise ValueError("Der Bestand darf nicht negativ sein.")

        self.quantity = quantity
        self.active = quantity > 0

    def is_active(self):
        return self.active

    def deactivate(self):
        self.active = False

#    def show(self):
#        print("Name:", self.name, "Price", self.price, "Quantity", self.quantity)

    def buy(self, quantity) -> float:
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Die Kaufmenge muss eine positive ganze Zahl sein.")

        if not self.active:
            raise ValueError(
                f"Es tut uns leid, aber {self.name} haben wir nicht mehr im Sortiment."
            )

        if quantity > self.quantity:
            raise ValueError(
                f"Der Lagerbestand gibt das nicht her! Du kannst maximal {self.quantity} von {self.name} bestellen."
            )

        price_total = quantity * self.price
        self.quantity -= quantity

        if self.quantity == 0:
            self.deactivate()

        return price_total

    def __str__(self) -> str:
        return f"Name: {self.name} Price {self.price} Quantity {self.quantity}"

def main():
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)

    print(bose.buy(50))
    print(mac.buy(100))
    print(mac.is_active())

    print(bose)
    print(mac)
#    bose.show()
#    mac.show()

    bose.set_quantity(1000)
    print(bose)
#    bose.show()

    # Zu viel bestellt: Warnung und Abbruch
    bose.buy(50000000)
#    bose.show()
    print(bose)

    # Gültige Bestellung, neuer Lagerbestand wird angezeigt
    bose.buy(5)
#    bose.show()
    print(bose)

if __name__ == "__main__":
    main()