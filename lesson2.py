import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("datasets/avocado.csv")

albany_df = df[df['region']=="Albany"]
albany_df.set_index("Date", inplace=True)

albany_df["AveragePrice"].plot()

