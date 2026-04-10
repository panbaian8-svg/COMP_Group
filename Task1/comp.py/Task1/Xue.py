from abc import ABC, abstractmethod

# ==============================================
# Task2 New Data Structure: Graph (Integrated in dish.py)
# Purpose: Manage dish pairing recommendations (Vertex = Dish, Edge = Pairing Relationship)
# ==============================================
class DishGraph:
    def __init__(self):
        # Adjacency List: Core storage structure of Graph (Uncovered in course)
        self.adjacency_list = {}

    # Add dish vertex to the graph
    def add_vertex(self, dish_name: str):
        if dish_name not in self.adjacency_list:
            self.adjacency_list[dish_name] = []

    # Add undirected edge (pairing relationship between two dishes)
    def add_pair(self, dish1: str, dish2: str):
        if dish1 in self.adjacency_list and dish2 in self.adjacency_list:
            if dish2 not in self.adjacency_list[dish1]:
                self.adjacency_list[dish1].append(dish2)
            if dish1 not in self.adjacency_list[dish2]:
                self.adjacency_list[dish2].append(dish1)

    # Get recommended paired dishes (Core function)
    def get_recommendations(self, dish_name: str) -> list:
        return self.adjacency_list.get(dish_name, [])

# ==============================================
# Task1 OOP Core: Abstract Base Class + Encapsulation + Inheritance + Polymorphism
# ==============================================
class AbstractDish(ABC):
    @abstractmethod
    def describe(self):
        pass

    @abstractmethod
    def get_final_price(self):
        pass

    @abstractmethod
    def reduce_inventory(self):
        pass

# Base Dish Class (Encapsulation)
class Dish(AbstractDish):
    def __init__(self, name, price, inventory, category):
        self.name = name
        self.category = category
        self._price = price
        self.__inventory = inventory  # Private attribute (Encapsulation)

    @property
    def inventory(self):
        return self.__inventory

    def reduce_inventory(self, amount=1):
        if self.__inventory >= amount:
            self.__inventory -= amount
            return True
        return False

    def get_final_price(self):
        return self._price

    def describe(self):
        return f"[{self.category}] {self.name} | Price: ${self._price} | Stock: {self.__inventory}"

# Main Dish Subclass (Inheritance + Polymorphism)
class MainDish(Dish):
    def __init__(self, name, price, inventory):
        super().__init__(name, price, inventory, "Main Course")

    def get_final_price(self):
        return self._price * 1.1  # Main course includes 10% tax

# Drink Subclass (Inheritance + Polymorphism)
class Drink(Dish):
    def __init__(self, name, price, inventory):
        super().__init__(name, price, inventory, "Beverage")

# ==============================================
# Core Integration: Dish Manager (Combines Dish + DishGraph)
# ==============================================
class DishManager:
    def __init__(self):
        self.menu = {}  # Store all dish objects
        self.graph = DishGraph()  # New Data Structure: Graph (for pairing recommendations)

    # Add dish + auto create vertex in the graph
    def add_dish(self, dish: Dish):
        self.menu[dish.name] = dish
        self.graph.add_vertex(dish.name)

    # Set pairing relationship between two dishes
    def set_pairing(self, dish1_name: str, dish2_name: str):
        self.graph.add_pair(dish1_name, dish2_name)

    # Get recommended dishes (call Graph structure)
    def get_recommended_dishes(self, dish_name: str):
        recommended_names = self.graph.get_recommendations(dish_name)
        return [self.menu[name] for name in recommended_names if name in self.menu]

# ==============================================
# Test Code (Run to verify all functions)
# ==============================================
if __name__ == "__main__":
    # 1. Create dish instances
    burger = MainDish("Beef Burger", 12.99, 10)
    cola = Drink("Cola", 3.99, 20)
    fries = MainDish("French Fries", 5.99, 15)

    # 2. Initialize dish manager (Integrated OOP + Graph)
    manager = DishManager()
    manager.add_dish(burger)
    manager.add_dish(cola)
    manager.add_dish(fries)

    # 3. Set dish pairings (Use Graph Data Structure)
    manager.set_pairing("Beef Burger", "Cola")
    manager.set_pairing("Beef Burger", "French Fries")

    # 4. Test recommendation function
    print("Ordered [Beef Burger], recommended pairings:")
    for dish in manager.get_recommended_dishes("Beef Burger"):
        print("-", dish.describe())