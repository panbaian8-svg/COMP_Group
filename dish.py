from abc import ABC, abstractmethod

# ==============================================
# Graph Data Structure: Manages dish pairing recommendations
# Vertex = Dish, Edge = Pairing Relationship
# ==============================================
class DishGraph:
    def __init__(self):
        # Adjacency List: Stores the graph structure {dish_name: [list of paired dishes]}
        self.adjacency_list = {}

    def add_vertex(self, dish_name: str):
        """Adds a dish as a vertex in the graph"""
        if dish_name not in self.adjacency_list:
            self.adjacency_list[dish_name] = []

    def add_pair(self, dish1: str, dish2: str):
        """Adds an undirected edge between two dishes to create a pairing"""
        self.add_vertex(dish1)
        self.add_vertex(dish2)
        if dish2 not in self.adjacency_list[dish1]:
            self.adjacency_list[dish1].append(dish2)
        if dish1 not in self.adjacency_list[dish2]:
            self.adjacency_list[dish2].append(dish1)

    def add_pairing(self, dish1: str, dish2: str):
        """Alias for add_pair"""
        self.add_pair(dish1, dish2)

    def get_recommendations(self, dish_name: str) -> list:
        """Returns a list of paired dish names for a given dish"""
        return self.adjacency_list.get(dish_name, [])

# ==============================================
# OOP Core: Abstraction, Encapsulation, Inheritance, and Polymorphism
# ==============================================
class AbstractDish(ABC):
    """Abstract Base Class defining the required interface for all dishes"""
    @abstractmethod
    def describe(self):
        pass

    @abstractmethod
    def get_final_price(self):
        pass

    @abstractmethod
    def reduce_inventory(self):
        pass

class Dish(AbstractDish):
    """Base Dish class implementing common attributes and encapsulation"""
    def __init__(self, name, price, inventory, category):
        self.name = name
        self.category = category
        self._price = price           # Protected attribute
        self.__inventory = inventory  # Private attribute (Encapsulation)

    @property
    def inventory(self):
        """Getter for inventory"""
        return self.__inventory

    def reduce_inventory(self, amount=1):
        """Reduces stock; returns True if successful"""
        if self.__inventory >= amount:
            self.__inventory -= amount
            return True
        return False

    def get_final_price(self):
        """Returns the base price"""
        return self._price

    def describe(self):
        """Returns a formatted string describing the dish"""
        return f"[{self.category}] {self.name} | Price: ${self._price} | Stock: {self.__inventory}"

class MainDish(Dish):
    """Subclass for main courses (Inheritance)"""
    def __init__(self, name, price, inventory):
        super().__init__(name, price, inventory, "Main Course")

    def get_final_price(self):
        """Polymorphism: Returns price without extra tax (as requested)"""
        return self._price

class Drink(Dish):
    """Subclass for beverages (Inheritance)"""
    def __init__(self, name, price, inventory):
        super().__init__(name, price, inventory, "Beverage")

class DishManager:
    """Manager class that integrates Dish objects with the Recommendation Graph"""
    def __init__(self):
        self.menu = {}  # Dictionary mapping dish names to Dish objects
        self.graph = DishGraph()

    def add_dish(self, dish: Dish):
        """Registers a dish and adds it to the graph"""
        self.menu[dish.name] = dish
        self.graph.add_vertex(dish.name)

    def set_pairing(self, dish1_name: str, dish2_name: str):
        """Establishes a pairing relationship between two items"""
        self.graph.add_pair(dish1_name, dish2_name)

    def get_recommended_dishes(self, dish_name: str):
        """Returns Dish objects recommended for the specified dish"""
        recommended_names = self.graph.get_recommendations(dish_name)
        return [self.menu[name] for name in recommended_names if name in self.menu]

# Alias for project-wide compatibility
DishPairingGraph = DishGraph
