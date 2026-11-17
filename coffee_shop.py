"""
Coffee Shop Order Management System

A command-line program that takes orders from several customers, applies
customisations, service charge, tiered discounts and VAT, runs a lucky draw,
prints and saves an itemised receipt, and keeps track of stock.

Run with:  python coffee_shop.py
"""

import datetime
import random

# ---------------------------------------------------------------
# Settings
# ---------------------------------------------------------------

menu = {
    'Coffee': 2.50,
    'Tea': 2.00,
    'Croissant': 3.00,
    'Muffin': 2.75,
    'Pineapple Juice': 3.25,
    'Peppermint Tea': 2.20,
    'Chocolate Cookie': 2.30,
    'White Chocolate Cookie': 2.40
}

# Customisation options and their extra cost (drinks only)
customisations = {
    'Extra Shot': 0.50,
    'Oat Milk': 0.30,
    'Sugar': 0.10,
    'Whipped Cream': 0.40
}

# How many of each item are in stock
inventory = {
    'Coffee': 10,
    'Tea': 10,
    'Croissant': 5,
    'Muffin': 5,
    'Pineapple Juice': 3,
    'Peppermint Tea': 5,
    'Chocolate Cookie': 8,
    'White Chocolate Cookie': 8
}

VAT_RATE = 0.20
SERVICE_RATE = 0.10
lucky_prizes = ["free cookie", "free coffee", "10% off next order"]
grand_prize = "free meal for two"


def get_positive_int(prompt):
    """Keep asking until the user types a whole number greater than 0."""
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a number greater than 0.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a number.")


# ---------------------------------------------------------------
# Main program
# ---------------------------------------------------------------

print("Welcome to our Coffee Shop! Here's our menu:")
max_length = max(len(item) for item in menu)
for item, price in menu.items():
    print("- " + item.ljust(max_length) + f" : £{price:.2f}")

all_customers = []
num_customers = get_positive_int("\nEnter number of customers: ")

for i in range(num_customers):
    print(f"\n--- Customer {i+1} ---")

    # Customer info
    customer_name = input("Please enter the customer's name: ")
    today = datetime.date.today()

    # Take order
    customer_order = []
    while True:
        order_item = input("What would you like to order? (Type 'done' to finish): ").strip().title()

        if order_item == 'Done':
            break

        elif order_item in menu:
            # Check stock
            if inventory[order_item] == 0:
                print(f"Sorry, {order_item} is out of stock!")
                continue

            quantity = get_positive_int(f"How many {order_item}s? ")
            if quantity > inventory[order_item]:
                print(f"Only {inventory[order_item]} {order_item}(s) available. Please adjust quantity.")
                continue

            # Customisations (drinks only)
            item_customisations = []
            if order_item in ['Coffee', 'Tea']:
                print("Available customisations: ", ", ".join(customisations.keys()))
                while True:
                    cust = input("Add a customisation (type 'done' to finish): ").strip().title()
                    if cust == 'Done':
                        break
                    elif cust in customisations:
                        item_customisations.append(cust)
                        print(f"Added {cust} (+£{customisations[cust]:.2f})")
                    else:
                        print("Invalid option, try again.")

            customer_order.append((order_item, quantity, item_customisations))
            inventory[order_item] -= quantity
            print(f"Added {quantity} x {order_item} to your order with "
                  f"{', '.join(item_customisations) if item_customisations else 'no customisations'}.")

        else:
            print("Sorry, that item is not on our menu. Please choose from the list.")

    # Skip billing if the customer ordered nothing
    if not customer_order:
        print("No items ordered, so no receipt is needed.")
        continue

    # Subtotal, including customisations
    subtotal = 0
    for item, qty, cust_list in customer_order:
        base_price = menu[item]
        cust_price = sum(customisations[c] for c in cust_list)
        subtotal += (base_price + cust_price) * qty

    # Service charge on orders over £15
    service_charge = subtotal * SERVICE_RATE if subtotal > 15 else 0

    # Tiered discount, based on the subtotal before service charge,
    # so the service charge can't push a bill over a discount threshold
    if subtotal > 15:
        discount_rate = 0.15
    elif subtotal > 10:
        discount_rate = 0.10
    else:
        discount_rate = 0
    discount_amount = subtotal * discount_rate

    # VAT is applied after discount and service charge
    subtotal_after_discount = subtotal - discount_amount + service_charge
    tax_amount = subtotal_after_discount * VAT_RATE
    total_due = subtotal_after_discount + tax_amount

    # Lucky draw: only for bills over £5, with a rare grand prize
    if total_due > 5:
        if random.random() < 0.01:
            lucky_message = f"*** GRAND PRIZE! You won a {grand_prize}! ***"
        elif random.random() < 0.30:
            lucky_message = f"*** Lucky Draw! You won a {random.choice(lucky_prizes)}! ***"
        else:
            lucky_message = "Better luck next time in our Lucky Draw!"
    else:
        lucky_message = "Spend over £5 to enter the Lucky Draw!"

    # Build the receipt once, then print it and save it
    line = "-" * 62
    receipt_text = "\n--- Your Coffee Shop Receipt ---\n"
    receipt_text += f"Customer: {customer_name}\nDate: {today}\n\n"
    receipt_text += f"{'Item':<23} {'Qty':<5} {'Price':<8} {'Total':<8} Customisations\n{line}\n"
    for item, qty, cust_list in customer_order:
        base_price = menu[item]
        cust_price = sum(customisations[c] for c in cust_list)
        line_total = (base_price + cust_price) * qty
        cust_text = ", ".join(cust_list) if cust_list else "None"
        receipt_text += f"{item:<23} {qty:<5} £{base_price:<7.2f} £{line_total:<7.2f} {cust_text}\n"
    receipt_text += f"{line}\n"
    receipt_text += f"Subtotal:        £{subtotal:>8.2f}\n"
    if service_charge > 0:
        receipt_text += f"Service Charge:  £{service_charge:>8.2f}\n"
    if discount_amount > 0:
        receipt_text += f"Discount:       -£{discount_amount:>8.2f}\n"
    receipt_text += f"VAT (20%):       £{tax_amount:>8.2f}\n"
    receipt_text += f"Total Due:       £{total_due:>8.2f}\n{line}\n"
    receipt_text += lucky_message + "\nThank you for your order!\n"

    print(receipt_text)

    safe_name = customer_name.lower().replace(" ", "_")
    filename = f"receipt_{safe_name}_{today}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(receipt_text)
    print(f"Receipt saved to file: {filename}")

    # Keep a record of every transaction
    all_customers.append({
        "name": customer_name,
        "date": today,
        "order": customer_order,
        "subtotal": subtotal,
        "service_charge": service_charge,
        "discount": discount_amount,
        "VAT": tax_amount,
        "total_due": total_due,
        "lucky_draw": lucky_message
    })

# Summary
print("\n=== Summary of All Customers ===")
for cust in all_customers:
    print(f"{cust['name']}: £{cust['total_due']:.2f}, Lucky Draw: {cust['lucky_draw']}")

print("\n=== Remaining Inventory ===")
for item, stock in inventory.items():
    print(f"{item}: {stock} left")
