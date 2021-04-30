# class and many things
class ClassName:
    'Optional class docummentation string'  # can be accessed by __doc__
    class_suite


# example
class Employee:
    'common base class for all employees'
    empCount = 0  # class variable
    # class varialbe shared amon all instance of a class

    # this is the first methods called class constructor or initialization method
    def __init__(self, name, salary):
        # and creates a new instance of the class
        self.name = name
        self.salary = salary
        Employee.empCount += 1  # accessing shared class varaible
# methods in class are similar to function except they have self
# argument and will not be included when called the methods

    def displayCount(self):
        # accessing shared class variable
        print("Total Employee %d" % Employee.empCount)

    def displayEmployee(self):
        print("Name: ", self.name, ",Salary:", self.salary)


# to create instance of a class you call the calss using the class
#  name and pass what ever argument its __init__ method accepts

# example
# create first object of Employee class
emp1 = Employee("Manni", 50000)  # name and salary

# create second object
emp2 = Employee("Ase", 50000)

# now access the object attribute
# let's try for first object
emp1.displayCount()
emp1.displayEmployee()


# let's modify salary which is an instance or attribute
emp1.salary = 5670  # add salary attribute

emp1.name = 'Blen'
del emp1.salary  # delete salary attribute

# __dict__: dictionary containing the class namespace
#  __doc__: class documatnation
# __name__ :class name
# __module__: module name


# example
print("Employee.__doc__: ", Employee.__doc__)

# when excuted the above
# Employee.__doc__: common base class for all employees


# inheritance
# format class SubClassName(ParentClass1, ParentClass2,....):


# example
class Parent:
    parentAttr = 10000

    def __init__(self):
        print('calling parent constructor/initializer')

    def parentMethod(self):
        print("Calling paraent method")

    def setAttr(self, attr):
        Parent.parentAttr = attr

    def getAttr(self):
        print('parent aatribute:', Parent.parentAttr)


class Child(Parent):  # define child class
    def __init__(self):
        print('Calling child initialized')

    def childMethod(self):
        print('calling child method')


# let's create child object
c = Child()  # instance of child
c.childMethod()  # child calls its method
c.parentMethod()  # calls parant's method
c.setAttr()  # again calls paraent method
c.getAttr()  # again calls parent method


# issubclass() and isinstance() function can be used to check relationship of two classes

