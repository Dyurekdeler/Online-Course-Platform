class Person:
    def __init__(self, firstname, lastname, email, address, password, bday, phone ):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.address = address
        self.password = password
        self. bday = bday
        self.phone = phone


class Student(Person):
    def __init__(self, firstname, lastname, email,address,password,bday, phone, familyId, universityId):
        super().__init__(firstname, lastname, email, address, password, bday, phone)
        self.familyId = familyId
        self.universityId = universityId