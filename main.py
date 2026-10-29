"""Erstellt das Sortiment und startet die Anwendung."""

import product
import promotion
import store


def go_ahead(this_store, choice):
    """Verarbeitet eine Menüauswahl und meldet, ob es weitergeht."""
    try:
        choice = int(choice)
    except ValueError:
        print("\nPlease enter a number from 1 to 6.\n")
        return True

    if choice == 1:
        print("\nAll products available:\n")
        this_store.show_all_products()

    elif choice == 2:
        print(f"\nTotal amount in store: {this_store.get_total_quantity()}")

    elif choice == 3:
        make_order(this_store)

    elif choice == 4:
        this_store.show_basket()
        return True
    elif choice == 5:
        this_store.clear_order()
        print("\nOrder cancelled. Stock restored.")
        return True

    elif choice == 6:
        print("\nGoodbye!")
        return False

    else:
        print("\nPlease enter a number from 1 to 6.\n")

    return True


def make_order(this_store):
    """Erlaubt mehrere Artikel und behandelt ungültige Eingaben."""
    while True:
        # Nach jedem Kauf die aktuelle Liste neu laden.
        available_products = this_store.get_all_products()
        if not available_products:
            print("Keine Produkte verfügbar.")
            return

        this_store.show_all_products()

        try:
            number = int(input("\nChoose product: "))
            if not 1 <= number <= len(available_products):
                print("Dieses Produkt gibt es nicht.")
                continue
            amount = int(input("\nAmount to buy: "))
        except ValueError:
            print("Bitte gib eine ganze Zahl ein.")
            continue

        this_product = available_products[number - 1]
        try:
            total = this_store.order([(this_product, amount)])
        except ValueError as error:
            print(f"Bestellung nicht möglich: {error}")
            continue

        print(f"\nTotal: {total:.2f} €\nBasket:")
        this_store.show_basket()

        while True:
            answer = input(
                "\nAdd another item? (y/n): "
            ).strip().lower()
            if answer in ("n", "no", "nein"):
                return
            if answer in ("y", "yes", "j", "ja"):
                break
            print("Bitte y oder n eingeben.")


def start(this_store):
    """Zeigt das Hauptmenü."""
    menu = [
        "List all products in store",
        "Show total amount in store",
        "Add to basket",
        "Show basket",
        "Clear basket",
        "Quit"
    ]
    while True:
        print("\n===== Best Buy =====\n")
        for index, item in enumerate(menu, start=1):
            print(f"{index}. {item}")
        choice = input("\nPlease choose a number: ").strip()
        if not go_ahead(this_store, choice):
            break


def main():

    # setup initial stock of inventory
    """Erstellt das Sortiment und startet die Anwendung."""
    product_list = [
        product.Product("MacBook Air M2", price=1450, quantity=100),
        product.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        product.Product("Google Pixel 7", price=500, quantity=250),
        product.NonStockedProduct("Windows License", price=125),
        product.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    ]

    # Create promotion catalog
    second_half_price = promotion.SecondHalfPrice("Second Half price!")
    third_one_free = promotion.ThirdOneFree("Third One Free!")
    thirty_percent = promotion.PercentDiscount("30% off!", percent=30)

    # Add promotions to products
    product_list[0].set_promotion(second_half_price)
    product_list[1].set_promotion(third_one_free)
    product_list[3].set_promotion(thirty_percent)

    best_buy = store.Store(product_list)

    start(best_buy)


if __name__ == "__main__":
    main()
