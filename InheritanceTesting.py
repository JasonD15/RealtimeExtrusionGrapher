class MyClassOne(object):
    def __init__(self):
        self.my_attribute = "class1" 

    @property                           #getter
    def my_attribute(self):
        # Do something if you want
        return self._my_attribute

    @my_attribute.setter                #setter
    def my_attribute(self, value):
        # Do something if you want
        self._my_attribute = value

class MyClassTwo(object):
    def __init__(self):
        self.my_attribute = "class2" 

    @property                           #getter
    def my_attribute(self):
        # Do something if you want
        return self._my_attribute

    @my_attribute.setter                #setter
    def my_attribute(self, value):
        # Do something if you want
        self._my_attribute = value

list = {} #dictionary collection
#for x in (MyClassOne, MyClassTwo):
#    page_name = x.__name__
#print(page_name)

list['jason'] = MyClassOne()
list['dichoso'] = MyClassTwo()
print(list['dichoso'].my_attribute)




