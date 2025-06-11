from src.pizza import Pizza

class Order:
    def __init__(self):
        """
        Initialize an order with:
        - an empty list of pizzas
        - cost set to 0
        - unpaid status
        """
        self.pizzas = []
        self.cost = 0
        self.paid = False

    def input_pizza(self, crust, sauce, cheese, toppings):
        """
        Create a Pizza object and add it to the order.
        Update the total cost of the order.
        """
        pizza = Pizza(crust, sauce, cheese, toppings)
        self.pizzas.append(pizza)
        self.cost += pizza.cost()

    def order_paid(self):
        """
        Mark the order as paid.
        """
        self.paid = True

    def __str__(self):
        """
        Return a string representation of the full order.
        Includes each pizza and total cost.
        """
        order_summary = "\n".join(str(pizza) for pizza in self.pizzas)
        paid_status = "paid" if self.paid else "not paid"
        return f"{order_summary}\nTotal: ${self.cost} ({paid_status})"
        
        
