import pandas as pd
import numpy as np

from helpers import hdr

pd.options.display.width = 0

# In this lesson we'll try to find correlation between unemployment and the minimum wage

unemp_county = pd.read_csv('datasets/unemployment-by-county-us/output.csv')

hdr('unemp_county.head()')
print(unemp_county.head())

df = pd.read_csv('datasets/minwage.csv')

act_min_wage = pd.DataFrame()

for name, group in df.groupby('State'):
    if act_min_wage.empty:
        act_min_wage = group.set_index('Year')[['Low.2018']].rename(columns={'Low.2018':name})
    else:
        act_min_wage = act_min_wage.join(group.set_index('Year')[['Low.2018']].rename(columns={'Low.2018':name}))

hdr('act_min_wage.head()')
print(act_min_wage.head())

act_min_wage = act_min_wage.replace(0, np.NaN).dropna(axis=1)

hdr('act_min_wage.head() after dropping NaN')
print(act_min_wage.head())

def get_min_wage(year, state):
    try:
        # loc function accesses a group of rows and columns by label(s or a boolean array)
        return act_min_wage.loc[year][state]
    except:
        return np.NaN

# Testing the function
hdr("get_min_wage(2012, 'Alaska')")
print(get_min_wage(2012, 'Alaska'))

print("!")
# Now we will map the function to a new column
unemp_county['min_wage'] = list(map(get_min_wage, unemp_county['Year'], unemp_county['State']))
print("!")

hdr('unemp_county.head()')
print(unemp_county.head())

# Checking the correlation between the unemployment rate and the minimum wage
hdr("unemp_county[['Rate', 'min_wage']].corr()")
print(unemp_county[['Rate', 'min_wage']].corr())

# Checking the covariance between the unemployment rate and the minimum wage (if they vary similarly)
hdr("unemp_county[['Rate', 'min_wage']].cov()")
print(unemp_county[['Rate', 'min_wage']].cov())

pres16 = pd.read_csv('datasets/pres16results.csv')
hdr("pres16.head()")
print(pres16.head())

# Now we'll combine all this data on county and state and share percentage vote

# len(unemp_county) == 885548 ; This is a huge dataset. We'll use only the 2015 February data

county_2015 = unemp_county.copy()[(unemp_county['Year'] == 2015) & (unemp_county['Month'] == 'February')]
hdr("county_2015.head()")
print(county_2015.head())

# The "st" column of pres16 are the postal codes of the states
# We already got the mapping of it in the previous lesson:
state_abbv = pd.read_csv('datasets/state_postal_code.csv', index_col=0)
state_abbv = state_abbv[['Postal Code']]

state_abbv_dict = state_abbv.to_dict()['Postal Code']

county_2015['State'] = county_2015['State'].map(state_abbv_dict)

hdr("county_2015.tail()")
print(county_2015.tail())

# len(county_2015) == 2802
# len(pres16) == 18475
# Now we map pres16 to county_2015
# There's one issue: the column names of the two dataframes are not the same:
#   State is "State" for county_2015 and "st" for pres16
#   County is "County" for county_2015 and "county" for pres16
# We'll fix that
pres16.rename(columns={'county':'County', 'st':'State'}, inplace=True)

# We'll join them now by double index
for df in [county_2015, pres16]:
    df.set_index(['County', 'State'], inplace=True)

# Focusing on Donald Trump
pres16 = pres16[ pres16['cand'] == 'Donald Trump' ]

pres16 = pres16[['pct']] # Only the percent column
pres16.dropna(inplace=True)

hdr("pres16.head()")
print(pres16.head())

# Now we're ready to merge
all_together = county_2015.merge(pres16, on=['County', 'State'])
all_together.dropna(inplace=True)

# Let's drop the year column
all_together.drop('Year', axis=1, inplace=True)

hdr("all_together.head()")
print(all_together.head())

hdr("all_together.corr().head()")
print(all_together.corr().head())

hdr("all_together.cov().head()")
print(all_together.cov().head())
