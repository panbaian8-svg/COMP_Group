from dish import MainDish, Drink, DishPairingGraph
from order import Order
from algorithms import radix_sort_prices

class RestaurantSystem:
    def __init__(self):
        # Initialize menu with default items
        self.menu = {
            "Beef Burger": MainDish("Beef Burger", 12.99, 10),
            "Cola": Drink("Cola", 3.00, 50)
        }
        # Initialize pairings using the Graph structure
        self.pairings = DishPairingGraph()
        self.pairings.add_pairing("Beef Burger", "Cola")

    def run(self):
        """Starts the interactive CLI system"""
        print("HKMU Restaurant System v1.0")
        current_order = Order("TXN001")
        
        while True:
            print("\n1. Menu (Sorted) | 2. Order | 3. Checkout | 4. Exit")
            cmd = input("Choice: ")
            
            if cmd == "1":
                # Extract and sort prices using Member 2's algorithm
                prices = [d.get_final_price() for d in self.menu.values()]
                sorted_p = radix_sort_prices(prices)
                print(f"Current Prices: {sorted_p}")
                for d in self.menu.values(): 
                    print(d.describe())
                
            elif cmd == "2":
                # Handle ordering and display Member 1's graph-based recommendations
                name = input("Dish name: ")
                if name in self.menu and current_order.add_item(self.menu[name]):
                    print(f"Added {name}!")
                    recs = self.pairings.get_recommendations(name)
                    if recs: 
                        print(f"Suggested with this: {recs}")
                else: 
                    print("Error: Out of stock or not found.")

            elif cmd == "3":
                # Finalize order and print receipt
                print(current_order.generate_receipt())
                break
                
            elif cmd == "4": 
                break

if __name__ == "__main__":
    RestaurantSystem().run()
