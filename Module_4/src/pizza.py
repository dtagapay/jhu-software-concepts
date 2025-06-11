class Pizza:
    """
    A class to represent a customizable pizza and compute its cost.

    Attributes:
        crust (str): Type of crust.
        sauce (list of str): List of sauces.
        cheese (str): Type of cheese.
        toppings (list of str): List of toppings.
        total_cost (int): Total computed cost of the pizza.
    """

    # Ingredient price mappings
    CRUST_COST = {
        "thin": 5,
        "thick": 6,
        "gluten_free": 7
    }

    SAUCE_COST = {
        "marinara": 2,
        "pesto": 3,
        "liv_sauce": 5
    }

    CHEESE_COST = {
        "mozzarella": 1
    }

    TOPPING_COST = {
        "pepperoni": 2,
        "mushrooms": 3,
        "pineapple": 3
    }

    def __init__(self, crust, sauce, cheese, toppings):
        """
        Initialize a Pizza instance with selected ingredients.

        Args:
            crust (str): Type of crust.
            sauce (list of str): List of sauces.
            cheese (str): Type of cheese.
            toppings (list of str): List of toppings.
        """
        self.crust = crust
        self.sauce = sauce
        self.cheese = cheese
        self.toppings = toppings
        self.total_cost = self.cost()

    def cost(self):
        """
        Calculate and return the total cost of the pizza.

        Returns:
            int: Total cost of the pizza.
        """
        cost = 0
        cost += self.CRUST_COST.get(self.crust, 0)
        cost += sum(self.SAUCE_COST.get(s, 0) for s in self.sauce)
        cost += self.CHEESE_COST.get(self.cheese, 0)
        cost += sum(self.TOPPING_COST.get(t, 0) for t in self.toppings)
        return cost

    def __str__(self):
        """
        Return a human-readable description of the pizza.

        Returns:
            str: Description including crust, sauce, cheese, toppings, and cost.
        """
        return (
            f"Pizza with {self.crust} crust, "
            f"sauce(s): {', '.join(self.sauce)}, "
            f"cheese: {self.cheese}, "
            f"toppings: {', '.join(self.toppings)} "
            f"=> Cost: ${self.total_cost}"
        )
