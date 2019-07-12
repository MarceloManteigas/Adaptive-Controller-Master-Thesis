# -*- coding: utf-8 -*-

#INSTALATION !!!!
#pip install epanettools

#LINKS
#https://pypi.org/project/EPANETTOOLS/
#https://wntr.readthedocs.io/en/latest/apidoc/wntr.epanet.toolkit.html
#https://github.com/Vitens/epynet/blob/master/epynet/epanet2.py


import os,pprint
pp=pprint.PrettyPrinter()
from epanettools.epanettools import EPANetSimulation,Node,Link,Network,Nodes, Links,Patterns,Pattern,Controls,Control
from epanettools.examples import simple
file = os.path.join(os.path.dirname(simple.__file__),'Net3.inp')
es=EPANetSimulation(file)

'''
getting to understand the network
'''

#Number of elements
Number_nodes=len(es.network.nodes)
Number_links=len(es.network.links)
Number_controls=len(es.network.controls)

#List of indexes
List_constrols=[es.network.controls[x].index for x in list(es.network.controls)]
List_nodes=[es.network.nodes[x].id for x in list(es.network.nodes)]
List_links=[es.network.links[x].id for x in list(es.network.links)]

pp.pprint(Node.node_types)
pp.pprint(Link.link_types)
pp.pprint(Control.control_types)
pp.pprint(Link.value_type)
pp.pprint(Node.value_type)

#EN_STATUS : 11

es_links=es.network.links
es_nodes=es.network.nodes

#Pumps indexes
es_links['335'].link_type
es_links['10'].link_type
Pump1=es_links['10'].index
Pump2=es_links['335'].index


#Tanks indexes
es_nodes['1'].node_type
es_nodes['2'].node_type
es_nodes['3'].node_type
Tank1=es_nodes['1'].index
Tank2=es_nodes['2'].index
Tank3=es_nodes['3'].index

es.run()
#Pump status
pump=Link.value_type['EN_STATUS']#this gives the current status of the pump On or Off
print("%.1f" % es.network.links['335'].results[pump][0])
print("%.1f" % es.network.links['10'].results[pump][0])
    
#Tanks status

pressure=Node.value_type['EN_PRESSURE']#this gives the water level of the tank for each increment
for i in range(0,27):
    print("%.3f" % es.network.nodes['1'].results[pressure][i] )
    print("%.3f" % es.network.nodes['2'].results[pressure][i] )
    print("%.3f \n" % es.network.nodes['3'].results[pressure][i] )


'''
Simulation
'''
import os
from random import randint
from epanettools import epanet2 as et
from epanettools.examples import simple
file = os.path.join(os.path.dirname(simple.__file__),'Net3.inp')
ret=et.ENopen(file,"Net3B.rpt","")
time=[]
Pump_status1=[]
Pump_status2=[]
Tank_level1=[]
Tank_level2=[]
Tank_level3=[]


et.ENopenH()
et.ENinitH(0)

inc=0
p_status_1=[]
for i in range(0,25):
    p_status_1.append(randint(0,0))
p_status_2=[]
for i in range(0,25):
    p_status_2.append(randint(0,0))

while True:
    ret,t=et.ENrunH()
    if t%3600!=0:
        ret,tstep=et.ENnextH()
        if (tstep<=0):
            break
    else:   
        time.append(t)
        
        #play with pump status to obtain diferent water level curves
        
        ret=et.ENsetlinkvalue(Pump1,et.EN_STATUS,p_status_1[inc])
        ret=et.ENsetlinkvalue(Pump2,et.EN_STATUS,p_status_2[inc])

        ret,T1=et.ENgetnodevalue(Tank1, et.EN_PRESSURE )
        ret,T2=et.ENgetnodevalue(Tank2, et.EN_PRESSURE )
        ret,T3=et.ENgetnodevalue(Tank3, et.EN_PRESSURE )
        ret,P1=et.ENgetlinkvalue(Pump1,et.EN_STATUS)
        ret,P2=et.ENgetlinkvalue(Pump2,et.EN_STATUS)
        Pump_status1.append(P1)
        Pump_status2.append(P2)
        Tank_level1.append(T1)
        Tank_level2.append(T2)
        Tank_level3.append(T3)
        ret,tstep=et.ENnextH()
        inc=inc+1
        if (tstep<=0):
            break
ret=et.ENcloseH()

import matplotlib.pyplot as plt
import numpy as np;

#water level of the tanks
plt.figure(figsize=(7,7))
plt.plot(np.linspace(0,25,25),Tank_level1,label="Tank1")
plt.plot(np.linspace(0,25,25),Tank_level2,label="Tank2")
plt.plot(np.linspace(0,25,25),Tank_level3,label="Tank2")
plt.legend()
plt.title('water level over 24h')
plt.xlabel('Time (h)')
plt.ylabel('water level')
plt.grid()
plt.show()

#Pump Curves
plt.figure(figsize=(7,7))
plt.plot(np.linspace(0,25,25),Pump_status1,label="Pump1")
plt.plot(np.linspace(0,25,25),Pump_status2,label="Pump2")
plt.legend()
plt.title('water level over 24h')
plt.xlabel('Time (h)')
plt.ylabel('water level')
plt.grid()
plt.show()