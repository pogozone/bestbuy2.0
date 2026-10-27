
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
            print(f"{index}. {product}")

    def order(self, shopping_list):

        # Warenkorb auslesen
        existing_items = [(item["product"], item["amount"]) for item in self.basket]

        # Warenkorb und neue shopping_list kombinieren und Mengen für gleiche Produkte addieren
        combined_list = existing_items + shopping_list
        amounts = {}
        for product, amount in combined_list:
            amounts[product] = amounts.get(product, 0) + amount

        # Warenkorb leeren
        self.basket.clear()

        # Warenkorb füllen
        entries = []
        for product, amount in amounts.items():
            total = product.buy(amount)
            entries.append({
                "product": product,
                "name": product.name,
                "amount": amount,
                "total_price": total,
            })

        self.basket.extend(entries)
        return sum(item["total_price"] for item in entries)


    def clear_order(self):
        for item in self.basket:
            product = item["product"]
            product.set_quantity(product.quantity + item["amount"])

        self.basket.clear()

    def show_basket(self):
        for index, product in enumerate(self.basket, start=1):
            print(
                f'{index}. {product["name"]} | '
                f'Menge: {product["amount"]} | '
                f'Total: {product["total_price"]:.2f} €'
            )

    def get_total_quantity(self):
        total_quantity = 0
        for product in self.products_in_store:
            total_quantity += product.quantity
        return total_quantity

