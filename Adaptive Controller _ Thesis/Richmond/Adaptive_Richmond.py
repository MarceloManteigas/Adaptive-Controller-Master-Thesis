# -*- coding: utf-8 -*-
"""
Created on Thu May 30 10:21:45 2019

This file will propose an algorithm to apply the adaptive control methodology for the network of richmond
but solely for pump 4B

Tank D    min 0       max 2.11      initial 1.94  LZHZTariff

Linearization pump D to tank D- 0.3m/hour.pumping

@author: Marcelo
"""
#Define Initial conditions and Determine ID's of pumps and tanks

from Inital_Conditions import tarifario_ST,tarifario_CB,tarifario_S,tarifario_HH,tarifario_LZG,tarifario_LZHZ
from epanettools.epanettools import EPANetSimulation,Node,Link,Network,Nodes, Links,Patterns,Pattern,Controls,Control
es=EPANetSimulation('richmondNet.inp')

p_status_1A=[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #CBTariff
p_status_2A=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] #CBTariff
p_status_3A=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] #STTariff
p_status_4B=[0,1,1,1,0,0,1,0,1,0,1,0,1,1,0,1,0,1,0,0,1,0,0,1,1] #LZHZTariff
p_status_5C=[0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,1,1] #HHTariff
p_status_6D=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1] #LZGTariff
p_status_7F=[0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0] #STariff



es_links=es.network.links
es_nodes=es.network.nodes

Pump_7F=es_links['7F'].index
Pump_2A=es_links['2A'].index
Pump_5C=es_links['5C'].index
Pump_6D=es_links['6D'].index
Pump_3A=es_links['3A'].index
Pump_4B=es_links['4B'].index
Pump_1A=es_links['1A'].index

Tank_C=es_nodes['C'].index
Tank_A=es_nodes['A'].index
Tank_D=es_nodes['D'].index
Tank_B=es_nodes['B'].index
Tank_E=es_nodes['E'].index
Tank_F=es_nodes['F'].index



from aux_funcs import Prediction_Richmond,AdaptationOptions,dynamic_search
import os
from epanettools import epanet2 as et
from epanettools.examples import simple

network="richmondNet_1"
#Initializing Constants
Richmond=Prediction_Richmond(network)

ch_PA=0.3
disturbance_A=0
xcorrect_A=0
Tank_level_A=Richmond['Tanks']['A']
Pump_status_1A_2=Richmond['Pumps']['1A']
cost_1A=Richmond['Cost'][0]
Limits_A=[0,3.37]
tariff_CB=[2.40925,6.7945]

ch_PB=0.3
disturbance_B=0
xcorrect_B=0
Tank_level_B=Richmond['Tanks']['B']
Pump_status_4B_2=Richmond['Pumps']['4B']
cost_4B=Richmond['Cost'][3]
Limits_B=[0,3.65]
tariff_LZHZ=[2.456666667,12.34]

ch_PC=0.12
disturbance_C=0
xcorrect_C=0
Tank_level_C=Richmond['Tanks']['C']
Pump_status_5C_2=Richmond['Pumps']['5C']
cost_5C=Richmond['Cost'][4]
Limits_C=[0,2]
tariff_HH=[2.46,9.866]

ch_PD=0.3
disturbance_D=0
xcorrect_D=0
Tank_level_D=Richmond['Tanks']['D']
Pump_status_6D_2=Richmond['Pumps']['6D']
cost_6D=Richmond['Cost'][5]
Limits_D=[0,2.11]
tariff_LZG=[2.46,11.195]

ch_PF=0.4
disturbance_F=0
xcorrect_F=0
Tank_level_F=Richmond['Tanks']['F']
Pump_status_7F_2=Richmond['Pumps']['7F']
cost_7F=Richmond['Cost'][6]
Limits_F=[0,2.19]
tariff_S=[2.44,11.94]
        
#Start Simulation
for i in range(0,25):
    
    Richmond=Prediction_Richmond(network)
    time=[]
    inc=0
    
    cost_1A_2=[]
    cost_2A_2=[]
    cost_3A_2=[]
    Tank_level_A2=[]
    d_A=[]
    
    cost_4B_2=[]
    Tank_level_B2=[]
    d_B=[]
    
    cost_5C_2=[]
    Tank_level_C2=[]
    d_C=[]
    
    cost_6D_2=[]
    Tank_level_D2=[]
    d_D=[]

    Tank_level_E2=[]

    cost_7F_2=[]
    Tank_level_F2=[]
    d_F=[]
    network_real="richmondNet_2_Under"
    file2 = os.path.join(os.path.dirname(simple.__file__),network_real+'.inp')
    ret=et.ENopen(file2,network_real+".rpt","")
    
    
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
            
            ret=et.ENsetlinkvalue(Pump_1A,et.EN_STATUS,Pump_status_1A_2[inc])
            ret=et.ENsetlinkvalue(Pump_2A,et.EN_STATUS,p_status_2A[inc])
            ret=et.ENsetlinkvalue(Pump_3A,et.EN_STATUS,p_status_3A[inc])
            ret=et.ENsetlinkvalue(Pump_4B,et.EN_STATUS,Pump_status_4B_2[inc])
            ret=et.ENsetlinkvalue(Pump_5C,et.EN_STATUS,Pump_status_5C_2[inc])
            ret=et.ENsetlinkvalue(Pump_6D,et.EN_STATUS,Pump_status_6D_2[inc])
            ret=et.ENsetlinkvalue(Pump_7F,et.EN_STATUS,Pump_status_7F_2[inc])
                   
            ret,TA=et.ENgetnodevalue(Tank_A, et.EN_PRESSURE)
            ret,P1A=et.ENgetlinkvalue(Pump_1A,et.EN_STATUS)
            ret,P2A=et.ENgetlinkvalue(Pump_2A,et.EN_STATUS)
            ret,P3A=et.ENgetlinkvalue(Pump_3A,et.EN_STATUS)
    
            ret,TB=et.ENgetnodevalue(Tank_B, et.EN_PRESSURE)
            ret,P4B=et.ENgetlinkvalue(Pump_4B,et.EN_STATUS)

            ret,TC=et.ENgetnodevalue(Tank_C, et.EN_PRESSURE)
            ret,P5C=et.ENgetlinkvalue(Pump_5C,et.EN_STATUS)   

            ret,TD=et.ENgetnodevalue(Tank_D, et.EN_PRESSURE)
            ret,P6D=et.ENgetlinkvalue(Pump_6D,et.EN_STATUS)

            ret,TE=et.ENgetnodevalue(Tank_E, et.EN_PRESSURE)

            ret,TF=et.ENgetnodevalue(Tank_F, et.EN_PRESSURE)
            ret,P7F=et.ENgetlinkvalue(Pump_7F,et.EN_STATUS)
    
            if t==0: 
                Price1A=tarifario_CB(0)
                Price2A=tarifario_CB(0)
                Price3A=tarifario_ST(0)
                Price4B=tarifario_LZHZ(0)
                Price5C=tarifario_HH(0)
                Price6D=tarifario_LZG(0)
                Price7F=tarifario_S(0)
                d_A.append(TA-Richmond['Tanks']['A'][0])
                d_B.append(TB-Richmond['Tanks']['B'][0])
                d_C.append(TC-Richmond['Tanks']['C'][0])
                d_D.append(TC-Richmond['Tanks']['D'][0])
                d_F.append(TF-Richmond['Tanks']['F'][0])
    
            else: 
                Price1A=tarifario_CB(t/3600)
                Price2A=tarifario_CB(t/3600)
                Price3A=tarifario_ST(t/3600)
                Price4B=tarifario_LZHZ(t/3600)
                Price5C=tarifario_HH(t/3600)
                Price6D=tarifario_LZG(t/3600)
                Price7F=tarifario_S(t/3600)
                d_A.append(TA-Richmond['Tanks']['A'][int(t/3600)])
                d_B.append(TB-Richmond['Tanks']['B'][int(t/3600)])
                d_C.append(TC-Richmond['Tanks']['C'][int(t/3600)])
                d_D.append(TD-Richmond['Tanks']['D'][int(t/3600)])
                d_F.append(TF-Richmond['Tanks']['F'][int(t/3600)])
    
            ret,E1A=et.ENgetlinkvalue(Pump_1A,et.EN_ENERGY)
            ret,E2A=et.ENgetlinkvalue(Pump_2A,et.EN_ENERGY)
            ret,E3A=et.ENgetlinkvalue(Pump_3A,et.EN_ENERGY)    
            ret,E4B=et.ENgetlinkvalue(Pump_4B,et.EN_ENERGY)
            ret,E5C=et.ENgetlinkvalue(Pump_5C,et.EN_ENERGY)
            ret,E6D=et.ENgetlinkvalue(Pump_6D,et.EN_ENERGY)
            ret,E7F=et.ENgetlinkvalue(Pump_7F,et.EN_ENERGY)

            cost_1A_2.append(E1A*Price1A)   
            cost_2A_2.append(E2A*Price2A)   
            cost_3A_2.append(E3A*Price3A)             
            cost_4B_2.append(E4B*Price4B)   
            cost_5C_2.append(E5C*Price5C)   
            cost_6D_2.append(E6D*Price6D) 
            cost_7F_2.append(E7F*Price7F)   
            
            Tank_level_A2.append(TA)
            Tank_level_B2.append(TB)
            Tank_level_C2.append(TC)    
            Tank_level_D2.append(TD) 
            Tank_level_E2.append(TE) 
            Tank_level_F2.append(TF) 
            
            ret,tstep=et.ENnextH()
            inc=inc+1
            if (tstep<=0):
                break
            
    ret=et.ENcloseH()
    
    disturbance_A=d_A[i]
    disturbance_B=d_B[i]
    disturbance_C=d_C[i]
    disturbance_D=d_D[i]
    disturbance_F=d_F[i]

    xcorrect_A=xcorrect_A-disturbance_A/ch_PA   
    xcorrect_B=xcorrect_B-disturbance_B/ch_PB
    xcorrect_C=xcorrect_C-disturbance_C/ch_PC
    xcorrect_D=xcorrect_D-disturbance_D/ch_PD
    xcorrect_F=xcorrect_F-disturbance_F/ch_PF


    xcorrect_A,Tank_level_A,Pump_status_1A_2=dynamic_search(xcorrect_A,Tank_level_A,Pump_status_1A_2,i,Limits_A,ch_PA,tariff_CB)    
    xcorrect_B,Tank_level_B,Pump_status_4B_2=dynamic_search(xcorrect_B,Tank_level_B,Pump_status_4B_2,i,Limits_B,ch_PB,tariff_LZHZ)
    xcorrect_C,Tank_level_C,Pump_status_5C_2=dynamic_search(xcorrect_C,Tank_level_C,Pump_status_5C_2,i,Limits_C,ch_PC,tariff_HH)
    xcorrect_D,Tank_level_D,Pump_status_6D_2=dynamic_search(xcorrect_D,Tank_level_D,Pump_status_6D_2,i,Limits_D,ch_PD,tariff_LZG)
    xcorrect_F,Tank_level_F,Pump_status_7F_2=dynamic_search(xcorrect_F,Tank_level_F,Pump_status_7F_2,i,Limits_F,ch_PF,tariff_S)
                

#Cost
Richmond=Prediction_Richmond(network)
Cost_total=0
for i in range(0,len(Richmond['Cost'])):
    Cost_total=Cost_total+sum(Richmond['Cost'][i])       

Richmond2=Prediction_Richmond(network_real)
Cost_total_2=0
for i in range(0,len(Richmond2['Cost'])):
    Cost_total_2=Cost_total_2+sum(Richmond2['Cost'][i])    

Cost_total_3=sum(cost_1A_2)+sum(cost_2A_2)+sum(cost_3A_2)+sum(cost_4B_2)+sum(cost_5C_2)+sum(cost_6D_2)+sum(cost_7F_2)


import matplotlib.pyplot as plt
import numpy as np;


#water level of the tanks
plt.figure(figsize=(10,10))
plt.plot(np.linspace(0,24,25),Richmond['Tanks']['A'],'*k',label="TankA")
plt.plot(np.linspace(0,24,25),Richmond['Tanks']['A'])

plt.plot(np.linspace(0,24,25),Richmond['Tanks']['B'],'+k',label="TankB")
plt.plot(np.linspace(0,24,25),Richmond['Tanks']['B'],)

plt.plot(np.linspace(0,24,25),Richmond['Tanks']['C'],'^k',label="TankC")
plt.plot(np.linspace(0,24,25),Richmond['Tanks']['C'])

plt.plot(np.linspace(0,24,25),Richmond['Tanks']['D'],'ok',label="TankD")
plt.plot(np.linspace(0,24,25),Richmond['Tanks']['D'])

plt.plot(np.linspace(0,24,25),Richmond['Tanks']['E'],'1k',label="TankE")
plt.plot(np.linspace(0,24,25),Richmond['Tanks']['E'])

plt.plot(np.linspace(0,24,25),Richmond['Tanks']['F'],'sk',label="TankF")
plt.plot(np.linspace(0,24,25),Richmond['Tanks']['F'])
plt.legend()
plt.title('water level over 24h')
plt.xlabel('Time (h)')
plt.ylabel('water level')
plt.grid()
plt.show()

#water level of the tanks uncontrolled

#water level of the tanks
plt.figure(figsize=(10,10))
plt.plot(np.linspace(0,24,25),Richmond2['Tanks']['A'],'*k',label="TankA")
plt.plot(np.linspace(0,24,25),Richmond2['Tanks']['A'])

plt.plot(np.linspace(0,24,25),Richmond2['Tanks']['B'],'+k',label="TankB")
plt.plot(np.linspace(0,24,25),Richmond2['Tanks']['B'],)

plt.plot(np.linspace(0,24,25),Richmond2['Tanks']['C'],'^k',label="TankC")
plt.plot(np.linspace(0,24,25),Richmond2['Tanks']['C'])

plt.plot(np.linspace(0,24,25),Richmond2['Tanks']['D'],'ok',label="TankD")
plt.plot(np.linspace(0,24,25),Richmond2['Tanks']['D'])

plt.plot(np.linspace(0,24,25),Richmond2['Tanks']['E'],'1k',label="TankE")
plt.plot(np.linspace(0,24,25),Richmond2['Tanks']['E'])

plt.plot(np.linspace(0,24,25),Richmond2['Tanks']['F'],'sk',label="TankF")
plt.plot(np.linspace(0,24,25),Richmond2['Tanks']['F'])
plt.legend()
plt.title('water level over 24h')
plt.xlabel('Time (h)')
plt.ylabel('water level')
plt.grid()
plt.show()

#water level of the tanks controlled

plt.figure(figsize=(10,10))
plt.plot(np.linspace(0,24,25),Tank_level_A2,'*k',label="TankA2")
plt.plot(np.linspace(0,24,25),Tank_level_A2)

plt.plot(np.linspace(0,24,25),Tank_level_B2,'+k',label="TankB2")
plt.plot(np.linspace(0,24,25),Tank_level_B2)

plt.plot(np.linspace(0,24,25),Tank_level_C2,'^k',label="TankC2")
plt.plot(np.linspace(0,24,25),Tank_level_C2)

plt.plot(np.linspace(0,24,25),Tank_level_D2,'ok',label="TankD2")
plt.plot(np.linspace(0,24,25),Tank_level_D2)

plt.plot(np.linspace(0,24,25),Tank_level_E2,'1k',label="TankE2")
plt.plot(np.linspace(0,24,25),Tank_level_E2)

plt.plot(np.linspace(0,24,25),Tank_level_F2,'sk',label="TankF2")
plt.plot(np.linspace(0,24,25),Tank_level_F2)

plt.legend()
plt.title('water level over 24h')
plt.xlabel('Time (h)')
plt.ylabel('water level')
plt.grid()
plt.show()

print("the cost of the predicted control w/predicted consumption is {}".format(Cost_total))
print("the cost of the predicted control w/real consumption is {}".format(Cost_total_2))
print("the cost of the adaptive control w/real consumption is {}".format(Cost_total_3))


