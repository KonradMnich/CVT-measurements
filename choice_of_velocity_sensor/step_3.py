#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 21:47:12 2020

@author: konrad

This script serves to compute velocity and acceleration
basing on displacement time series

"""
import pandas as pd
import numpy as np
#first try - simple difference
path_in = "step_2_out/"
path_out = "step_3_out/"

x = pd.read_csv(path_in+"all_x_data.csv")
x.drop(['l1'],axis=1,inplace=True)

v = pd.DataFrame()
a = pd.DataFrame()
for i in range(9):
    col = x.iloc[1:,i].astype(float).to_numpy()
    dxdt = np.diff(col)
    v[str(i)] = dxdt
    ddxddt = np.diff(dxdt)
    a[str(i)] = ddxddt
