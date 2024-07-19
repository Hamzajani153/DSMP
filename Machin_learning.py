class Person:
    # Person = "Human"# class variable
    addperson = []
    def __init__(self, name,age):
        self.n = name # instance variable
        self.a = age 

    def add_person(self , add):
        self.addperson.append(add)


P1 = Person("John", 36) #class object
P2 = Person("Smith", 25)
P1.add_person("John")

