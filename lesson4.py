import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

from helpers import hdr

pd.options.display.width = 0

df = pd.read_csv('datasets/minwage.csv')

act_min_wage = pd.DataFrame()

for name, group in df.groupby('State'):
    if act_min_wage.empty:
        act_min_wage = group.set_index('Year')[['Low.2018']].rename(columns={'Low.2018':name})
    else:
        act_min_wage = act_min_wage.join(group.set_index('Year')[['Low.2018']].rename(columns={'Low.2018':name}))

hdr('act_min_wage.head()')
print(act_min_wage.head())

min_wage_corr = act_min_wage.replace(0, np.NaN).dropna(axis=1).corr()

hdr('min_wage_corr.head()')
print(min_wage_corr.head())

plt.matshow(min_wage_corr)
plt.show()

labels = [c[:2].upper() for c in min_wage_corr.columns]

def show_heatmap(labels):
    fig = plt.figure(figsize=(12, 12))
    #                     <- all the subplots in the figure are in a 1 by 1 grid, and this is number one (only 1 graph)
    ax = fig.add_subplot(111)
    ax.matshow(min_wage_corr, cmap=plt.cm.RdYlGn)
    ax.set_yticklabels(labels)
    ax.set_xticklabels(labels)
    # matplotlib will truncate some of the states, which is undesirable.
    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))

    plt.show()

show_heatmap(labels)

# Now we need to map the states names to two letter words.
# We will use the website https://www.infoplease.com/state-abbreviations-and-state-postal-codes
# Pandas will try to take every table from this website and put it in a dataframe.
dfs = pd.read_html('https://www.infoplease.com/state-abbreviations-and-state-postal-codes')
hdr('dfs:')
for scraped_df in dfs:
    print(scraped_df.head())

state_abbv = dfs[0]

if not os.path.isfile('datasets/state_postal_code.csv'):
    # We'll save that scraped data just in case:
    state_abbv.to_csv('datasets/state_postal_code.csv', index=False)

state_abbv = pd.read_csv('datasets/state_postal_code.csv', index_col=0)
hdr("state_abbv.head()")
print(state_abbv.head())

abbv_dict = state_abbv[['Postal Code']].to_dict()
abbv_dict = abbv_dict['Postal Code']

# Now we want to use this dictionary to map it to our graph.
# We'll just first add 'FLSA', 'Guam' and 'Puero Rico' manually to avoid KeyError:
abbv_dict['Federal (FLSA)'] = 'FLSA'
abbv_dict['Guam'] = 'GU'
abbv_dict['Puerto Rico'] = 'PR'
labels = [abbv_dict[c] for c in min_wage_corr.columns]

show_heatmap(labels)

