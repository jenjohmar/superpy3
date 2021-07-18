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
                        
            console.print(f"Product {prod_name} sold succesfully!", style="bold green")
        else:
            console.print(f"Amount exceeds product count in inventory! You can currently sell {len(inventory)} of {prod_name}.")

        
    else:
        console.print("Please enter the date in correct format yyyy-mm-dd.", style="bold red")
                        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sell product(s).")
                
    parser.add_argument("prod_name", help="Enter product name in lowercase (i.e. 'orange').")
    parser.add_argument("sell_price", type=float, help="Enter product sell price (format: 0.00).")
    parser.add_argument("sell_date", help="Enter product sell date (format: yyyy-mm-dd).")
    parser.add_argument("amount", type=int, help="Enter amount (number) to sell.")

    args = parser.parse_args()

    sell(prod_name=args.prod_name, sell_price=args.sell_price, sell_date=args.sell_date, amount=args.amount)
