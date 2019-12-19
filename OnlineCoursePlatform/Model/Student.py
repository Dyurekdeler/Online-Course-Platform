from Model.Person import Person

class Student(Person):
    def __init__(self, firstname, lastname, email,address,password,bday, phone, universityId):
        super().__init__(firstname, lastname, email, address, password, bday, phone)
        self.universityId = universityId