from helpers import *

# 1. variable bought_list gets the output (list) of get_bought(), sold_list gets the output (list) of get_sold() (with the date passed into get_inventory) and exp_list get the ouput (list) of get_expired() 
# 2. if user passes in "all" the turnover of complete inventory is displayed within specified time frame (start_date, end_date)
# 3. if user passes in a product the turnover for this product is displayed within specified time frame
# 4. error message if type of product passed in is incorrect
# 5. error message if product passed in does not exist in inventory
def profit(start_date: str, end_date: str, product: str):
    #checks if format of dates are correct
    checkStartDate = checkDate(start_date)
    checkEndDate = checkDate(end_date)

    if checkStartDate == True and checkEndDate == True:

        bought_list = get_bought(end_date)
        sold_list   = get_sold(end_date)
        exp_list    = get_expired(end_date)
        
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
                sell_date = sold_product[4]
                if sell_date >= start_date and sell_date <= end_date:
                    sell_price = float(sold_product[3])
                    total_sold += sell_price
            
            for exp_product in exp_list:
                exp_date = exp_product[4]
                if exp_date >= start_date and exp_date < end_date:
                    buy_price = float(exp_product[2])
                    total_exp += buy_price
            
            profit = (total_sold - total_bought) - total_exp
            
            print(f"The total profit from {start_date} until {end_date} for {product} is {profit:.2f}")
                    
            
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
                        sell_date = sold_product[4]
                        if product in sold_product and sell_date >= start_date and sell_date <= end_date:
                            sell_price = float(sold_product[3])
                            total_sold += sell_price

                    for exp_product in exp_list:
                        exp_date = exp_product[4]
                        if product in exp_product and exp_date >= start_date and exp_date < end_date:
                            buy_price = float(exp_product[4])
                            total_sold += buy_price

                    profit = (total_sold - total_bought) - total_exp
                    print(f"The total profit from {start_date} until {end_date} for {product} is {profit:.2f}.")

                    return    
                
            print("Product not in inventory.")    
            
        else:
            print("Please enter a valid product name (i.e. 'orange') or 'all'.")
    else:
        print(f"Please enter the [underline]dates[/] in correct format yyyy-mm-dd.")

profit("2021-01-01", "2021-07-18", "laptop")