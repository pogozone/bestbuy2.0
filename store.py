import product

class Store:

    def __init__(self, product_list):
        self.basket = []
        self.products_in_store = []
        self.product_list = product_list
        for this_product in product_list:
            self.add_product(this_product)

    def add_product(self, this_product):
        self.products_in_store.append(this_product)

    def remove_product(self, this_product):
        self.products_in_store.remove(this_product)

    def get_all_products(self):
        return [
            product
            for product in self.products_in_store
                if product.is_active()
        ]

    def show_all_products(self):
        for index, this_product in enumerate(self.get_all_products(), start=1):
            print(
                f"{index}. {this_product.name} | "
                f"Price: {this_product.price:.2f} | "
                f"Quantity: {this_product.quantity}"
            )

    @staticmethod
    def order(shopping_list):
        total_price = 0.0
        for this_product, amount in shopping_list:
            total_price += this_product.buy(amount)
        return total_price

    def create_basket(self, shopping_list):
        for this_product, amount in shopping_list:
            self.basket.append({
                "product": this_product,
                "name": this_product.name,
                "amount": amount,
                "total_price": this_product.price * amount,
            })

        return self.basket

    def clear_order(self):
        for item in self.basket:
            this_product = item["product"]
            this_product.set_quantity(this_product.quantity + item["amount"])

        self.basket.clear()

    def clear_basket(self):
        self.basket = []

    def show_basket(self):
        for index, this_product in enumerate(self.basket, start=1):
            print(
                f'{index}. {this_product["name"]} | '
                f'Menge: {this_product["amount"]} | '
                f'Total: {this_product["total_price"]:.2f} €'
            )

    def get_total_quantity(self):
        total_quantity = 0
        for this_product in self.products_in_store:
            total_quantity += this_product.quantity
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

    # setup initial stock of inventory
    product_list = [product.Product("MacBook Air M2", price=1450, quantity=100),
                    product.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    product.Product("Google Pixel 7", price=500, quantity=250),
                    product.NonStockedProduct("Windows License", price=125),
                    product.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
                    ]
    best_buy = Store(product_list)

if __name__ == "__main__":
    main()