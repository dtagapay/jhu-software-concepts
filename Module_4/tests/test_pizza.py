import pytest
from src.pizza import Pizza

# Test 1: Initialization
@pytest.mark.pizza
def test_pizza_init():
    pizza = Pizza("thin", ["marinara"], "mozzarella", ["pepperoni"])
    assert pizza.crust == "thin"
    assert pizza.sauce == ["marinara"]
    assert pizza.cheese == "mozzarella"
    assert pizza.toppings == ["pepperoni"]

# Test 2: Cost calculation
@pytest.mark.pizza
def test_pizza_cost():
    pizza = Pizza("thin", ["pesto"], "mozzarella", ["mushrooms"])
    expected_cost = 5 + 3 + 1 + 3  # crust + pesto + cheese + topping
    assert pizza.cost() == expected_cost

# Test 3: String output
@pytest.mark.pizza
def test_pizza_str():
    pizza = Pizza("thick", ["marinara", "liv_sauce"], "mozzarella", ["pepperoni", "mushrooms"])
    pizza_str = str(pizza)
    assert "thick" in pizza_str
    assert "marinara" in pizza_str and "liv_sauce" in pizza_str
    assert "mozzarella" in pizza_str
    assert "pepperoni" in pizza_str and "mushrooms" in pizza_str
    assert "$" in pizza_str
