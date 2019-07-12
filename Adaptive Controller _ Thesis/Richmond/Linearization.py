# -*- coding: utf-8 -*-
"""
Created on Wed May 29 10:42:29 2019
The purpose of this file is to discover the relation between the increase in pumping time and the amount of pumped water
This relation is different for every link node relation (pump tank relation)

@author: Marcelo
"""
from epanettools.epanettools import EPANetSimulation,Node,Link,Network,Nodes, Links,Patterns,Pattern,Controls,Control
es=EPANetSimulation('richmondNet.inp')

es_links=es.network.links
es_nodes=es.network.nodes

#Pumps indexes

Pump_7F=es_links['7F'].index
Pump_2A=es_links['2A'].index
Pump_5C=es_links['5C'].index
Pump_6D=es_links['6D'].index
Pump_3A=es_links['3A'].index
Pump_4B=es_links['4B'].index
Pump_1A=es_links['1A'].index

#Tanks indexes

Tank_C=es_nodes['C'].index
Tank_A=es_nodes['A'].index
Tank_D=es_nodes['D'].index
Tank_B=es_nodes['B'].index
Tank_E=es_nodes['E'].index
Tank_F=es_nodes['F'].index

'''
Simulation
'''
import os
from random import randint
from epanettools import epanet2 as et
from epanettools.examples import simple
file = os.path.join(os.path.dirname(simple.__file__),'richmondNet_1.inp')
ret=et.ENopen(file,"richmondNet_1.rpt","")


time=[]
Pump_status_1A=[]
Pump_status_2A=[]
Pump_status_3A=[]
Pump_status_4B=[]
Pump_status_5C=[]
Pump_status_6D=[]
Pump_status_7F=[]
Tank_level_A=[]
Tank_level_B=[]
Tank_level_C=[]
Tank_level_D=[]
Tank_level_E=[]
Tank_level_F=[]




inc=0
p_status_1A=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #CBTariff
p_status_2A=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #CBTariff
p_status_3A=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #STTariff
p_status_4B=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #LZHZTariff
p_status_5C=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #HHTariff
p_status_6D=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #LZGTariff
p_status_7F=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #STariff
h=[]

for a in range(0,25):
    p_status_1A[a]=1
    p_status_2A[a]=1    
    p_status_3A[a]=1
    p_status_4B[a]=1
    p_status_5C[a]=1
    p_status_6D[a]=1
    p_status_7F[a]=1


    
    
    
    time=[]
    Tank_level_A=[]
    Tank_level_B=[]
    Tank_level_C=[]
    Tank_level_D=[]
    Tank_level_E=[]
    Tank_level_F=[]
    inc=0

    et.ENopenH()
    et.ENinitH(0)

    while True:
        ret,t=et.ENrunH()
        
        
        if t%3600!=0:
            ret,tstep=et.ENnextH()
            
    
            if (tstep<=0):
                break
        else:   
            time.append(t)
            
            #play with pump status to obtain diferent water level curves
            
            ret=et.ENsetlinkvalue(Pump_1A,et.EN_STATUS,p_status_1A[inc])
            ret=et.ENsetlinkvalue(Pump_2A,et.EN_STATUS,p_status_2A[inc])
            ret=et.ENsetlinkvalue(Pump_3A,et.EN_STATUS,p_status_3A[inc])
            ret=et.ENsetlinkvalue(Pump_4B,et.EN_STATUS,p_status_4B[inc])
            ret=et.ENsetlinkvalue(Pump_5C,et.EN_STATUS,p_status_5C[inc])
            ret=et.ENsetlinkvalue(Pump_6D,et.EN_STATUS,p_status_6D[inc])
            ret=et.ENsetlinkvalue(Pump_7F,et.EN_STATUS,p_status_7F[inc])
            
            
            ret,TA=et.ENgetnodevalue(Tank_A, et.EN_PRESSURE)
            ret,TB=et.ENgetnodevalue(Tank_B, et.EN_PRESSURE)
            ret,TC=et.ENgetnodevalue(Tank_C, et.EN_PRESSURE)
            ret,TD=et.ENgetnodevalue(Tank_D, et.EN_PRESSURE)
            ret,TE=et.ENgetnodevalue(Tank_E, et.EN_PRESSURE)
            ret,TF=et.ENgetnodevalue(Tank_F, et.EN_PRESSURE)
            ret,P1A=et.ENgetlinkvalue(Pump_1A,et.EN_STATUS)
            ret,P2A=et.ENgetlinkvalue(Pump_2A,et.EN_STATUS)
            ret,P3A=et.ENgetlinkvalue(Pump_3A,et.EN_STATUS)
            ret,P4B=et.ENgetlinkvalue(Pump_4B,et.EN_STATUS)
            ret,P5C=et.ENgetlinkvalue(Pump_5C,et.EN_STATUS)
            ret,P6D=et.ENgetlinkvalue(Pump_6D,et.EN_STATUS)
            ret,P7F=et.ENgetlinkvalue(Pump_7F,et.EN_STATUS)
            
            #ret,TF2=et2.ENgetnodevalue(Tank_F, et.EN_PRESSURE )
            #print('TF={} and TF2={}, the distubarnce=TF-TF2={} '.format(TF, TF2,TF-TF2))
            #d.append(TF-TF2)
    
            #ret,E7F=et.ENgetlinkvalue(Pump_7F,et.EN_ENERGY)
            #print(E7F)
            
            
            Tank_level_A.append(TA)
            Tank_level_B.append(TB)
            Tank_level_C.append(TC)
            Tank_level_D.append(TD)
            Tank_level_E.append(TE)
            Tank_level_F.append(TF)
            
            ret,tstep=et.ENnextH()
            inc=inc+1
            if (tstep<=0):
                break
            
    ret=et.ENcloseH()
    
    h.append(Tank_level_F[24])

import matplotlib.pyplot as plt
import numpy as np;

#water level of the tanks
plt.figure(figsize=(10,10))
plt.plot(np.linspace(0,25,25),Tank_level_A,label="TankA")
plt.plot(np.linspace(0,25,25),Tank_level_B,label="TankB")
plt.plot(np.linspace(0,25,25),Tank_level_C,label="TankC")
plt.plot(np.linspace(0,25,25),Tank_level_D,label="TankD")
plt.plot(np.linspace(0,25,25),Tank_level_E,label="TankE")
plt.plot(np.linspace(0,25,25),Tank_level_F,label="TankF")
plt.legend()
plt.title('water level over 24h')
plt.xlabel('Time (h)')
plt.ylabel('water level')
plt.grid()
plt.show()

#water level of the tanks
plt.figure(figsize=(10,10))
plt.plot(np.linspace(0,24,25),h[0:25],label="TankA")
#plt.plot(np.linspace(0,25,25),Tank_level_A2,label="TankA2")
plt.legend()
plt.title('water level over 24h')
plt.xlabel('Time (h)')
plt.ylabel('water level')
plt.grid()
plt.show()

from sklearn.linear_model import LinearRegression

model = LinearRegression()

x = np.array([8,9,10,11,12,13]).reshape((-1, 1))
y = np.array(h[8:14])
model.fit(x,y)
slope=model.coef_
'''
#Pump Curves
plt.figure(figsize=(10,10))
plt.plot(np.linspace(0,25,25),Pump_status_1A,label="Pump1A")
plt.plot(np.linspace(0,25,25),Pump_status_2A,label="Pump2A")
plt.plot(np.linspace(0,25,25),Pump_status_3A,label="Pump3A")
plt.plot(np.linspace(0,25,25),Pump_status_4B,label="Pump4B")
plt.plot(np.linspace(0,25,25),Pump_status_5C,label="Pump5C")
plt.plot(np.linspace(0,25,25),Pump_status_6D,label="Pump6D")
plt.plot(np.linspace(0,25,25),Pump_status_7F,label="Pump7F")
plt.legend()
plt.title('Pump Status over 24h')
plt.xlabel('Time (h)')
plt.ylabel('pump status')
plt.grid()
plt.show()
'''

'''
slopes 
Pumps A to tank A- 0.3m/hour.pumping (the 3 pumps in a sinronized way)
Pump B to tank B- 0.3m/hour.pumping
pump C to tank C- 0.12m/hour.pumping
pump D to tank D- 0.3m/hour.pumping
pump D to tank E- 0.25m/hour.pumping
pump F to tank F- 0.4m/hour.pumping

This difference is due to the type of pump to the distance of the pump/tank, 
to whether or not the pump is using the force of gravity(if the tank is much higher or much lower than the tank) and many other
factor, thus this linearization process is very useful to understand in a simple way the correlation betwwen the pumps and the
tanks they feed.


'''