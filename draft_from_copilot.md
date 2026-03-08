# Copilot-Generated UML Diagram
classDiagram
  class Restaurant {
    - name : String
    - customers : List<Customers>
    - itemsCollection : List<FoodItems>
    - categories : List<FoodCategories>
    - orders : List<Orders>
  }

  class Customers {
    - name : String
    - purchaseHistory : List<Orders>
  }

  class FoodCategories {
    - categoryName : String
    - items : List<FoodItems>
  }

  class FoodItems {
    - name : String
    - price : Float
    - category : FoodCategories
    - popularityRating : Float
  }

  class Orders {
    - id : String
    - items : List<FoodItems>
    - totalCost : Float <<computed>>
    + computeTotal() : Float
  }

  Restaurant "1" o-- "*" Customers : manages
  Restaurant "1" o-- "*" FoodCategories : maintains
  Restaurant "1" o-- "*" FoodItems : offers
  Restaurant "1" o-- "*" Orders : records

  FoodCategories "1" o-- "*" FoodItems : contains
  Customers "1" o-- "*" Orders : places
  Orders "*" o-- "*" FoodItems : includes