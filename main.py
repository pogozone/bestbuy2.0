import product
import store
import promotion

from product import NonStockedProduct

def go_ahead(this_store, choice):
    try:
        choice = int(choice)
    except ValueError:
        print("\nPlease enter a number from 1 to 5.\n")
        return True

    if choice == 1:
        print("\nAll products available:\n")
        this_store.show_all_products()

    elif choice == 2:
        print(f"\nTotal amount in store: {this_store.get_total_quantity()}")

    elif choice == 3:

        available_products = this_store.get_all_products()
        this_store.show_all_products()

        try:

            number = int(input("\nChoose product: "))
            if not 1 <= number <= len(available_products):
                print("Dieses Produkt gibt es nicht.")
                return True

            this_product = available_products[number - 1]

            amount = int(input("\nAmount to buy: "))
            if amount < 1 or (not isinstance(this_product, NonStockedProduct) and amount > this_product.quantity):
                print(f"Bitte wähle zwischen 1 und {this_product.quantity} Stück.")
                return True

        except ValueError:
            print("Bitte gib eine ganze Zahl ein.")
            return True

        shopping_list = [(this_product, amount)]
        total = this_store.order(shopping_list)
        print(f"\nTotal: {total:.2f} €\nBasket:")
        this_store.show_basket()
        return True

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
        print("\nPlease enter a number from 1 to 5.\n")

    return True

def start(this_store):
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
        if not go_ahead(this_store, choice):
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

    start(best_buy)

# setup initial stock of inventory
    mac =  product.Product("MacBook Air M2", price=1450, quantity=100)
    bose = product.Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    pixel = product.LimitedProduct("Google Pixel 7", price=500, quantity=250, maximum=1)

    best_buy = store.Store([mac, bose])
#    mac.price = -100         # Should give error
    print(mac)               # Should print `MacBook Air M2, Price: $1450 Quantity:100`
    print(mac > bose)        # Should print True
    print(mac in best_buy)   # Should print True
    print(pixel in best_buy) # Should print False

if __name__ == "__main__":
    main()
