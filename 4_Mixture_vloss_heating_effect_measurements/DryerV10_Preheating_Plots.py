#**************************************************************************
#   Company:        SUPSI DTI ISEA
#   Project:        DEMETO
#   Date:           28.05.2020
#   Author:         S.Schütz
#   File:           DryerV10_Preheating_Plots.py
#   Description:    Analysis of Ansys result of Vloss vs Temp and ConcH2O
#                   per versione da 0p a 100p 
#**************************************************************************

#*************************** Data file structure*******************************
# "$Mix_Temp []"	"Vloss [] - $conc_H2O='0' $Er='1.76802014977206' $tanD='0.015782328317683' Freq='2.45GHz' Phase='0deg'"	"Vloss [] - $conc_H2O='0' $Er='2.22805215603226' $tanD='0.0222671156004489' Freq='2.45GHz' Phase='0deg'"	"Vloss [] - $conc_H2O='0' $Er='2.5075163329478' $tanD='0.0411111998084138' Freq='2.45GHz' Phase='0deg'"	"Vloss [] - $conc_H2O='0' $Er='3.44063623476822' $tanD='0.0466408682242719' Freq='2.45GHz' Phase='0deg'"
# 30	0.902423340606861
# 50	0.867023484087784	
# 70	0.83129855572956			
# 90	0.706388440664558		
#******************************************************************************

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd


# List of samples
myConc_lst = ["0p", "10p", "20p", "30p", "40p", "50p", "60p", "70p", "80p", "90p", "100p"]

# Load data from folder
myCurrFolder_str = os.getcwd()
DataFolder_str = myCurrFolder_str + "/Data"
os.chdir(DataFolder_str)

FilesData_str = os.listdir()

File_cnt_int = 0
for File in FilesData_str:
    
    Data_DF = pd.read_csv(FilesData_str[File_cnt_int], sep='\t', names=['Temp','Vloss'], skiprows=1)
    
    if File_cnt_int == 0: #First time build the np-array/matrix
        NrRow = Data_DF.shape[0]
        NrCol = 2 # Temp, Vloss
        NrConc = len(myConc_lst) # 0%, 10%, ...
        allData_DF = np.ones((NrRow, NrCol, NrConc))   
        
    allData_DF[:,:,File_cnt_int] = Data_DF.values
    File_cnt_int = File_cnt_int + 1;



# Plot data 3D
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
conc_bar_arr = np.linspace(0, 100, NrConc)
temp_bar_arr = allData_DF[:,0,0];
myTitle = "Vloss = f(T,C) @ f = 2.45GHz";

# Construct 3d points
x_matarr = np.zeros((len(temp_bar_arr), len(conc_bar_arr)))
y_matarr  = np.zeros((len(temp_bar_arr), len(conc_bar_arr)))
z_matarr  = allData_DF[:,1]

for x_idx in range(x_matarr.shape[1]):
    x_matarr[:,x_idx] = temp_bar_arr;
    
for y_idx in range(y_matarr.shape[0]):
    y_matarr[y_idx, :] = conc_bar_arr;
 
surf = ax.plot_surface(x_matarr, y_matarr, z_matarr, cmap=cm.jet, linewidth=0, antialiased=False)
ax.set_xlabel("Temp. [°C]")
ax.set_ylabel("Conc H2O [%]")
ax.set_title(myTitle)

ax.set_facecolor('w') # white background

fig.colorbar(surf) # Add a color bar which maps values to colors.


os.chdir(myCurrFolder_str)
plt.savefig(myTitle +'.jpg')
fig.show()



# Plot data
fig, ax = plt.subplots()
myTitle = "Vloss = f(C) @ f = 2.45GHz";
ax.set_xlabel("Conc H2O [%]")
ax.set_ylabel("Vloss [ ]")
ax.set_title(myTitle)

legend_str_list = ['']*len(temp_bar_arr)
Temp_cnt_int = 0
for myTempVar in temp_bar_arr:
    Vloss_data = allData_DF[Temp_cnt_int, 1, :]
    ax.plot(conc_bar_arr, Vloss_data, marker='o')
    legend_str_list[Temp_cnt_int] = "T = " + str(myTempVar) + "°C"
    Temp_cnt_int = Temp_cnt_int + 1

fig.legend(legend_str_list, loc='center', bbox_to_anchor=(0.75, 0.5))
os.chdir(myCurrFolder_str)
plt.savefig(myTitle +'.jpg')
fig.show()
  

