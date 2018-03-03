#-*- coding: cp1252 -*-
#HT5.py
#Ana Lucia Hernandez 17138
#Andres Urizar 17632

import simpy
import random
import math
#import numpy as np
#import statistics as stats


TiempoProcesos = [] #Lista para poder almacenar los tiempos de los procesos
class Computer:
    def __init__(self, env):
        self.RAM = simpy.Container(env, init = 0, capacity =50)
        self.CPU = simpy.Resource(env, capacity =1)
        
def proceso(env, name, numero, arriving_time, computadora):
    
    yield env.timeout(arriving_time)
    #Momento en el que llega 
    horaLlegada = env.now
    print "Proceso %s solicita memoria en tiempo =  %s" % (name, env.now)
    cantidadMemoria = random.randint(1, 30)
    print "Proceso %s necesita %d cantidad de memoria." % (name, cantidadMemoria)
    yield computadora.RAM.put(cantidadMemoria)
    print "Memoria otorgada al proceso %s. Ha pasado al estado 'Ready' en tiempo = %s." % (name, env.now)

    terminado = False
    while not terminado:
        with computadora.CPU.request() as req:
            waiting =0
            #Momento para espere a que lo atienda el CPU
            print "Espera al CPU el proceso %s con %d instrucciones en tiempo = %s"% (name,cantidadMemoria,env.now)
            yield req
            if cantidadMemoria > 0: #Si el proceso todavia tiene instrucciones por realizar     
                for i in range(3): #Realiza solamente 3 instrucciones
                    cantidadMemoria -=1
                    computadora.RAM.get(1)

                waiting = random.randint(0,2)
                yield env.timeout(1)
            #Finaliza de estar en la CPU
            #Ingresa a cola de Waiting, si random ==0, pasa a cola ready
            if (waiting ==0):
                print "Proceso %s en cola de Ready en %s"% (name,env.now)
            elif waiting == 1:
                print "Proceso %s en cola de Waiting para hacer operaciones I/O en tiempo =  %s"% (name,env.now)
                yield env.timeout(2)
            #Deja el CPU
            if cantidadMemoria <3 :
                if cantidadMemoria > 0:
                    computadora.RAM.get(cantidadMemoria)
                terminado = True
    
    print "Proceso %s ha dejado el CPU en tiempo = %s"% (name,env.now)
    print "MEMORIA RESTANTE: %d" % (computadora.RAM.capacity - computadora.RAM.level) +'\n'
    fin = env.now
    tiempototal =  fin - horaLlegada
    TiempoProcesos.insert(numero,tiempototal) #Para almacenar los tiempos de los procesos   
        

# ----------------------

env = simpy.Environment() #ambiente de simulacion
random.seed(10)
compu = Computer(env)
cantidadProcesos = 5
for i in range(cantidadProcesos):
    env.process(proceso(env, '%d'%i, i+1, random.expovariate(1.0/10), compu))
    cantidadProcesos -=1
env.run(until = None)  #correr la simulacion hasta que ya no hayan procesos
tiempoPromedio = sum(TiempoProcesos)*1.0/len(TiempoProcesos)
print "\n \n \t ---> TIEMPO PROMEDIO PARA CADA PROCESO: "+ str(tiempoPromedio)
