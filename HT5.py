#-*- coding: cp1252 -*-
#HT5.py
#Ana Lucia Hernandez 17138
#Andres Urizar 17632

import simpy
import random


class Computer:
    def __init__(self, env):
        self.RAM = simpy.Container(env, init = 0, capacity =100)
        self.CPU = simpy.Resource(env, capacity =1)
        
def proceso(env, name, arriving_time, computadora):
    #
    yield env.timeout(arriving_time)
    #Momento en el que llega 
    horaLlegada = env.now
    print "Proceso %s solicita memoria en el momento %s" % (name, env.now)
    cantidadMemoria = random.randint(1, 30)
    print "Proceso %s necesita %d cantidad de memoria." % (name, cantidadMemoria)
    yield computadora.RAM.put(cantidadMemoria)
    print "Memoria otorgada al momento %d al proceso %s. Ha pasado al estado 'Ready' en %s." % (cantidadMemoria, name, env.now)




# ----------------------

env = simpy.Environment() #ambiente de simulacion
#memoria = simpy.Container(env,init =0,capacity = 100)
#CPU = simpy.Resource(env, capacity = 1)
random.seed(10)
compu = Computer(env)
for i in range(10):
    env.process(proceso(env,'Proceso %d'%i,random.expovariate(1.0/10), compu))
env.run(50)  #correr la simulacionn hasta el tiempo = 50

#print ("tiempo promedio por vehiculo es: ", totalDia/5.0)
