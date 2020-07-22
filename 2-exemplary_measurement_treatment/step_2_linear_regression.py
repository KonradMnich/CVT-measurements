# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 16:28:34 2020

@author: konrad
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns

path_in = "step_1_out/"
path_out = "step_2_out/"

file_name = "smooth_plus.csv"

df = pd.read_csv(path_in+file_name)
df['positive'] = df['a [m/s^2]'].apply(lambda a: a >= 0)

#%%
# choose inputs
X = df[['v [m/s]','a [m/s^2]']]

# choose output
y = df['F [N]']

# create training and test sets 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)

# create linear model object
lm = LinearRegression()

# fit data to the linear model object
lm.fit(X_train,y_train)

# print coefficients resulting from the model (inertance and viscous friction)
coeff_df = pd.DataFrame(lm.coef_,X.columns,columns=['Coefficient'])

# compute predictions based on the model
predictions = lm.predict(X_test)

# see predctions vs test data
plt.scatter(y_test,predictions)

# see distribution of errors
plt.figure()
sns.distplot((y_test-predictions),bins=50);

#%%
# see predictions vs test data with hue (acceleration positive)
df2 = pd.DataFrame()
df2['p'] = predictions
df2['t'] = y_test.tolist()
df2['+'] = [a > 0 for a in X_test['a [m/s^2]']]
#%%
sns.scatterplot(data=df2,x='t',y='p',hue='+')