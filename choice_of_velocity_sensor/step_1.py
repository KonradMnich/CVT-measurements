#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 21:35:11 2020

@author: konrad

This script converts data obtained from various sensors to SI units
and saves them into uniform csv files

"""
from Data_conversion import Data_conversion as Dc
#%%        
servo = Dc()
servo.get_series("r0v0a0mr.csv", "v_const", Dc.rpm2mps)
servo.get_series("r0a1mr.csv" , "a_const", Dc.rpm2mps)
servo.get_series("r0a1bmr.csv" , "smooth", Dc.rpm2mps)
servo.cumtrapz('v_const')
servo.cumtrapz('a_const')
servo.cumtrapz('smooth')
servo.save("v_mr.csv")

#%%
encoder = Dc()
encoder.get_series("r0v0a0enk.csv", "v_const", Dc.r2m,col=2)
encoder.get_series("r0a1enk.csv" , "a_const", Dc.r2m,col=2)
encoder.get_series("r0a1benk.csv" , "smooth", Dc.r2m,col=2)
encoder.save("x_enc.csv")

#%%
potentiometer = Dc()
potentiometer.get_series("r0v0a0pot.csv", "v_const", Dc.V2m,col=3)
potentiometer.get_series("r0a1pot.csv" , "a_const", Dc.V2m,col=3)
potentiometer.get_series("r0a1bpot.csv" , "smooth", Dc.V2m,col=3)
potentiometer.save("x_pot.csv")


