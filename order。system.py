

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
        """

        """

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