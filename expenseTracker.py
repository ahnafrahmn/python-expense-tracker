import os
import sys
import json
import datetime

file_path = "./Expense-Tracker/data.json"




def main():
    load_from_file()
    while True:
        menu()


def load_from_file():
    global expense_list, Total_Expense
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                expense_list = data.get("expenses", [])
                Total_Expense = data.get("total_expense", 0.00)
        except (FileNotFoundError, json.JSONDecodeError):
            expense_list = []
            Total_Expense = 0.0

    else:
        expense_list = []
        Total_Expense = 0.00

def save_to_file():
    with open(file_path, "w") as f:
        json.dump({"expenses" : expense_list, "total_expense" : Total_Expense}, f, indent=4)




def menu():
    print("="*55)
    print(" "*19, "Expense Tracker 💰")
    print("="*55)

    print("\
          \t (1) Add Expense\n\
          \t (2) View Expenses\n\
          \t (3) Delete Expense\n\
          \t (4) Show Summary\n\
          \t (5) Exit\n\
          ")
    opt = ask_Valid_Int(" Enter Option : ", 1, 5)

    match opt:
        case 1: add_expense()
        case 2: view_expenses()
        case 3: delete_expense()
        case 4: show_summary()
        case 5: exit_app()

def add_expense():
    global Total_Expense, expense_list
    print("="*55)
    expCatag = input(" Enter Category (Food, Transport, Rent, etc.): ").title()
    expAmount = ask_Valid_Float(" Enter Amount : ", 0, float('inf'))
    
    Total_Expense += expAmount
    expense_list.append({"date" : datetime.date.today().strftime("%d/%m/%y"), "category" : expCatag, "amount" : expAmount})
    
    print(" Expense Added Successfully! ✅\n\n")
    save_to_file()


    
def view_expenses():
    print("="*55)
    if Total_Expense:
        print("\n\n Date ", " "*5, "Expense Category ", " "*10, " Expense Amount ")
        print("="*55)
        for i in expense_list:
            print(f" {i['date']:<13} {i['category']:<30} ${i['amount']:<10.2f}")
        print("-"*55)
        print(f"\t Total Expense\t:\t${Total_Expense:.2f} \n\n")
        
    else:
        print("\n\n Expense list is empty!\n Add Expense to View.\n\n")

def delete_expense():
        global Total_Expense
        if Total_Expense < 1:
            print("\n\n Expense list is empty! \n Add Expense to Delete. \n\n")
            return
        print("\n\n", "="*55)
        opt = ask_Valid_Int(" (1) Delete expense of a category.\n (2) Delete them all \n\n Enter an option : ", 1, 2)
        match opt:
            case 1: 
                view_expenses()
                while True:
                    opt1 = input("\n Enter the category name to delete it : ").title()
                    for i in expense_list:
                        if opt1 == i["category"]:
                            Total_Expense -= i["amount"]
                            expense_list.remove(i)
                            save_to_file()
                            print(f"\n Expenses of '{opt1}' has been deleted successfully! \n\n")
                            view_expenses() 
                            return
                    print(" \n Invalid Category Name !! ")
                    opt2 = ask_Valid_Int("\n (1) Try Again \n (2) Back to Menu \n Enter your option : ", 1, 2)
                    if opt2 == 2:
                        return
                    
            case 2:
                expense_list.clear()
                Total_Expense = 0.00
                print(f"\n All expenses deleted successfully! \n\n")
                save_to_file()
        

def show_summary():
    print("\n\n", "="*55)
    print("-"*18, "> Expense Summary <", "-"*18)
    global Total_Expense
    print(f"\n Total Expenses : ${Total_Expense}")
    maxdict = max(expense_list, key=lambda x: x['amount'])
    if maxdict['amount'] > 0:
        print(f" Maximum Spending Category : {maxdict['category']}, Amount : ${maxdict['amount']} \n\n")
    else:
        print(" No Expenses to Summarize.\n\n")

def exit_app():
    print("\n\n\n Goodbye! 👋 Your expenses are saved. \n\n")
    save_to_file()
    sys.exit()



def ask_Valid_Int(s, x=None, y=None):  # this function will retrun when user input is integer and also in the range of x <= input <= y
    while True:
        temp = input(s)
        try:
            if not is_Digit(temp) or y < int(temp) or int(temp) < x:    # to use this function you have to add "is_Digit(n)" function, that's given below
                print("\t **Invalid Input !!\n") 
            else:
                return int(temp)
        except TypeError:
            if not is_Digit(temp):    # to use this function you have to add "is_Digit(n)" function, that's given below
                print("\t **Invalid Input !!\n") 
            else:
                return int(temp)

def ask_Valid_Float(s, x=None, y=None):  # this function will retrun when user input is float and also in the range of x <= input <= y
    while True:
        temp = input(s)
        try:
            if not is_Float(temp) or y < float(temp) or float(temp) < x:    # to use this function you have to add "is_Float(n)" function, that's given below
                print("\t **Invalid Input !!\n") 
            else:
                return round(float(temp), 2)
        except TypeError:
            if not is_Float(temp):    # to use this function you have to add "is_Float(n)" function, that's given below
                print("\t **Invalid Input !!\n") 
            else:
                return round(float(temp), 2)
        
# it's "is_Digit(n)" function, this function takes any type of variable and checks if thats digit or not. 
def is_Digit(n):
    try:
        int(n)
        return True
    except ValueError:
        return False

def is_Float(n):
    try:
        float(n)
        return True
    except ValueError:
        return False


main()