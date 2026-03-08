@startuml
skinparam classAttributeIconSize 0

class Restaurant {
  +name: String
  +menu: List<FoodItem>
  +categories: List<FoodCategory>
  +customers: List<Customer>
  +orders: List<Order>
  +addItem(item: FoodItem): void
  +getItemsByCategory(categoryName: String): List<FoodItem>
  +registerCustomer(customer: Customer): void
  +placeOrder(customer: Customer, items: List<FoodItem>): Order
}

class Customer {
  +id: UUID
  +name: String
  +purchaseHistory: List<Order>
  +verify(): Boolean
  +addPurchase(order: Order): void
}

class FoodCategory {
  +id: UUID
  +name: String
  +items: List<FoodItem>
  +addItem(item: FoodItem): void
  +removeItem(item: FoodItem): void
  +listItems(): List<FoodItem>
}

class FoodItem {
  +id: UUID
  +name: String
  +price: Decimal
  +category: FoodCategory
  +popularityRating: Float
  +updatePrice(newPrice: Decimal): void
  +updatePopularity(newRating: Float): void
}

class Order {
  +id: UUID
  +customer: Customer
  +items: List<FoodItem>
  +totalCost: Decimal
  +timestamp: DateTime
  +status: String
  +computeTotal(): Decimal
  +addItem(item: FoodItem): void
  +removeItem(item: FoodItem): void
}

' Relationships '
Restaurant "1" o-- "*" Customer : has
Restaurant "1" o-- "*" FoodCategory : manages
Restaurant "1" o-- "*" FoodItem : offers
Restaurant "1" o-- "*" Order : records

Customer "1" o-- "*" Order : places
Order "*" o-- "*" FoodItem : contains
FoodItem "*" --> "1" FoodCategory : belongs to
FoodCategory "1" o-- "*" FoodItem : groups

@enduml