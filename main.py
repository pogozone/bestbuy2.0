import product
import store
import promotion

from product import NonStockedProduct

def go_ahead(store, choice):
    try:
        choice = int(choice)
    except ValueError:
        print("\nPlease enter a number from 1 to 5.\n")
        return True

    if choice == 1:
        print("\nAll products available:\n")
        store.show_all_products()

    elif choice == 2:
        print(f"\nTotal amount in store: {store.get_total_quantity()}")

    elif choice == 3:

        available_products = store.get_all_products()
        store.show_all_products()

        try:

            number = int(input("\nChoose product: "))
            if not 1 <= number <= len(available_products):
                print("Dieses Produkt gibt es nicht.")
                return True

            product = available_products[number - 1]

            amount = int(input("\nAmount to buy: "))
            if amount < 1 or (not isinstance(product, NonStockedProduct) and amount > product.quantity):
                print(f"Bitte wähle zwischen 1 und {product.quantity} Stück.")
                return True

        except ValueError:
            print("Bitte gib eine ganze Zahl ein.")
            return True

        shopping_list = [(product, amount)]
        total = store.order(shopping_list)
        print(f"\nTotal: {total:.2f} €\nBasket:")
        store.show_basket()
        return True

    elif choice == 4:
        store.show_basket()
        return True
    elif choice == 5:
        store.clear_order()
        print("\nOrder cancelled. Stock restored.")
        return True

    elif choice == 6:
        print("\nGoodbye!")
        return False

    else:
        print("\nPlease enter a number from 1 to 5.\n")

    return True

def start(store):
    menu = [
        "List all products in store",
        "Show total amount in store",
        "Make an order",
        "Show basket",
        "Clear basket",
        "Quit"
    ]
    while True:
        print("\n===== Best Buy =====\n")
        for index, item in enumerate(menu, start=1):
            print(f"{index}. {item}")
        choice = input("\nPlease choose a number: ").strip()
        if not go_ahead(store, choice):
            break

def main():

    # setup initial stock of inventory
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
    product_list[3].set_promotion(third_one_free)

    best_buy = store.Store(product_list)

    for index, prod in enumerate(product_list):
        print(f"Produkt {index} :: {prod}")

    start(best_buy)

if __name__ == "__main__":
    main()
