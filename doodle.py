
date = "2021-11-"

def checkDate(string_date):
    count_num = 0
    count_dash = 0
    
    for i in string_date:
        if i.isnumeric():
            count_num += 1
        if i == "-":
            count_dash += 1
    
    if (count_num != 6 and count_number != 7) or (count_dash != 2):
    
        print(f"Please enter the date in correct format yyyy-m-d")

checkDate(date)