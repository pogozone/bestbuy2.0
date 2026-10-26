import pytest

from product import Product

def test_get_quantity():
    product = Product("Test Product", price=250, quantity=10)
    assert product.get_quantity() == 10


def test_set_quantity_success():
    # Testet den normalen Fall mit einer positiven Zahl
    product = Product("Test Product", price=250, quantity=10)
    product.set_quantity(5)
    assert product.quantity == 5
    assert product.active is True


def test_set_quantity_to_zero():
    # Testet den Grenzfall: Bestand wird 0 -> active muss False werden
    product = Product("Test Product", price=250, quantity=10)
    product.set_quantity(0)
    assert product.quantity == 0
    assert product.active is False


def test_set_quantity_negative_raises_error():
    # Testet den Fehlerfall: Negative Zahl wirft ValueError
    product = Product("Test Product", price=250, quantity=10)

    with pytest.raises(ValueError):
        product.set_quantity(-10)

def test_is_active():
    product = Product("Test Product", price=250, quantity=10)
    assert product.active is True

def test_is_active_not():
    product = Product("Test Product", price=250, quantity=10)
    product.set_quantity(0)
    assert product.active is False

def test_deactivate():
    product = Product("Test Product", price=250, quantity=10)
    product.deactivate()
    assert product.active is False

def test_buy_success():
    product = Product("Test Product", price=250, quantity=10)
    total = product.buy(2)
    assert total == 500
    assert product.quantity == 8
    assert product.active is True


def test_buy_exact_stock_deactivates_product():#  product = Product("Test", price=10.0, quantity=2)
    product = Product("Test Product", price=250, quantity=10)
    total = product.buy(10)
    assert total == 2500
    assert product.quantity == 0
    assert product.active is False


def test_buy_invalid_type_or_negative_quantity():
    product = Product("Test Product", price=250, quantity=10)

    with pytest.raises(ValueError):
        product.buy(-1)

    with pytest.raises(ValueError):
        product.buy(2.5)  # float statt int


def test_buy_exceeds_stock():
    product = Product("Test Product", price=250, quantity=10)

    with pytest.raises(ValueError, match="Lagerbestand"):
        product.buy(100)


def test_buy_inactive_product():
    product = Product("Test Product", price=250, quantity=10)
    product.deactivate()

    with pytest.raises(ValueError):
        product.buy(1)
