# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 12:42:43 2021

@author: sebas
"""

#**************************************************************************
#   Company:        SUPSI DTI ISEA
#   Project:        DEMETO
#   Date:           12.04.2021
#   Author:         S.Schütz
#   File:           PTA_Plot_Conc_Temp.py
#   Description:    Analysis of the Dieletric constant and
#                   loss factor of the Dryer mixture at different
#                   concentration, drink-water and PTA vesus temperature
#                   Conc is done from 0% to 100%
#**************************************************************************

import os
import numpy as np
import matplotlib.pyplot as plt

# Setups
DataCorr = 1; # YES = 1
DataCorr_Er = 1;
DataCorr_tanD = 0;

# Loading data

# Folder path identification
currentFolder = os.getcwd()

os.chdir(currentFolder + '\\30 gradi')
Data_30g_Folder = os.getcwd()

os.chdir(currentFolder + '\\50 gradi')
Data_50g_Folder = os.getcwd()

os.chdir(currentFolder + '\\70 gradi')
Data_70g_Folder = os.getcwd()

os.chdir(currentFolder + '\\90 gradi')
Data_90g_Folder = os.getcwd()


myListDir = [Data_30g_Folder, Data_50g_Folder, Data_70g_Folder, Data_90g_Folder]

# Import files CSV
j = 0
for mydir in myListDir: 
    # Import files 30g
    os.chdir(mydir) #Change directory
    FilesData = os.listdir() #Find all CSV file into folder
    print(FilesData,'\n')
    i = 0
    for element in FilesData: #Loading all CSV file for all folders
        Data  = np.loadtxt(element, skiprows = 1)
        if j == 0 and i == 0: #First time build the np-array/matrix
            NrRows = Data.shape[0]
            NrCol = 3
            NrWidh = len(FilesData)
            NrTemp = len(myListDir)
            # allData[Nr.Measure,Variables(freq,e1,e2),Concentration,Temperature]
            allData = np.ones((NrRows, NrCol, NrWidh, NrTemp))
        
        allData[:,:,i, j] = Data
        i = i + 1
    j = j + 1
# Return to home folder
os.chdir(currentFolder) 
 
# Calculate tanD and Er for all data
allData_calc = np.ones((NrRows, NrCol, NrWidh,NrTemp))
# allData_calc[Nr.Measure,Variables(freq,er,tanD),Concentration,Temperature]
allData_calc[:,0,:,:] = allData[:,0,:,:] # freq
allData_calc[:,1,:,:] = np.sqrt(allData[:,1,:,:]**2 + allData[:,2,:,:]**2) # er
allData_calc[:,2,:,:] = np.abs(allData[:,2,:,:]/allData[:,1,:,:]) # tanD

# Extract 2.4GHz data 
idx = np.where(allData_calc[:,0,:,:] == 2400000000.0)

# Create 2.4GHz data matrix
# allData_calc_2G4[Variables(er,tanD),Concentration,Temperature]
allData_calc_2G4= allData_calc[idx[0][0],:,:,:]
allData_calc_2G4 = allData_calc_2G4[-2:,:,:]

## Correction of datas due to measurement errors
# Define matrix according to measured data
X,Y,Z = allData_calc_2G4.shape;
allData_teo_2G4 = np.ones((X, Y, Z)) # Create theoretical matrix
allData_Error_2G4 = np.ones((X, Y, Z)) # Create theoretical matrix 

# Import data measured for H2O and Pouder
allData_teo_2G4[:,0,:] = np.copy(allData_calc_2G4[:,0,:])
allData_teo_2G4[:,-1,:] = np.copy(allData_calc_2G4[:,-1,:])

# Calculation of theoretical values
mix_conc = np.linspace(0, 1,len(allData_teo_2G4[0,:,0]))

TemperatureList = np.linspace(30, 90,len(allData_teo_2G4[0,0,:]))


for temp_idx in range(len(TemperatureList)):
    # Calculation of theoretical Er tanD values
    allData_teo_2G4[0,:,temp_idx] = allData_teo_2G4[0,0,temp_idx]*(1-mix_conc) + allData_teo_2G4[0,-1,temp_idx]*mix_conc
    allData_teo_2G4[1,:,temp_idx] = allData_teo_2G4[1,0,temp_idx]*(1-mix_conc) + allData_teo_2G4[1,-1,temp_idx]*mix_conc

# Relative error calculation
allData_Error_2G4 = np.abs(allData_teo_2G4-allData_calc_2G4)/allData_teo_2G4

# Error compensation
if DataCorr == 1:
    allData_Comp_2G4 = np.copy(allData_calc_2G4)
    tollerance = 0.1 # if measured value is out of +- TOLLERANCE we correct it
    
    if DataCorr_Er == 1:
        print('Correction of datas will be applied on Er\n')
        # Er compensation
        for temp_idx in range(len(TemperatureList)):
            for conc_idx in range(len(mix_conc)):
                if(allData_Error_2G4[0,conc_idx,temp_idx] >= tollerance):
                    if(allData_calc_2G4[0,conc_idx,temp_idx] >= allData_teo_2G4[0,conc_idx,temp_idx]):
                        allData_Comp_2G4[0,conc_idx,temp_idx] = allData_calc_2G4[0,conc_idx,temp_idx] * (1 - allData_Error_2G4[0,conc_idx,temp_idx])
                    else:
                        allData_Comp_2G4[0,conc_idx,temp_idx] = allData_calc_2G4[0,conc_idx,temp_idx] * (1 + allData_Error_2G4[0,conc_idx,temp_idx])
    
    if DataCorr_tanD == 1:
        print('Correction of datas will be applied on tan(d)\n')
        # tanD compensation                                                                                                 
        for temp_idx in range(len(TemperatureList)):
            for conc_idx in range(len(mix_conc)):
                if(allData_Error_2G4[1,conc_idx,temp_idx] >= tollerance):
                    if(allData_calc_2G4[1,conc_idx,temp_idx] >= allData_teo_2G4[1,conc_idx,temp_idx]):
                        allData_Comp_2G4[1,conc_idx,temp_idx] = allData_calc_2G4[1,conc_idx,temp_idx] * (1 - allData_Error_2G4[1,conc_idx,temp_idx] )
                    else:
                        allData_Comp_2G4[1,conc_idx,temp_idx] = allData_calc_2G4[1,conc_idx,temp_idx] * (1 + allData_Error_2G4[1,conc_idx,temp_idx] )
    
    allData_calc_2G4 = np.copy(allData_Comp_2G4)
    
# Data regression
Reg_Order = 3
NrPoint = 10
TemperatureSweep = np.linspace(min(TemperatureList),max(TemperatureList),NrPoint)
allData_Regr_2G4 = np.zeros( (len(allData_calc_2G4[:,0,0]), len(mix_conc), len(TemperatureSweep)))

# Create Polynomial coefficient matrix to calculate Er and tan(d) vs Temperature
Poly_Coeff_Temp = np.zeros( (len(allData_calc_2G4[:,0,0]), len(mix_conc), (Reg_Order+1)))

for conc_idx in range(len(mix_conc)): 
    Poly_Coeff_Temp[0,conc_idx,:] = np.polyfit(TemperatureList, allData_calc_2G4[0,conc_idx,:], Reg_Order) #Er
    Poly_Coeff_Temp[1,conc_idx,:] = np.polyfit(TemperatureList, allData_calc_2G4[1,conc_idx,:], Reg_Order) #tan(d)

for conc_idx in range(len(mix_conc)): 
    allData_Regr_2G4[0,conc_idx,:] = np.polyval(Poly_Coeff_Temp[0,conc_idx,:], TemperatureSweep)
    allData_Regr_2G4[1,conc_idx,:] = np.polyval(Poly_Coeff_Temp[1,conc_idx,:], TemperatureSweep)

# Data plotting
legend_str_list = [0]*len(mix_conc)

plt.figure(1)
fig, ax = plt.subplots()
plt.style.use('bmh')
fig.set_figheight(10)
fig.set_figwidth(10)

for conc_idx in range(len(mix_conc)): 
    ax.plot(TemperatureList,allData_calc_2G4[0,conc_idx,:], marker="o")
    legend_str_list[conc_idx] = "TPA " + str(round(mix_conc[conc_idx]*100)) + "[%]"
    
ax.set_xlabel('Temperature [°C]')
ax.set_ylabel('Equivalent Er  [-]')   
ax.set_title('Measured data - Er = f(C,T) @ f = 2.45GHz')                                                                                    
ax.legend(legend_str_list,loc='upper right')
plt.savefig('fig1 - Measured data - Er = f(C,T) @ f = 2.45GHz.jpg')

plt.figure(2)
fig, ax = plt.subplots()
plt.style.use('bmh')
fig.set_figheight(10)
fig.set_figwidth(10)

for conc_idx in range(len(mix_conc)): 
    ax.plot(TemperatureList,allData_calc_2G4[1,conc_idx,:], marker="o")
    legend_str_list[conc_idx] = "TPA " + str(round(mix_conc[conc_idx]*100)) + "[%]"
    
ax.set_xlabel('Temperature [°C]')
ax.set_ylabel('Equivalent tan(d)  [-]')   
ax.set_title('Measured data - tan(d) = f(C,T) @ f = 2.45GHz')                                                                                    
ax.legend(legend_str_list,loc='upper right')
plt.savefig('fig2 - Measured data - tan(d) = f(C,T) @ f = 2.45GHz.jpg')


plt.figure(3)
fig, ax = plt.subplots()
plt.style.use('bmh')
fig.set_figheight(10)
fig.set_figwidth(10)

for conc_idx in range(len(mix_conc)): 
    ax.plot(TemperatureSweep,allData_Regr_2G4[0,conc_idx,:], marker="o")
    legend_str_list[conc_idx] = "TPA " + str(round(mix_conc[conc_idx]*100)) + "[%]"
    
ax.set_xlabel('Temperature [°C]')
ax.set_ylabel('Equivalent Er  [-]')   
ax.set_title('Regression data - Er = f(C,T) @ f = 2.45GHz')                                                                                    
ax.legend(legend_str_list,loc='upper right')
plt.savefig('fig3 - Regression data - Er = f(C,T) @ f = 2.45GHz.jpg')


plt.figure(4)
fig, ax = plt.subplots()
plt.style.use('bmh')
fig.set_figheight(10)
fig.set_figwidth(10)

for conc_idx in range(len(mix_conc)): 
    ax.plot(TemperatureSweep,allData_Regr_2G4[1,conc_idx,:], marker="o")
    legend_str_list[conc_idx] = "TPA " + str(round(mix_conc[conc_idx]*100)) + "[%]"
    
ax.set_xlabel('Temperature [°C]')
ax.set_ylabel('Equivalent tan(d)  [-]')   
ax.set_title('Regression data - tan(d) = f(C,T) @ f = 2.45GHz')                                                                                    
ax.legend(legend_str_list,loc='upper right')
plt.savefig('fig4 - Regression data - tan(d) = f(C,T) @ f = 2.45GHz.jpg')


