# -*- coding: utf-8 -*-
"""
Created on Thu May 30 16:49:02 2019

@author: Marcelo
"""
import numpy as np
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

es._close



#Start Simulation
import os
from epanettools import epanet2 as et
from epanettools.examples import simple


def Prediction_Richmond(network):
    
    file = os.path.join(os.path.dirname(simple.__file__),network+".inp")
    ret=et.ENopen(file,network+".rpt","")
    
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
    
    price_1A=[]
    price_2A=[]
    price_3A=[]
    price_4B=[]
    price_5C=[]
    price_6D=[]
    price_7F=[]
    
    #Prediction Model
    while True:
        ret,t=et.ENrunH()
        
        
        if t%3600!=0:
            ret,tstep=et.ENnextH()
            
    
            if (tstep<=0):
                break
        else:   
            time.append(t)
            
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
    
    cost=[price_1A,price_2A,price_3A,price_4B,price_5C,price_6D,price_7F]
    
    Richmond = {
            'Tanks': {'A':Tank_level_A ,'B':Tank_level_B,'C':Tank_level_C,'D':Tank_level_D,'E':Tank_level_E,'F':Tank_level_F,},
            'Pumps':{'1A':Pump_status_1A,'2A':Pump_status_2A,'3A':Pump_status_3A,'4B':Pump_status_4B,'5C':Pump_status_5C,'6D':Pump_status_6D,'7F':Pump_status_7F,},
            'Cost': cost,};
    
    return Richmond



def AdaptationOptions(Tank_level,Pump_status,inc,tariff):
    
    def PricePyramic():
    
        def tarifario(ti):
        # definição do tarifário usando o tempo inicial do incremento
            tarifHora = [None]*3; tarifCusto = [None]*3;
            set(tarifHora)
            tarifHora[0]= 0; tarifCusto[0]=tariff[0] #2.40925 
            tarifHora[1]=8; tarifCusto[1]=tariff[1] #6.7945
            tarifHora[2]=25; 
            tarifF = 0.
            for i in range(0, len(tarifHora)-1):
                if (ti >= tarifHora[i]) & (ti < tarifHora[i+1]):
                    tarifF = tarifCusto[i]
                    
            if tarifF == tariff[0]: level='1'
            if tarifF == tariff[1]: level='2'
                  
            if tarifF == 0.: print("Erro no tarifário",ti,i); quit()
            return level
    
        level1=[]
        level2=[]
        
        for ti in range(0,25):
            level=tarifario(ti)
            if level=="1": level1.append(ti)
            if level=="2": level2.append(ti)
                  
        Price=[level1,level2]
        
        return Price
    
    def HiearchyPump(Tank_level):
        hsorted=np.argsort(Tank_level[inc:len(Tank_level)])
        hsort=[hsorted[i]+inc for i in range(0,len(hsorted))]
        return hsort
    
    
    def BestPumpOptions(hsorted,Price):
        
        bestStep=[]
        Step=[] 
        best=0
        a=len(Price)
        b=len(hsorted)
        for z in range(0,a):
            for y in range(0,b):
                if hsorted[y] in Price[z]:
                    best=best+1
                    bestStep.append(hsorted[y])
                    Step.append(y)

        pumpOptions=bestStep
        return pumpOptions

    Price=PricePyramic()
    hsorted=HiearchyPump(Tank_level)
    pumpPlace=BestPumpOptions(hsorted,Price)     
    
    # definição dos dicionários
    empty_AdaptationState = {
            'TLevel': None,
            'TimeStep': None, 
            'Pump':None,};
    # Create the list to hold the dictionaries
    #print(disturbance)
    AdaptationState=[]
    
    for c in range(0,len(pumpPlace)):
        #Create the dictionary for the current calculated option x
        AdaptationState.append(empty_AdaptationState.copy())  
        #water level without disturbance for option x
        AdaptationState[c]['TLevel']=Tank_level[pumpPlace[c]]
        #Time step of option x
        AdaptationState[c]['TimeStep']=pumpPlace[c]
        #Pump Planned of option x
        AdaptationState[c]['Pump']=Pump_status[pumpPlace[c]]

    return AdaptationState

def dynamic_search(xcorrect,Tank_level,Pump_status,i,Limits,ch,tariff):
    
        
    if xcorrect>1:
            
            #print("need to add pump {} at inc {}".format(xcorrect,i))
            #xcorrect=xcorrect-1
        AdaptationState=AdaptationOptions(Tank_level,Pump_status,i,tariff)
            
        timestepUp=25
        for a in range(0,len(Tank_level)-i):
            if Tank_level[a+i]>Limits[1]-0.3:
                timestepUp=a+i
                break
                
        for c in range(0,len(AdaptationState)):
            if AdaptationState[c]['TimeStep']<timestepUp and AdaptationState[c]['Pump']!=1 and xcorrect>=1:
                Pump_status[AdaptationState[c]['TimeStep']]=1
                xcorrect=xcorrect-1
                    
                for l in range(AdaptationState[c]['TimeStep'],25):
                    Tank_level[l]=Tank_level[l]+ch
            
                    
    if xcorrect<-1:
    
            #print("need to add pump {} at inc {}".format(xcorrect,i))
            #xcorrect=xcorrect-1
        AdaptationState=AdaptationOptions(Tank_level,Pump_status,i,tariff)
            
        timestepDown=25
        for a in range(0,len(Tank_level)-i):
            if Tank_level[a+i]<Limits[0]+0.3:
                timestepDown=a+i
                break
                
        for c in range(1,len(AdaptationState)+1):
            if AdaptationState[-c]['TimeStep']<timestepDown and AdaptationState[-c]['Pump']!=0 and xcorrect<=-1:
                Pump_status[AdaptationState[-c]['TimeStep']]=0
                xcorrect=xcorrect+1
                    
                for l in range(AdaptationState[-c]['TimeStep'],25):
                    Tank_level[l]=Tank_level[l]-ch
                
    return xcorrect,Tank_level,Pump_status