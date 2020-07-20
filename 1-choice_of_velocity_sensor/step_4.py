# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 12:01:48 2020

@author: Konrad

In this script I prepare the graphs for visual assessment of data.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns #only for style

sns.set_style("whitegrid")

path_in = "step_3_out/"
path_out = "step_4_out/"
a = pd.read_csv(path_in+"a.csv")

#%% normalize data
a_ref1 = a['0'].max()
a_ref2 = a['3'].max()
a_ref3 = a['6'].max()
a.iloc[:,0:3] = a.iloc[:,0:3].apply(lambda x: x/a_ref1)
a.iloc[:,3:6] = a.iloc[:,3:6].apply(lambda x: x/a_ref2)
a.iloc[:,6:9] = a.iloc[:,6:9].apply(lambda x: x/a_ref3)

#%% case 1 - constant speed - not filtered
# Fig 1:

plt.figure()
ax = a[['1','2','0']].plot()
ax.set_xlabel("samples [-]")
ax.set_ylabel("acceleration [-]")
ax.legend(['potentiometer','encoder','servo (ref)'])
ax.set_title('Constant speed - not filtered')
plt.savefig(fname=path_out+'Fig1_const_speed.png',\
            dpi=600,transparent=True, bbox_inches='tight')

#%% case 2 - constant acceleration - not filtered
# Fig 2:

plt.figure()
ax = a[['4','5','3']].plot()
ax.set_xlabel("samples [-]")
ax.set_ylabel("acceleration [-]")
ax.legend(['potentiometer','encoder','servo (ref)'])
ax.set_title('Constant acceleration - not filtered')
plt.savefig(fname=path_out+'Fig2_const_acc.png',\
            dpi=600,transparent=True, bbox_inches='tight')

#%% case 3 - smooth - not filtered
# Fig 3:
    
plt.figure()
ax = a[['7','8','6']].plot()
ax.set_xlabel("samples [-]")
ax.set_ylabel("acceleration [-]")
ax.legend(['potentiometer','encoder','servo (ref)'])
ax.set_title('Smooth-not_filtered')
plt.savefig(fname=path_out+'Fig3_smooth.png',\
            dpi=600,transparent=True, bbox_inches='tight')

#%% rolling mean "filter"
# Fig 4:
    
plt.figure()
ax = a[['7','8','6']].rolling(20).mean().plot()
ax.set_xlabel("samples [-]")
ax.set_ylabel("acceleration [-]")
ax.legend(['potentiometer','encoder','servo (ref)'])
ax.set_title('Smooth - rolling mean (20)')
plt.savefig(fname=path_out+'Fig4_smooth-movmean_20.png',\
            dpi=600,transparent=True, bbox_inches='tight')

#%% rolling mean vs true
# Fig 5:
    
plt.figure()
ax = a['6'].plot()
ax = a['6'].rolling(10).mean().plot()
ax = a['6'].rolling(20).mean().plot()
ax.set_xlabel("samples [-]")
ax.set_ylabel("acceleration [-]")
ax.set_title('Smooth - rolling mean influence')
ax.legend(['oryginal','window=10','window=20'])
plt.savefig(fname=path_out+'Fig5_smooth-movmean_var_windows.png',\
            dpi=600,transparent=True, bbox_inches='tight')

#%% rolling mean - center parameter
# Fig6:
    
plt.figure()
ax = a['6'].rolling(10).mean().plot()
ax = a['6'].rolling(10,center=True).mean().plot()
ax.set_xlabel("samples [-]")
ax.set_ylabel("acceleration [-]")
ax.set_title('Smooth - rolling mean center influence')
ax.legend(['center=False','center=True'])
plt.savefig(fname=path_out+'Fig6_smooth-movmean_center mean.png',\
            dpi=600,transparent=True, bbox_inches='tight')
