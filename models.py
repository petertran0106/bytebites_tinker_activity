# The four classes genereated based on the ByteBites specifications are as follows:
# 1. Restaurant: This class will represent the restaurant itself and may include attributes such as name, location, and a list of food items offered.
# 2. Customer: This class will represent the customers of the restaurant, with attributes like name and purchase history to track their interactions with the restaurant.
# 3. FoodCategory: This class will represent different categories of food items (e.g., "Drinks", "Desserts"), allowing for organization and filtering of the menu.
# 4. FoodItem: This class will represent individual food items, including attributes such as name, price, category, and popularity rating.
# 5. Order: This class will represent a customer's order, containing a list of selected food items and a method to compute the total cost of the order.
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


class OrderStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PREPARING = "PREPARING"
    READY = "READY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


@dataclass
class FoodCategory:
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    items: List[FoodItem] = field(default_factory=list)  # forward ref handled by __future__ annotations

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("FoodCategory.name must be a non-empty string")

    def add_item(self, item: FoodItem) -> None:
        if item not in self.items:
            self.items.append(item)
            item.category = self

    def remove_item(self, item: FoodItem) -> None:
        if item in self.items:
            self.items.remove(item)
            item.category = None

    def list_items(self) -> List[FoodItem]:
        return list(self.items)


@dataclass
class FoodItem:
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    price: Decimal = Decimal("0.00")
    category: Optional[FoodCategory] = None
    popularity_rating: float = 0.0  # 0.0 - 5.0

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("FoodItem.name must be a non-empty string")
        self.price = self._coerce_price(self.price)
        if self.price < Decimal("0.00"):
            raise ValueError("FoodItem.price must be non-negative")
        self.update_popularity(self.popularity_rating)

    @staticmethod
    def _coerce_price(value) -> Decimal:
        if isinstance(value, Decimal):
            return value
        return Decimal(str(value))

    def update_price(self, new_price) -> None:
        new_price = self._coerce_price(new_price)
        if new_price < Decimal("0.00"):
            raise ValueError("price must be non-negative")
        self.price = new_price

    def update_popularity(self, new_rating: float) -> None:
        if new_rating is None:
            new_rating = 0.0
        if not (0.0 <= float(new_rating) <= 5.0):
            raise ValueError("popularity_rating must be between 0.0 and 5.0")
        self.popularity_rating = float(new_rating)


@dataclass
class OrderLine:
    food_item: FoodItem
    quantity: int = 1
    unit_price: Decimal = None

    def __post_init__(self):
        if self.quantity < 1:
            raise ValueError("OrderLine.quantity must be >= 1")
        if self.unit_price is None:
            self.unit_price = self.food_item.price
        elif not isinstance(self.unit_price, Decimal):
            self.unit_price = Decimal(str(self.unit_price))
        if self.unit_price < Decimal("0.00"):
            raise ValueError("OrderLine.unit_price must be non-negative")

    def line_total(self) -> Decimal:
        return self.unit_price * Decimal(self.quantity)


@dataclass
class Customer:
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    purchase_history: List[Order] = field(default_factory=list)

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Customer.name must be a non-empty string")

    def verify(self) -> bool:
        return bool(self.id and self.name.strip())

    def add_purchase(self, order: Order) -> None:
        if order not in self.purchase_history:
            self.purchase_history.append(order)


@dataclass
class Order:
    id: UUID = field(default_factory=uuid4)
    customer: Customer = None
    items: List[OrderLine] = field(default_factory=list)
    status: OrderStatus = OrderStatus.PENDING
    placed_at: datetime = field(default_factory=now_utc)
    updated_at: datetime = field(default_factory=now_utc)

    def add_item(self, food_item: FoodItem, quantity: int = 1, unit_price: Optional[Decimal] = None) -> None:
        line = OrderLine(food_item=food_item, quantity=quantity, unit_price=(unit_price if unit_price is not None else food_item.price))
        self.items.append(line)
        self.touch()

    def remove_item(self, food_item: FoodItem) -> None:
        self.items = [l for l in self.items if l.food_item != food_item]
        self.touch()

    def compute_total(self, tax_rate: Decimal = Decimal("0.00")) -> Decimal:
        # Compute order subtotal from OrderLine entries and apply optional tax_rate (e.g., Decimal("0.08") for 8%).
        subtotal = Decimal("0.00")
        for line in self.items:
            subtotal += line.line_total()
        if not isinstance(tax_rate, Decimal):
            tax_rate = Decimal(str(tax_rate))
        if tax_rate < Decimal("0"):
            raise ValueError("tax_rate must be non-negative")
        tax = (subtotal * tax_rate).quantize(Decimal("0.01"))
        return (subtotal + tax)

    def set_status(self, new_status: OrderStatus) -> None:
        if not isinstance(new_status, OrderStatus):
            raise ValueError("new_status must be an OrderStatus")
        self.status = new_status
        self.touch()

    def touch(self) -> None:
        self.updated_at = now_utc()


@dataclass
class Restaurant:
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    menu: List[FoodItem] = field(default_factory=list)
    categories: List[FoodCategory] = field(default_factory=list)
    customers: List[Customer] = field(default_factory=list)
    orders: List[Order] = field(default_factory=list)

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Restaurant.name must be a non-empty string")

    def add_item(self, item: FoodItem, category_name: Optional[str] = None) -> None:
        if item not in self.menu:
            self.menu.append(item)
        if category_name:
            cat = self._get_or_create_category(category_name)
            cat.add_item(item)

    def _get_or_create_category(self, name: str) -> FoodCategory:
        for c in self.categories:
            if c.name == name:
                return c
        new_cat = FoodCategory(name=name)
        self.categories.append(new_cat)
        return new_cat

    def get_items_by_category(self, category_name: str) -> List[FoodItem]:
        # Return a list of FoodItem objects in the named category (case-insensitive).
        if not category_name or not category_name.strip():
            return []
        target = category_name.strip().lower()
        for c in self.categories:
            if c.name.strip().lower() == target:
                return c.list_items()
        return []

    def register_customer(self, customer: Customer) -> None:
        if customer not in self.customers:
            self.customers.append(customer)

    def place_order(self, customer: Customer, items: List[FoodItem]) -> Order:
        if customer not in self.customers:
            raise ValueError("customer is not registered with this restaurant")
        order = Order(customer=customer)
        for item in items:
            order.add_item(item, quantity=1)
        self.orders.append(order)
        customer.add_purchase(order)
        return order
    
    def get_menu_sorted(self, by: str = "price", reverse: bool = False) -> List[FoodItem]:
        # Return a new list of menu items sorted by 'price', 'name', or 'popularity'.
        key = by.strip().lower() if by else "price"
        if key == "price":
            return sorted(self.menu, key=lambda i: i.price, reverse=reverse)
        if key == "name":
            return sorted(self.menu, key=lambda i: i.name.lower(), reverse=reverse)
        if key in ("popularity", "rating"):
            return sorted(self.menu, key=lambda i: i.popularity_rating, reverse=reverse)
        # fallback to price if unknown key
        return sorted(self.menu, key=lambda i: i.price, reverse=reverse)