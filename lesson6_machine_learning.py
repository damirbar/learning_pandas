import pandas as pd

from helpers import hdr

pd.options.display.width = 0

df = pd.read_csv("datasets/diamonds.csv", index_col=0)

hdr("df.head()")
print(df.head())


# Starting with linear regression
# It would be ideal that our string classifications are linear, meaning they have a meaningful order.
# Let's see what all of our cuts are, for example
hdr("df['cut'].unique()")
print(df['cut'].unique())

# Now we hard-code the order:
cut_class_dict = {'Fair': 1, 'Good': 2, 'Very Good': 3, 'Premium': 4, 'Ideal': 5}

# Let's see clarity
hdr("df['clarity'].unique()")
print(df['clarity'].unique())
clarity_dict = {"I3": 1, "I2": 2, "I1": 3, "SI2": 4, "SI1": 5, "VS2": 6, "VS1": 7, "VVS2": 8, "VVS1": 9, "IF": 10, "FL": 11}

# Now the color
hdr("df['color'].unique()")
print(df['color'].unique())
color_dict = {"J": 1,"I": 2,"H": 3,"G": 4,"F": 5,"E": 6,"D": 7}

# Using the new dictionaries to map the dataframe
df['cut']     = df['cut'].map(cut_class_dict)
df['clarity'] = df['clarity'].map(clarity_dict)
df['color']   = df['color'].map(color_dict)

hdr("df.head()")
print(df.head())

# Great. Now we have numeric values
# Training a regression model to figure this out. Supervised learning.
# We will use SGD (Stochastic Gradient Descent) Regressor.

import sklearn
from sklearn.linear_model import SGDRegressor

# Shuffle the data to avoid any biases that may emerge because of some order.
df = sklearn.utils.shuffle(df)

# We want to predict the price
X = df.drop("price", axis=1).values
y = df["price"].values

test_size = 200

# Training set
X_train = X[:-test_size]
y_train = y[:-test_size]

# Test set
X_test = X[-test_size:]
y_test = y[-test_size:]

# Classifier
clf = SGDRegressor(max_iter=1000)
clf.fit(X_train, y_train)

hdr("clf.score(X_test, y_test)")
print(clf.score(X_test, y_test))

for X,y in list(zip(X_test, y_test))[:10]:
    print(clf.predict([X])[0], y)


# We got bad scores. Let's use support vector instead
import sklearn
from sklearn import svm, preprocessing

df = sklearn.utils.shuffle(df) # always shuffle your data to avoid any biases that may emerge b/c of some order.

X = df.drop("price", axis=1).values
X = preprocessing.scale(X)
y = df["price"].values

test_size = 200

X_train = X[:-test_size]
y_train = y[:-test_size]

X_test = X[-test_size:]
y_test = y[-test_size:]

clf = svm.SVR()

clf.fit(X_train, y_train)
hdr("clf.score(X_test, y_test)")
print(clf.score(X_test, y_test))

for X,y in list(zip(X_test, y_test))[:10]:
    print(f"model predicts {clf.predict([X])[0]}, real value: {y}")




