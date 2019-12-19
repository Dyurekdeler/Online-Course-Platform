
GET_ALL_COURSES = ''' SELECT * FROM tbl_course order by course_id ; '''
GET_ALL_UNIS = ''' SELECT university_id, university_name FROM tbl_university order by university_id ; '''

def remove_by_id(rowid, tablename):
    return ''' DELETE FROM %s WHERE id = '%s' ; ''' %(tablename, rowid)

def user_login(username, password):
    return ''' SELECT * FROM tbl_person WHERE email = '%s' AND password = '%s' ; ''' %(username, password)

def get_person_by_email(email):
    return ''' SELECT * FROM tbl_person WHERE email = '%s' ; ''' %(email)

def get_person_student(username):
    return ''' SELECT * FROM tbl_person, tbl_student WHERE person_id = student_id AND email = '%s' ; ''' %(username)

def update_person(personid, firstname, lastname, email, address, phone, bday, pwd):
    return ''' UPDATE tbl_person SET first_name = '%s', last_name = '%s', email= '%s', password= '%s', date_of_birth= '%s', address= '%s', phone= '%s' WHERE person_id = '%s' ; ''' %( firstname, lastname, email,pwd,bday,address,phone,personid)

def update_student(studentid, universityid):
    return ''' UPDATE tbl_student SET university_id = '%s' WHERE student_id = '%s' ; ''' &(universityid, studentid)

def delete_person(personid):
    return ''' DELETE FROM tbl_person WHERE person_id = '%s' ; ''' %(personid)

def delete_student(personid):
    return ''' DELETE FROM tbl_student WHERE student_id = '%s' ; ''' %(personid)

def add_person_student(firstname, lastname, email,address,phone,bday,pwd, uni):
    return ''' WITH new_student as (
            INSERT INTO public.tbl_person(first_name, last_name, email, password, date_of_birth, address, phone, person_type)
            VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', 'STU') returning person_id )
            INSERT INTO tbl_student(student_id, university_id) SELECT person_id, %s FROM new_student ''' %( firstname, lastname, email, pwd, bday, address, phone, uni)

def add_person_lecturer(firstname, lastname, email,address,phone,bday,pwd, uni):
    return ''' WITH new_lecturer as (
            INSERT INTO public.tbl_person(first_name, last_name, email, password, date_of_birth, address, phone, person_type)
            VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', 'LEC') returning person_id )
            INSERT INTO tbl_lecturer(lecturer_id, university_id) SELECT person_id, %s FROM new_lecturer ''' %( firstname, lastname, email, pwd, bday, address, phone, uni)

def get_ordered_courses(studentid):
    return ''' SELECT * FROM tbl_course WHERE course_id IN (SELECT course_id FROM tbl_order WHERE student_id = '%s') ; ''' %(studentid)

def get_course(courseid):
    return ''' SELECT * FROM tbl_course WHERE course_id = '%s' ; ''' %(courseid)
