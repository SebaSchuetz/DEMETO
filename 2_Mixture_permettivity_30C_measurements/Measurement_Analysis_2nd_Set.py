# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 12:42:43 2021

@author: sebas
"""

#**************************************************************************
#   Company:        SUPSI DTI ISEA
#   Project:        DEMETO
#   Date:           13.04.2021
#   Author:         S.Schütz
#   File:           PMeasurement_Analysis_2nd_Set.py
#   Description:    Analysis of the Dieletric constant and
#                   loss factor of the Dryer mixture at different
#                   concentration.Conc is done from 0% to 100%
#**************************************************************************

import os
import numpy as np
import matplotlib.pyplot as plt

# Setups
mydir = os.getcwd()
os.chdir(mydir + '\\30g_Data_Files') #Change directory
FilesData = os.listdir() #Find all CSV file into folder
print(FilesData,'\n')
Mix_conc = np.linspace(0,1,len(FilesData))

# Load Data
i = 0
for element in FilesData: #Loading all CSV file for all folders
    Data  = np.loadtxt(element, skiprows = 1)
    if i == 0: #First time build the np-array/matrix
        NrRows = Data.shape[0]
        NrCol = 3
        NrWidth = len(FilesData)
        # allData[Nr.Measure,Variables(freq,e1,e2),Concentration]
        allData = np.ones((NrRows, NrCol, NrWidth))

    allData[:,:,i] = Data
    i = i + 1

# Calculate tanD and Er for all data
allData_calc = np.ones((NrRows, NrCol, NrWidth))

allData_calc[:,0,:] = allData[:,0,:] # freq
allData_calc[:,1,:] = np.sqrt(allData[:,1,:]**2 + allData[:,2,:]**2) # er
allData_calc[:,2,:] = np.abs(allData[:,2,:]/allData[:,1,:]) # tanD

# Search 2.4Ghz data
idx = np.where(allData_calc[:,0,:] == 2400000000.0)
idx2 = np.where(allData[:,0,:] == 2400000000.0)

# Create 2.4GHz data matrix
allData_calc_2G4= allData_calc[idx[0][0],:,:]
allData_calc_2G4 = allData_calc_2G4[-2:,:]
allData_2G4 = allData[idx[0][0],:,:]
allData_2G4 = allData_2G4[-2:,:]


# Calculate Theoretial data
allData_2G4_Theo_scal = np.zeros( (len(allData_calc_2G4[:,0]), len(Mix_conc)))
allData_2G4_Theo_polar = np.zeros( (len(allData_calc_2G4[:,0]), len(Mix_conc)))
allData_2G4_Theo_scal[0,:] = allData_2G4[0,-1] * Mix_conc[:] +  allData_2G4[0,0] * (1 - Mix_conc[:])
allData_2G4_Theo_scal[1,:] = allData_2G4[1,-1] * Mix_conc[:] +  allData_2G4[1,0] * (1 - Mix_conc[:])
allData_2G4_Theo_polar[0,:] = np.sqrt(allData_2G4_Theo_scal[0,:]**2  +  allData_2G4_Theo_scal[1,:]**2)
allData_2G4_Theo_polar[1,:] = np.abs(allData_2G4_Theo_scal[1,:]  /  allData_2G4_Theo_scal[0,:])

# # Data regression
# Reg_Order = 3
# NrPoint = 10
# ConcetrationSweep = np.linspace(min(Mix_conc),max(Mix_conc),NrPoint)
# allData_Regr_2G4_polar = np.zeros( (len(allData_calc_2G4[:,0]), len(ConcetrationSweep)))
# allData_Regr_2G4_scal = np.zeros( (len(allData_calc_2G4[:,0]), len(ConcetrationSweep)))

# # # Create Polynomial coefficient matrix to calculate Er and tan(d) vs conc
# Poly_Coeff_Conc_polar = np.zeros( (len(allData_calc_2G4[:,0]), (Reg_Order+1)))
# Poly_Coeff_Conc_scal = np.zeros( (len(allData_calc_2G4[:,0]), (Reg_Order+1)))

# # Calculate regression coeff.
# Poly_Coeff_Conc_polar[0,:] = np.polyfit(Mix_conc, allData_calc_2G4[0,:], Reg_Order) #Er
# Poly_Coeff_Conc_polar[1,:] = np.polyfit(Mix_conc, allData_calc_2G4[1,:], Reg_Order) #tan(d)
# Poly_Coeff_Conc_scal[0,:] = np.polyfit(Mix_conc, allData_2G4[0,:], Reg_Order) #E1
# Poly_Coeff_Conc_scal[1,:] = np.polyfit(Mix_conc, allData_2G4[1,:], Reg_Order) #E2

# # Evaluate regression
# allData_Regr_2G4_polar[0,:] = np.polyval(Poly_Coeff_Conc_polar[0,:], ConcetrationSweep) #Er
# allData_Regr_2G4_polar[1,:] = np.polyval(Poly_Coeff_Conc_polar[1,:], ConcetrationSweep) #tan(d)
# allData_Regr_2G4_scal[0,:] = np.polyval(Poly_Coeff_Conc_scal[0,:], ConcetrationSweep) #E1
# allData_Regr_2G4_scal[1,:] = np.polyval(Poly_Coeff_Conc_scal[1,:], ConcetrationSweep) #E2

# Data plotting
plt.figure(1)
fig, ax = plt.subplots()
plt.style.use('bmh')
ax.plot(Mix_conc*100,allData_2G4[0,:], 'ro', linestyle="None") 
ax.plot(Mix_conc*100,allData_2G4_Theo_scal[0,:], color='red') 
ax.set_xlabel('TPA Concentration [%]')
ax.set_ylabel('Equivalent Re(Er)  [-]')   
ax.set_title('Re(Er) = f(C) @ f = 2.45GHz')      
ax.legend(['Meas', 'Teo'],loc='upper right')                                                                              
# home directory
os.chdir(mydir)
plt.savefig('fig1 - Re(Er) = f(C) @ f = 2.45GHz.jpg')

plt.figure(2)
fig, ax = plt.subplots()
plt.style.use('bmh')
ax.plot(Mix_conc*100,allData_2G4[1,:], 'ro', linestyle="None") 
ax.plot(Mix_conc*100,allData_2G4_Theo_scal[1,:], color='red') 
ax.set_xlabel('TPA Concentration [%]')
ax.set_ylabel('Equivalent Im(Er)  [-]')   
ax.set_title('Im(Er) = f(C) @ f = 2.45GHz')        
ax.legend(['Meas', 'Teo'],loc='upper right')                                                                               
# home directory
os.chdir(mydir)
plt.savefig('fig2 - Im(Er) = f(C) @ f = 2.45GHz.jpg')

plt.figure(3)
fig, ax = plt.subplots()
plt.style.use('bmh')

ax.plot(Mix_conc*100,allData_calc_2G4[0,:], 'bo', linestyle="None") 
ax.plot(Mix_conc*100,allData_2G4_Theo_polar[0,:], color='blue') 
ax.set_xlabel('TPA Concentration [%]')
ax.set_ylabel('Equivalent Er  [-]')   
ax.set_title('Er = f(C) @ f = 2.45GHz')        
ax.legend(['Meas', 'Teo'],loc='upper right')                                                                               
# home directory
os.chdir(mydir)
plt.savefig('fig3 - Er = f(C) @ f = 2.45GHz.jpg')

plt.figure(4)
fig, ax = plt.subplots()
plt.style.use('bmh')

ax.plot(Mix_conc*100,allData_calc_2G4[1,:], 'bo', linestyle="None") 
ax.plot(Mix_conc*100,allData_2G4_Theo_polar[1,:], color='blue') 
ax.set_xlabel('TPA Concentration [%]')
ax.set_ylabel('Equivalent tan(d)  [-]')   
ax.set_title('tan(d) = f(C) @ f = 2.45GHz')  
ax.legend(['Meas', 'Teo'],loc='upper right')                                                                                     
# home directory
os.chdir(mydir)
plt.savefig('fig4 - tan(d) = f(C) @ f = 2.45GHz.jpg')


plt.figure(5)
fig, axs = plt.subplots(2,2)
plt.style.use('bmh')
fig.suptitle('Mixture (TPA & H2O) - Concentration @ 2.45GHz', fontsize=16)              
fig.set_figheight(10)
fig.set_figwidth(10)

axs[0,0].plot(Mix_conc*100,allData_2G4[0,:], 'ro', linestyle="None") 
axs[0,0].plot(Mix_conc*100,allData_2G4_Theo_scal[0,:], color='red') 
axs[0,0].set_xlabel('TPA Concentration [%]')
axs[0,0].set_ylabel('Equivalent Re(Er)  [-]')        
axs[0,0].legend(['Meas', 'Teo'],loc='upper right')   
axs[0,0].set_title('Complex representation', fontweight='bold')

axs[1,0].plot(Mix_conc*100,allData_2G4[1,:], 'ro', linestyle="None") 
axs[1,0].plot(Mix_conc*100,allData_2G4_Theo_scal[1,:], color='red') 
axs[1,0].set_xlabel('TPA Concentration [%]')
axs[1,0].set_ylabel('Equivalent Im(Er)  [-]')        
axs[1,0].legend(['Meas', 'Teo'],loc='upper right')  

axs[0,1].plot(Mix_conc*100,allData_calc_2G4[0,:], 'bo', linestyle="None") 
axs[0,1].plot(Mix_conc*100,allData_2G4_Theo_polar[0,:], color='blue') 
axs[0,1].set_xlabel('TPA Concentration [%]')
axs[0,1].set_ylabel('Equivalent Er  [-]')         
axs[0,1].legend(['Meas', 'Teo'],loc='upper right')     
axs[0,1].set_title('Polar representation', fontweight='bold')

axs[1,1].plot(Mix_conc*100,allData_calc_2G4[1,:], 'bo', linestyle="None") 
axs[1,1].plot(Mix_conc*100,allData_2G4_Theo_polar[1,:], color='blue') 
axs[1,1].set_xlabel('TPA Concentration [%]')
axs[1,1].set_ylabel('Equivalent tan(d)  [-]')   
axs[1,1].legend(['Meas', 'Teo'],loc='upper right')    

# Tight layout often produces nice results
# but requires the title to be spaced accordingly
fig.tight_layout()
fig.subplots_adjust(top=0.91)

# home directory
os.chdir(mydir)
plt.savefig('fig5 - Mixture (TPA & H2O) - Concentration @ 2.45GHz.jpg')