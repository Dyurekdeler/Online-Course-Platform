

GET_ALL_PERSON = ''' SELECT * FROM tbl_person '''

def remove_by_id(rowid, tablename):
    return ''' DELETE FROM %s WHERE id = '%s' ; ''' %(tablename, rowid)

def add_person( firstname, lastname, email,address,phone,bday,pwd):
    return ''' INSERT INTO tbl_person(first_name, last_name, email, password, date_of_birth, address, phone, person_type) VALUES ('%s', '%s', '%s','%s','%s','%s','%s','STU') RETURNING person_id; ''' %( firstname, lastname, email,pwd,bday,address,phone)

def get_person_by_email(email):
    return ''' SELECT * FROM tbl_person WHERE email = '%s' ; ''' %(email)

def add_student_with_uni( studentid, universityid):
    return ''' INSERT INTO tbl_student(student_id, university_id) VALUES ('%s', '%s') ; ''' %(studentid, universityid)

def get_person_student(username):
    return ''' SELECT * FROM tbl_person, tbl_student WHERE person_id = student_id AND email = '%s' ; ''' %(username)

def update_person(personid, firstname, lastname, email,address,phone,bday,pwd):
    return ''' UPDATE tbl_person SET first_name = '%s', last_name = '%s', email= '%s', password= '%s', date_of_birth= '%s', address= '%s', phone= '%s' WHERE person_id = '%s' ; ''' %( firstname, lastname, email,pwd,bday,address,phone,personid)

def update_student(studentid, universityid):
    return ''' UPDATE tbl_student SET university_id = '%s' WHERE student_id = '%s' ; ''' &(universityid, studentid)

def delete_person(personid):
    return ''' DELETE FROM tbl_person WHERE person_id = '%s' ; ''' %(personid)

def delete_student(personid):
    return ''' DELETE FROM tbl_student WHERE student_id = '%s' ; ''' %(personid)