# instance varialbe

# __init__ is hte initializer often called constructor, which initilizes the intance variables
# self.radius, self.date and self.metal are the instance variables which are created by the __init__

import math
import time


class Ring(object):

    ''' here we will see the actual logic behind variaouse picese of python language 
    e.g. instances, variables, methods and @property
    '''
    date = time.strftime("%Y-%m-%d", time.gmtime())
    center = 0.0

    def __init__(self, date=date, metal='Copper', radius=5.0, price=5.0, quantity=5):
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


def main():
    print("Center of the Ring is at:", Ring.center)
    r = Ring(price=8)  # modify only price
    print("Radius:{0},cost:{1}".format(r.radius, r.cost()))


if __name__ == '__main__':
    main()


'''
There are three operation in python
every thing is object
1) get
r.radius is get
2) set
r.radius=5.0 is set
3) del
del r.radius
now r.radisu is deleted
''''
