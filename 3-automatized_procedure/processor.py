#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 13:08:18 2020

@author: konrad
"""
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

class Processor:
    def __init__(self, df):
        self.df = df
        self.customize_data()
        self.df_temp = pd.DataFrame()
        self.lm = LinearRegression(fit_intercept=False)
        self.last_coeffs = pd.DataFrame()
    
    def customize_data(self):
        # signum column replaces is for dry friction sign
        self.df['v_sign'] = self.df['v'].apply(np.sign)
        # preliminary analysis has shown that the force is proportional
        # to a root of velocity rather than velocity itself
        self.df['v**'] = self.df['v'].apply(abs)**1*self.df['v_sign']
    
    def train(self, pos_v=[True,False], pos_a=[True,False], t_size=0.4):
        self.df_temp = self.df[(self.df['v']>0).isin(pos_v) &\
                               (self.df['a']>0).isin(pos_a)]
        # measurement method bugs the results when system is not in motion
        self.df_temp = self.df_temp[self.df_temp['v'] != 0]
        X = self.df_temp[['v_sign','v**','a']]
        y = self.df_temp['F']
        X_train, X_test, y_train, y_test =\
            train_test_split(X, y, test_size=t_size)
        self.lm.fit(X_train,y_train)
        self.last_coeffs = pd.DataFrame(self.lm.coef_,['dry','viscous','inertance']\
                                        ,columns=['Coefficient'])
        #self.last_coeffs.loc['free term'] = [self.lm.intercept_]
        print(self.last_coeffs)
        
        predictions = self.lm.predict(X_test)
        plt.figure()
        sns.distplot((y_test-predictions),bins=50);
        plt.figure()
        sns.scatterplot(x=predictions,y=y_test)
        
    def out(self):
        return self.last_coeffs