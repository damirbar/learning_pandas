import pandas as pd
import matplotlib.pyplot as plt
from helpers import hdr

'''
Description of the data:

Year: Year of data

State: State/Territory of data

Table_Data: The scraped, unclean data from the US Department of Labor.

Footnote: The footnote associated with Table_Data, provided by the US Department of Labor.

High.Value: As there were some values in Table_Data that had multiple values (usually associated with footnotes),
this is the higher of the two values in the table. It could be useful for viewing the proposed minimum wage, because
in most cases, the higher value meant that all persons protected under minimum wage laws eventually had minimum wage
set at that value.

Low.Value: This is the same as High.Value, but has the lower of the two values. This could be useful for viewing the
effective minimum wage at the year of setting the minimum wage, as peoples protected under such minimum wage laws made
that value during that year (although, in most cases, they had a higher minimum wage after that year).

CPI.Average: This is the average Consumer Price Index associated with that year. It was used to calculate
2018-equivalent values.

High.2018: This is the 2018-equivalent dollars for High.Value.

Low.2018: This is the 2018-equivalent dollars for Low.Value.
'''

# Displaying all columns without '...'
pd.options.display.width = 0

df = pd.read_csv('datasets/Minimum Wage Data.csv', encoding="latin")
df.to_csv('datasets/minwage.csv', encoding="utf-8")
df = pd.read_csv('datasets/minwage.csv')

hdr("df.head()")
print(df.head())

# Now we use group-by:
gb = df.groupby('State')

hdr("gb.get_group('Alabama').set_index('Year').head()")
print(gb.get_group('Alabama').set_index('Year').head())

# The above is the same as the following syntax, but using pandas instead of regular Python
# print(df[df['State'] == 'Alabama'].set_index('Year').head())

# Iterating over groups
act_min_wage = pd.DataFrame()

for name, group in df.groupby('State'):
    if act_min_wage.empty:
        act_min_wage = group.set_index('Year')[['Low.2018']].rename(columns={'Low.2018': name})
    else:
        act_min_wage = act_min_wage.join(group.set_index('Year')[['Low.2018']].rename(columns={'Low.2018': name}))

hdr("act_min_wage.head()")
print(act_min_wage.head())

# Describe generates descriptive statistics
# count, mean, std (standard deviation), min, percentiles, max
# A usage for example is graphing the standard deviation for each state
hdr("act_min_wage.describe()")
print(act_min_wage.describe())

# Correlation
hdr("act_min_wage.corr().head()")
print(act_min_wage.corr().head())

# We'll get a lot of "NaN"s for Alabama (as far as we know in this point) in this dataset because of the "..."s in
# the Table_Data column

issue_df = df[ df['Low.2018'] == 0 ]
hdr("issue_df.head()")
print(issue_df.head())

hdr("issue_df['State'].unique() - The states we can't get data from")
print(issue_df['State'].unique())

import numpy as np

# if a col contains NaN it will get rid of that
# The default value for axis is 0. In this case it would get rid of the rows containing NaNs
hdr("act_min_wage.replace(0, np.NaN).dropna(axis=1).corr().head()")
print(act_min_wage.replace(0, np.NaN).dropna(axis=1).corr().head())

# We dropped a lot of states, but maybe Texas (for example) didn't have minimum wage and later on it got it.


min_wage_corr = act_min_wage.replace(0, np.NaN).dropna(axis=1).corr()
for problem in issue_df['State'].unique():
    if problem in min_wage_corr.columns:
        print("We're missing something here")

grouped_issues = issue_df.groupby('State')
hdr("grouped_issues.get_group('Alabama').head()")
print(grouped_issues.get_group('Alabama').head())

# Making sure the minimum wage was always zero for Alabama
hdr("grouped_issues.get_group('Alabama')['Low.2018'].sum()")
print(grouped_issues.get_group('Alabama')['Low.2018'].sum())


for state, data in grouped_issues:
    if data['Low.2018'].sum() != 0.0:
        print("We missed something")

