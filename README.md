# Coffee Shop Order Management System (Python)

A command-line program that runs the till for a small coffee shop: it takes orders from several customers, works out the bill, prints and saves an itemised receipt, and keeps track of stock.
Python course project, awarded **Distinction**.

## What it does

- **Menu display** with names and prices aligned automatically, however long the item name
- **Order taking** for multiple customers in one run, with quantities
- **Input validation:** rejects text and zero or negative quantities, and asks again instead of crashing
- **Empty orders handled:** a customer who orders nothing doesn't get a £0.00 receipt
- **Customisations** for drinks (extra shot, oat milk, sugar, whipped cream), each with its own price
- **Inventory management:** stock goes down with each order, and out-of-stock items can't be ordered
- **Billing rules:**
  - 10% service charge on orders over £15
  - tiered discount: 10% over £10, 15% over £15, based on the subtotal **before** service charge, so the service charge can't push a bill over a discount threshold
  - 20% VAT applied after discount and service charge
- **Lucky draw** for bills over £5, with a rare 1% grand prize
- **Receipts** printed to the screen and saved as a text file named after the customer and date
- **End-of-day summary** of every customer's total and the remaining stock

## Example receipt

```
--- Your Coffee Shop Receipt ---
Customer: Alex Smith
Date: 2026-11-17

Item                    Qty   Price    Total    Customisations
--------------------------------------------------------------
Coffee                  2     £2.50    £5.60    Oat Milk
White Chocolate Cookie  8     £2.40    £19.20   None
--------------------------------------------------------------
Subtotal:        £   24.80
Service Charge:  £    2.48
Discount:       -£    3.72
VAT (20%):       £    4.71
Total Due:       £   28.27
--------------------------------------------------------------
*** Lucky Draw! You won a free coffee! ***
Thank you for your order!
```

## Python skills used

| Skill | Where |
|---|---|
| Dictionaries | Menu, prices, customisations and stock levels |
| Lists of tuples and dictionaries | Each order line; each customer's transaction record |
| `while` and `for` loops | Taking orders until "done"; looping through customers |
| `if` / `elif` / `else` | Discount tiers, service charge, stock checks |
| `try` / `except` | Validating number input |
| Functions | `get_positive_int()` for reusable input checking |
| f-strings and string methods | Aligned receipts; `.strip().title()` so "white chocolate cookie" matches the menu |
| `random` and `datetime` modules | Lucky draw; date on receipts |
| File handling | Saving each receipt to a `.txt` file |

## How to run

You need Python 3 installed. Download `coffee_shop.py`, then run:

```
python coffee_shop.py
```

Follow the prompts, and type `done` to finish each order.

## What I would improve next

- **Split the program into functions** such as `display_menu()`, `take_order()`, `calculate_bill()` and `print_receipt()`, so each part can be tested and reused on its own.
- **Create PDF receipts** as well as text files.
- **Store prices as exact decimals** (Python's `decimal` module), because ordinary decimal numbers can create tiny rounding errors in money calculations.
- **Save every transaction to a CSV file or SQLite database**, so sales can be analysed with SQL or pandas: best-selling items, revenue by day, and stock to reorder.
- **Build a sales dashboard** in Power BI or Tableau from that data.

## Files

| File | Contents |
|---|---|
| [`coffee_shop.py`](coffee_shop.py) | The complete program |
| [`sample_receipt.txt`](sample_receipt.txt) | A receipt the program produced in a test run |
| `.gitignore` | Stops receipts created on your computer from being uploaded |
