import unittest
from product import Product, LimitedProduct, NonStockedProduct
from promotion import PercentDiscount
from store import Store


class OrderTests(unittest.TestCase):
    def test_repeated_addition(self):
        item = Product("Test", 10, 5)
        shop = Store([item])
        shop.order([(item, 2)])
        shop.order([(item, 1)])
        self.assertEqual(item.quantity, 2)
        self.assertEqual(shop.basket[0]["amount"], 3)

    def test_failure_preserves_basket_and_stock(self):
        item = Product("Test", 10, 5)
        shipping = LimitedProduct("Shipping", 10, 250, 1)
        shop = Store([item, shipping])
        shop.order([(item, 1)])
        with self.assertRaises(ValueError):
            shop.order([(item, 1), (shipping, 2)])
        self.assertEqual(item.quantity, 4)
        self.assertEqual(shop.basket[0]["amount"], 1)

    def test_limit_applies_to_entire_basket(self):
        item = LimitedProduct("Shipping", 10, 250, 1)
        shop = Store([item])
        shop.order([(item, 1)])
        with self.assertRaises(ValueError):
            shop.order([(item, 1)])
        self.assertEqual(item.quantity, 249)

    def test_unlimited_and_single_promotion(self):
        item = NonStockedProduct("Windows", 125)
        item.set_promotion(PercentDiscount("Discount", 30))
        self.assertIn("Unlimited", str(item))
        self.assertIn("30%", str(item))
        self.assertAlmostEqual(item.buy(3), 262.5)
        item.set_promotion(PercentDiscount("Other", 10))
        self.assertAlmostEqual(item.buy(3), 337.5)

    def test_clear_restores_stock(self):
        item = LimitedProduct("Shipping", 10, 250, 1)
        shop = Store([item])
        shop.order([(item, 1)])
        shop.clear_order()
        self.assertEqual(item.quantity, 250)
        self.assertEqual(shop.basket, [])


if __name__ == "__main__":
    unittest.main()
