class Pizza:
    # Pizza objects and associated costs
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

    # Initialize a pizza with crust, sauce, cheese, and toppings
    def __init__(self, crust, sauce, cheese, toppings):
        self.crust = crust
        self.sauce = sauce
        self.cheese = cheese
        self.toppings = toppings
        self.total_cost = self.cost()

    # Calculate the cost of the pizza based on ingredients.
    def cost(self):
        cost = 0
        cost += self.CRUST_COST.get(self.crust, 0)
        cost += sum(self.SAUCE_COST.get(s, 0) for s in self.sauce)
        cost += self.CHEESE_COST.get(self.cheese, 0)
        cost += sum(self.TOPPING_COST.get(t, 0) for t in self.toppings)
        return cost
    
    # Return a readable string representation of the pizza
    def __str__(self):
        return (
            f"Pizza with {self.crust} crust, "
            f"sauce(s): {', '.join(self.sauce)}, "
            f"cheese: {self.cheese}, "
            f"toppings: {', '.join(self.toppings)} "
            f"=> Cost: ${self.total_cost}"
        )