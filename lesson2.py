import pandas as pd
import matplotlib.pyplot as plt

from helpers import hdr

df = pd.read_csv("datasets/avocado.csv")

# Convert the Date column to datetime objects
df['Date'] = pd.to_datetime(df['Date'])

hdr("df.head()")
print(df.head())

albany_df = df[df['region']=="Albany"]
albany_df.set_index("Date", inplace=True)

albany_df["AveragePrice"].plot()
plt.show()

# Rolling average of size 25
albany_df["AveragePrice"].rolling(25).mean().plot()
plt.show()
# It doesn't look right.
# We need to sort the dataset by the Date, which is the index:
albany_df.sort_index(inplace=True)

albany_df["AveragePrice"].rolling(25).mean().plot(title="AveragePrice with rolling average=25")
plt.show()



