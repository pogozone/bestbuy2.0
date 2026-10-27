from promotion import Promotion


class Product:

    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = quantity > 0
        self.promotion_list = []

    def get_quantity(self) -> int:
        return self.quantity

    def get_price(self) -> float:
        return self.price

    def set_quantity(self, quantity: int):
        if quantity < 0:
            raise ValueError("Der Bestand darf nicht negativ sein.")

        self.quantity = quantity
        self.active = quantity > 0

    def is_active(self) -> bool:
        return self.active

    def deactivate(self):
        self.active = False

    def set_promotion(self, promotion_name):
        self.promotion_list.append(promotion_name)

    def remove_promotion(self, promotion):
        self.promotion_list.remove(promotion)

    def get_total_price(self, quantity: int) -> float:
        # Der Normalpreis
        prices = [quantity * self.price]
        # Die Promotion Preis
        prices.extend(p.apply_promotion(self, quantity) for p in self.promotion_list)
        # Der beste/niedrigste Preis wird ermittelt
        return min(prices)

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

        price_total = self.get_total_price(quantity)

        self.quantity -= quantity

        if self.quantity == 0:
            self.deactivate()

        return price_total

    def __str__(self) -> str:
        return f"Name: {self.name} Price: {self.price} Quantity: {self.quantity} Promotions: {self.promotion_list}"

#    def __str__(self) -> str:
#        promo_names = [type(p).__name__ for p in self.promotion_list]
#        promo_text = f", Promotions: {', '.join(promo_names)}" if promo_names else ""
#        return f"Name: {self.name} Price: {self.price} Quantity: {self.quantity}{promo_text}"

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

        return self.get_total_price(quantity)


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

        return self.get_total_price(quantity)
