#from product import Product

class Promotion:
    def __init__(self, name):
        self.name = name
#        self.promotion_list = []
#        self.promotion_list = []
#
#    def set_promotion(self, name, product_id):
#        self.promotion_list[name].append(product_id)
#
#    def remove_promotion(self, name, product_id):
#        self.promotion_list[name].remove(product_id)
#
#    def get_all_promotions(self):
#        return self.promotion_list
#
#    def apply_promotion(self, product, quantity: int):
#        pass


class SecondHalfPrice(Promotion):
    def __init__(self, name):
        super().__init__(name)

    def apply_promotion(self, product, quantity: int):

        # Beispiel-Logik: Jedes zweite Produkt zum halben Preis
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

    def apply_promotion(self, product, quantity: int):
        return (quantity - quantity // 3) * product.price

    def __repr__(self) -> str:
        return "ThirdOneFree"


class PercentDiscount(Promotion):
    def __init__(self, name, percent):
        super().__init__(name)
        self.name = name
        self.percent = percent

    def apply_promotion(self, product, quantity: int):
        price = product.price * quantity
        return price * (1 - self.percent / 100)

    def __repr__(self) -> str:
        return "PercentDiscount"
