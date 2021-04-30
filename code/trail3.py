# instance varialbe

# __init__ is hte initializer often called constructor, which initilizes the intance variables
# self.radius, self.date and self.metal are the instance variables which are created by the __init__

from abc import abstractmethod
from typing import Match


import math


class Ring(object):

    ''' here we will see the actual logic behind variaouse picese of python language 
    e.g. instances, variables, methods and @property
    '''

    def __init__(self, date, metal, radius, price, quantity):
        ''' init is not hte contructor, but the initializer whihc initialize the intance variable
        self is the instance
        __init__ takes the instance 'self' and populates it with raiduse, metal, date etc and store in a dictionary
        self.radiuse, self.metal, etc are the instanc evariable which must be unique.
        '''
        self.date = date
        self.metal = metal
        self.radius = radius
        self.price = price
        self.quantity = quantity

    def cost(self):
        return self.price*self.quantity

    def area(self):
        return math.pi*self.radius**2
