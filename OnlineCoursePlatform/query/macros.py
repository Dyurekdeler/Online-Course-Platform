
GET_ALL_COURSES = ''' SELECT * FROM tbl_course order by course_id ; '''
GET_ALL_UNIS = ''' SELECT * FROM tbl_university order by university_id ; '''
GET_ALL_COMMENTS = ''' SELECT * FROM tbl_comment order by comment_id ; '''
GET_ALL_REPORTS = ''' SELECT * FROM tbl_report order by report_id ; '''
GET_ALL_ORDERS = ''' SELECT * FROM tbl_order order by order_id ; '''
GET_ALL_USERS = ''' SELECT * FROM users ; '''


def add_person(firstname, lastname, email,pwd,bday,address,phone, uni, type):
    return ''' CALL add_person('%s', '%s', '%s', '%s','%s', '%s', '%s','%s' ,'%s'); ''' %(firstname, lastname, email,pwd,bday,address,phone, uni, type)

def update_person(personid, firstname, lastname, email, pw, bday, address, phone,   persontype, uni):
    print(persontype, uni)
    if persontype == 'STU':
        return ''' BEGIN; UPDATE tbl_person SET first_name = '%s', last_name = '%s', email= '%s', password = '%s', date_of_birth= '%s', address= '%s', phone= '%s' WHERE person_id = '%s' ; 
         UPDATE tbl_student SET university_id = '%s' WHERE student_id = '%s'; COMMIT; ''' %( firstname, lastname, email,pw,bday,address,phone,personid, uni, personid)
    else:
        return ''' BEGIN; UPDATE tbl_person SET first_name = '%s', last_name = '%s', email= '%s', password = '%s', date_of_birth= '%s', address= '%s', phone= '%s' WHERE person_id = '%s' ; 
                 UPDATE tbl_lecturer SET university_id = '%s' WHERE lecturer_id = '%s'; COMMIT; ''' % (
        firstname, lastname, email, pw, bday, address, phone, personid, uni, personid)

def delete_person(personid, persontype):
    if persontype == 'LEC':
        return ''' BEGIN; 
        DELETE FROM tbl_lecturer WHERE lecturer_id = '%s';
        DELETE FROM tbl_person WHERE person_id = '%s' ; 
        COMMIT; ''' % (personid,personid)
    else:
        return ''' BEGIN; 
        DELETE FROM tbl_student WHERE student_id = '%s'; 
        DELETE FROM tbl_person WHERE person_id = '%s' ; 
        COMMIT; ''' % (personid,personid)

def get_comment_counts(courseid):
    return ''' SELECT tbl_course.course_id,  count(comment_id) FROM tbl_course 
            LEFT OUTER JOIN tbl_comment 
            ON tbl_course.course_id = tbl_comment.course_id 
            WHERE tbl_course.course_id = '%s'
            GROUP BY tbl_course.course_id  ''' %(courseid)

def get_user(personid):
    return ''' SELECT * FROM users WHERE person_id = %s ; ''' %(personid)

def authenticate_user(username, pw):
    return ''' SELECT person_id , count(person_id) FROM users
            WHERE email = '%s' AND password = '%s'
            GROUP BY person_id ''' %(username, pw)

def update_password(personid, pw):
    return  ''' UPDATE tbl_person SET password = '%s' WHERE person_id = '%s' ; ''' %(pw, personid)

def add_uni(name, location):
    return  ''' INSERT INTO public.tbl_university(
	university_name, university_location)
	VALUES ('%s','%s'); ''' %(name,location)

def update_uni(uni_id,name, location):
    return  ''' UPDATE public.tbl_university
	SET university_name='%s', university_location='%s'
	WHERE university_id = '%s' ''' %(uni_id,name,location)

def add_course(title, desc, price, video_link, category, lecturer_id, thumbnail):
    return ''' INSERT INTO tbl_course (title, description, price, video_link, category, lecturer_id, thumbnail)
	VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s' );''' %(title, desc, price, video_link, category, lecturer_id, thumbnail)

def update_course(course_id, title, desc, price, video_link, category, lecturer_id, thumbnail):
    return ''' UPDATE public.tbl_course
	SET title=%s, description=%s, price=%s, video_link=%s, category=%s,  lecturer_id=%s, thumbnail=%s
	WHERE course_id = %s;''' %(title, desc, price, video_link, category, lecturer_id, thumbnail, course_id)

def add_comment_to_course(personid,desc, title,courseid, date):
    return ''' INSERT INTO tbl_comment (person_id, description, title, course_id, post_date) VALUES ('%s', '%s', '%s', '%s', '%s') ;''' %(personid,desc, title, courseid, date)

def update_comment(comment_id, personid,desc, title,courseid, date):
    return ''' UPDATE public.tbl_comment
	SET person_id=%s, description=%s, title=%s, course_id=%s, post_date=%s
	WHERE comment_id = %s ; ''' %(personid,desc, title,courseid, date, comment_id)

def add_report_to_course(person_id, description, course_id, report_date):
    return ''' INSERT INTO tbl_report (student_id, description, course_id, report_date) VALUES ('%s', '%s', '%s', '%s') ; ''' %(person_id,description, course_id, report_date)

def update_report(report_id, person_id, description, course_id, report_date ):
    return  ''' UPDATE public.tbl_report
	SET  student_id=%s, description=%s, course_id=%s, report_date=%s
	WHERE report_id = %s; ''' %(person_id, description, course_id, report_date , report_id)

def buy_course(person_id, course_id, date):  ##### this stands for add order
    return ''' INSERT INTO public.tbl_order (student_id, course_id, order_date) VALUES ('%s', '%s', '%s') ; '''%(person_id, course_id, date )

def update_order(order_id, person_id, course_id, date):
    return  ''' UPDATE public.tbl_order
	SET  student_id=%s, course_id=%s, order_date=%s
	WHERE order_id = %s ;''' %(person_id, course_id, date, order_id)


####################################################################################################################################

def get_ordered_courses(studentid):
    return ''' SELECT * FROM tbl_course WHERE course_id IN (SELECT course_id FROM tbl_order WHERE student_id = '%s') ; ''' %(studentid)

def get_course(courseid):
    return ''' SELECT * FROM tbl_course WHERE course_id = '%s' ; ''' %(courseid)

def get_bought_course(courseid, personid):
    return ''' SELECT student_id FROM tbl_order WHERE course_id = '%s' AND student_id = '%s' ; ''' %(courseid, personid)

def get_course_of_lecturer(personid):
    return ''' SELECT * FROM tbl_course WHERE lecturer_id = '%s' ; ''' %(personid)

def get_course_comments(courseid):
    return ''' SELECT first_name, description, title, post_date FROM tbl_person INNER JOIN tbl_comment ON tbl_person.person_id = tbl_comment.person_id WHERE course_id = '%s' ; ''' %(courseid)

def add_favorite(person_id,course_id):
    return ''' INSERT INTO tbl_favorites (student_id, course_id) VALUES ('%s', '%s') ; ''' %(person_id,course_id)

def get_users_favorites(person_id):
    return ''' SELECT tbl_course.course_id, title, description, price, video_link, category, lecturer_id, thumbnail FROM tbl_course INNER JOIN tbl_favorites ON tbl_course.course_id = tbl_favorites.course_id WHERE student_id = '%s' ; ''' %(person_id)