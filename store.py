import product

class Store:

    def __init__(self, product_list):
        self.basket = []
        self.products_in_store = []
        self.product_list = product_list
        for product in product_list:
            self.add_product(product)

    def add_product(self, product):
        self.products_in_store.append(product)

    def remove_product(self, product):
        self.products_in_store.remove(product)

    def get_all_products(self):
        return [
            product
            for product in self.products_in_store
            if product.is_active()
        ]

    def show_all_products(self):
        for index, product in enumerate(self.get_all_products(), start=1):
            print(
                f"{index}. {product.name} | "
                f"Price: {product.price:.2f} | "
                f"Quantity: {product.quantity}"
            )

    def order(self, shopping_list):
        total_price = 0.0
        for product, amount in shopping_list:
            total_price += product.buy(amount)
        return total_price

    def create_basket(self, shopping_list):
        for product, amount in shopping_list:
            self.basket.append({
                "product": product,
                "name": product.name,
                "amount": amount,
                "total_price": product.price * amount,
            })

        return self.basket

    def clear_order(self):
        for item in self.basket:
            product = item["product"]
            product.set_quantity(product.quantity + item["amount"])

        self.basket.clear()

    def clear_basket(self):
        self.basket = []

    def show_basket(self):
        for index, item in enumerate(self.basket, start=1):
            print(
                f'{index}. {item["name"]} | '
                f'Menge: {item["amount"]} | '
                f'Total: {item["total_price"]:.2f} €'
            )

    def get_total_quantity(self):
        total_quantity = 0
        for product in self.products_in_store:
            total_quantity += product.quantity
        return total_quantity

def main():

    product_list = [product.Product("MacBook Air M2", price=1450, quantity=100),
                    product.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    product.Product("Google Pixel 7", price=500, quantity=250),
                    ]

    best_buy = Store(product_list)
    available_products = best_buy.get_all_products()

    print(f"Produkte insgesamt: {best_buy.get_total_quantity()}")

    shopping_list = [(available_products[0], 1), (available_products[1], 2)]
    print(f"Total: {best_buy.order(shopping_list)}")
    print(f"Basket: {best_buy.create_basket(shopping_list)}")

    print(f"Restbestand: {best_buy.get_total_quantity()}")

if __name__ == "__main__":
    main()