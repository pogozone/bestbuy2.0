class Product:

    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = quantity > 0

    def get_quantity(self) -> int:
        return self.quantity

    def set_quantity(self, quantity: int):
        if quantity < 0:
            raise ValueError("Der Bestand darf nicht negativ sein.")

        self.quantity = quantity
        self.active = quantity > 0

    def is_active(self) -> bool:
        return self.active

    def deactivate(self):
        self.active = False

    def buy(self, quantity: int) -> float:
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


class NonStockedProduct(Product):

    def __init__(self, name, price):
        super().__init__(name, price, 0)
        self.active = True

    def set_quantity(self, quantity):
        pass

    def buy(self, quantity):

        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Die Kaufmenge muss eine positive ganze Zahl sein.")


        if not self.active:
            raise ValueError(
                f"{self.__class__.__name__}: Es tut uns leid, aber {self.name} haben wir nicht mehr im Sortiment."
            )

        return quantity * self.price

    def __str__(self) -> str:
        return f"Name: {self.name} Price {self.price} Quantity {self.quantity}"

class LimitedProduct(Product):
    def __init__(self, name, price, quantity, maximum=1):
        super().__init__(name, price, quantity)
        self.maximum = maximum
        self.active = True

    def buy(self, quantity: int) -> float:
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Die Kaufmenge muss eine positive ganze Zahl sein.")

        if quantity > self.maximum:
            raise ValueError(
                f"Du kannst von '{self.name}' maximal {self.maximum} Stück pro Bestellung kaufen!"
            )

        return quantity * self.price

    def __str__(self) -> str:
        return f"Name: {self.name} Price {self.price} Quantity {self.quantity}"

def main():




    testtomate1 = NonStockedProduct("Testtomate", 100)
    print(testtomate1)
    testtomate1.buy(100)
    print(testtomate1)
#    testtomate2 = LimitedProduct("Testtomate", 100, 50)

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
#    bose.buy(50000000)
#    bose.show()
#    print(bose)

    # Gültige Bestellung, neuer Lagerbestand wird angezeigt
    bose.buy(5)
#    bose.show()
    print(bose)

if __name__ == "__main__":
    main()