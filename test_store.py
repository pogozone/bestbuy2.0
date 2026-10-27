import unittest

from product import Product
from store import Store


class TestStore(unittest.TestCase):
    def setUp(self):
        self.mac = Product("MacBook Air M2", price=1450, quantity=100)
        self.bose = Product("Bose Earbuds", price=250, quantity=500)
        self.store = Store([self.mac, self.bose])

    def test_initial_stock(self):
        self.assertEqual(self.store.get_all_products(), [self.mac, self.bose])
        self.assertEqual(self.store.get_total_quantity(), 600)
        self.assertEqual(self.store.basket, [])

    def test_add_and_remove_product(self):
        pixel = Product("Google Pixel 7", price=500, quantity=250)

        self.store.add_product(pixel)
        self.assertIn(pixel, self.store.get_all_products())
        self.assertEqual(self.store.get_total_quantity(), 850)

        self.store.remove_product(pixel)
        self.assertNotIn(pixel, self.store.get_all_products())
        self.assertEqual(self.store.get_total_quantity(), 600)

    def test_stores_have_separate_lists(self):
        other_store = Store([])
        other_store.add_product(self.mac)

        self.assertEqual(other_store.get_all_products(), [self.mac])
        self.assertEqual(len(self.store.get_all_products()), 2)
        self.assertIsNot(self.store.basket, other_store.basket)

    def test_order_price_and_remaining_stock(self):
        total = self.store.order([(self.mac, 1), (self.bose, 2)])

        self.assertAlmostEqual(total, 1950.0)
        self.assertEqual(self.mac.quantity, 99)
        self.assertEqual(self.bose.quantity, 498)
        self.assertEqual(self.store.get_total_quantity(), 597)

    def test_order_same_product_multiple_times(self):
        total = self.store.order([(self.bose, 5), (self.bose, 10)])

        self.assertAlmostEqual(total, 3750.0)
        self.assertEqual(self.bose.quantity, 485)

    def test_sold_out_product_is_hidden(self):
        self.store.order([(self.mac, 100)])

        self.assertEqual(self.mac.quantity, 0)
        self.assertNotIn(self.mac, self.store.get_all_products())
        self.assertIn(self.bose, self.store.get_all_products())

    def test_create_basket_does_not_change_stock(self):
        basket = self.store.order([(self.mac, 2)])

        self.assertEqual(len(basket), 1)
        self.assertIs(basket[0]["product"], self.mac)
        self.assertEqual(basket[0]["name"], "MacBook Air M2")
        self.assertEqual(basket[0]["amount"], 2)
        self.assertAlmostEqual(basket[0]["total_price"], 2900.0)
        self.assertEqual(self.mac.quantity, 100)

    def test_cancel_restores_stock_and_empties_basket(self):
        shopping_list = [(self.mac, 1), (self.bose, 2)]
        self.store.order(shopping_list)

        self.store.clear_order()

        self.assertEqual(self.mac.quantity, 100)
        self.assertEqual(self.bose.quantity, 500)
        self.assertEqual(self.store.basket, [])

        # Erneutes Stornieren darf den Bestand nicht erhöhen.
        self.store.clear_order()
        self.assertEqual(self.store.get_total_quantity(), 600)

    def test_cancel_reactivates_sold_out_product(self):
        shopping_list = [(self.mac, 100)]
        self.store.order(shopping_list)

        self.store.clear_order()

        self.assertEqual(self.mac.quantity, 100)
        self.assertTrue(self.mac.is_active())
        self.assertIn(self.mac, self.store.get_all_products())

    def test_clear_basket_does_not_restore_stock(self):
        shopping_list = [(self.mac, 2)]
        self.store.order(shopping_list)

        self.store.clear_order()

        self.assertEqual(self.store.basket, [])
        self.assertEqual(self.mac.quantity, 98)

    def test_empty_store_and_empty_order(self):
        empty_store = Store([])

        self.assertEqual(empty_store.get_all_products(), [])
        self.assertEqual(empty_store.get_total_quantity(), 0)
        self.assertEqual(empty_store.order([]), 0.0)
        empty_store.clear_order()


if __name__ == "__main__":
    unittest.main()