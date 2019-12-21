
GET_ALL_COURSES = ''' SELECT * FROM tbl_course order by course_id ; '''
GET_ALL_UNIS = ''' SELECT university_id, university_name FROM tbl_university order by university_id ; '''
GET_ALL_PEOPLE = ''' SELECT * FROM tbl_person order by person_id ; '''

def remove_by_id(rowid, tablename):
    return ''' DELETE FROM %s WHERE id = '%s' ; ''' %(tablename, rowid)

def get_user_by_id(personid):
    return ''' SELECT person_id, first_name, last_name, email, password, date_of_birth, address, phone, person_type FROM tbl_person WHERE person_id = '%s' ; ''' %(personid)

def get_user(username, password):
    return ''' SELECT person_id, first_name, last_name, email, password, date_of_birth, address, phone, person_type FROM tbl_person WHERE email = '%s' AND password = '%s' ; ''' %(username, password)

def update_person(personid, firstname, lastname, email, address, phone, bday, pwd):
    return ''' UPDATE tbl_person SET first_name = '%s', last_name = '%s', email= '%s', password= '%s', date_of_birth= '%s', address= '%s', phone= '%s' WHERE person_id = '%s' ; ''' %( firstname, lastname, email,pwd,bday,address,phone,personid)

def update_student(studentid, universityid):
    return ''' UPDATE tbl_student SET university_id = '%s' WHERE student_id = '%s' ; ''' %(universityid, studentid)

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

def get_bought_course(courseid, personid):
    return ''' SELECT student_id FROM tbl_order WHERE course_id = '%s' AND student_id = '%s' ; ''' %(courseid, personid)

def buy_course(person_id, course_id, date):
    return ''' INSERT INTO public.tbl_order (student_id, course_id, order_date) VALUES ('%s', '%s', '%s') ; '''%(person_id, course_id, date )

def get_user_uni(person_id,person_type):
    if person_type == 'STU':
        return ''' SELECT university_name FROM tbl_person INNER JOIN tbl_student ON person_id = student_id INNER JOIN tbl_university ON tbl_student.university_id = tbl_university.university_id WHERE person_id = '%s' ; ''' %(person_id)
    else:
        return ''' SELECT university_name FROM tbl_person INNER JOIN tbl_lecturer ON person_id = lecturer_id INNER JOIN tbl_university ON tbl_lecturer.university_id = tbl_university.university_id WHERE person_id = '%s' ; ''' % (person_id)

def add_course(title, desc, price, video_link, category, lecturer_id, thumbnail):
    return ''' INSERT INTO tbl_course (title, description, price, video_link, category, lecturer_id, thumbnail)
	VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s' );''' %(title, desc, price, video_link, category, lecturer_id, thumbnail)

def get_user_type(personid):
    return ''' SELECT first_name, person_type FROM tbl_person WHERE person_id = '%s' ; ''' %(personid)

def get_course_of_lecturer(personid):
    return ''' SELECT * FROM tbl_course WHERE lecturer_id = '%s' ; ''' %(personid)

def get_course_comments(courseid):
    return ''' SELECT first_name, description, title, post_date FROM tbl_person INNER JOIN tbl_comment ON tbl_person.person_id = tbl_comment.person_id WHERE course_id = '%s' ; ''' %(courseid)

def add_comment_to_course(personid,desc, title,courseid, date):
    return ''' INSERT INTO tbl_comment(person_id, description, title, course_id, post_date) VALUES ('%s', '%s', '%s', '%s', '%s') ;''' %(personid,desc, title, courseid, date)