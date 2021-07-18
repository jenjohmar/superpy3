# Imports
import argparse
import csv
import datetime as dt
from datetime import date, time
import os
import operator
from types import new_class


# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'

current_date = dt.date.today()

header_bought       = ["product_id", "product_name", "buy_price", "buy_date", "exp_date"]
header_sold         = ["product_id", "bought_id",  "product_name", "sell_date", "sell_price"]

# writes the data from the dictionary passed in through the buy function, to bought.csv 
def write_to_bought(bought_dict): # new_product_dict from buy function gets passed in
    create_csv("bought.csv", header_bought)
    with open('bought.csv', 'a', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=header_bought)
        csv_writer.writerow(bought_dict)

# writes the data from the dictionary passed in through the sell function, to sold.csv
def write_to_sold(sold_dict): # new_product_dict from sell function gets passed in
    create_csv("sold.csv", header_sold)
    with open('sold.csv', 'a', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=header_sold)
        csv_writer.writerow(sold_dict)

# 1. opens bought.csv looks at current total line count
# 2. increments total line count with 1 = id
# 3. creates new dict from data passed in and adds the id
# 4. writes dict to bought.csv
# 5. if amount > 1 each product gets own line and unique id

def buy(prod_name: str, buy_price: float, buy_date: str, exp_date: str, amount: int):
    number_of_lines = 0
    with open('bought.csv', 'r') as csv_file:
        for line in csv_file:
            number_of_lines += 1

    id = number_of_lines

    new_product_dict = {
        "product_id": id,
        "product_name": prod_name,
        "buy_price": buy_price,
        "buy_date": buy_date,
        "exp_date": exp_date,
    }
    for i in range(amount):
        old_id = new_product_dict["product_id"]
        new_id = old_id + 1
        new_product_dict["product_id"] = new_id
        write_to_bought(new_product_dict)

# 1. opens sold.csv looks at current total line count
# 2. increments total line count with 1 = id
# 3. creates new dict from data passed in, adds id + finds bought_id and adds that
# 4. writes dict to sold.csv
# 5. if amount > 1 each product gets own line and unique sold_id

def sell(prod_name: str, sell_date: str, sell_price, amount):
    number_of_lines = 0
    with open('sold.csv', 'r') as csv_file:
        for line in csv_file:
            number_of_lines += 1

    id = number_of_lines
 
    new_product_dict = {
        "product_id": id,
        "bought_id": 0,
        "product_name": prod_name,
        "sell_date": sell_date,
        "sell_price": sell_price,
    }
    
    # 1. makes sure product id is incremented by 1 for each row so each product has unique sold id
    # 2. searches bought_id for each product and adds that to each product
    # 3. calls write_to_sold, row created for each unique product 
    for number in range(amount):
        old_id = new_product_dict["product_id"]
        new_id = old_id + 1
        new_product_dict["product_id"] = new_id

        bought_id = find_product_id(prod_name, "bought.csv", (number + 1))

        new_product_dict["bought_id"] = bought_id

        write_to_sold(new_product_dict)

# 1. variable bought_list gets the output (list) of get_bought(), sold_list gets the output (list) of get_sold() (with the date passed into get_inventory) and exp_list get the ouput (list) of get_expired() 
# 2. if bought_id in sold_list == product_id in bought_list, removes product from bought_list
# 3. if product_id in exp_list == product_id in bought_list, removes product from bought_list
# 4. inventory is now that which can be sold (not expired or already sold)
# 5. writes exp_list to separate csv 
# 6. it then stores the result of the function count_inventory, which displays the current amount of all products in inventory, in a variable called inv_list
# 7. if user passes in argument "all" he gets complete inventory (up to and including passed in date)
# 8. if user passes in argument "product" he gets the inventory for this product (up to and including passed in date)
def get_inventory(date, product):
    bought_list = get_bought(date)
    sold_list = get_sold(date)
    exp_list = get_expired()
    
    if len(sold_list) == 0:
        return(bought_list)
    
    for sold_product in sold_list:
        for bought_product in bought_list:
            if sold_product[1] == bought_product[0]:
                bought_list.remove(bought_product)

    for exp_product in exp_list:
        for bought_product in bought_list:
            if exp_product[0] == bought_product[0]:
                bought_list.remove(exp_product)
    
    store_expired(exp_list)
    
    inv_list = count_inventory(bought_list)

    if product == "all":
        print_dict(inv_list)
    elif type(product) == str:
        if product in inv_list:
            print_dict({product: inv_list[product]})
        else:
            print("Product not found.")        
    else:
        print("Format not correct.")

# 1. variable bought_list gets the output (list) of get_bought(), sold_list gets the output (list) of get_sold() (with the date passed into get_inventory) and exp_list get the ouput (list) of get_expired() 
# 2. if user passes in "all" the turnover of complete inventory is displayed within specified time frame (start_date, end_date)
# 3. if user passes in a product the turnover for this product is displayed within specified time frame
# 4. error message if type of product passed in is incorrect
# 5. error message if product passed in does not exist in inventory
def turnover(start_date, end_date, product):
    bought_list = get_bought(end_date)
    sold_list   = get_sold(end_date)
    exp_list    = get_expired()
    
    if product == "all":
        total_bought = 0
        total_sold   = 0
        total_exp    = 0
        
        for bought_product in bought_list:
            buy_date = bought_product[3]
            if buy_date >= start_date and buy_date <= end_date:
                buy_price = float(bought_product[2])
                total_bought += buy_price
        
        for sold_product in sold_list:
            sell_date = sold_product[3]
            if sell_date >= start_date and sell_date <= end_date:
                sell_price = float(sold_product[4])
                total_sold += sell_price
        
        for exp_product in exp_list:
            exp_date = exp_product[4]
            if exp_date >= start_date and exp_date <= end_date:
                buy_price = float(exp_product[2])
                total_exp += buy_price
        
        
        profit = (total_sold - total_bought) - total_exp
        
        print(f"The total turnover from {start_date} until {end_date} for {product} is {profit:.2f}")
         
    elif type(product) == str:
        total_bought = 0
        total_sold   = 0
        total_exp    = 0
        for list_item in bought_list:
            if product in list_item:
                for bought_product in bought_list:
                    buy_date = bought_product[3]
                    if product in bought_product and buy_date >= start_date and buy_date <= end_date:
                        buy_price = float(bought_product[2])
                        total_bought += buy_price

                for sold_product in sold_list:
                    sell_date = sold_product[3]
                    if product in sold_product and sell_date >= start_date and sell_date <= end_date:
                        sell_price = float(sold_product[4])
                        total_sold += sell_price

                for exp_product in exp_list:
                    exp_date = exp_product[4]
                    if product in exp_product and exp_date >= start_date and exp_date <= end_date:
                        buy_price = float(exp_product[4])
                        total_sold += buy_price

                profit = (total_sold - total_bought) - total_exp
                print(f"The total turnover from {start_date} until {end_date} for {product} is {profit:.2f}")

                return    
            
        print("Product not in inventory.")    
        
    else:
        print("Please enter a valid product name or 'all'.")
            

# HELPER FUNCTIONS

# creates needed csv database if it doesn't yet exist
def create_csv(name_csv, header):
    current_dir = os.getcwd() + ("/" + name_csv)
    if not os.path.exists(current_dir):
        with open(name_csv, 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=header)
            csv_writer.writeheader()
            
# 1. finds bought id (in bought.csv) of the Nth product given to sell function
# 2. return bought_id for each product
def find_product_id(product_name, csv, n):
    found = 0
    with open(csv, 'r') as csv_file:
        for list_item in csv_file:
            if product_name in list_item:
                found += 1
                if found == n:
                    li = list(list_item.split(","))
                    return li[0]

# 1. reads bought.csv and skips header line
# 2. looks for buy date (str) in line, stores this date as date-object
# 3. compares buy date to date passed in as argument in get_inventory()
# 4. if buy date <= to date passed in, adds product to bought_list as list
# 5. returns bought_list
def get_bought(date):
    date = dt.datetime.strptime(date, "%Y-%m-%d").date()
    bought_list = []

    with open('bought.csv', 'r') as csv_file:
        for line in csv_file:
            if "product_id" in line:
                continue
            line = line[:-1]
            buy_date = line.split(",")[3]
            buy_date = dt.datetime.strptime(buy_date, "%Y-%m-%d").date()
            
            if buy_date <= date:
                bought_list.append(line.split(","))
                 
    return bought_list 

# 1. reads sold.csv and skips header line
# 2. looks for sell date (str) in line, stores this date as date-object
# 3. compares sell date to date passed in as argument in get_inventory()
# 4. if sell date <= to date passed in, adds product to sold_list 
# 5. returns sold_list
def get_sold(date):
    date = dt.datetime.strptime(date, "%Y-%m-%d").date()
    sold_list = []

    with open('sold.csv', 'r') as csv_file:
        for line in csv_file:
            if "product_id" in line:
                continue
            line = line[:-1]
            sell_date = line.split(",")[3]
            sell_date2 = dt.datetime.strptime(sell_date, "%Y-%m-%d").date()

            if sell_date2 <= date:
                sold_list.append(line.split(","))

    return sold_list

# 1. reads bought.csv and skips header line
# 2. looks for exp_date (str) in line, stores this date as date-object
# 3. compares exp_date to current date
# 4. if exp_date < to current date, adds product to exp_list 
# 5. returns exp_list
def get_expired():
    exp_list = []
    with open("bought.csv", "r") as csv_file:
        for line in csv_file:
            if "product_id" in line:
                continue
            line = line[:-1]
            exp_date = line.split(",")[4]
            exp_date = dt.datetime.strptime(exp_date, "%Y-%m-%d").date()
            if exp_date < current_date:
                exp_list.append(line.split(","))
   
    return exp_list

# 1. creates expired.csv
# 2. opens expired.csv in write mode
# 3. writes each item from exp_list as row to expired.csv
def store_expired(exp_list):
    create_csv("expired.csv", header_bought)
    with open("expired.csv", "w", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(exp_list)


# 1. "list" = list of the first elements of lists in bought_list passed in via get_inventory()
# 2. list items from list are stored in new_dict with their amount
# 3. returns new_dict
def count_inventory(list1):
    list = [item[1] for item in list1]
    new_dict = {}

    for product in list:
        if product not in new_dict:
            count = list.count(product)
            new_dict[product] = count
    return new_dict        

# 1. prints header
# 2. prints product name and amount
def print_dict(dict):
    print(f"Product, Amount")
    for product, count in dict.items():
        print(f"{product}, {count}")
        
# run code    
def main():
    # create_csv("bought.csv", header_bought)
    # create_csv("sold.csv", header_sold)
        
    # buy("shampoobar", 1.32, "2021-6-16", "2021-6-1", 5)
    # buy("peanut", 0.03, "2021-6-8", "2030-3-02", 5)
    # buy("apple", 0.87, "2021-6-17", "2021-6-25", 5)
    
    # sell("peanut", "2021-6-10", 0.10, 1)
    # sell("peanut", "2021-6-17", 0.10, 1)

    print(get_inventory("2021-6-16", "all"))
    # print(get_inventory("2021-6-17"), len(get_inventory("2021-6-17")))
    # get_inventory("2021-6-18", "all")
    # turnover("2021-6-1", "2021-6-9", "all")
    # turnover("2021-6-1", "2021-6-17", "peanut")
    # turnover("2021-6-18", 3)
    # turnover("2021-6-18", "orange")
    
    
    
if __name__ == '__main__':
    main()
    

