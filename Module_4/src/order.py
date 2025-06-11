from src.pizza import Pizza

class Order:
    """
    A class to manage a customer's pizza order.

    Attributes:
        pizzas (list of Pizza): List of pizzas in the order.
        cost (int): Total cost of the order.
        paid (bool): Payment status.
    """

    def __init__(self):
        """
        Initialize an empty Order with zero cost and unpaid status.
        """
        self.pizzas = []
        self.cost = 0
        self.paid = False

    def input_pizza(self, crust, sauce, cheese, toppings):
        """
        Create and add a pizza to the order and update the cost.

        Args:
            crust (str): Type of crust.
            sauce (list of str): Sauce(s) used.
            cheese (str): Type of cheese.
            toppings (list of str): Toppings list.
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
        Return a detailed string summary of the order.

        Returns:
            str: Pizza list with total cost and payment status.
        """
        order_summary = "\n".join(str(pizza) for pizza in self.pizzas)
        paid_status = "paid" if self.paid else "not paid"
        return f"{order_summary}\nTotal: ${self.cost} ({paid_status})"
