"""Produktverwaltung und Warenkorb."""

from product import LimitedProduct, NonStockedProduct


class Store:

    """Verwaltet das Sortiment und den Warenkorb."""
    def __init__(self, product_list):
        self.basket = []
        self.products_in_store = []
        self.product_list = product_list
        for product in product_list:
            self.add_product(product)

    def add_product(self, product):
        """Fügt ein Produkt zum Sortiment hinzu."""
        self.products_in_store.append(product)

    def remove_product(self, product):
        """Entfernt ein Produkt aus dem Sortiment."""
        self.products_in_store.remove(product)

    def get_all_products(self):
        """Gibt alle Produkte zurück."""
        return [
            product
            for product in self.products_in_store
            if product.is_active()
        ]

    def show_all_products(self):
        """Listet die Produkte auf."""
        for index, product in enumerate(self.get_all_products(), start=1):
            print(f"{index}. {product}")

    def order(self, shopping_list):
        # Nur die neu hinzugefügten Mengen zusammenfassen.
        """Fügt Produkte zum Warenkorb hinzu."""
        additions = {}
        for product, amount in shopping_list:
            if product not in self.products_in_store:
                raise ValueError("Dieses Produkt gehört nicht zum Store.")
            if not isinstance(amount, int) or amount <= 0:
                raise ValueError("Bitte eine positive ganze Menge angeben.")
            additions[product] = additions.get(product, 0) + amount

        amounts = {
            item["product"]: item["amount"] for item in self.basket
        }

        # Alles prüfen, bevor Bestand oder Warenkorb verändert werden.
        for product, amount in additions.items():
            if not product.is_active():
                raise ValueError(f"{product.name} ist nicht mehr verfügbar.")
            if (
                not isinstance(product, NonStockedProduct)
                and amount > product.quantity
            ):
                raise ValueError(
                    f"Von {product.name} sind noch "
                    f"{product.quantity} Stück verfügbar."
                )
            combined_amount = amounts.get(product, 0) + amount
            if (
                isinstance(product, LimitedProduct)
                and combined_amount > product.maximum
            ):
                raise ValueError(
                    f"Von {product.name} sind maximal "
                    f"{product.maximum} Stück pro Bestellung erlaubt."
                )
            amounts[product] = combined_amount

        # Rabatt anhand der gesamten Menge im Warenkorb berechnen.
        entries = []
        for product, amount in amounts.items():
            entries.append({
                "product": product,
                "name": product.name,
                "amount": amount,
                "total_price": product.get_total_price(amount),
            })

        # Nur neue Mengen abbuchen, niemals den alten Warenkorb erneut.
        for product, amount in additions.items():
            if not isinstance(product, NonStockedProduct):
                product.set_quantity(product.quantity - amount)

        self.basket = entries
        return sum(item["total_price"] for item in self.basket)

    def clear_order(self):
        """Leert den Warenkorb und fügt die Waren dem Bestand wieder hinzu."""
        for item in self.basket:
            product = item["product"]
            product.set_quantity(product.quantity + item["amount"])

        self.basket.clear()

    def show_basket(self):
        """Zeigt Mengen und Gesamtpreise im Warenkorb."""
        for index, product in enumerate(self.basket, start=1):
            print(
                f'{index}. {product["name"]} | '
                f'Menge: {product["amount"]} | '
                f'Total: {product["total_price"]:.2f} €'
            )

    def get_total_quantity(self):
        """Summiert den vorhandenen Lagerbestand."""
        total_quantity = 0
        for product in self.products_in_store:
            total_quantity += product.quantity
        return total_quantity

    def __contains__(self, product) -> bool:
        return product in self.products_in_store
