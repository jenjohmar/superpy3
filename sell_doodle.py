import argparse
from helpers import *


# 5. if amount > 1 each product gets own line and unique sold_id

def sell(prod_name: str, sell_price: float, sell_date: str, amount: int):
    #checks if format of date is correct, if yes executes code if not error message
    checkSellDate = checkDate(sell_date)
    if checkSellDate == True:
        create_csv("sold.csv", header_sold)
        
        number_of_lines = 0
        
        with open('sold.csv', 'r') as csv_file:
            for line in csv_file:
                # looks at current line count adss 1 to number_of_lines for each line, skips header
                if "sold_id" in line:
                    continue
                number_of_lines += 1

        # id is the same as number of lines counted
        id = number_of_lines

        # returns inventory of today  
        inventory = check_inventory(current_date, prod_name)
        items_to_be_sold = []
        

        # creates new dict from data passed in, adds sold_id + bought_id 
        new_product_dict = {
            "sold_id": id,
            "bought_id": 0,
            "product_name": prod_name,
            "sell_price": sell_price,
            "sell_date": sell_date,
        }
        
        sold_list = get_sold(current_date)
        
        #removes  all items from inventory that are not the requested product
        if len(sold_list) == 0:
            for item in inventory:
                if prod_name in item:
                    items_to_be_sold.append(item)
        else:
            for sold_item in sold_list:
                for item in inventory:
                    if prod_name in item and sold_item[1] != item[0]:
                        items_to_be_sold.append(item)
        
        # checks if there are enough items in inventory i.e. >= amount given
        if len(items_to_be_sold) >= amount:
            # reduces items in inventory to amount given
            items_to_be_sold = items_to_be_sold[:amount]
            # writes to sold amount times
            for product in items_to_be_sold:
                bought_id = product[0]
                id += 1
                new_product_dict["sold_id"] = id
                new_product_dict["bought_id"] = bought_id
                
                write_to_sold(new_product_dict) 
                        
            print(f"Product {prod_name} sold succesfully!")
        else:
            print(f"Amount exceeds product count in inventory! You can currently sell {len(items_to_be_sold)} of {prod_name}.")

        
    else:
        print("Please enter the date in correct format yyyy-mm-dd.")


# sell("peanut", 0.10, "2021-07-18", 2)
sell('laptop', 300, "2021-07-15", 1)
