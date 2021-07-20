# DEMETO - Dryer system
European Union’s Horizon 2020 research and innovation programme, No 768573, project DEMETO

This repository was created to share datas and codes used into the paper:
 - **Title:** "Microwave cavity design and optimisation for a homogeneous and faster drying process inside an industrial agitated nutsche filter", 
 - **Authors:** Sebastiano Schütz, Mauro Di Domenico, Matthieu Jaccard, 
 - **Company:** SUPSI - Department of Innovative Technologies (DTI), Institute for Systems and Applied Electronics (ISEA), Lugano, Ticino, 6900, Switzerland
 - **Corresponding author:** Sebastiano Schuetz (sebastiano.schuetz@suspsi.ch)
 - **URL:** https://www.supsi.ch/isea_en.html
 
The magazine is available on:
  - https://open-research-europe.ec.europa.eu/

## Repository description:
This project is organised into 4 Spyder (Python) projects:
* **1_Mixture_permettivity_theoretical:** contains the Python script that calculate the relative permettivity of the DEMETO mixture for some change of water concentration (0% - 100%). The results of the elaboration are also saved as *picture.jpg* format.
* **2_Mixture_permettivity_30C_measurements:** contains the Python script that loads all *laboratory-measure.prn* databases and plots the measured permettivity of the DEMETO mixture for a constant temperature of 30°C and some change of water concentration (0% - 100%). The results of the elaboration are also saved as *picture.jpg* format.
* **3_Mixture_permettivity_30C-90C_measurements:** contains the Python script that loads all *laboratory-measure.prn*  databases and plots the measured permettivity of the DEMETO mixture for temperature of 30°C to 90C and some change of water concentration (0% - 100%). The results of the elaboration are also saved as *picture.jpg* format.
* **4_Mixture_vloss_heating_effect_measurements:** contains the Python script that loads all *Ansys-HFSS-simulation-results.tab* databases and plots the vloss (heating efficiency) of the microwave cavity during the process of drying the mixture. The results of the elaboration are also saved as *picture.jpg* format.


## Database description:
### Measurement database:
The measurement of the eletricall permettivity of the mixture (TPA + Water) were performed with the *Agilent’s 85070E Dielectric Probe* and the *N5230A vector analyser* and saved as *Measure.prn*. 

For every concentration and temperature a *Measure.prn* was generated according to the following rule:
* **FilePathLocation:** *ProjectFolder/XY gradi*, where XY = temperature °C and contains all File.prn data.
* **File name:** *XY_ABCp_mix.prn*, where XY = temperature °C, ABC = water concentration in %
* **File content:** The shape of the file is always (Nr X 3), Column 1 is the frequency in Hz, Column 2 is the Real Permettivity and Column 3 is the Complex permittivity
  * *Row 1:* frequency	e'	e''
  *	*Row 2:* 1000000000.0000	  75.8813	   5.1081
  *	*Row 3:* 1008000000.0000	  75.5569	   4.9932
  *	*Row 4:* 1016000000.0000	  75.3051	   4.7867
  *	*Row 5:* 1024000000.0000	  75.1730	   4.4877
  *	*Row n:* ...               ...        ...

### Simulation results database:
The simulation results of the heating efficiency into the microwave cavity were performed with  *Ansys Electromagnetics version R2020 – R2, www.ansys.com* with the
*Ansys - 3D High Frequency Electromagnetic Simulation Software  (HFSS)* toll and were saved as *Ansys-HFSS-simulation-results.tab*.

For every concentration and temperature a *Ansys-HFSS-simulation-results.tab* was generated according to the following rule:
* **FilePathLocation:** *ProjectFolder/Data*
* **File name:** *Vloss-@Temp-ConcH2O-ABCp.tab*, ABC = water concentration in %
* **File content:** The shape of the file is always (Nr X 2), Column 1 is the temperature in °C and Column 2 is the Vloss (heating efficency)
  * *Row 1:* "$Mix_Temp []"	"Vloss [] - $conc_H2O='0' $Er='1.76802014977206' ...
  * *Row 2:* 30	0.902423340606861
  * *Row 2:* 50	0.867023484087784
  * *Row 2:* 70	0.83129855572956
  * *Row n:* ... ...
  
  
