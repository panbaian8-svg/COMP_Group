class Order:
    def __init__(self, order_id):
        self.__order_id = order_id
        self.__items = []      # List of items added to the current order
        self.__is_paid = False

    def add_item(self, dish):
        """Attempts to add a dish to the order after checking inventory"""
        if dish.inventory > 0:
            if dish.reduce_inventory(1):
                self.__items.append(dish)
                return True
        return False

    def suggest_alternative(self, dish_name, menu_dict):
        """Suggests an alternative dish if the requested one is unavailable"""
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
        """Calculates the total cost of the order using polymorphic price methods"""
        total = sum(item.get_final_price() for item in self.__items)
        return round(total, 2)

    def get_receipt(self):
        """Generates a formatted receipt string"""
        if not self.__items:
            return "Order is empty."

        receipt = f"\n--- Receipt (ID: {self.__order_id}) ---\n"
        for item in self.__items:
            # Formatted column output for dish name and price
            receipt += f"{item.name:15} | ${item.get_final_price():>6.2f}\n"
        receipt += "-" * 30
        receipt += f"\nTotal Amount:   ${self.calculate_total():>6.2f}\n"
        return receipt

    def generate_receipt(self):
        """Alias for get_receipt"""
        return self.get_receipt()

    @property
    def order_id(self):
        return self.__order_id
