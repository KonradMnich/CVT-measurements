#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 14:47:52 2020

@author: konrad
"""
import matplotlib.pyplot as plt
import seaborn as sns

class Postprocessor:
    """ Postprocessor sums up the results of identification. Here we recompute
    the force basing on the linear regression obtained by the Processor and
    compare it with the measure force."""
    
    def __init__(self, experimental_data, coeffs):
        self.exp_data = experimental_data
        self.coeffs = coeffs
        self.model = self.compute_model()
    
    def compute_model(self):
        model = (self.exp_data['v**'] * self.coeffs.loc['viscous'].to_numpy()
                 + self.exp_data['a'] * self.coeffs.loc['inertance'].to_numpy()
                 + self.exp_data['v_sign'] * self.coeffs.loc['dry'].to_numpy())
        return model
    
    def show(self, lim1=0, lim2=1000):
        sns.set_style('whitegrid')
        model = self.model.iloc[lim1:lim2].tolist()
        exp = self.exp_data['F'].iloc[lim1:lim2].tolist()
        fig = plt.figure()
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
        ax.plot(exp, label='experiment')
        ax.plot(model, label='model',linestyle='--')
        ax.set_xlabel('Samples [-]')
        ax.set_ylabel('F [N]')
        ax.legend()
        ax.set_title('Model vs experiment')
        fig.set_dpi(600)