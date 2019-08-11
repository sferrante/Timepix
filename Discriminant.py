import numpy as np
%matplotlib inline
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import glob
import time
import random
from scipy.stats import norm
plt.rcParams["figure.figsize"] = (3,3)

########################## New Block ##############################################################################

######## Assuming we already have: #######
##    deltaT_b, deltaT_s
##    dT_b, dT_s 
##    NewdeltaT_b, NewdeltaT_s
##    eb, es
##    ebpair, espair
######## Print their lengths...   #########
print('deltaT (bkg & sig)                       : ' + str(len(deltaT_b)) + ' ' +  str(len(deltaT_s)))
print('deltaT (bkg & sig) w/ events thrown away : ' + str(len(dT_b)) + ' ' +  str(len(dT_s)))
print('NEWdeltaT (bkg & sig)                    : ' + str(len(NewdeltaTb)) + ' ' +  str(len(NewdeltaTs)))
print('Energy (bkg & sig)           : ' + str(len(eb)) + ' ' + str(len(es)))
print('Energy from pairs (bkg & sig): ' + str(len(ebpair)) + ' ' + str(len(espair)))

########################## New Block ##############################################################################

# dT Probability Distribution
Prob_Tbkg = []; Prob_Tsig = []
for i in range(len(NewdeltaTs)):  # Mapping w the 1/(1+x) function ... 
    Prob_Tsig.append(1/(1+abs(1*NewdeltaTs[i])))
for i in range(len(NewdeltaTb)):
    Prob_Tbkg.append(1/(1+abs(1*NewdeltaTb[i])))
# for i in range(200):
#     print(deltaT[i],Probability[i])
fig, ax0 = plt.subplots(nrows=1, ncols=1, figsize=(12, 4))
(n_dT_B, bins_dT_B, patches) = ax0.hist(Prob_Tbkg, bins=400, range = (0, 1), color = 'r', histtype = 'step', density=True)
(n_dT_S, bins_dT_S, patches) = ax0.hist(Prob_Tsig, bins=400, range = (0, 1), color = 'b', histtype = 'step', density=True)
ax0.set_title("deltaT -> 'Probability'", fontsize = 12)
ax0.set_xlabel('[-inf,inf] -> [0,1]',fontsize = 12)
ax0.set_ylabel('Probability',fontsize = 12)
ax0.set_xlim(0,1)
plt.yscale('log')
plt.show()

########################## New Block ##############################################################################

#########################... Shift the e's ...####################################################
espair = list(np.asarray(espair)-405)
ebpair = list(np.asarray(ebpair)-405)  ## --> Don't run this block multiple times!
##################################################################################################

########################## New Block ##############################################################################

# E Probability Distribution
Prob_Ebkg = []; Prob_Esig = []
for i in range(len(ebpair)):   # Mapping w the 1/(1+x) function ... 
    Prob_Ebkg.append(1/(1+abs(1*ebpair[i])))
for i in range(len(espair)):
    Prob_Esig.append(1/(1+abs(1*espair[i])))
# for i in range(200):
#     print(deltaT[i],Probability[i])
fig, ax0 = plt.subplots(nrows=1, ncols=1, figsize=(12, 4))
(n_E_B, bins_E_B, patches) = ax0.hist(Prob_Ebkg, bins=400, range = (0, 1), color = 'r', histtype = 'step', density=True)
(n_E_S, bins_E_S, patches) = ax0.hist(Prob_Esig, bins=400, range = (0, 1), color = 'b', histtype = 'step', density=True)
ax0.set_title("Energy -> Probability", fontsize = 12)
ax0.set_xlabel('[-inf,inf] -> [0,1]',fontsize = 12)
ax0.set_ylabel('Probability',fontsize = 12)
ax0.set_xlim(0,1)
plt.yscale('log')
plt.show()

########################## New Block ##############################################################################

### Try combining..... --> Prob_Tsig & Prob_Tbkg
###                    --> Prob_Esig & Prob_Ebkg
### element-wise multiplication ... ??? --> may not be the best way 
Combined_S = []; Combined_B = []
for i in range(len(Prob_Tsig)):
    Combined_S.append(Prob_Tsig[i]*Prob_Esig[i])
for i in range(len(Prob_Tbkg)):
    Combined_B.append(Prob_Tbkg[i]*Prob_Ebkg[i])
print('T_Prob (bkg & sig): ' + str(len(Prob_Tbkg)) + ' ' +  str(len(Prob_Tsig)))
print('E_Prob (bkg & sig): ' + str(len(Prob_Ebkg)) + ' ' +  str(len(Prob_Esig)))
print('Combined_Prob     : ' + str(len(Combined_B)) + ' ' +  str(len(Combined_S)))

########################## New Block ##############################################################################

## Combined plot
fig, ax0 = plt.subplots(nrows=1, ncols=1, figsize=(12, 4))
(n_CombinedB, bins_CombinedB, patches) = ax0.hist(Combined_B, bins=400, range = (0, 1), color = 'r', histtype = 'step', density=True)
(n_CombinedS, bins_CombinedS, patches) = ax0.hist(Combined_S, bins=400, range = (0, 1), color = 'b', histtype = 'step', density=True)
ax0.set_title("P(Energy) * P(dT)", fontsize = 12) # change the title
ax0.set_xlabel('[-inf,inf] -> [0,1]',fontsize = 12)
ax0.set_ylabel('Probability',fontsize = 12)
ax0.set_xlim(0,1)
plt.yscale('log')
plt.show()

########################## New Block ##############################################################################

# CUT EFFICIENCIES  Background & Signal - Combined
Eff_C_B = []; Eff_C_S = []
Range = []
Ntot_B = sum(n_CombinedB)
Ntot_S = sum(n_CombinedS)
for i in range(len(n_CombinedB)):      ## Traverse across the bins, calculate eff. for each bin 
    Range.append(i/len(n_CombinedB))
    value = 0
    for j in range(len(n_CombinedB)-i):
        value += n_CombinedB[i+j]
    Eff_C_B.append(value/Ntot_B)
for i in range(len(n_CombinedS)):
    value = 0
    for j in range(len(n_CombinedS)-i):
        value += n_CombinedS[i+j]
    Eff_C_S.append(value/Ntot_S)

########################## New Block ##############################################################################

# CUT EFFICIENCIES  Background & Signal - dT
Eff_T_B = []; Eff_T_S = []
Ntot_dT_B = sum(n_dT_B)
Ntot_dT_S = sum(n_dT_S)
for i in range(len(n_dT_B)):
    value = 0
    for j in range(len(n_dT_B)-i):
        value += n_dT_B[i+j]
    Eff_T_B.append(value/Ntot_dT_B)
for i in range(len(n_dT_S)):
    value = 0
    for j in range(len(n_dT_S)-i):
        value += n_dT_S[i+j]
    Eff_T_S.append(value/Ntot_dT_S)
    
########################## New Block ##############################################################################

# CUT EFFICIENCIES  Background&Signal - E
Eff_E_B = []; Eff_E_S = []
Ntot_E_B = sum(n_E_B)
Ntot_E_S = sum(n_E_S)
for i in range(len(n_E_B)):
    value = 0
    for j in range(len(n_E_B)-i):
        value += n_E_B[i+j]
    Eff_E_B.append(value/Ntot_E_B)
for i in range(len(n_E_S)):
    value = 0
    for j in range(len(n_E_S)-i):
        value += n_E_S[i+j]
    Eff_E_S.append(value/Ntot_E_S)

########################## New Block ############################################################################## 

##### Plot Efficiencies vs. Cut  #####
plt.figure(figsize=(8,8))
plt.plot(Range,Eff_C_S)
plt.plot(Range,Eff_C_B)
plt.plot(Range,Eff_T_S)
plt.plot(Range,Eff_T_B)
plt.plot(Range,Eff_E_S)
plt.plot(Range,Eff_E_B)
plt.title('Cut Efficiencies')
plt.xlabel('Cut (Bin #) / 400')
plt.ylabel('Efficiency')
plt.legend(['Combined Signal','Combined Background','dT Signal', 'dT Background', 'E Signal', 'E Background'])


########################## New Block ############################################################################## 

# Try plotting Eff_sig vs Eff_bkg (ROC Curve)
plt.figure(figsize=(8,8))
plt.plot(Eff_T_S,1-np.asarray(Eff_T_B))
plt.plot(Eff_E_S,1-np.asarray(Eff_E_B))
plt.plot(Eff_C_S,1-np.asarray(Eff_C_B))
#plt.title('1 - Eff$_{bkg}$ vs. Eff$_{sig}$')
plt.title('ROC')
plt.xlabel('Eff$_{sig}$')
plt.ylabel('1 - Eff$_{bkg}$')
plt.legend(['dT', 'E', 'Combined'])
# plt.yscale('log')
# plt.xscale('log')
# plt.yscale('logit')
# plt.xscale('logit')
