# -*- coding: utf-8 -*-
"""
Created on Fri May 24 21:11:21 2019

@author: Marcelo
"""

P_1A=[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #CBTariff
P_2A=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] #CBTariff
P_3A=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] #STTariff
P_4B=[0,1,1,1,0,0,1,0,1,0,1,0,1,1,0,1,0,1,0,0,1,0,0,1] #LZHZTariff
P_5C=[0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,1] #HHTariff
P_6D=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1] #LZGTariff
P_7F=[0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0] #STariff

def tarifario_CB(ti):
        # definição do tarifário usando o tempo inicial do incremento
    tarifHora = [None]*3; tarifCusto = [None]*3;
    set(tarifHora)
    tarifHora[0]= 0; tarifCusto[0]= 2.40925 
    tarifHora[1]=8; tarifCusto[1]= 6.7945
    tarifHora[2]=25; 
    tarifF = 0.
    for i in range(0, len(tarifHora)-1):
        if (ti >= tarifHora[i]) & (ti < tarifHora[i+1]):
            tarifF = tarifCusto[i]
            break
    if tarifF == 0.: print("Erro no tarifário",ti,i); quit()
    return tarifF
    
def tarifario_HH(ti):
        # definição do tarifário usando o tempo inicial do incremento
    tarifHora = [None]*3; tarifCusto = [None]*3;
    set(tarifHora)
    tarifHora[0]= 0; tarifCusto[0]= 2.46
    tarifHora[1]=8; tarifCusto[1]= 9.866
    tarifHora[2]=25; 
    tarifF = 0.
    for i in range(0, len(tarifHora)-1):
        if (ti >= tarifHora[i]) & (ti < tarifHora[i+1]):
            tarifF = tarifCusto[i]
            break
    if tarifF == 0.: print("Erro no tarifário",ti,i); quit()
    return tarifF

def tarifario_LZG(ti):
        # definição do tarifário usando o tempo inicial do incremento
    tarifHora = [None]*3; tarifCusto = [None]*3;
    set(tarifHora)
    tarifHora[0]= 0; tarifCusto[0]= 2.46
    tarifHora[1]=8; tarifCusto[1]= 11.195
    tarifHora[2]=25; 
    tarifF = 0.
    for i in range(0, len(tarifHora)-1):
        if (ti >= tarifHora[i]) & (ti < tarifHora[i+1]):
            tarifF = tarifCusto[i]
            break
    if tarifF == 0.: print("Erro no tarifário",ti,i); quit()
    return tarifF

def tarifario_LZHZ(ti):
        # definição do tarifário usando o tempo inicial do incremento
    tarifHora = [None]*3; tarifCusto = [None]*3;
    set(tarifHora)
    tarifHora[0]= 0; tarifCusto[0]= 2.456666667
    tarifHora[1]=8; tarifCusto[1]= 12.34 
    tarifHora[2]=25; 
    tarifF = 0.
    for i in range(0, len(tarifHora)-1):
        if (ti >= tarifHora[i]) & (ti < tarifHora[i+1]):
            tarifF = tarifCusto[i]
            break
    if tarifF == 0.: print("Erro no tarifário",ti,i); quit()
    return tarifF

def tarifario_S(ti):
        # definição do tarifário usando o tempo inicial do incremento
    tarifHora = [None]*3; tarifCusto = [None]*3;
    set(tarifHora)
    tarifHora[0]= 0; tarifCusto[0]= 2.44
    tarifHora[1]=8; tarifCusto[1]= 11.94 
    tarifHora[2]=25; 
    tarifF = 0.
    for i in range(0, len(tarifHora)-1):
        if (ti >= tarifHora[i]) & (ti < tarifHora[i+1]):
            tarifF = tarifCusto[i]
            break
    if tarifF == 0.: print("Erro no tarifário",ti,i); quit()
    return tarifF

def tarifario_ST(ti):
        # definição do tarifário usando o tempo inicial do incremento
    tarifHora = [None]*3; tarifCusto = [None]*3;
    set(tarifHora)
    tarifHora[0]= 0; tarifCusto[0]= 2.41
    tarifHora[1]=8; tarifCusto[1]= 7.535
    tarifHora[2]=25; 
    tarifF = 0.
    for i in range(0, len(tarifHora)-1):
        if (ti >= tarifHora[i]) & (ti < tarifHora[i+1]):
            tarifF = tarifCusto[i]
            break
    if tarifF == 0.: print("Erro no tarifário",ti,i); quit()
    return tarifF

'''
Assumptions
Pumps A probably doesn't require any control
Pump 4B definetely requires control
Pump 6D require control
Pump 5C requires control
Pump 7F requires control
'''

'''
linearization ideas
set every single pump to 0 at every time step, increse one time step for 1 and measure the amount of water it increases

'''

'''
Restrições
    min      max      inital
C    0        2        1.84
A    0       3.37      3.12
D    0       2.11      1.94
B    0       3.65      3.37
E    0       2.69      2.47
F    0       2.19      1.96
'''


#Patterns 

Predicted=[1.10,1.61,1.53,1.4,1.15,1.06,1.04,1,0.92,0.95,1.16,1.34,1.45,1.32,1.33,1.11,1.07,0.71,0.48,0.46,0.4,0.39,0.41,0.52]
Real_Over=[1.30,1.81,1.73,1.6,1.35,1.26,1.24,1.2,1.12,1.15,1.26,1.54,1.55,1.52,1.43,1.21,1.27,0.91,0.68,0.66,0.6,0.59,0.61,0.72]
Real_Fire=[1.20,1.51,1.63,1.3,1.25,0.96,1.14,1.9,2.78,2.88,2.86,3.84,2.95,2.82,2.93,1.21,1.07,0.68,0.45,0.49,0.27,0.49,0.51,0.42]
Real_Under=[0.90,1.41,1.33,1.2,0.95,0.86,0.84,0.8,0.72,0.75,0.96,1.14,1.25,1.12,1.13,0.91,0.97,0.51,0.28,0.26,0.2,0.19,0.21,0.32]
Real_Noise=[1.20,1.51,1.63,1.3,1.25,0.96,1.14,0.9,1.08,0.88,1.16,1.04,1.25,1.42,1.23,1.21,1.07,0.68,0.45,0.49,0.27,0.49,0.51,0.42]

import matplotlib.pyplot as plt
import numpy as np
'''
plt.figure(figsize=(15,10))
plt.plot(np.linspace(0,23,24),Predicted,label="Predicted")
#plt.plot(np.linspace(0,23,24),Real_Over,'*k',label="Real_Over")
plt.plot(np.linspace(0,23,24),Real_Fire)

plt.plot(np.linspace(0,23,24),Real_Fire,'*k',label="Real_Fire")
#plt.plot(np.linspace(0,23,24),Real_Under,'*k',label="Real_Under")
#plt.plot(np.linspace(0,23,24),Real_Noise,'*k',label="Real_Noise")
plt.legend()
plt.title('Consumption Patterns')
plt.xlabel('Time (h)')
plt.ylabel('Pattern Multiplier')
plt.grid()
plt.show()
'''