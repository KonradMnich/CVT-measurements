#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 00:01:24 2020

@author: konrad
"""

import pandas as pd

inertance = 63 #kg
viscous_fric = 63 #Ns/m
dry_fric = 15 #N

#df = pd.read_csv('step_1_out/smooth_a10_sym_shifted_plus.csv')
df = pd.read_csv('step_1_out/meta_smooth.csv')
'''
df['F_model'] = inertance * df['a [m/s^2]'] +\
    viscous_fric * df['v [m/s]']**0.5 + dry_fric
df['F [N]'] = df['F [N]']
df = df[df['v [m/s]']>0]

df[['F [N]','F_model']].plot()
'''

df['F_model'] = inertance * df['a'] +\
    viscous_fric * df['v']**0.5 + dry_fric
df = df[df['v']>0]

df[['F','F_model']].plot()