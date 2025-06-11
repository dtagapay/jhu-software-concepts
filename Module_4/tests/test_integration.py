import pytest
from src.order import Order

@pytest.mark.order
def test_multiple_pizzas_per_order():
    # Order 1
    order1 = Order()
    order1.input_pizza("thin", ["pesto"], "mozzarella", ["mushrooms"])
    order1.input_pizza("thick", ["marinara"], "mozzarella", ["mushrooms"])
    
    assert len(order1.pizzas) == 2
    assert order1.cost == 12+ 12 # From assignment example
    
    print("\nCustomer Requested:")
    for pizza in order1.pizzas:
            print(f"Crust: {pizza.crust}, Sauce: {pizza.sauce}, Cheese: {pizza.cheese}, Toppings: {pizza.toppings}, Cost: {pizza.cost()}")

    # Order 2
    order2 = Order()
    order2.input_pizza("gluten_free", ["marinara"], "mozzarella", ["pineapple"])
    order2.input_pizza("thin", ["liv_sauce", "pesto"], "mozzarella", ["mushrooms", "pepperoni"])
    
    assert len(order2.pizzas) == 2
    assert order2.cost == 13 + 19  # From assignment example
    print("\nCustomer Requested:")
    for pizza in order2.pizzas:
        print(f"Crust: {pizza.crust}, Sauce: {pizza.sauce}, Cheese: {pizza.cheese}, Toppings: {pizza.toppings}, Cost: {pizza.cost()}")
