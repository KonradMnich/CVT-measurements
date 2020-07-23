# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 18:49:37 2020

@author: Konrad

sketch of a quick idea - > repeat for v+ and v-

"""
import pandas as pd
import numpy as np


#file = "step_1_in/22.07.2020/r0a1bpot.csv"
file = "step_1_out/smooth_a5_sym_plus.csv"
df = pd.read_csv(file,names=['F','x','v','a'],usecols=[1,2,3,4],skiprows=1)
df['a_sign'] = df['a'].apply(np.sign)
'''
df = pd.read_csv(file, skiprows=4, usecols=[1,3],names=['F','x'])
df['F'] = df['F'] - df['F'].mean()
df['F'] *= -200

df['x'] = df['x'] - df['x'].iloc[1:10].mean()
df['x'] /= 55.4

T = 0.0005 #[s]
df['v_temp'] = [0, *np.diff(df['x'])/T]
df['v'] = df['v_temp'].rolling(100, center=True).mean()
#df[['v','v2']].plot()

df['a_temp'] = [0, *np.diff(df['v'])/T]
df['a'] = df['a_temp'].rolling(100, center=True).mean()
#df[['a2']].plot()

#bonus columns
df['a_sign'] = df['a'].apply(np.sign)
#df['F-a-const'] = df['F']-df['a']*61-df['v'].apply(np.sign)*40

#df = df.iloc[:1470,:]
'''
#%%
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
df.fillna(0,inplace=True)

X = df[['v','a']]
y = df['F']

# create training and test sets 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)

# create linear model object
lm = LinearRegression()

# fit data to the linear model object
lm.fit(X_train,y_train)

# print coefficients resulting from the model (inertance and viscous friction)
coeff_df = pd.DataFrame(lm.coef_,X.columns,columns=['Coefficient'])
print(lm.intercept_)

# compute predictions based on the model
predictions = lm.predict(X_test)


# see distribution of errors
plt.figure()
sns.distplot((y_test-predictions),bins=50);

#%%
# see predictions vs test data with hue (acceleration positive)
df2 = pd.DataFrame()
df2['p'] = predictions
df2['t'] = y_test.tolist()
df2['+'] = [a > 0 for a in X_test['a']]
plt.figure()
sns.scatterplot(data=df2,x='t',y='p',hue='+')
#ax=sns.pairplot(df[['x','v','a','F','vel_sign','F-a-const']], hue='vel_sign')
ax=sns.pairplot(df[['v','a','F','a_sign']], hue='a_sign')