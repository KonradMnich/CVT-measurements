#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 16:06:34 2020

@author: konrad
"""
from preprocessor import Preprocessor
from processor import Processor
from postprocessor import Postprocessor

#%% Preprocess data
pre = Preprocessor(list_of_inputs="list.csv",ratios=[32], breaks=[False,True])
pre_out = pre.out()

#%% Perform linear regression
pro = Processor(pre_out)
pro.train(pos_v=[True, False])
pro_out = pro.out()

#%% Visually validate the fit
post = Postprocessor(experimental_data=pre_out, coeffs=pro_out)
post.show(lim1=2100, lim2=3000)

#%% Save results
pro.last_coeffs.to_csv('results/25072020-r32_coeffs.csv')

#%% debug
'''
import matplotlib.pyplot as plt
F = post.exp_data['F']
v = post.exp_data['v']
a = post.exp_data['a']
plt.scatter(v,F-a*61)
'''