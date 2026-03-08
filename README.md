# Summary

## Core Concept

Domain modeling: Map real-world concepts to small, single-responsibility classes (Restaurant, Customer, FoodCategory, FoodItem, Order) and choose types/fields that preserve invariants (e.g., money, timestamps, IDs).

## Where students will struggle

Money & rounding: Choosing Decimal vs float and where to round/quantize.
References vs copies: Deciding whether orders store object references or immutable snapshots (unit price at purchase).
Relationships & mutability: Managing shared mutable objects (category lists, menu items) and avoiding accidental aliasing.
Boundary cases: Empty orders, zero/negative quantities, missing categories, and timezone-aware datetimes.

## AI — Helpful vs Misleading

Helpful: Rapidly generates scaffolds, method stubs, and test templates; suggests common validations and edge cases.
Misleading: May assume persistence/ORM or add unneeded complexity, pick unsafe defaults (floats for money), or produce code with subtle runtime issues (missing imports, forward-ref bugs, or wrong rounding semantics).
## A guiding hint (without giving the answer)

Prompt to student: "List the fields Order needs and what an OrderLine must remember so totals remain correct later; then write a one-line pseudo-signature for compute_total() describing inputs/outputs and rounding expectations."




# Activity Reflection
My prompt involved 5 candidate classes rather than 4; I included a class for Restaurants that relates to all the other classes (Customers, FoodCatergories, FoodItems, Orders). Copilot was able to make these relationships between the Restaurants class and the other classes, even when there was little information in the Client Feature Request. In addition, there was a computeTotal() function in the Orders class. No core features or attributes were missing.