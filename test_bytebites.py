from decimal import Decimal
import models

def test_calculate_total_with_multiple_items():
    """Verify order total equals sum of item prices."""
    r = models.Restaurant(name="ByteBites")
    c = models.Customer(name="Alice")
    r.register_customer(c)

    burger = models.FoodItem(name="Spicy Burger", price=Decimal("10.00"))
    soda = models.FoodItem(name="Large Soda", price=Decimal("5.00"))

    r.add_item(burger, category_name="Mains")
    r.add_item(soda, category_name="Drinks")

    order = r.place_order(c, [burger, soda])
    assert order.compute_total() == Decimal("15.00")


def test_order_total_is_zero_when_empty():
    """Verify empty order total is zero."""
    c = models.Customer(name="Bob")
    order = models.Order(customer=c)
    assert order.compute_total() == Decimal("0.00")


def test_filter_menu_items_by_category():
    """Verify filtering by category returns only items in that category (case-insensitive)."""
    r = models.Restaurant(name="ByteBites")

    tea = models.FoodItem(name="Green Tea", price=Decimal("2.00"))
    cake = models.FoodItem(name="Cheesecake", price=Decimal("4.50"))

    r.add_item(tea, category_name="Drinks")
    r.add_item(cake, category_name="Desserts")

    drinks = r.get_items_by_category("drinks")
    assert tea in drinks
    assert cake not in drinks
    assert r.get_items_by_category("Drinks")[0].name == "Green Tea"