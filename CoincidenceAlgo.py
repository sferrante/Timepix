import numpy as np
%matplotlib inline
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib.ticker import NullFormatter
from scipy.stats import norm
import glob
import time
plt.rcParams["figure.figsize"] = (3,3)
from collections import defaultdict
print(time.ctime())


########################## New Block ##############################################################################

# read a data file, store all data in arrays
file = " < path/file.csv > "    # filepath  -- csv
data=np.loadtxt(file, dtype= float, delimiter=",", usecols = (0,1,2,3,4)) # save csv file into 'data'

y   = data[:, 0]
x   = data[:, 1]
t   = data[:, 2]
a   = data[:, 3]
n   = data[:, 4]

########################## New Block ##############################################################################
# x,y plot
fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=(9.5, 4))
h = ax0.hist2d(x, y, bins = 256, range = [(0, 256), (0, 256)])
fig.colorbar(h[3], ax = ax0)
h = ax1.hist2d(x, y, bins = 256, range = [(0, 256), (0, 256)], norm=mpl.colors.LogNorm())
fig.colorbar(h[3], ax = ax1)
fig.tight_layout()
plt.show()

########################## New Block ##############################################################################
# select lists of photons which belong to a selected area on the sensor

x1 = []; y1 = []; t1 = []; a1 = []; n1 = []; #tof1 = []; ID1 = []
x2 = []; y2 = []; t2 = []; a2 = []; n2 = []; #tof2 = []; ID2 = []
channel1 = []; channel2 = [];
# Boundaries
px1min = 10;  px1max = 240; py1min = 145; py1max = 160;      # channel 1 x,y window
px2min = 10; px2max = 240; py2min = 75; py2max = 90;         # channel 2 x,y window
nmin = 0
for i in range(len(x)-1):
    if ( px1min < x[i] < px1max and py1min < y[i] < py1max and nmin < n[i]):   # append channel 1 events
        x1.append(x[i])
        y1.append(y[i])
        t1.append(t[i]/4096.*25)
        a1.append(a[i])
        channel1.append(1)
    if ( px2min < x[i] < px2max and py2min < y[i] < py2max and nmin < n[i]):   # append channel 2 events
        x2.append(x[i])
        y2.append(y[i])
        t2.append(t[i]/4096.*25)
        a2.append(a[i])
        channel2.append(2)

        
########################## New Block ##############################################################################
# Preparations 
TimeChan1 = []; TimeChan2 = []; XChan1 = []; XChan2 = []; YChan1 = []; YChan2 = []; AChan1 = []; AChan2 = []
new_X = []; new_T = []; new_Y = []; new_A = []; new_C = []
T = t1 + t2
X = x1 + x2
Y = y1 + y2
A = a1 + a2
C = channel1 + channel2
print('Lenth of X, Y, T, and A: ' + str(len(X)) + ' ' + str(len(Y)) + ' ' + str(len(T)) + ' ' + str(len(A)))
sorting_key = np.argsort(T)
print('Sorting key is: ' + str(sorting_key))
for j in range(len(sorting_key)):
    new_X.append(X[sorting_key[j]])
    new_T.append(T[sorting_key[j]])
    new_Y.append(Y[sorting_key[j]])
    new_C.append(C[sorting_key[j]])
    new_A.append(A[sorting_key[j]])
    
    ####### T ########    //  make the TimeChan arrarys with 0s
for i in range(len(t1) + len(t2)):
    if (new_C[i] == 1):
        TimeChan1.append(new_T[i])
        TimeChan2.append(0)
    if (new_C[i] == 2):
        TimeChan1.append(0)
        TimeChan2.append(new_T[i])
        
################## Clean top of data #########################
trash = 0
if TimeChan1[0]==0:
    for i in range(len(TimeChan1)):
        if TimeChan1[i]!=0:
            break
        trash+=1
        
elif TimeChan2[0]==0:
    for i in range(len(TimeChan2)):
        if TimeChan2[i]!=0:
            break     # trash is the # of events to delete in the beginning
        trash+=1      # for the improved algorithm
#############################################################
        
print('Values of TimeChan 1 and 2 before :')    
for i in range(5):
    print(TimeChan1[i], TimeChan2[i])
        
for i in range(len(TimeChan1)):    # // Fill in the 0s 
    if(TimeChan1[i]==0):
        TimeChan1[i]=TimeChan1[i-1]   
    if(TimeChan2[i]==0):
        TimeChan2[i]=TimeChan2[i-1]  
        
print('Values of TimeChan 1 and 2 after :')    
for i in range(5):
    print(TimeChan1[i], TimeChan2[i])
      
# Repeat for A, X, and Y       
    ####### A ######## 
for i in range(len(a1) + len(a2)):
    if (new_C[i] == 1):
        AChan1.append(new_A[i])
        AChan2.append(0)
    if (new_C[i] == 2):
        AChan1.append(0)
        AChan2.append(new_A[i])
for i in range(len(AChan1)):
    if(AChan1[i]==0):
        AChan1[i]=AChan1[i-1]   
    if(AChan2[i]==0):
        AChan2[i]=AChan2[i-1] 
    
    ####### X ########
for i in range(len(x1) + len(x2)):
    if (new_C[i] == 1):
        XChan1.append(new_X[i])
        XChan2.append(0)
    if (new_C[i] == 2):
        XChan1.append(0)
        XChan2.append(new_X[i])
for i in range(len(XChan1)):
    if(XChan1[i]==0):
        XChan1[i]=XChan1[i-1]   
    if(XChan2[i]==0):
        XChan2[i]=XChan2[i-1] 
        
    ####### Y ######## 
for i in range(len(y1) + len(y2)):
    if (new_C[i] == 1):
        YChan1.append(new_Y[i])
        YChan2.append(0)
    if (new_C[i] == 2):
        YChan1.append(0)
        YChan2.append(new_Y[i])
for i in range(len(YChan1)):
    if(YChan1[i]==0):
        YChan1[i]=YChan1[i-1]   
    if(YChan2[i]==0):
        YChan2[i]=YChan2[i-1] 
print('Length of TimeChan1: ' + str(len(TimeChan1)))
print('Length of TimeChan2: ' + str(len(TimeChan2)))
print('Length of XChan1: ' + str(len(XChan1)))
print('Length of XChan1: ' + str(len(XChan2)))
print('Length of AChan1: ' + str(len(AChan1)))
print('Length of AChan1: ' + str(len(AChan2)))
                # Make the initial dT array
deltaT = []
TC1 = np.asarray(TimeChan1)
TC2 = np.asarray(TimeChan2)
dT = TC1 - TC2
for i in range(len(dT)-1):
    deltaT.append(dT[i])
print('Length of deltaT: ' + str(len(dT)))
print('trash: ' + str(trash))
print('done')

########################## New Block ##############################################################################
  ## Fix data -- remove first few (n) points
n = trash  #  --> # of bad points    **Make sure to only run this block once
for i in (range(n)):
    print(i)
    del TimeChan1[0]
    del TimeChan2[0]
    del XChan1[0]
    del XChan2[0]
    del YChan1[0]
    del YChan2[0]
    del AChan1[0]
    del AChan2[0]
print('Values of TimeChan 1 and 2 after :')    
for i in range(5):
    print(TimeChan1[i], TimeChan2[i])
    
########################## New Block ##############################################################################

#      *** Improved Algorithm ***
NewdeltaT = []
subgrp = []
sublength1 = 1
sublength2 = 1
i = 0
saved_indices = []

## ** For loops can't alter range in i ... must use while loop!! ########
## All printing for debugging have been deleted here
while (i < len(TimeChan1)-5):
    ####### For the left hand column ########
    while TimeChan1[i]==TimeChan1[i+sublength1]:
        sublength1+=1
    if sublength1==1: 
        ####### For the right hand column ########
        while TimeChan2[i]==TimeChan2[i+sublength2]:
            sublength2+=1
        for b in range(sublength2):
            subgrp.append(TimeChan1[i+b]-TimeChan2[i+b])
        newsubgrp = []
        for v in range(len(subgrp)):
            newsubgrp.append(abs(subgrp[v]))
        min_index = newsubgrp.index(min(newsubgrp)) 
######## This is where NewdeltaT gets appended .. the dT window can be specified here!!! ##########
        if (len(NewdeltaT)!=0):
            if (NewdeltaT[-1]!=subgrp[min_index]):
                NewdeltaT.append(subgrp[min_index])
                if -100 < subgrp[min_index] < 100: 
                    saved_indices.append(i+min_index)
        if (len(NewdeltaT)==0):
            NewdeltaT.append(subgrp[min_index])
            if -100 < subgrp[min_index] < 100: 
                saved_indices.append(i+min_index)
##########################################################################################
        subgrp = []
        i += (sublength2-1)
        sublength2 = 1
    if sublength1 != 1:
        for k in range(sublength1):
            subgrp.append(TimeChan1[i+k]-TimeChan2[i+k])
        newsubgrp = []
        for w in range(len(subgrp)):
            newsubgrp.append(abs(subgrp[w]))
        min_index = newsubgrp.index(min(newsubgrp))
######## This is (also) where NewdeltaT gets appended .. the dT window can be specified here!!! ##########
        if (len(NewdeltaT)!=0):
            if (NewdeltaT[-1]!=subgrp[min_index]):
                NewdeltaT.append(subgrp[min_index])
                if -100 < subgrp[min_index] < 100: 
                    saved_indices.append(i+min_index)
        if (len(NewdeltaT)==0):
            NewdeltaT.append(subgrp[min_index])
            if -100 < subgrp[min_index] < 100: 
                saved_indices.append(i+min_index)
##########################################################################################
        subgrp = []
        i += (sublength1-1)
        sublength1 = 1  
print('done')

########################## New Block ##############################################################################

# Plot deltaT and Improved deltaT (NewdeltaT)
fig, ax0 = plt.subplots(nrows=1, ncols=1, figsize=(12, 4))
Tlim = 1000;
nbins = int((2*Tlim)/1.5625); 
ax0.hist(deltaT, bins=nbins, range = (-Tlim, Tlim), color = 'r', histtype = 'step') # old
ax0.hist(NewdeltaT, bins=nbins, range = (-Tlim, Tlim), color = 'b', histtype = 'step') # Improved
ax0.set_title("deltaT", fontsize = 12)
ax0.set_xlabel('deltaT, ns',fontsize = 12)
ax0.set_ylabel('counts',fontsize = 12)
ax0.set_xlim(-Tlim,Tlim)
plt.yscale('log')
plt.show()
print('Red - Vector Algorithm before Corrections: ') # to see how many events the improved algorithm took away
print(str(len(deltaT)) + ' events' ) 
print('Blue - Vector Algorithm after Corrections: ')
print(str(len(NewdeltaT)) + ' events' ) 

########################## New Block ##############################################################################

# We can create the X, Y, T, and A arrays corresponding to the pairs from improved dT algorithm
# note - ** they will be in the dT window specified in algorithm **....... uses --- (saved indices) 
x1pair = []; x2pair = []; y1pair = []; y2pair = []; t1pair = []; t2pair = []; a1pair = []; a2pair = [];
for i in range(len(saved_indices)):
    index = saved_indices[i]
    x1pair.append(XChan1[index])
    x2pair.append(XChan2[index])
    y1pair.append(YChan1[index])
    y2pair.append(YChan2[index])
    t1pair.append(TimeChan1[index])
    t2pair.append(TimeChan2[index])
    a1pair.append(AChan1[index])
    a2pair.append(AChan2[index])
print(len(x1pair), len(x2pair))
print(len(y1pair), len(y2pair))
print(len(t1pair), len(t2pair))
print(len(a1pair), len(a2pair))

########################## New Block ##############################################################################



