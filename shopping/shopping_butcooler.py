"""
Grocery shopping simulator (v2).

Practice: functions with arguments and return values, nested dictionaries,
input validation, and keeping game state in one place instead of globals.

Money is stored in cents (integers) so we never get floating-point junk
like 97.53999999999999 on screen. money() turns cents into a "$1.23" string.
"""

START_CASH = 10_000        # cents -> $100.00
SELL_PERCENT = 50          # shops buy goods back at 50% of their selling price

GOODS = ("apples", "bread", "butter", "cheese", "eggs",
         "flour", "milk", "pasta", "sausage")

# price in cents, stock in pieces
shops = {
    "Shop 1": {
        "apples":  {"price": 246, "stock": 200},
        "bread":   {"price": 189, "stock": 100},
        "butter":  {"price": 329, "stock": 80},
        "cheese":  {"price": 475, "stock": 60},
        "eggs":    {"price": 299, "stock": 120},
        "flour":   {"price": 149, "stock": 150},
        "milk":    {"price": 179, "stock": 100},
        "pasta":   {"price": 219, "stock": 130},
        "sausage": {"price": 549, "stock": 70},
    },
    "Shop 2": {
        "apples":  {"price": 289, "stock": 140},
        "bread":   {"price": 159, "stock": 180},
        "butter":  {"price": 375, "stock": 55},
        "cheese":  {"price": 429, "stock": 90},
        "eggs":    {"price": 349, "stock": 75},
        "flour":   {"price": 129, "stock": 200},
        "milk":    {"price": 209, "stock": 65},
        "pasta":   {"price": 179, "stock": 160},
        "sausage": {"price": 499, "stock": 45},
    },
}


# ---------- small helpers ----------

def money(cents):
    """12345 -> '$123.45'"""
    return f"${cents / 100:.2f}"


def sell_price(price):
    """What a shop pays you for one item."""
    return price * SELL_PERCENT // 100


def ask_choice(prompt, valid):
    """Keep asking until the answer is one of `valid` (case-insensitive)."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in valid:
            return answer
        print(f"Please choose one of: {', '.join(valid)}")


def pick_item():
    """Ask for an item by number or name. Returns the name, or None for 'back'."""
    while True:
        answer = input("Which item? (number or name, 0 = back) ").strip().lower()
        if answer == "0":
            return None
        if answer.isdigit() and 1 <= int(answer) <= len(GOODS):
            return GOODS[int(answer) - 1]
        if answer in GOODS:
            return answer
        print("Pick a valid item from the list.")


def ask_quantity(item, limit, verb):
    """Ask for a whole number between 1 and `limit`."""
    while True:
        answer = input(f"How many {item} do you want to {verb}? (1-{limit}) ")
        try:
            quantity = int(answer)
        except ValueError:
            quantity = 0
        if 1 <= quantity <= limit:
            return quantity
        print(f"Enter a whole number from 1 to {limit}.")


# ---------- game actions ----------

def show_shop(name, items):
    print(f"\nWelcome to {name}. On the shelves:")
    for number, item in enumerate(GOODS, start=1):
        info = items[item]
        print(f"{number}. {item:<8} {money(info['price']):>7}"
              f"   (in stock: {info['stock']})")


def buy_item(player, items, item):
    price = items[item]["price"]
    limit = min(items[item]["stock"], player["cash"] // price)

    if limit == 0:
        if items[item]["stock"] == 0:
            print(f"Sorry, no {item} left.")
        else:
            print(f"You can't afford even one ({money(price)}).")
        return

    quantity = ask_quantity(item, limit, "buy")
    cost = price * quantity
    player["cash"] -= cost
    items[item]["stock"] -= quantity
    player["bag"][item] = player["bag"].get(item, 0) + quantity
    print(f"You bought {quantity} {item} for {money(cost)}. "
          f"You have {money(player['cash'])} left.")


def sell_item(player, items, item):
    have = player["bag"].get(item, 0)
    if have == 0:
        print(f"You have no {item} to sell.")
        return

    unit = sell_price(items[item]["price"])
    print(f"This shop pays {money(unit)} per piece.")
    quantity = ask_quantity(item, have, "sell")
    income = unit * quantity
    player["cash"] += income
    items[item]["stock"] += quantity
    player["bag"][item] -= quantity
    if player["bag"][item] == 0:
        del player["bag"][item]          # keep the bag free of zero entries
    print(f"You sold {quantity} {item} for {money(income)}. "
          f"You have {money(player['cash'])}.")


def visit_shop(player, name, items):
    while True:
        show_shop(name, items)
        print(f"\nCash: {money(player['cash'])}")
        action = ask_choice("(B)uy, (S)ell or (L)eave? ", ("b", "s", "l"))
        if action == "l":
            return

        item = pick_item()
        if item is None:
            continue
        if action == "b":
            buy_item(player, items, item)
        else:
            sell_item(player, items, item)


def show_inventory(player):
    print(f"\nYou have {money(player['cash'])} in your pocket.")
    if not player["bag"]:
        print("Your bag is empty. Buy something NOW!")
        return
    print("Your shopping bag contains:")
    for number, (item, amount) in enumerate(player["bag"].items(), start=1):
        print(f"{number}. {item}: {amount}")


def go_home(player):
    print(f"\nYou came home with {money(player['cash'])} in your wallet.")
    if not player["bag"]:
        print("You haven't bought anything in the end. "
              "But tomorrow is another day.")
    else:
        print("You managed to buy:")
        for item, amount in player["bag"].items():
            print(f"  {item}: {amount}")
        print("This will keep you alive for some time.")


# ---------- main loop ----------

def main():
    player = {"cash": START_CASH, "bag": {}}
    shop_names = list(shops)
    inventory_key = str(len(shop_names) + 1)
    home_key = str(len(shop_names) + 2)
    valid = tuple(str(n) for n in range(1, len(shop_names) + 3))

    while True:
        print(f"\nYou have {money(player['cash'])}. Where do you go?")
        for number, name in enumerate(shop_names, start=1):
            print(f"{number}) {name}")
        print(f"{inventory_key}) Inventory")
        print(f"{home_key}) Home")

        choice = ask_choice(f"Pick number 1-{home_key}: ", valid)

        if choice == inventory_key:
            show_inventory(player)
        elif choice == home_key:
            go_home(player)
            break                         # no exit() needed, the loop just ends
        else:
            name = shop_names[int(choice) - 1]
            visit_shop(player, name, shops[name])


if __name__ == "__main__":
    main()
