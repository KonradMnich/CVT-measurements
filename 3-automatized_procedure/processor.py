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
    """ Class used to identify physical parameters of the system
    basing on the linear regression. """
    
    def __init__(self, df):
        self.df = df
        self.customize_data()
        self.df_temp = pd.DataFrame()
        self.lm = LinearRegression(fit_intercept=False)
        self.last_coeffs = pd.DataFrame()
    
    def customize_data(self):
        """ Infere two new columns potentially usefull in regression."""
        
        # Signum column is used for dry friction sign.
        self.df['v_sign'] = self.df['v'].apply(np.sign)
        # Preliminary analysis has shown that the force is proportional
        # to a power of velocity rather than velocity itself.
        self.df['v**'] = self.df['v'].apply(abs)**1*self.df['v_sign']
    
    def train(self, pos_v=[True,False], pos_a=[True,False], t_size=0.4):
        """ This function computes linear regression basing on data
        from preprocessor. """
        
        self.df_temp = self.df[(self.df['v']>0).isin(pos_v) &
                               (self.df['a']>0).isin(pos_a)]
        # Measurement method bugs the results when system is not in motion
        # and therefor we exclude zero velocities form the model.
        self.df_temp = self.df_temp[self.df_temp['v'] != 0]
        X = self.df_temp[['v_sign', 'v**', 'a']]
        y = self.df_temp['F']
        X_train, X_test, y_train, y_test =\
            train_test_split(X, y, test_size=t_size)
        self.lm.fit(X_train, y_train)
        self.last_coeffs = pd.DataFrame(self.lm.coef_,
                                        ['dry','viscous','inertance'],
                                        columns=['Coefficient'])
        print(self.last_coeffs)
        
        predictions = self.lm.predict(X_test)
        # Plot the errors histogram and correlation plot to asses
        # the quality of fit.
        plt.figure()
        sns.distplot((y_test-predictions),bins=50);
        plt.figure()
        sns.scatterplot(x=predictions,y=y_test)
        
    def out(self):
        """ Function added for consistency."""
        return self.last_coeffs