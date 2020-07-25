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
pre = Preprocessor(list_of_inputs="list.csv",ratios=[0], breaks=[False])
pre_out = pre.out()

#%% Perform linear regression
pro = Processor(pre_out)
pro.train()
pro_out = pro.out()

#%% Visually validate the fit
post = Postprocessor(experimental_data=pre_out, coeffs=pro_out)
post.show()
