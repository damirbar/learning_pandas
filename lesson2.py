import pandas as pd
import matplotlib.pyplot as plt

from helpers import hdr

df = pd.read_csv("datasets/avocado.csv")

# Convert the Date column to datetime objects
df['Date'] = pd.to_datetime(df['Date'])

hdr("df.head()")
print(df.head())

albany_df = df.copy()[df['region']=="Albany"]
albany_df.set_index("Date", inplace=True)

albany_df["AveragePrice"].plot()
plt.show()

# Moving average of size 25
albany_df["AveragePrice"].rolling(25).mean().plot()
plt.show()
# It doesn't look right.
# We need to sort the dataset by the Date, which is the index:
albany_df.sort_index(inplace=True)

albany_df["AveragePrice"].rolling(25).mean().plot(title="AveragePrice with rolling average=25")
plt.show()

# Put this data as a new column in our dataframe:
albany_df["price25ma"] = albany_df["AveragePrice"].rolling(25).mean()

hdr("albany_df.head()")
print(albany_df.head())

hdr("albany_df.tail()")
print(albany_df.tail())


# The next step is to get a list of all the regions:
print("df['region'].unique()")
print(df['region'].unique()) # Returns the type numpy.ndarray

# Now we will graph prices in the different regions:

def generate_graph_df(df):
    graph_df = pd.DataFrame()
    unique_regions = df['region'].unique()
    print(unique_regions)

    for region in unique_regions: # We'll use 16 regions to avoid exploding the RAM
        region_df = df.copy()[ df['region'] == region ]
        region_df.set_index("Date", inplace=True)
        region_df.sort_index(inplace=True)
        region_df[f'{region}_price25ma'] = region_df['AveragePrice'].rolling(25).mean()

        if graph_df.empty:
            # The double square brackets indicate a dataframe, rather than a series
            graph_df = region_df[[f'{region}_price25ma']]

        else:
            graph_df = graph_df.join(region_df[f'{region}_price25ma'])

    return graph_df

# We CANNOT run generate_graph_df yet due to an issue in the dataset: Dates are still
#   getting duplicated. The issue is that avocados have multiple types, Organic and Conventional.
#   Let's choose organic:

df = pd.read_csv("datasets/avocado.csv")
df = df.copy()[df['type']=='organic']

df["Date"] = pd.to_datetime(df["Date"])

df.sort_values(by="Date", ascending=True, inplace=True)
hdr("df.head() with only organic type")
print(df.head())


graph_df = generate_graph_df(df)

hdr("graph_df.tail()")
print(graph_df.tail())

# Now we can plot this dataframe regularly with pandas, but it would be too complicated and the legend is too massive.
# We could use a matplotlib plot, but for now let's just suppress the legend:
graph_df.dropna().plot(figsize=(8,5), legend=False)
plt.show()

