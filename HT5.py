#-*- coding: cp1252 -*-
#HT5.py
#Ana Lucia Hernandez 17138
#Andres Urizar 17632

import simpy
import random
#import numpy as np
#import statistics as stats


Tiempoprocesos = [] #Lista para poder almacenar los tiempos de los procesos
class Computer:
    def __init__(self, env):
        self.RAM = simpy.Container(env, init = 0, capacity =100)
        self.CPU = simpy.Resource(env, capacity =1)
        
def proceso(env, name, numero, arriving_time, computadora):
    #
    yield env.timeout(arriving_time)
    #Momento en el que llega 
    horaLlegada = env.now
    print "Proceso %s solicita memoria en el momento %s" % (name, env.now)
    cantidadMemoria = random.randint(1, 30)
    print "Proceso %s necesita %d cantidad de memoria." % (name, cantidadMemoria)
    yield computadora.RAM.put(cantidadMemoria)
    print "Memoria otorgada al momento %d al proceso %s. Ha pasado al estado 'Ready' en %s." % (cantidadMemoria, name, env.now)

    terminado = False
    while not terminado:
        with computadora.CPU.request() as req:
            #Momento para espere a que lo atienda el CPU
            instrucciones = random.randint(1,10)
            print "Espera al CPU el proceso %s con %d instrucciones en %s"% (name,instrucciones,env.now)
            yield req

            #Inicio de CPU o running
            print "Proceso %s encuentra atendido por el CPU en %s"% (name,env.now)
            for i in range(3): #Realiza solamente 3 instrucciones
                if instrucciones > 0:   #Si llegara a tener operaciones, llega a ejecutar una
                    instrucciones -= 1
                    waiting = random.randint(1,2)
                yield env.timeout(1)
            #Finaliza de estar en la CPU
            #Ingresa a cola de Waiting
            if waiting == 1:
                print "Proceso %s en cola de Waiting para hacer operaciones I/O en %s"% (name,env.now)
                yield env.timeout(1)
            #Deja el CPU
            if instrucciones <= 0:
                terminado = True

    print "Proceso %s ha dejado el CPU en %s"% (name,env.now)
    fin = env.now
    tiempototal = horaLlegada - fin
    Tiempoprocesos.insert(numero,tiempototal) #Para almacenar los tiempos de los procesos   
            
                    
            




# ----------------------

env = simpy.Environment() #ambiente de simulacion
#memoria = simpy.Container(env,init =0,capacity = 100)
#CPU = simpy.Resource(env, capacity = 1)
random.seed(10)
compu = Computer(env)
for i in range(10):
    env.process(proceso(env,'Proceso %d'%i,i,random.expovariate(1.0/10), compu))
env.run(50)  #correr la simulacionn hasta el tiempo = 50
tiempopromedio = sum(Tiempoprocesos)*1.0/len(Tiempoprocesos)
#desvestandar = np.std(Tiempoprocesos)
#desvestandar = stats.pstdev(Tiempoprocesos)

#print ("tiempo promedio por vehiculo es: ", totalDia/5.0)
