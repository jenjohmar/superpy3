from helpers import *

# 1. variable bought_list gets the output (list) of get_bought(), sold_list gets the output (list) of get_sold() (with the date passed into get_inventory) and exp_list get the ouput (list) of get_expired() 
# 2. if bought_id in sold_list == product_id in bought_list, removes product from bought_list
# 3. if product_id in exp_list == product_id in bought_list, removes product from bought_list
# 4. inventory is now that which can be sold (not expired or already sold)
# 5. writes exp_list to separate csv 
# 6. it then stores the result of the function count_inventory, which displays the current amount of all products in inventory, in a variable called inv_list
# 7. if user passes in argument "all" he gets complete inventory (up to and including passed in date)
# 8. if user passes in argument "product" he gets the inventory for this product (up to and including passed in date)
def get_inventory(date: str, product: str):
    #checks if format of date is correct
    checkInvDate = checkDate(date)
    
    if checkInvDate == True:

        bought_list = get_bought(date)
        sold_list = get_sold(date)
        exp_list = get_expired(date)
        
        for sold_product in sold_list:
            for bought_product in bought_list:
                if sold_product[1] == bought_product[0]:
                    bought_list.remove(bought_product)

        for exp_product in exp_list:
            for bought_product in bought_list:
                if exp_product[0] == bought_product[0]:
                    bought_list.remove(exp_product)
        
    
        inv_list = count_inventory(bought_list)
        
        
        if len(bought_list) > 0:
            if product == "all":
                print_dict(inv_list)
            elif type(product) == str:
                if product in inv_list:
                    print_dict({product: inv_list[product]})
                else:
                    console.print("Product [bold underline]not[/] in inventory.")        
            else:
                console.print("Format not correct.", style="bold red")
            
        else:
            print("Nothing in inventory.")
    else:
        console.print(f"Please enter the date in correct format yyyy-mm-dd.", style="bold red")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Report inventory.")
                
    parser.add_argument("date", help="Enter date for the inventory on that date (format yyyy-mm-dd).")
    parser.add_argument("product", help="Enter product name (i.e. 'orange') in lowercase or 'all'.")


    args = parser.parse_args()

    get_inventory(date=args.date, product=args.product)



