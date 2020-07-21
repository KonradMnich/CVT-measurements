#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 08:55:51 2020

@author: konrad
"""
import pandas as pd
import numpy as np

class DataConditioner:
    def __init__(self, path_in, path_out):
        self.path_in = path_in
        self.path_out = path_out
        self.F_raw_ni = np.array([])
        self.x_raw_ni = np.array([])
        self.v_raw_mr = np.array([])
        self.F_ni = np.array([])
        self.x_ni = np.array([])
        self.v_mr = np.array([])
        self.x_mr = np.array([])
        self.df_ready = pd.DataFrame()
        self.T_ni = float()
        self.T_mr = float()

    def read_data_ni(self,name_ni,cols=[1,3]):
        df_raw_ni = pd.read_csv(self.path_in+name_ni,usecols=cols)
        self.T_ni = float(df_raw_ni.iloc[0,0])
        self.F_raw_ni = df_raw_ni.iloc[4:,0].astype(float).to_numpy()
        self.x_raw_ni = df_raw_ni.iloc[4:,1].astype(float).to_numpy()
        self.F_ni = self.F_raw_ni
        self.x_ni = self.x_raw_ni
        pass
    
    def read_data_mr(self,name_mr,cols=[1]):
        df_raw_mr = pd.read_csv(self.path_in+name_mr,usecols=cols)
        self.T_mr = float(df_raw_mr.iloc[1,0])/1000
        self.v_raw_mr = df_raw_mr.iloc[5:,0].astype(float).to_numpy()
        self.v_mr = self.v_raw_mr
        pass
    
    def condition(self):
        self.resample()
        self.scale()
        self.synchronize()
        self.assemble()
    
    def resample(self):
        t_old = np.arange(0,len(self.F_ni)*self.T_ni,self.T_ni)
        t_new = np.arange(0,max(t_old),self.T_mr)
        self.F_ni = np.interp(t_new,t_old,self.F_ni)
        self.x_ni = np.interp(t_new,t_old,self.x_ni)
        pass
    
    def scale(self):
        self.F_ni = -(self.F_ni - np.mean(self.F_ni[0:10]))*200
        self.v_mr = -self.v_mr*20/60/1000
        self.x_mr = np.cumsum(self.v_mr)*self.T_mr
        self.x_ni = (self.x_ni - np.mean(self.x_ni[0:10]))
        x_factor = max(self.x_mr)/max(self.x_ni)
        self.x_ni *= x_factor        
        pass
    
    def synchronize(self):
        v = self.x_mr
        w = self.x_ni
        F = self.F_ni
        diff = len(v) - len(w)
        if diff > 0:
            w = np.append(w,[0]*diff)
            F = np.append(F,[0]*diff)
        else:
            v = np.append(v,[0]*diff)
            self.x_mr = v
        se = sum((v[:-100]-w[:-100])**2)
        k = 0
        for i in range(len(v)):
            w = np.insert(w,0,w[-1])
            w = np.delete(w,-1)
            if se > sum((v[:-100]-w[:-100])**2):
                se = sum((v[:-100]-w[:-100])**2)
                k = i
        self.x_ni = np.concatenate((w[-k:], w[:-k]))
        self.F_ni = np.concatenate((F[-k:], F[:-k]))
        pass

    def assemble(self):
        self.df_ready['t [s]'] = [0,*np.cumsum([self.T_mr]*(len(self.x_mr)-1))]
        self.df_ready['F [N]'] = self.F_ni
        self.df_ready['x [m]'] = self.x_mr
        self.df_ready['v [m/s]'] = self.v_mr
    
    def save(self,name="preprocessed_data.csv"):
        self.df_ready.to_csv(self.path_out+name,index=False)
        pass