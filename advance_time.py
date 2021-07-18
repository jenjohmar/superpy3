from helpers import *

# advances time
def advance_time(num):
    current_date = dt.date.today()
    num = int(num)
    for i in range(num):
        current_date += dt.timedelta(days=1)
    print(current_date)

parser = argparse.ArgumentParser(description="Advance date with specified number of days")
            
parser.add_argument("number", help="Enter number of days you wish to advance.")

args = parser.parse_args()

advance_time(num=args.number)
