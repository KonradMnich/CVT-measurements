#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 09:34:51 2020

@author: konrad
"""


import numpy as np
#import pandas as pd
from reusable import DataConditioner

test = DataConditioner("step_1_in/", "step_1_out/")
test.read_data_ni("r0a1bpot.csv")
test.read_data_mr("r0a1bmr.csv")
#t_old = np.arange(0,len(test.F_ni)*test.T_ni,test.T_ni)
test.resample()
test.scale()
test.synchronize()
test.assemble()
test.df_ready.plot(subplots=True)
test.save()