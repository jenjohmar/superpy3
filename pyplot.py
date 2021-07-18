import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from helpers import *
import numpy as np
import datetime

dates = ["2021-06-01", "2021-06-23"]
x_values = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in dates]

y_values = [5, 8, 1, 10, 2]

ax = plt.gca()

formatter = mdates.DateFormatter("%Y-%m-%d")

ax.xaxis.set_major_formatter(formatter)

locator = mdates.DayLocator()
ax.xaxis.set_major_locator(locator)

plt.plot_date(x_values, y_values)
plt.show()