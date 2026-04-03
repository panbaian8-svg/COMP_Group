# ==============================================
# Cafeteria Ordering System - Main Program
# ==============================================

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
                    print(f"[OK] Successfully added: {dish_name}")
                else:
                    # Out of stock, suggest alternative
                    alt = order.suggest_alternative(dish_name, manager.menu)
                    if alt:
                        print(f"[!] {dish_name} out of stock, recommended alternative: {alt.name}")
                        confirm = input("Choose alternative dish? (y/n): ").strip().lower()
                        if confirm == 'y':
                            if order.add_item(alt):
                                print(f"[OK] Successfully added alternative: {alt.name}")
                            else:
                                print(f"[X] Failed to add alternative")
                    else:
                        print(f"[X] {dish_name} out of stock, no alternative available")
            else:
                print(f"[X] Dish '{dish_name}' does not exist")
        
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
                    print(f"[!] '{dish_name}' has no recommendations")
            else:
                print(f"[X] Dish '{dish_name}' does not exist")
        
        elif choice == "4":
            # View current order
            print(order.get_receipt())
        
        elif choice == "5":
            # Checkout and print receipt
            print(order.get_receipt())
            confirm = input("Confirm payment? (y/n): ").strip().lower()
            if confirm == 'y':
                print("[OK] Payment successful! Thank you for visiting!")
                break
            else:
                print("[!] Payment cancelled")
        
        elif choice == "6":
            # Exit
            print("Thank you for using, goodbye!")
            break
        
        else:
            print("[X] Invalid selection, please try again")


if __name__ == "__main__":
    main()
