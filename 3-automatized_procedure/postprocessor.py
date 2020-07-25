#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 14:47:52 2020

@author: konrad
"""
import matplotlib.pyplot as plt

class Postprocessor:
    def __init__(self, experimental_data, coeffs):
        self.exp_data = experimental_data
        self.coeffs = coeffs
        self.model = self.compute_model()
    
    def compute_model(self):
        model = self.exp_data['v**']*self.coeffs.loc['viscous'].to_numpy()+\
                self.exp_data['a']*self.coeffs.loc['inertance'].to_numpy()+\
                self.exp_data['v_sign']*self.coeffs.loc['dry'].to_numpy()
        return model
    
    def show(self,lim1=0,lim2=1000):
        plt.figure()
        ax = self.exp_data['F'].iloc[lim1:lim2].plot(label='experiment')
        self.model.iloc[lim1:lim2].plot(label='model', style='--')
        ax.legend()
       