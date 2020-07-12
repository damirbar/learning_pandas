import pandas as pd
import matplotlib.pyplot as plt
from helpers import hdr

# df is a dataframe
df = pd.read_csv("datasets/avocado.csv")

# First x rows
hdr("df.head(4)")
print(df.head(4))

# Last x rows
hdr("df.tail(5)")
print(df.tail(5))

# Get the column AveragePrice
hdr("df['AveragePrice'].head()")
print(df['AveragePrice'].head())

# The dot notation is uncommon! (df.AveragePrice.head())

# Get all rows where region == Albany
albany_df = df[ df['region'] == "Albany" ]
# The result is a new dataframe

hdr("albany_df.head()")
print(albany_df.head())

# Show the indexes of the dataframe
hdr("albany_df.index")
print(albany_df.index)


# Set the Date column as the new index of the dataframe.
# This will return a dataframe, but will not change the "albany_df" dataframe:
# albany_df.set_index("Date")
# So we can either do this:
# albany_df = albany_df.set_index("Date")
# Or we can use the "inplace" parameter:
albany_df.set_index("Date", inplace=True)

hdr("albany_df with Date as index")
print(albany_df.head())

albany_df['AveragePrice'].plot()
plt.show()
