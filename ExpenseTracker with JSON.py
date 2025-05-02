from collections import OrderedDict
import json
import sys

BACK = "b"
EXIT = "*"

# I consciously decided not to ask the user if they want to continue adding/removing/editing a new expense/credit
# after they've done it once as it would not be time or logic efficient:
# it would require the same extra step required by being sent back to the main menu and having to reselect the same option(=no saved time);
# also, it would require a lot more code in order to prompt an input and to validate it

# Since this is an EXPENSE TRACKER and not a BANK ACCOUNT and it only abstractly registers transactions without dealing with actual money,
# expenses larger than the current budget are allowed and so are negative amounts for the total budget


def get_budget():
    while True:
        try:
            budget = float(input("Please enter your initial budget: "))
            return budget
        except ValueError:
            print("Invalid entry. Enter a number")


def add_item(type, type_dict):
    while True:
        description = input(
            f"Enter {type} description or '*' for main menu: ").strip().capitalize()
        # allow non-alphabetic descriptions as they might be meaningful to the user
        if description == EXIT:
            return
        else:
            while True:
                amount = input(
                    "Enter amount or 'b' for description or '*' for main menu: ").strip().lower()
                if amount == EXIT:
                    return
                if amount == BACK:
                    break
                else:
                    try:
                        amount = float(amount)
                        print(
                            f"ADDED {type.upper()}: {description}  AMOUNT: {amount} ")
                        type_dict[description] = type_dict.get(
                            description, 0) + amount
                        return
                    except ValueError:
                        print("Invalid entry")


def edit_item(type, type_dict):
    if not type_dict:
        print("The list is empty")
    else:
        while True:
            display_items(type_dict)
            choose = input(
                f"Which {type} would you like to edit? - Enter description or '*' for main menu: ").strip().capitalize()
            if choose == EXIT:
                return
            elif choose in type_dict.keys():
                while True:
                    edit = input(
                        f"Edit description or amount? - 'd'= description, 'a'= amount, 'b'= choose {type} again, '*'= main menu: ").strip().lower()
                    print()
                    if edit == BACK:
                        break
                    elif edit == EXIT:
                        return
                    elif edit == "d":
                        new_desc = edit_description(
                            type_dict, choose)
                        if new_desc:
                            return
                        else:
                            continue
                    elif edit == "a":
                        new_am = edit_amount(type_dict, choose)
                        if new_am:
                            return
                        else:
                            continue
                    else:
                        print("Invalid entry")
                        continue
            else:
                print(f"{type} not found\n")


def edit_description(dictionary, choose):
    new_desc = input(
        "Enter new description or '*' to go back: ").strip().capitalize()
    if new_desc == EXIT:
        return False
    else:
        new_entry = OrderedDict()

        for desc, amount in dictionary.items():
            if desc == choose:
                new_entry[new_desc] = dictionary[choose]
            else:
                new_entry[desc] = amount
        dictionary.clear()
        dictionary.update(new_entry)
        print(f"'{choose}' updated to '{new_desc}'")
        return dictionary


def edit_amount(dictionary, choose):
    while True:
        new_am = input(
            "Enter new amount or '*' to go back: ").strip()
        if new_am == EXIT:
            return False
        else:
            try:
                new_am = float(new_am)
                print(
                    f"{choose} updated from {dictionary[choose]} to {new_am}")
                dictionary[choose] = new_am
                return dictionary
            except ValueError:
                print("Invalid entry")


def remove_item(type, type_dict):
    if not type_dict:
        print(f"The {type} list is empty")
    else:
        while True:
            display_items(type_dict)
            choose = input(
                f"Which {type} would you like to remove? - Enter description or '*' for main menu: ").strip().capitalize()
            if choose == EXIT:
                return
            elif choose in type_dict.keys():
                while True:
                    sure = input(
                        f"Are you sure you want to permanently delete '{choose}'? - Enter y/n: ").lower().strip()
                    if sure == "y":
                        type_dict.pop(choose)
                        print(f"'{choose}' successfully removed")
                        return
                    elif sure == "n":
                        break
                    else:
                        print('Invalid entry')
            else:
                print(f"{type} not found\n")


def show_items(type, type_dict):
    print(f"\n{type.capitalize()}:")
    total = sum(type_dict.values())
    display_items(type_dict)
    print(f"Total {type}: {total}")


def show_total_budget(init_budget, budget, expenses, credit):
    print("\nBUDGET BREAKDOWN")
    if not expenses and not credit:
        print(f"\nNo expenses or credit. \nInitial budget {init_budget}")
    elif not credit:
        print(f"\nInitial budget: {init_budget}")
        show_items("expenses", expenses)
        print("\nNo credit added")
        print(f"\nRemaining budget: {budget}")
    elif not expenses:
        print(f"\nInitial budget: {init_budget}")
        print("\nNo expenses added")
        show_items("credit", credit)
        print(f"\nRemaining budget: {budget}")
    elif expenses and credit:
        print(f"\nInitial budget: {init_budget}")
        show_items("expenses", expenses)
        show_items("credit", credit)
        print(f"\nRemaining budget: {budget}")


def display_items(dictionary):
    for desc, amount in dictionary.items():
        print(f"- {desc}: {amount}")


def load_budget_data(saved_expenses_json):
    try:
        with open(saved_expenses_json) as f:
            data = json.load(f)
            return data['Initial budget'], data['expenses'], data['credit']
    except FileNotFoundError:
        return 0, {}, {}


def save_budget_details(init_budget, expenses, credit, saved_expenses_json):
    data = {'Initial budget': init_budget,
            'expenses': expenses, 'credit': credit}
    with open(saved_expenses_json, 'w') as f:
        json.dump(data, f, indent=2)


def main():
    print("Welcome to the expense tracker")
    saved_expenses_json = 'saved_expenses.json'
    init_budget, expenses, credit = load_budget_data(saved_expenses_json)
    if init_budget == 0:
        init_budget = get_budget()
        budget = init_budget
    else:
        budget = init_budget - sum(expenses.values()) + sum(credit.values())

    while True:

        print("\nWhat would you like to do?")
        print("1. Add an expense")
        print("2. Edit expense")
        print("3. Remove expense")
        print("4. Add credit")
        print("5. Edit credit")
        print("6. Remove credit")
        print("7. Show budget details")
        print("8. Exit and save")
        print("9. Exit without saving")
        choice = input("Enter choice (1/2/3/4/5/6/7/8): ").strip()

        if choice == "1":
            add_item("expense", expenses)
        elif choice == "2":
            edit_item("expense", expenses)
        elif choice == "3":
            remove_item("expense", expenses)
        elif choice == "4":
            add_item("credit", credit)
        elif choice == "5":
            edit_item("credit", credit)
        elif choice == "6":
            remove_item("credit", credit)
        elif choice == "7":
            show_total_budget(init_budget, budget, expenses, credit)
        elif choice == "8":
            while True:
                sure = input(
                    "Are you sure you want to save your updates? y/n: ").lower().strip()
                if sure == "y":
                    save_budget_details(init_budget, expenses,
                                        credit, saved_expenses_json)
                    print("Updates saved! Goodbye")
                    sys.exit()
                elif sure == "n":
                    break
                else:
                    print("Invalid entry")
        elif choice == "9":
            while True:
                sure = input(
                    "Are you sure you want to leave without saving? y/n: ").lower().strip()
                if sure == "y":
                    print("No updates saved. Goodbye")
                    sys.exit()
                elif sure == "n":
                    break
                else:
                    print("Invalid entry")
        else:
            print("Invalid entry. Please enter (1/2/3/4/5/6/7/8)")

        budget = init_budget - sum(expenses.values()) + sum(credit.values())


if __name__ == "__main__":
    main()
