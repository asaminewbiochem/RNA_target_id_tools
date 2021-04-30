'''
method       : it uses the instance variable self.x which is set by __init__ function
classmethod  : it uses class variable 
staticmethod : it uses the value of x which is defined in main program i.e outside class
'''


x = 20


class Add(object):
    x = 9  # class variable

    def __init__(self, x):
        self.x = x  # instance variable

    def addMethod(self, y):
        print("method:", self.x+y)

    @classmethod
    # as convention, cls must be used for classmethod, instead of self
    def addClass(self, y):
        print("classmethod:", self.x+y)

    @staticmethod
    def addStatic(y):
        print("staticmethod:", x+y)


def main():
    # method
    m = Add(x=4)  # or m=Add(4) same thing

    m.addMethod(10)

    # classmethod
    c = Add(4)
    # for class method
    c.addClass(10)
    s = Add(4)
    s.addStatic(10)


if __name__ == '__main__':
    main()
