#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 11:50:51 2020

@author: konrad
"""

from reusable import DataConditioner

dc = DataConditioner("step_1_in/", "step_1_out/")
dc.read_data_mr("r0a1bmr.csv")
dc.read_data_ni("r0a1bpot.csv")
dc.condition()
dc.df_ready.plot(subplots=True)
dc.save()
