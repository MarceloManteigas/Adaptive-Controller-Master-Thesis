# -*- coding: utf-8 -*-
import os, pprint
pp=pprint.PrettyPrinter() # we'll use this later.
from  epanettools.epanettools import EPANetSimulation, Node, Link, Network, Nodes,Links, Patterns, Pattern, Controls, Control # import all elements needed
from epanettools.examples import simple # this is just to get the path of standard examples
file = os.path.join(os.path.dirname(simple.__file__),'Net3.inp') # open an example
es=EPANetSimulation(file)

#https://pypi.org/project/EPANET/

#Nodes
len(es.network.nodes)

list(es.network.nodes)[:5]
[es.network.nodes[x].id for x in list(es.network.nodes)[:5]] # Get ids of first five nodes.

n=es.network.nodes
n[4].id
n[94].id
n['10'].index # get the index of the node with id '10'

#Links
m=es.network.links
len(m)
m[1].id
m[3].id
m[119].id

#connectivity
[m[1].start.id,m[1].end.id] # get the two ends of a link
[m[118].start.id,m[118].end.id]
sorted([i.id for i in n['169'].links])

#Types of links and nodes
pp.pprint(Node.node_types) # these are the type codes for nodes
n[94].node_type
n[1].node_type
n['2'].node_type
pp.pprint(Link.link_types) # these are the type codes for links
m['335'].link_type # Pump
m['101'].link_type # PIPE
[y.id for x,y in m.items() if y.link_type==Link.link_types['PUMP']] # get ids of pumps
[y.id for x,y in n.items() if y.node_type==Node.node_types['TANK']] # get ids of tanks

#Network properties are available (even before we run the simulation)
es.network.links['335'].results[12] #this gives the value of the pump 1 or 0
es.network.links['10'].results[12] #this gives the value of the pump 1 or 0

d=Link.value_type['EN_DIAMETER']
print("%.3f" % es.network.links[1].results[d][0])
p1=es.network.patterns[1]
l=list(p1.values())
print("%2.1f "*len(l) % tuple(l )) # doctest: +NORMALIZE_WHITESPACE

#para o nivel inicial usa en tanklevel para os niveis seguintes usa a pressão
es.run()
a=Node.value_type['EN_TANKLEVEL']
waterlevel=es.network.nodes['2'].results[a]

p=Node.value_type['EN_PRESSURE']
print("%.3f" % es.network.nodes['103'].results[p][8])
d=Node.value_type['EN_DEMAND']
h=Node.value_type['EN_HEAD']
print("%.3f" % es.network.nodes['103'].results[h][5])
d=Link.value_type['EN_DIAMETER']
print("%.3f" % es.network.links[1].results[d][0])
es.runq() # run water quality simulation
q=Node.value_type['EN_QUALITY']
print("%.3f" % es.network.nodes['117'].results[q][4])
e=Link.value_type['EN_ENERGY']
print("%.5f" % es.network.links['111'].results[e][23])

#Some advanced result queries

print("%.3f" % min(es.network.nodes['103'].results[p])) # minimum recorded pressure of node '103'
n=es.network.nodes
# All nodes recording negative pressure.
sorted([y.id for x,y in n.items() if min(y.results[p])<0])
# Nodes that deliver a flow of more than 4500 flow units
d=Node.value_type['EN_DEMAND']
j=Node.node_types['JUNCTION']
sorted([y.id for x,y in n.items() if ( max(y.results[d])>4500 and y.node_type==j )])

j=Node.node_types['TANK']
sorted([y.id for x,y in n.items() if ( max(y.results[h])>0 and y.node_type==j )])

'''
Changing the network
Currently the new (object-based) interface above only supports read access to the underlying network. To change the values of the network, it is recommended to use the Legacy interface calls. Legacy calls can be accessed from within the new interface. The steps in changing network:

Create an object of EPANetSimulation with the network file
Change needed values using ENsetxxxx calls (just changing the attributes of EPANetSimulation will not work!)
Save the changed data to a new file using ENsaveinpfile.
Create an object of EPANetSimulation with the new saved file.
'''
d=Link.value_type['EN_DIAMETER']
e=Node.value_type['EN_ELEVATION']
es.network.links[81].results[d] # new interface
es.ENgetnodevalue(55,e)[1] # low level interface
es.network.nodes[55].results[e] #new interface
r=es.ENsetlinkvalue(81,d,99) # now let's change values - link
r # zero means no error!
r=es.ENsetnodevalue(55,e,18.25) # change elevation of node
r #zero means no error
 # Note: the original network is not changed! Only the low level values changed. This is a limitation of current implementation
es.network.links[81].results[d], es.ENgetlinkvalue(81,d)[1], es.network.nodes[55].results[e], es.ENgetnodevalue(55,e)[1]
# to permanantly change values, the changed network has to  be written to a new file
import tempfile, os
f=os.path.join(tempfile.gettempdir(),"temp.inp")
es.ENsaveinpfile(f) # save the changed file
e2=EPANetSimulation(f)
e2.network.links[81].results[d], e2.ENgetlinkvalue(81,d)[1], e2.network.nodes[55].results[e], e2.ENgetnodevalue(55,e)[1]

# now in both high level and low level interfaces, we have the right value.

'''
changing the pattern of the network
'''
patId = "NewPattern";
ret=es.ENaddpattern(patId)
print(ret)
patFactors=[0.8, 1.1, 1.4, 1.1, 0.8, 0.7, 0.9, 0.0, 0.8, 0.8, 0.0, 0.0]
ret,patIndex=es.ENgetpatternindex(patId)
print(patIndex)
es.ENsetpattern(patIndex, patFactors)
es.ENgetpatternid(6)[1]
es.ENgetpatternlen(6)
[round(es.ENgetpatternvalue(6,i)[1],3) for i in range(1,12+1)]
es.ENsetpatternvalue(6,9,3.3)
[round(es.ENgetpatternvalue(6,i)[1],3) for i in range(1,12+1)]


"""

hidraulic simulation realm

"""

import os
from epanettools import epanet2 as et
from epanettools.examples import simple
file = os.path.join(os.path.dirname(simple.__file__),'Net3.inp')
ret=et.ENopen(file,"Net3.rpt","")

#Basic properties of the network

ret,result=et.ENgetcount(et.EN_LINKCOUNT)
print(ret)
print(result)
ret,result=et.ENgetcount(et.EN_NODECOUNT)
print(ret)
print(result)
node='10'
ret,index=et.ENgetnodeindex(node)
print(ret)
print ("Node " + node + " has index : " + str(index))

#Get the list of nodes

ret,nnodes=et.ENgetcount(et.EN_NODECOUNT)
retl,nlinks=et.ENgetcount(et.EN_LINKCOUNT)
links=[]
nodes=[]
pres=[]
time=[]
for index in range(1,nnodes):
    ret,t=et.ENgetnodeid(index)
    nodes.append(t)
    t=[]
    pres.append(t)
print (nodes) 
for index in range(1,nlinks):
    ret,t=et.ENgetlinkid(index)
    links.append(t)
    t=[]
    pres.append(t)
print(links)
     #doctest: +ELLIPSIS
                   #doctest: +NORMALIZE_WHITESPACE

#Get nodes indexes on either side of a link with given index

et.ENgetlinknodes(55) # note the first item in the list should be ignored.

#Hydraulic Simulation
pump=[]


et.ENopenH()
et.ENinitH(0)


while True :
    ret,t=et.ENrunH()
    if t%3600!=0:
        ret,tstep=et.ENnextH()
        if (tstep<=0):
            break
    else:   
        time.append(t)
        # Retrieve hydraulic results for time t
        for  i in range(0,len(nodes)):
            ret,p=et.ENgetnodevalue(i+1, et.EN_PRESSURE )
            pres[i].append(p)
        ret,tstep=et.ENnextH()
        a=et.ENsetlinkvalue(nlinks,et.EN_STATUS,1)
        a,b=et.ENgetlinkvalue(nlinks,et.EN_STATUS)
        pump.append(b)
        if (tstep<=0):
            break
ret=et.ENcloseH()
print([round(x,4) for x in pres[94]])

for i in range(0,len(time)):
    print(time[i]/3600)
    print(pump[i])


#pumps id is 10 and 335