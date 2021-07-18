# Imports
import argparse
import csv
import datetime as dt
from datetime import date, time
import os
import operator
from types import new_class
from rich.console import Console
from rich.traceback import install
install()


console = Console()

current_date = dt.date.today()
current_date = current_date.strftime("%Y-%m-%d")

header_bought       = ["bought_id", "product_name", "buy_price", "buy_date", "exp_date"]
header_sold         = ["sold_id", "bought_id",  "product_name", "sell_price", "sell_date"]

# creates needed csv database if it doesn't yet exist
def create_csv(name_csv, header):
    current_dir = os.getcwd() + ("/" + name_csv)
    if not os.path.exists(current_dir):
        with open(name_csv, 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=header)
            csv_writer.writeheader()

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

    create_csv("bought.csv", header_bought)

    with open('bought.csv', 'r') as csv_file:
        for line in csv_file:
            if "bought_id" in line:
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
    
    create_csv("sold.csv", header_sold)

    with open('sold.csv', 'r') as csv_file:
        for line in csv_file:
            if "sold_id" in line:
                continue
            line = line[:-1]
            sell_date = line.split(",")[4]
            sell_date2 = dt.datetime.strptime(sell_date, "%Y-%m-%d").date()

            if sell_date2 <= date:
                sold_list.append(line.split(","))

    return sold_list

# 1. reads bought.csv and skips header line
# 2. looks for exp_date (str) in line, stores this date as date-object
# 3. compares exp_date to current date
# 4. if exp_date < to current date, adds product to exp_list 
# 5. returns exp_list
def get_expired(date):
    date = dt.datetime.strptime(date, "%Y-%m-%d").date()
    exp_list = []
    with open("bought.csv", "r") as csv_file:
        for line in csv_file:
            if "bought_id" in line:
                continue
            line = line[:-1]
            exp_date = line.split(",")[4]
            exp_date = dt.datetime.strptime(exp_date, "%Y-%m-%d").date()
            if exp_date < date:
                exp_list.append(line.split(","))
   
    return exp_list

# 1. creates expired.csv
# 2. opens expired.csv in write mode
# 3. writes each item from exp_list as row to expired.csv
# def store_expired(exp_list):
#     create_csv("expired.csv", header_bought)
#     with open("expired.csv", "w", newline='') as csv_file:
#         writer = csv.writer(csv_file)
#         writer.writerows(exp_list)

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
    print("Product, Amount")
    for product, count in dict.items():
        print(f"{product}, {count}")

#creates txt file in turnover function
def create_txt(file):
    current_dir = os.getcwd() + ("/" + file)
    if not os.path.exists(current_dir):
        txt_file = open(file, "w+")

# checks inventory in sell function to see if product can be sold
def check_inventory(date, product):
    bought_list = get_bought(date)
    sold_list = get_sold(date)
    exp_list = get_expired(date)
    
    if len(sold_list) == 0:
        return bought_list
    
    for sold_product in sold_list:
        for bought_product in bought_list:
            if sold_product[1] == bought_product[0]:
                bought_list.remove(bought_product)

    for exp_product in exp_list:
        for bought_product in bought_list:
            if exp_product[0] == bought_product[0]:
                bought_list.remove(exp_product)
    
    return bought_list

# check to see if dates are passed in in the correct format
def checkDate(date):
    count_num = 0
    count_dash = 0

    for i in date:
        if i.isnumeric():
            count_num += 1
        if i == "-":
            count_dash += 1
    if (count_num < 6 or count_num > 8) or count_dash != 2:
        return False

    else:
        return True