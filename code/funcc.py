# callable function inluding user-defined funcitons


def add2Num(a, b):
    return a+b


def diff2Num = lambda x, y: x-y


#  to call the two funciton
add2Num(3, 5)
diff2Num(3, 4)


class Spam():
    num = 10  # class variable

    def __init__(self, num=3):  # initia the value by a default 3
        self.num = num  # assigned the value of the class to the variable num

    def imethod(self):  # prints the instance variable
        print("imethod ", self.num)

    @classmethod
    def cmethod(cls):  # print class variable
        print("cmethod ", cls.num)

    @staticmethod
    def smethod(cls):  # print variable defined in the file
        print("smethod ", num)


s = Spam()
s.imethod()
type(s)
