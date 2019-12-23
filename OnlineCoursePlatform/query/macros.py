
GET_ALL_COURSES = ''' SELECT * FROM tbl_course order by course_id ; '''
GET_ALL_UNIS = ''' SELECT * FROM tbl_university order by university_id ; '''
GET_ALL_PEOPLE = ''' SELECT * FROM tbl_person order by person_id ; '''
GET_ALL_STUDENTS = ''' SELECT * FROM tbl_student order by student_id ; '''
GET_ALL_LECTURERS = ''' SELECT * FROM tbl_lecturer order by lecturer_id ; '''
GET_ALL_COMMENTS = ''' SELECT * FROM tbl_comment order by comment_id ; '''
GET_ALL_REPORTS = ''' SELECT * FROM tbl_report order by report_id ; '''
GET_ALL_ORDERS = ''' SELECT * FROM tbl_order order by order_id ; '''

def remove_by_id(rowid, tablename):
    return ''' DELETE FROM %s WHERE id = '%s' ; ''' %(tablename, rowid)

def get_user_by_id(personid):
    return ''' SELECT person_id, first_name, last_name, email, password, date_of_birth, address, phone, person_type FROM tbl_person WHERE person_id = '%s' ; ''' %(personid)

def get_user(username, password):
    return ''' SELECT person_id, first_name, last_name, email, password, date_of_birth, address, phone, person_type FROM tbl_person WHERE email = '%s' AND password = '%s' ; ''' %(username, password)

def update_person(personid, firstname, lastname, email, address, phone, bday, uni):
    return ''' UPDATE tbl_person SET first_name = '%s', last_name = '%s', email= '%s', university_id= '%s', date_of_birth= '%s', address= '%s', phone= '%s' WHERE person_id = '%s' ; ''' %( firstname, lastname, email,uni,bday,address,phone,personid)

def update_student(studentid, universityid):
    return ''' UPDATE tbl_student SET university_id = '%s' WHERE student_id = '%s' ; ''' %(universityid, studentid)

def delete_person(personid):
    return ''' DELETE FROM tbl_person WHERE person_id = '%s' ; ''' %(personid)

def delete_student(personid):
    return ''' DELETE FROM tbl_student WHERE student_id = '%s' ; ''' %(personid)

def add_person(firstname, lastname, email,pwd,bday,address,phone, uni, type):
    return ''' CALL Add_Person('%s', '%s', '%s', '%s','%s', '%s', '%s','%s' ,'%s'); ''' %(firstname, lastname, email,pwd,bday,address,phone, uni, type)

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
    return ''' INSERT INTO tbl_comment (person_id, description, title, course_id, post_date) VALUES ('%s', '%s', '%s', '%s', '%s') ;''' %(personid,desc, title, courseid, date)

def add_report_to_course(person_id, description, course_id, report_date):
    return ''' INSERT INTO tbl_report (student_id, description, course_id, report_date) VALUES ('%s', '%s', '%s', '%s') ; ''' %(person_id,description, course_id, report_date)

def add_favorite(person_id,course_id):
    return ''' INSERT INTO tbl_favorites (student_id, course_id) VALUES ('%s', '%s') ; ''' %(person_id,course_id)

def update_password(personid, pw):
    return  ''' UPDATE tbl_person SET password = '%s' WHERE person_id = '%s' ; ''' %(pw, personid)

def get_users_favorites(person_id):
    return ''' SELECT tbl_course.course_id, title, description, price, video_link, category, lecturer_id, thumbnail FROM tbl_course INNER JOIN tbl_favorites ON tbl_course.course_id = tbl_favorites.course_id WHERE student_id = '%s' ; ''' %(person_id)