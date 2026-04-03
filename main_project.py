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

class Order:
    def __init__(self, order_id):
        self.__order_id = order_id
        self.__items = []
        self.__is_paid = False

    def add_item(self, dish):
        if dish.inventory > 0:
            if dish.reduce_inventory(1):
                self.__items.append(dish)
                return True
        return False

    def suggest_alternative(self, dish_name, menu_dict):
        recommendation_map = {
            "burger": "chicken_burger",
            "cola": "lemon_tea",
            "fries": "onion_rings"
        }

        alt_name = recommendation_map.get(dish_name.lower())
        if alt_name and alt_name in menu_dict:
            alt_dish = menu_dict[alt_name]
            if alt_dish.inventory > 0:
                return alt_dish
        return None

    def calculate_total(self):
        total = sum(item.get_price() for item in self.__items)
        return round(total, 2)

    def get_receipt(self):
        if not self.__items:
            return "Order is empty."

        receipt = f"\n--- Receipt (ID: {self.__order_id}) ---\n"
        for item in self.__items:
            receipt += f"{item.name:15} | ${item.get_price():>6.2f}\n"
        receipt += "-" * 30
        receipt += f"\nTotal Amount:   ${self.calculate_total():>6.2f}\n"
        return receipt

    @property
    def order_id(self):
        return self.__order_id

# Dynamic fix: Order class calls get_price(), but Dish class provides get_final_price()
# Without modifying original classes, unify interface via monkey patching
Dish.get_price = Dish.get_final_price


def main():
    # Initialize dish manager
    manager = DishManager()
    
    # Add 6 dishes (main courses and beverages)
    dishes = [
        MainDish("Beef Burger", 12.99, 10),
        MainDish("Chicken Burger", 10.99, 8),
        MainDish("French Fries", 5.99, 15),
        Drink("Cola", 3.99, 20),
        Drink("Lemon Tea", 4.99, 12),
        Drink("Coffee", 5.49, 10)
    ]
    
    for dish in dishes:
        manager.add_dish(dish)
    
    # Set dish pairing relationships
    manager.set_pairing("Beef Burger", "Cola")
    manager.set_pairing("Beef Burger", "French Fries")
    manager.set_pairing("Chicken Burger", "Lemon Tea")
    manager.set_pairing("French Fries", "Coffee")
    manager.set_pairing("Cola", "French Fries")
    
    # Create order
    order = Order("ORD001")
    
    # Main loop: interactive menu
    while True:
        print("\n" + "=" * 35)
        print("   Cafeteria Ordering System")
        print("=" * 35)
        print("1. Display Full Menu")
        print("2. Order Dish")
        print("3. View Recommendations")
        print("4. View Current Order")
        print("5. Checkout & Print Receipt")
        print("6. Exit")
        print("-" * 35)
        
        choice = input("Please select operation (1-6): ").strip()
        
        if choice == "1":
            # Display full menu
            print("\n--- Menu List ---")
            for dish in manager.menu.values():
                print(dish.describe())
        
        elif choice == "2":
            # Order dish
            dish_name = input("Please enter dish name: ").strip()
            if dish_name in manager.menu:
                dish = manager.menu[dish_name]
                if order.add_item(dish):
                    print(f"Successfully added: {dish_name}")
                else:
                    # Out of stock, suggest alternative
                    alt = order.suggest_alternative(dish_name, manager.menu)
                    if alt:
                        print(f"{dish_name} out of stock, recommended alternative: {alt.name}")
                        confirm = input("Choose alternative dish? (y/n): ").strip().lower()
                        if confirm == 'y':
                            if order.add_item(alt):
                                print(f"Successfully added alternative: {alt.name}")
                            else:
                                print("Failed to add alternative")
                    else:
                        print(f"{dish_name} out of stock, no alternative available")
            else:
                print(f"Dish '{dish_name}' does not exist")
        
        elif choice == "3":
            # View recommendations
            dish_name = input("Please enter dish name: ").strip()
            if dish_name in manager.menu:
                recommendations = manager.get_recommended_dishes(dish_name)
                if recommendations:
                    print(f"\nPairings for '{dish_name}':")
                    for dish in recommendations:
                        print(f"  - {dish.name} (${dish.get_final_price():.2f})")
                else:
                    print(f"'{dish_name}' has no recommendations")
            else:
                print(f"Dish '{dish_name}' does not exist")
        
        elif choice == "4":
            # View current order
            print(order.get_receipt())
        
        elif choice == "5":
            # Checkout and print receipt
            print(order.get_receipt())
            confirm = input("Confirm payment? (y/n): ").strip().lower()
            if confirm == 'y':
                print("Payment successful! Thank you for visiting!")
                break
            else:
                print("Payment cancelled")
        
        elif choice == "6":
            # Exit
            print("Thank you for using, goodbye!")
            break
        
        else:
            print("Invalid selection, please try again")


if __name__ == "__main__":
    main()
