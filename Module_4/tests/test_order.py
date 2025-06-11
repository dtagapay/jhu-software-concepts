import pytest
from src.order import Order

# Test 1: Order initialization
@pytest.mark.order
def test_order_init():
    order = Order()
    assert order.pizzas == []
    assert order.cost == 0
    assert not order.paid

# Test 2: Adding a pizza updates cost and list
@pytest.mark.order
def test_order_input_pizza():
    order = Order()
    order.input_pizza("thin", ["marinara"], "mozzarella", ["pineapple"])
    assert len(order.pizzas) == 1
    assert order.cost > 0

# Test 3: String representation of order
@pytest.mark.order
def test_order_str():
    order = Order()
    order.input_pizza("thin", ["marinara"], "mozzarella", ["pineapple"])
    output = str(order)
    assert "pineapple" in output
    assert "$" in output
    assert "not paid" in output or "paid" in output

# Test 4: Marking order as paid
@pytest.mark.order
def test_order_paid():
    order = Order()
    assert not order.paid
    order.order_paid()
    assert order.paid
