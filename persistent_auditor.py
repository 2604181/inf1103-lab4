"""
INF1103 Week 4 - Persistent Auditor
"""
import os

# Global Constants
MAX_INVENTORY = 500
TAX_RATE = 0.1  # 10% tax rate
INVENTORY_FILE = "inventory.txt"

def get_valid_input():
    user_input = input("Enter stock quantity (or 'quit' to quit): ")

    if user_input == "quit":
        return "quit"

    if not user_input.isdigit():
        print("Error. Please enter a valid whole number.")
        return None

    quantity = int(user_input)

    if quantity < 0:
        print("Error. Quantity cannot be negative.")
        return None

    return quantity

def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total

def calculate_tax(amount):
    tax = amount * TAX_RATE
    return tax

def generate_report(total_units, failed_entries):
    print("\n---- Inventory Audit Summary ----")
    print(f"Total Units Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_entries}")

def load_inventory():
    if not os.path.exists(INVENTORY_FILE):
        return 0, []
    
    with open(INVENTORY_FILE, "r") as file:
        lines = file.readlines()
        inventory = int(lines[0].strip())
        
        if len(lines) < 2 or lines[1].strip() == "":
            transaction_history = []
        else:
            transaction_history = [int(x) for x in lines[1].strip().split(",")]
        
        return inventory, transaction_history

def save_inventory(inventory, transaction_history):
    with open(INVENTORY_FILE, "w") as file:
        file.write(f"{inventory}\n")
        history_strings = [str(x) for x in transaction_history]
        file.write(",".join(history_strings))

def main():
    """
    Main function to run inventory auditor program.
    """
    # local variables
    inventory, transaction_history = load_inventory()
    tax_amount = 0
    exit_program = False
    failed = 0

    while not exit_program:
        user_input = get_valid_input()

        if user_input == "quit":
            exit_program = True

        elif user_input is None:
            failed += 1

        else:
            inventory = process_delivery(inventory, user_input)
            transaction_history.append(user_input)
            tax_amount = calculate_tax(user_input)
            print(
                f"Processed {user_input} units. Current inventory: {inventory}. Tax amount: {tax_amount:.2f}"
                )

            if inventory > MAX_INVENTORY:
                print(
                    f"Overstock Alert: Total inventory is ({inventory}) units, which exceeds {MAX_INVENTORY} units!"
                )
                exit_program = True

    save_inventory(inventory, transaction_history)
    generate_report(inventory, failed)


# __name__ (Program Entry Point)
if __name__ == "__main__":
    main()