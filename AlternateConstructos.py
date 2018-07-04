class Person(object):
    race = ""
    def __init__(self, age_, name_):
        self.age = age_
        self.name = name_
    
    @classmethod    #do work before passing variable to one and only constructor
    def alternateConstructor(cls,age_, name_, race_):
        age = age_
        name = name_
        cls.race = race_
        return cls(age, name)


#class Student(Person):
#    def __init__(self):
#        Person.__init__(age, name)

#    #@classmethod
#    def secondConstructor(self, age, name, gender):
#        Person.__init__(age, name)
#        self.gender = gender

    
p1 = Person.alternateConstructor(26, "jason", "filipino")
p1.race = Person.race
print(str(p1.age) + ' ' + p1.name + ' ' + p1.race)