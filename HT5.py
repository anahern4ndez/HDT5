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
        
def proceso(env, name, computadora):
    print "Proceso %s solicita memoria en el momento %s" % (name, env.now)
    cantidadMemoria = random.randint(1, 30)
    print "Proceso %s necesita %d cantidad de memoria." % (name, cantidadMemoria)

    print "Proceso %s esta listo en el momento %s" % (name, env.now)
    yield computadora.RAM.get(cantidadMemoria)
    ###
    memory = computadora.RAM.capacity - computadora.RAM.level
    yield computadora.RAM.put(memory)










# ----------------------

env = simpy.Environment() #ambiente de simulacion
#memoria = simpy.Container(env,init =0,capacity = 100)
#CPU = simpy.Resource(env, capacity = 1)
random.seed(10)
compu = Computer(env)
for i in range(10):
    env.process(proceso(env,'carro %d'%i,compu))
env.run(50)  #correr la simulacionn hasta el tiempo = 50

#print ("tiempo promedio por vehiculo es: ", totalDia/5.0)
