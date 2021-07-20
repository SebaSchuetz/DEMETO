# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 15:49:42 2021

@author: sebas
"""
#**************************************************************************
#   Company:        SUPSI DTI ISEA
#   Project:        DEMETO
#   Date:           16.04.2021
#   Author:         S.Schütz
#   File:           TheoreticalCalculation_Permettivity_vs_water.py
#   Description:    Dielectric constant curve of Er and tan(D) theoretical
#                   calculation of the curves (dielectric vs concentration 
#                   of water) in order to use it in Anys simulation.
#**************************************************************************
import numpy as np
import matplotlib.pyplot as plt

# INPUT DATA FROM MEASUREMENTS (excel ConcentrazioneH2OTPA_graficoteorico)
Permettivity_H2O = [75.1367, 10.0208, -1, -1]; #e1, e2, er, tan(D)
Permettivity_TPA = [1.7398, -0.1255, -1, -1]; # LOW

# Calculate Er and tan(D)
Permettivity_H2O[2] = np.sqrt(Permettivity_H2O[0]**2 + Permettivity_H2O[1]**2);
Permettivity_H2O[3] = abs(Permettivity_H2O[1] / Permettivity_H2O[0]);

Permettivity_TPA[2] = np.sqrt(Permettivity_TPA[0]**2 + Permettivity_TPA[1]**2);
Permettivity_TPA[3] = abs(Permettivity_TPA[1] / Permettivity_TPA[0]);

# Theoretical Er and tan(D) in function of conc.
mix_conc_TPA = np.linspace(0,1,11)
Permettivity_mixture = np.zeros((4,len(mix_conc_TPA)))

Permettivity_mixture[0,:] = Permettivity_H2O[0] * (1 - mix_conc_TPA[:]) + Permettivity_TPA[0] * mix_conc_TPA[:]
Permettivity_mixture[1,:] = Permettivity_H2O[1] * (1 - mix_conc_TPA[:]) + Permettivity_TPA[1] * mix_conc_TPA[:]
Permettivity_mixture[2,:] = np.sqrt(Permettivity_mixture[1,:]**2 + Permettivity_mixture[0,:]**2);
Permettivity_mixture[3,:] = abs(Permettivity_mixture[1,:] / Permettivity_mixture[0,:]);

# Data regression
Regr_order = [1, 3] # Er order, tan(D) order
Coeff_Er_mixture = np.polyfit(mix_conc_TPA, Permettivity_mixture[2,:], Regr_order[0])
Coeff_tanD_mixture = np.polyfit(mix_conc_TPA, Permettivity_mixture[3,:], Regr_order[1])

mix_conc_TPA_sweep = np.linspace(0,1,11)
Permettivity_Regression_mixture = np.zeros((len(Permettivity_mixture[:,0]), len(mix_conc_TPA_sweep)))

Permettivity_Regression_mixture[0,:] = np.polyval(Coeff_Er_mixture, mix_conc_TPA_sweep)
Permettivity_Regression_mixture[1,:] = np.polyval(Coeff_tanD_mixture, mix_conc_TPA_sweep)

# Data Plot
plt.figure(1)
fig, axs = plt.subplots(2)
plt.style.use('bmh')
fig.suptitle('Mixture (TPA & H2O) - Concentration @ 2.45GHz', fontsize=16)    
fig.set_figheight(10)
fig.set_figwidth(10)          
# fig.set_figheight(10)
# fig.set_figwidth(10)

axs[0].plot(mix_conc_TPA*100,Permettivity_mixture[2,:], 'ro', linestyle="None") 
axs[0].plot(mix_conc_TPA_sweep*100,Permettivity_Regression_mixture[0,:], color='blue') 
axs[0].set_xlabel('TPA/H2O [%]')
axs[0].set_ylabel('Equivalent Er [-]')        
axs[0].legend(['Tab', 'Regr'],loc='upper right')   
axs[0].set_title('Theoretical Line VS Calculated Line of Er', fontweight='bold')


axs[1].plot(mix_conc_TPA*100,Permettivity_mixture[3,:], 'ro', linestyle="None") 
axs[1].plot(mix_conc_TPA_sweep*100,Permettivity_Regression_mixture[1,:], color='blue') 
axs[1].set_xlabel('TPA/H2O [%]')
axs[1].set_ylabel('Equivalent tan(D) [-]')        
axs[1].legend(['Tab', 'Regr'],loc='upper right')  
axs[1].set_title('Theoretical Line VS Calculated Line of tan(D)', fontweight='bold')

# Tight layout often produces nice results
# but requires the title to be spaced accordingly
fig.tight_layout()
fig.subplots_adjust(top=0.92)

# home directory
plt.savefig('fig1 - Theoretical Permettivity curve of the mixture@concTPA @ 2.45GHz.jpg')
