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

# Define some functions 
def pixTOnm(x):
    return 0.2745*x + 775 
def nmTOpix(x):
    return (x-775) / 0.2745
def g(x):
    return nmTOpix(  (405*pixTOnm(x)) / (pixTOnm(x)-405)  )
  
########################## New Block ##############################################################################

# Spatial and Temporal Distribution of **BACKGROUND** Events
#################### RATE & RESOLUTION ########################
NumberOfEvents_b = 1000000
RangeOfTime = 1000000000  # In nanosec
###############################################################

initial_xb = []; initial_yb = []; initial_tb = [];
HalfEvents = int(NumberOfEvents_b/2)
for i in range(HalfEvents):
    m = int(random.uniform(0,256))
    #n = int(random.uniform(0,256))
    n = int(random.uniform(90,110))
    o = int(random.uniform(0,256))
    #p = int(random.uniform(0,256))
    p = int(random.uniform(160,180))
    bkg_time_C1 = random.random()*RangeOfTime
    bkg_time_C2 = random.random()*RangeOfTime
    initial_tb.append(bkg_time_C1)
    initial_tb.append(bkg_time_C2)
    initial_xb.append(m)
    initial_yb.append(n)
    initial_xb.append(o)
    initial_yb.append(p)
print('xb, yb, and tb:')
print(len(initial_xb), len(initial_yb), len(initial_tb))



## Sort the initial arrays into time-ordered arrays ##
sort_key = np.argsort(initial_tb)
xb = []; yb = []; tb = []; SVM = []
for j in range(len(sort_key)):
    xb.append(initial_xb[sort_key[j]])
    yb.append(initial_yb[sort_key[j]])
    tb.append(initial_tb[sort_key[j]])
for i in range(5):
    print(xb[i],yb[i],tb[i])
fig, ax0 = plt.subplots(1,1, figsize=(5,4))
h = ax0.hist2d(xb,yb, bins = 256, range = [(0,256),(0,256)])
fig.colorbar(h[3], ax = ax0)
plt.show()

########################## New Block ##############################################################################

# Spatial and Temporal Distribution of **SIGNAL** Events
#################### RATE & RESOLUTION ########################
NumberOfEvents_s = 0.10*NumberOfEvents_b
RangeOfTime = RangeOfTime  # In nanosec (same as bkg)
Resolution = 5             # In nanosec
spatial_res = 7            # Resolution of spatial dispersions ... in pixels!!
###############################################################

initial_xs = []; initial_ys = []; initial_ts = []; SVM_Score = []
HalfEvents = int(NumberOfEvents_s/2)
for i in range(HalfEvents):
    m = int(random.uniform(0,256))
    n = int(random.uniform(160,180))
    o = int(g(m)) + int(random.gauss(0,spatial_res))
    #o = int(g(m))
    p = int(random.uniform(90,110))
    sig_time_C1 = random.random()*RangeOfTime
    resolution_noise = random.gauss(0,Resolution)
    sig_time_C2 = sig_time_C1 + resolution_noise
    initial_ts.append(sig_time_C1)
    initial_ts.append(sig_time_C2)
    initial_xs.append(m)
    initial_ys.append(n)
    initial_xs.append(o)
    initial_ys.append(p)
print('xs, ys, and ts:')
print(len(initial_xs), len(initial_ys), len(initial_ts))

## Sort the initial arrays into time-ordered arrays ##
sort_key = np.argsort(initial_ts)
xs = []; ys = []; ts = []; SVM = []
for j in range(len(sort_key)):
    xs.append(initial_xs[sort_key[j]])
    ys.append(initial_ys[sort_key[j]])
    ts.append(initial_ts[sort_key[j]])
for i in range(5):
    print(xs[i],ys[i],ts[i])
fig, ax0 = plt.subplots(1,1, figsize=(5,4))
h = ax0.hist2d(xs,ys, bins = 256, range = [(0,256),(0,256)])
fig.colorbar(h[3], ax = ax0)
plt.show()

########################## New Block ##############################################################################

# Append signal events to some arrays for  channel 1 & 2
# Append background events to some arrays for channel 1 & 2
# y is ignored for now...
x1_s = []; x2_s = []; t1_s = []; t2_s = []; channel1_s = []; channel2_s = []; 
for i in range(len(xs)):
    if(ys[i]>130): 
        x1_s.append(xs[i])
        t1_s.append(ts[i])
        channel1_s.append(1)
    if(ys[i]<130):
        x2_s.append(xs[i])
        t2_s.append(ts[i])
        channel2_s.append(2)
x1_b = []; x2_b = []; t1_b = []; t2_b = []; channel1_b = []; channel2_b = []
for i in range(len(xb)): 
    if(90<=yb[i]<=110): 
        x1_b.append(xb[i])
        t1_b.append(tb[i])
        channel1_b.append(1)
    if(160<=yb[i]<=180):
        x2_b.append(xb[i])
        t2_b.append(tb[i])
        channel2_b.append(2)

########################## New Block ##############################################################################

# Now apply the CoincidenceAlgorithm to signal and background -> * separately * 

# Preparations - Signal 
TChan1s = []; TChan2s = []; XChan1s = []; XChan2s = []; YChan1s = []; YChan2s = [];
new_Xs = []; new_Ts = []; new_Ys = []; new_Cs = []
Ts = t1_s + t2_s
Xs = x1_s + x2_s
#Ys = y1pair_s + y2pair_s
Cs = channel1_s + channel2_s
print('Lenth of X and T: ' + str(len(Xs)) + ' ' + str(len(Ts)))
sorting_key = np.argsort(Ts)
print('Sorting key is: ' + str(sorting_key))
for j in range(len(sorting_key)):
    new_Xs.append(Xs[sorting_key[j]])
    new_Ts.append(Ts[sorting_key[j]])
  #  new_Ys.append(Ys[sorting_key[j]])
    new_Cs.append(Cs[sorting_key[j]])

    ####### T ########
for i in range(len(t1_s) + len(t2_s)):
    if (new_Cs[i] == 1):
        TChan1s.append(new_Ts[i])
        TChan2s.append(0)
    if (new_Cs[i] == 2):
        TChan1s.append(0)
        TChan2s.append(new_Ts[i])
        
################## Clean top of data #########################
trashs = 0
if TChan1s[0]==0:
    for i in range(len(TChan1s)):
        if TChan1s[i]!=0:
            break
        trashs+=1
        
elif TChan2s[0]==0:
    for i in range(len(TChan2s)):
        if TChan2s[i]!=0:
            break   
        trashs+=1
print('# of elements to delete in the beginning: ' + str(trashs))
#############################################################

        
print('Values of TimeChan 1 and 2 before :')    
for i in range(5):
    print(TChan1s[i], TChan2s[i])
        
for i in range(len(TChan1s)):
    if(TChan1s[i]==0):
        TChan1s[i]=TChan1s[i-1]   
    if(TChan2s[i]==0):
        TChan2s[i]=TChan2s[i-1]  
        
print('Values of TChan 1 and 2 (signal) after :')    
for i in range(5):
    print(TChan1s[i], TChan2s[i])
      
    
    ####### X ########
for i in range(len(x1_s) + len(x2_s)):
    if (new_Cs[i] == 1):
        XChan1s.append(new_Xs[i])
        XChan2s.append(0)
    if (new_Cs[i] == 2):
        XChan1s.append(0)
        XChan2s.append(new_Xs[i])
for i in range(len(XChan1s)):
    if(XChan1s[i]==0):
        XChan1s[i]=XChan1s[i-1]   
    if(XChan2s[i]==0):
        XChan2s[i]=XChan2s[i-1] 
        
#     ####### Y ######## 
# for i in range(len(y1_s) + len(y2_s)):
#     if (new_Cs[i] == 1):
#         YChan1s.append(new_Ys[i])
#         YChan2s.append(0)
#     if (new_Cs[i] == 2):
#         YChan1s.append(0)
#         YChan2s.append(new_Ys[i])
# for i in range(len(YChan1)):
#     if(YChan1[i]==0):
#         YChan1[i]=YChan1[i-1]   
#     if(YChan2[i]==0):
#         YChan2[i]=YChan2[i-1] 
      
print('Length of TimeChan1s: ' + str(len(TChan1s)))
print('Length of TimeChan2s: ' + str(len(TChan2s)))
print('Length of XChan1s: ' + str(len(XChan1s)))
print('Length of XChan1s: ' + str(len(XChan2s)))
# print('Length of AChan1: ' + str(len(AChan1)))
# print('Length of AChan1: ' + str(len(AChan2)))
deltaT_s = []
TC1s = np.asarray(TChan1s)
TC2s = np.asarray(TChan2s)
dT_s = TC1s - TC2s
for i in range(len(dT_s)):
    deltaT_s.append(dT_s[i])
print('Length of deltaTs: ' + str(len(dT_s)))
print('trashs: ' + str(trashs))

############################################################################################################///
############################################################################################################
############################################################################################################///

# Preparations - Background 

TChan1b = []; TChan2b = []; XChan1b = []; XChan2b = []; YChan1b = []; YChan2b = [];
new_Xb = []; new_Tb = []; new_Yb = []; new_Cb = []
Tb = t1_b + t2_b
Xb = x1_b + x2_b
#Ys = y1pair_s + y2pair_s
Cb = channel1_b + channel2_b
print('Lenth of X and T: ' + str(len(Xb)) + ' ' + str(len(Tb)))
sorting_key = np.argsort(Tb)
print('Sorting key is: ' + str(sorting_key))
for j in range(len(sorting_key)):
    new_Xb.append(Xb[sorting_key[j]])
    new_Tb.append(Tb[sorting_key[j]])
  #  new_Ys.append(Ys[sorting_key[j]])
    new_Cb.append(Cb[sorting_key[j]])
    ####### T ########
for i in range(len(t1_b) + len(t2_b)):
    if (new_Cb[i] == 1):
        TChan1b.append(new_Tb[i])
        TChan2b.append(0)
    if (new_Cb[i] == 2):
        TChan1b.append(0)
        TChan2b.append(new_Tb[i])
        
################## Clean top of data #########################
trashb = 0
if TChan1b[0]==0:
    for i in range(len(TChan1b)):
        if TChan1b[i]!=0:
            break
        trashb+=1
        
elif TChan2b[0]==0:
    for i in range(len(TChan2b)):
        if TChan2b[i]!=0:
            break   
        trashb+=1
print('# of elements to delete in the beginning: ' + str(trashb))
#############################################################
        
print('Values of TimeChan 1 and 2 before :')    
for i in range(5):
    print(TChan1b[i], TChan2b[i])
        
for i in range(len(TChan1b)):
    if(TChan1b[i]==0):
        TChan1b[i]=TChan1b[i-1]   
    if(TChan2b[i]==0):
        TChan2b[i]=TChan2b[i-1]  
print('Values of TChan 1 and 2 (background) after :')    
for i in range(5):
    print(TChan1b[i], TChan2b[i])    
    
    ####### X ########
for i in range(len(x1_b) + len(x2_b)):
    if (new_Cb[i] == 1):
        XChan1b.append(new_Xb[i])
        XChan2b.append(0)
    if (new_Cb[i] == 2):
        XChan1b.append(0)
        XChan2b.append(new_Xb[i])   
for i in range(len(XChan1b)):
    if(XChan1b[i]==0):
        XChan1b[i]=XChan1b[i-1]   
    if(XChan2b[i]==0):
        XChan2b[i]=XChan2b[i-1] 
        
#     ####### Y ######## 
# for i in range(len(y1_s) + len(y2_s)):
#     if (new_Cs[i] == 1):
#         YChan1s.append(new_Ys[i])
#         YChan2s.append(0)
#     if (new_Cs[i] == 2):
#         YChan1s.append(0)
#         YChan2s.append(new_Ys[i])
# for i in range(len(YChan1)):
#     if(YChan1[i]==0):
#         YChan1[i]=YChan1[i-1]   
#     if(YChan2[i]==0):
#         YChan2[i]=YChan2[i-1] 
    
        
print('Length of TimeChan1b: ' + str(len(TChan1b)))
print('Length of TimeChan2b: ' + str(len(TChan2b)))
print('Length of XChan1s: ' + str(len(XChan1b)))
print('Length of XChan1s: ' + str(len(XChan2b)))
# print('Length of AChan1: ' + str(len(AChan1)))
# print('Length of AChan1: ' + str(len(AChan2)))
deltaT_b = []
TC1b = np.asarray(TChan1b)
TC2b = np.asarray(TChan2b)
dT_b = TC1b - TC2b
for i in range(len(dT_b)):
    deltaT_b.append(dT_b[i])
print('Length of deltaTb: ' + str(len(dT_b)))
print('trashb: ' + str(trashb))
print('done')


########################## New Block ##############################################################################

## Fix data -- remove first few (n) points ##
#trash  --> # of bad points
for i in (range(trashs)):
    print(i)
    del TChan1s[0]
    del TChan2s[0]
    del XChan1s[0]
    del XChan2s[0]
  #  del YChan1s[0]
  #  del YChan2s[0]
print('Values of TimeChan 1 and 2 after (signal):')    
for i in range(5):
    print(TChan1s[i], TChan2s[i])
###########################################
for i in (range(trashb)):
    print(i)
    del TChan1b[0]
    del TChan2b[0]
    del XChan1b[0]
    del XChan2b[0]
  #  del YChan1b[0]
  #  del YChan2b[0]
print('Values of TimeChan 1 and 2 after (background):')    
for i in range(5):
    print(TChan1b[i], TChan2b[i])

########################## New Block ##############################################################################

# Improved Algorithm -- Signal & Background separately

NewdeltaTs = []
subgrp_s = []
sublength1s = 1
sublength2s = 1
i = 0
saved_indices_s = []

while (i < len(TChan1s)-5):
    ####### For the left hand column ########
    while TChan1s[i]==TChan1s[i+sublength1s]:
        sublength1s+=1
    if sublength1s==1: 
        ####### For the right hand column ########
        while TChan2s[i]==TChan2s[i+sublength2s]:
            sublength2s+=1
        for b in range(sublength2s):
            subgrp_s.append(TChan1s[i+b]-TChan2s[i+b])
        newsubgrp_s = []
        for v in range(len(subgrp_s)):
            newsubgrp_s.append(abs(subgrp_s[v]))
        min_index = newsubgrp_s.index(min(newsubgrp_s)) 
##########################################################################################
        if (len(NewdeltaTs)!=0):
            if (NewdeltaTs[-1]!=subgrp_s[min_index]):
                NewdeltaTs.append(subgrp_s[min_index])
                if (-100 < subgrp_s[min_index] < 100) or 1==1: 
                    saved_indices_s.append(i+min_index)
        if (len(NewdeltaTs)==0):
            NewdeltaTs.append(subgrp_s[min_index])
            if (-100 < subgrp_s[min_index] < 100) or 1==1: 
                saved_indices_s.append(i+min_index)
##########################################################################################
        subgrp_s = []
        i += (sublength2s-1)
        sublength2s = 1
    if sublength1s != 1:
        for k in range(sublength1s):
            subgrp_s.append(TChan1s[i+k]-TChan2s[i+k])
        newsubgrp_s = []
        for w in range(len(subgrp_s)):
            newsubgrp_s.append(abs(subgrp_s[w]))
        min_index = newsubgrp_s.index(min(newsubgrp_s))
##########################################################################################
        if (len(NewdeltaTs)!=0):
            if (NewdeltaTs[-1]!=subgrp_s[min_index]):
                NewdeltaTs.append(subgrp_s[min_index])
                if (-50000 < subgrp_s[min_index] < 50000) or 1==1: 
                    saved_indices_s.append(i+min_index)
        if (len(NewdeltaTs)==0):
            NewdeltaTs.append(subgrp_s[min_index])
            if (-50000 < subgrp_s[min_index] < 50000) or 1==1: 
                saved_indices_s.append(i+min_index)
##########################################################################################
        subgrp_s = []
        i += (sublength1s-1)
        sublength1s = 1
      
for i in range(15):
    print('NewdeltaTs: ' + str(NewdeltaTs[i]))
#############################################################################################################
#############################################################################################################
#############################################################################################################

 ## BACKGROUND ##

NewdeltaTb = []
subgrp_b = []
sublength1b = 1
sublength2b = 1
i = 0
saved_indices_b = []

while (i < len(TChan1b)-5):
    ####### For the left hand column ########
    while TChan1b[i]==TChan1b[i+sublength1b]:
        sublength1b+=1
    if sublength1b==1: 
        ####### For the right hand column ########
        while TChan2b[i]==TChan2b[i+sublength2b]:
            sublength2b+=1
        for b in range(sublength2b):
            subgrp_b.append(TChan1b[i+b]-TChan2b[i+b])
        newsubgrp_b = []
        for v in range(len(subgrp_b)):
            newsubgrp_b.append(abs(subgrp_b[v]))
        min_index = newsubgrp_b.index(min(newsubgrp_b)) 
##########################################################################################
        if (len(NewdeltaTb)!=0):
            if (NewdeltaTb[-1]!=subgrp_b[min_index]):
                NewdeltaTb.append(subgrp_b[min_index])
                if (-1000000 < subgrp_b[min_index] < 1000000) or 1==1: 
                    saved_indices_b.append(i+min_index)
        if (len(NewdeltaTb)==0):
            NewdeltaTb.append(subgrp_b[min_index])
            if (-1000000 < subgrp_b[min_index] < 1000000) or 1==1: 
                saved_indices_b.append(i+min_index)
##########################################################################################
        subgrp_b = []
        i += (sublength2b-1)
        sublength2b = 1
    if sublength1b != 1:
        for k in range(sublength1b):
            subgrp_b.append(TChan1b[i+k]-TChan2b[i+k])
        newsubgrp_b = []
        for w in range(len(subgrp_b)):
            newsubgrp_b.append(abs(subgrp_b[w]))
        min_index = newsubgrp_b.index(min(newsubgrp_b))
##########################################################################################
        if (len(NewdeltaTb)!=0):
            if (NewdeltaTb[-1]!=subgrp_b[min_index]):
                NewdeltaTb.append(subgrp_b[min_index])
                if (-1000000 < subgrp_b[min_index] < 1000000) or 1==1: 
                    saved_indices_b.append(i+min_index)
        if (len(NewdeltaTb)==0):
            NewdeltaTb.append(subgrp_b[min_index])
            if (-1000000 < subgrp_b[min_index] < 1000000) or 1==1: 
                saved_indices_b.append(i+min_index)
##########################################################################################
        subgrp_b = []
        i += (sublength1b-1)
        sublength1b = 1
                                 
for i in range(15):
    print('NewdeltaTb: ' + str(NewdeltaTb[i]))
            
print('done')

########################## New Block ##############################################################################

# Plot dT and improved dT for signal & background
########### Calculate Rate #####################
Rate = (NumberOfEvents_b*10**-6)/(RangeOfTime*10**-9)
################################################
fig, ax0 = plt.subplots(nrows=1, ncols=1, figsize=(12, 4))
Tlim = 500;
nbins = int((2*Tlim)/1.5625); 
ax0.hist(deltaT_b, bins =nbins, range = (-Tlim, Tlim), color = 'k', histtype = 'step') # bkg dT
ax0.hist(deltaT_s, bins =nbins, range = (-Tlim, Tlim), color = 'g', histtype = 'step') # sig dT
ax0.hist(NewdeltaTs, bins =nbins, range = (-Tlim, Tlim), color = 'b', histtype = 'step') # sig improved dT
ax0.hist(NewdeltaTb, bins =nbins, range = (-Tlim, Tlim), color = 'r', histtype = 'step') # bkg improved dT
ax0.set_title("deltaT", fontsize = 12)
ax0.set_xlabel('deltaT, ns',fontsize = 12)
ax0.set_ylabel('counts',fontsize = 12)
ax0.set_xlim(-Tlim,Tlim)
ax0.legend(['Background - %f MHz Rate' %round(Rate,2),'Signal - %ins resolution' %Resolution, 'NEW_Background - %f MHz Rate' %round(Rate,2),'NEW_Signal - %ins resolution' %Resolution])
plt.yscale('log')
print('# deltaT (bkg & sig): ' + str(len(deltaT_b)) + ' ' +  str(len(deltaT_s)))
print('# NEWdeltaT (bkg & sig): ' + str(len(NewdeltaTb)) + ' ' +  str(len(NewdeltaTs)))
plt.show()

########################## New Block ##############################################################################

# By eye, throw away signal events outside of peak
dT_b = deltaT_b; dT_s = []
for i in range(len(deltaT_s)):
    if abs(deltaT_s[i])<40:
        dT_s.append(deltaT_s[i])
print('deltaT (bkg & sig)                       : ' + str(len(deltaT_b)) + ' ' +  str(len(deltaT_s)))
print('deltaT (bkg & sig) w/ events thrown away : ' + str(len(dT_b)) + ' ' +  str(len(dT_s)))
print('NEWdeltaT (bkg & sig)                    : ' + str(len(NewdeltaTb)) + ' ' +  str(len(NewdeltaTs)))     

########################## New Block ##############################################################################

### Find X and T *from Algorithm* ## (skipping Y)
x1pair_s = []; x2pair_s = []; y1pair_s = []; y2pair_s = []; t1pair_s = []; t2pair_s = [];
x1pair_b = []; x2pair_b = []; y1pair_b = []; y2pair_b = []; t1pair_b = []; t2pair_b = [];
for i in range(len(saved_indices_s)):
    index = saved_indices_s[i]
    x1pair_s.append(XChan1s[index])
    x2pair_s.append(XChan2s[index])
#     y1pair_s.append(YChan1s[index])
#     y2pair_s.append(YChan2s[index])
    t1pair_s.append(TChan1s[index])
    t2pair_s.append(TChan2s[index])
for i in range(len(saved_indices_b)):
    index = saved_indices_b[i]
    x1pair_b.append(XChan1b[index])
    x2pair_b.append(XChan2b[index])
#     y1pair_b.append(YChan1b[index])
#     y2pair_b.append(YChan2b[index])
    t1pair_b.append(TChan1b[index])
    t2pair_b.append(TChan2b[index])
print(len(x1pair_s), len(x2pair_s))
# print(len(y1pair_s), len(y2pair_s))
print(len(t1pair_s), len(t2pair_s))
print(len(x1pair_b), len(x2pair_b))
# print(len(y1pair_b), len(y2pair_b))
print(len(t1pair_b), len(t2pair_b))


########################## New Block ##############################################################################

## Plot x1 & x2 for *** Algorithm Pairs *** 
## Then plot 1-D variable: ~Energy
fig, (ax0,ax1) = plt.subplots(ncols=2, figsize=(10, 4))
h = ax0.hist2d(x1pair_b, x2pair_b, bins = 128, range = [(0, 256), (0, 256)])
h2 = ax1.hist2d(x1pair_s, x2pair_s, bins = 128, range = [(0, 256), (0, 256)])
fig.colorbar(h[3], ax = ax0)
fig.colorbar(h[3], ax = ax1)
fig.tight_layout()
plt.show()
##################################################################################
# 1-D energy plot...... SIGNAL & BACKGROUND
# energy related thing
espair = []; ebpair = []
##################################################################################
for i in range(len(x1pair_s)):
    espair.append( (1/ ((1/(pixTOnm(x1pair_s[i]))) + (1/(pixTOnm(x2pair_s[i])))) )  )
for i in range(len(x1pair_b)):
    ebpair.append( (1/ ((1/(pixTOnm(x1pair_b[i]))) + (1/(pixTOnm(x2pair_b[i])))) )  )
##################################################################################
xlim = (385, 425)
fig, ax0 = plt.subplots(nrows=1, ncols=1, figsize=(12, 4))
ax0.hist(espair, bins=300, range = xlim, color = 'b', histtype = 'step')
ax0.hist(ebpair, bins=300, range = xlim, color = 'r', histtype = 'step') 
ax0.set_title("~ Energy", fontsize = 12) # change the title
#ax0.set_xlabel('Energy in some unit.. (probably factors of $\hbar c$ off or something)',fontsize = 12)
ax0.set_xlabel('~ Energy',fontsize = 12)
ax0.set_ylabel('Count',fontsize = 12)
ax0.set_xlim(xlim)

########################## New Block ##############################################################################

## Plot x1 & x2 for *** Straight from x1_s, x1_b, etc... *** 
## Then plot 1-D variable: ~Energy
fig, (ax0,ax1) = plt.subplots(ncols=2, figsize=(10, 4))
h = ax0.hist2d(x1_b, x2_b, bins = 128, range = [(0, 256), (0, 256)])
h2 = ax1.hist2d(x1_s, x2_s, bins = 128, range = [(0, 256), (0, 256)])
fig.colorbar(h[3], ax = ax0)
fig.colorbar(h[3], ax = ax1)
fig.tight_layout()
plt.show()
##################################################################################################
# 1-D energy plot...... SIGNAL & BACKGROUND
# energy related thing
es = []; eb = []
####################################################################################################
for i in range(len(x1_s)):
    es.append( (1/ ((1/(pixTOnm(x1_s[i]))) + (1/(pixTOnm(x2_s[i])))) )  )
for i in range(len(x1_b)):
    eb.append( (1/ ((1/(pixTOnm(x1_b[i]))) + (1/(pixTOnm(x2_b[i])))) )  )
####################################################################################################
xlim = (385, 425)
fig, ax0 = plt.subplots(nrows=1, ncols=1, figsize=(12, 4))
ax0.hist(es, bins=300, range = xlim, color = 'b', histtype = 'step')
ax0.hist(eb, bins=300, range = xlim, color = 'r', histtype = 'step') 
ax0.set_title("~ Energy", fontsize = 12) # change the title
ax0.set_xlabel('Energy in some unit.. (probably factors of $\hbar c$ off or something)',fontsize = 12)
ax0.set_ylabel('Count',fontsize = 12)
ax0.set_xlim(xlim)
print('Energy (bkg & sig)           : ' + str(len(eb)) + ' ' + str(len(es)))
print('Energy from pairs (bkg & sig): ' + str(len(ebpair)) + ' ' + str(len(espair)))

########################## New Block ##############################################################################

# Printing lengths of different arrays ... 
print('deltaT (bkg & sig)                       : ' + str(len(deltaT_b)) + ' ' +  str(len(deltaT_s)))
print('deltaT (bkg & sig) w/ events thrown away : ' + str(len(dT_b)) + ' ' +  str(len(dT_s)))
print('NEWdeltaT (bkg & sig)                    : ' + str(len(NewdeltaTb)) + ' ' +  str(len(NewdeltaTs)))
print('Energy (bkg & sig)           : ' + str(len(eb)) + ' ' + str(len(es)))
print('Energy from pairs (bkg & sig): ' + str(len(ebpair)) + ' ' + str(len(espair)))

########################## New Block ##############################################################################





    
