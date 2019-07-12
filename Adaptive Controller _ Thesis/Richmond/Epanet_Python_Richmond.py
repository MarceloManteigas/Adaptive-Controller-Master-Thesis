# -*- coding: utf-8 -*-
#richmondNet

from Inital_Conditions import tarifario_ST,tarifario_CB,tarifario_S,tarifario_HH,tarifario_LZG,tarifario_LZHZ
import pprint
pp=pprint.PrettyPrinter()
from epanettools.epanettools import EPANetSimulation,Node,Link,Network,Nodes, Links,Patterns,Pattern,Controls,Control
es=EPANetSimulation('richmondNet.inp')

'''
getting to understand the network
'''
Number_nodes=len(es.network.nodes)
Number_links=len(es.network.links)
Number_controls=len(es.network.controls)

pp.pprint(Node.node_types)
pp.pprint(Link.link_types)
pp.pprint(Control.control_types)
pp.pprint(Link.value_type)
pp.pprint(Node.value_type)

[y.id for x,y in es.network.links.items() if y.link_type==Link.link_types['PUMP']] # get ids of pumps
[y.id for x,y in es.network.nodes.items() if y.node_type==Node.node_types['TANK']] # get ids of tanks

'''
['7F', '2A', '5C', '6D', '3A', '4B', '1A'] ---> pumps

['C', 'A', 'D', 'B', 'E', 'F'] ---> tanks
'''

es_links=es.network.links
es_nodes=es.network.nodes

#Pumps indexes
es_links['7F'].link_type
es_links['2A'].link_type
es_links['5C'].link_type
es_links['6D'].link_type
es_links['3A'].link_type
es_links['4B'].link_type
es_links['1A'].link_type
Pump_7F=es_links['7F'].index
Pump_2A=es_links['2A'].index
Pump_5C=es_links['5C'].index
Pump_6D=es_links['6D'].index
Pump_3A=es_links['3A'].index
Pump_4B=es_links['4B'].index
Pump_1A=es_links['1A'].index

#Tanks indexes
es_nodes['C'].node_type
es_nodes['A'].node_type
es_nodes['D'].node_type
es_nodes['B'].node_type
es_nodes['E'].node_type
es_nodes['F'].node_type
Tank_C=es_nodes['C'].index
Tank_A=es_nodes['A'].index
Tank_D=es_nodes['D'].index
Tank_B=es_nodes['B'].index
Tank_E=es_nodes['E'].index
Tank_F=es_nodes['F'].index


es.run()
#Pump status
pump=Link.value_type['EN_STATUS']#this gives the current status of the pump On or Off
print("%.1f" % es.network.links['7F'].results[pump][0])
print("%.1f" % es.network.links['2A'].results[pump][0])
    
#Tanks status

pressure=Node.value_type['EN_PRESSURE']#this gives the water level of the tank for each increment
for i in range(0,27):
    print("%.3f" % es.network.nodes['C'].results[pressure][i] )
    print("%.3f" % es.network.nodes['A'].results[pressure][i] )
    print("%.3f \n" % es.network.nodes['D'].results[pressure][i] )
    


es._close

'''
Simulation
'''
import os
from random import randint
from epanettools import epanet2 as et
from epanettools.examples import simple
file = os.path.join(os.path.dirname(simple.__file__),'richmondNet_1.inp')
ret=et.ENopen(file,"richmondNet.rpt_1","")


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


et.ENopenH()
et.ENinitH(0)


inc=0

d=[]

p_status_1A=[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #CBTariff
p_status_2A=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] #CBTariff
p_status_3A=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] #STTariff
p_status_4B=[0,1,1,1,0,0,1,0,1,0,1,0,1,1,0,1,0,1,0,0,1,0,0,1,1] #LZHZTariff
p_status_5C=[0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,1,1] #HHTariff
p_status_6D=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1] #LZGTariff
p_status_7F=[0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0] #STariff
'''
p_status_1A=[]
p_status_2A=[]
p_status_3A=[]
p_status_4B=[]
p_status_5C=[]
p_status_6D=[]
p_status_7F=[]


for i in range(0,25):
    p_status_1A.append(randint(0,1))
    p_status_2A.append(randint(0,1))
    p_status_3A.append(randint(0,1))
    p_status_4B.append(randint(0,1))
    p_status_5C.append(randint(0,1))
    p_status_6D.append(randint(0,1))
    p_status_7F.append(randint(0,1))
'''    
price_1A=[]
price_2A=[]
price_3A=[]
price_4B=[]
price_5C=[]
price_6D=[]
price_7F=[]

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
        
        
        ret,TA=et.ENgetnodevalue(Tank_A, et.EN_PRESSURE )
        ret,TB=et.ENgetnodevalue(Tank_B, et.EN_PRESSURE )
        ret,TC=et.ENgetnodevalue(Tank_C, et.EN_PRESSURE )
        ret,TD=et.ENgetnodevalue(Tank_D, et.EN_PRESSURE )
        ret,TE=et.ENgetnodevalue(Tank_E, et.EN_PRESSURE )
        ret,TF=et.ENgetnodevalue(Tank_F, et.EN_PRESSURE )
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
        
        #Now do the same for every other pump, and extract out the total cost
        if t==0: 
            Price1A=tarifario_CB(0)
            Price2A=tarifario_CB(0)
            Price3A=tarifario_ST(0)
            Price4B=tarifario_LZHZ(0)
            Price5C=tarifario_HH(0)
            Price6D=tarifario_LZG(0)
            Price7F=tarifario_S(0)
        else: 
            Price1A=tarifario_CB(t/3600)
            Price2A=tarifario_CB(t/3600)
            Price3A=tarifario_ST(t/3600)
            Price4B=tarifario_LZHZ(t/3600)
            Price5C=tarifario_HH(t/3600)
            Price6D=tarifario_LZG(t/3600)
            Price7F=tarifario_S(t/3600)
            
        ret,E1A=et.ENgetlinkvalue(Pump_1A,et.EN_ENERGY)
        ret,E2A=et.ENgetlinkvalue(Pump_2A,et.EN_ENERGY)
        ret,E3A=et.ENgetlinkvalue(Pump_3A,et.EN_ENERGY)
        ret,E4B=et.ENgetlinkvalue(Pump_4B,et.EN_ENERGY)
        ret,E5C=et.ENgetlinkvalue(Pump_5C,et.EN_ENERGY)            
        ret,E6D=et.ENgetlinkvalue(Pump_6D,et.EN_ENERGY)
        ret,E7F=et.ENgetlinkvalue(Pump_7F,et.EN_ENERGY)

        price_1A.append(E1A*Price1A)
        price_2A.append(E2A*Price2A)
        price_3A.append(E3A*Price3A)
        price_4B.append(E4B*Price4B)   
        price_5C.append(E5C*Price5C)        
        price_6D.append(E6D*Price6D)        
        price_7F.append(E7F*Price7F)
        
        Pump_status_1A.append(P1A)
        Pump_status_2A.append(P2A)
        Pump_status_3A.append(P3A)
        Pump_status_4B.append(P4B)
        Pump_status_5C.append(P5C)
        Pump_status_6D.append(P6D)
        Pump_status_7F.append(P7F)
        
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

cost=sum(price_1A)+sum(price_2A)+sum(price_3A)+sum(price_4B)+sum(price_5C)+sum(price_6D)+sum(price_7F)


Tank_level_A2=[]
Tank_level_B2=[]
Tank_level_C2=[]
Tank_level_D2=[]
Tank_level_E2=[]
Tank_level_F2=[]
inc=0

file2 = os.path.join(os.path.dirname(simple.__file__),'richmondNet_2.inp')
ret=et.ENopen(file2,"richmondNet_2.rpt","")
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
        
        
        ret,TA=et.ENgetnodevalue(Tank_A, et.EN_PRESSURE )
        ret,TB=et.ENgetnodevalue(Tank_B, et.EN_PRESSURE )
        ret,TC=et.ENgetnodevalue(Tank_C, et.EN_PRESSURE )
        ret,TD=et.ENgetnodevalue(Tank_D, et.EN_PRESSURE )
        ret,TE=et.ENgetnodevalue(Tank_E, et.EN_PRESSURE )
        ret,TF=et.ENgetnodevalue(Tank_F, et.EN_PRESSURE )
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
     
        Pump_status_1A.append(P1A)
        Pump_status_2A.append(P2A)
        Pump_status_3A.append(P3A)
        Pump_status_4B.append(P4B)
        Pump_status_5C.append(P5C)
        Pump_status_6D.append(P6D)
        Pump_status_7F.append(P7F)
      
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

plt.figure(figsize=(10,10))
plt.plot(np.linspace(0,25,25),Tank_level_A2,label="TankA2")
plt.plot(np.linspace(0,25,25),Tank_level_B2,label="TankB2")
plt.plot(np.linspace(0,25,25),Tank_level_C2,label="TankC2")
plt.plot(np.linspace(0,25,25),Tank_level_D2,label="TankD2")
plt.plot(np.linspace(0,25,25),Tank_level_E2,label="TankE2")
plt.plot(np.linspace(0,25,25),Tank_level_F2,label="TankF2")
plt.legend()
plt.title('water level over 24h')
plt.xlabel('Time (h)')
plt.ylabel('water level')
plt.grid()
plt.show()

plt.figure(figsize=(10,10))
plt.plot(np.linspace(0,25,25),Tank_level_C,label="TankB")
plt.plot(np.linspace(0,25,25),Tank_level_C2,label="TankB2")
plt.legend()
plt.title('water level over 24h')
plt.xlabel('Time (h)')
plt.ylabel('water level')
plt.grid()
plt.show()

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