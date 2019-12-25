CREATE TABLE tbl_person (
	person_id SERIAL PRIMARY KEY,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	email TEXT NOT NULL UNIQUE,
	password TEXT NOT NULL,
	date_of_birth DATE NOT NULL,
	address TEXT NOT NULL,
	phone VARCHAR(11),
	person_type VARCHAR(3) NOT NULL,
	CHECK (person_type in ('SUP','LEC','STU')),
	CHECK (char_length(password)>=8)
);

CREATE TABLE tbl_university (
	university_id SERIAL PRIMARY KEY,
	university_name TEXT NOT NULL UNIQUE,
	university_location TEXT NOT NULL
);

CREATE TABLE tbl_student(
	student_id INT NOT NULL PRIMARY KEY ,
	university_id INT,
	CONSTRAINT "fk_universityId" FOREIGN KEY("university_id") REFERENCES public."tbl_university"(university_id) ON DELETE CASCADE,
	CONSTRAINT "fk_studentId" FOREIGN KEY("student_id") REFERENCES public."tbl_person"(person_id) ON DELETE CASCADE
);

CREATE TABLE tbl_lecturer(
	lecturer_id INT NOT NULL PRIMARY KEY ,
	university_id INT NOT NULL ,
	CONSTRAINT "fk_lecturerId" FOREIGN KEY("lecturer_id") REFERENCES public."tbl_person"(person_id) ON DELETE CASCADE,
	CONSTRAINT "fk_universityId" FOREIGN KEY("university_id") REFERENCES public."tbl_university"(university_id) ON DELETE CASCADE
);

CREATE TABLE tbl_supervisor(
	supervisor_id INT NOT NULL PRIMARY KEY,
	authority_level INT DEFAULT 0 NOT NULL,
	CONSTRAINT "fk_supervisorId" FOREIGN KEY("supervisor_id") REFERENCES public."tbl_person"(person_id) ON DELETE CASCADE
);

CREATE TABLE tbl_course (
	course_id SERIAL PRIMARY KEY,
	title TEXT NOT NULL,
	description TEXT NOT NULL,
	price FLOAT NOT NULL,
	video_link TEXT NOT NULL,
	category TEXT NOT NULL,
	lecturer_id INT NOT NULL,
	thumbnail TEXT NOT NULL,
	CHECK((thumbnail LIKE 'https://%') or (thumbnail LIKE 'http://%')),
	CHECK (category in ('software','language','economy','fine arts','sport')),
	CONSTRAINT "fk_lecturerId" FOREIGN KEY("lecturer_id") REFERENCES public."tbl_lecturer"(lecturer_id) ON DELETE CASCADE
);

CREATE TABLE tbl_comment (
	comment_id SERIAL PRIMARY KEY,
	person_id INT NOT NULL,
	description TEXT NOT NULL,
	title TEXT NOT NULL,
	course_id INT NOT NULL,
	post_date TIMESTAMP WITH TIME ZONE NOT NULL,
	CONSTRAINT "fk_courseId" FOREIGN KEY("course_id") REFERENCES public."tbl_course"(course_id) ON DELETE CASCADE,
	CONSTRAINT "fk_personId" FOREIGN KEY("person_id") REFERENCES public."tbl_person"(person_id) ON DELETE CASCADE
);

CREATE TABLE tbl_report (
	report_id SERIAL PRIMARY KEY,
	student_id INT NOT NULL,
	description TEXT NOT NULL,
	course_id INT NOT NULL,
	report_date TIMESTAMP WITH TIME ZONE NOT NULL,
	CONSTRAINT "fk_courseId" FOREIGN KEY("course_id") REFERENCES public."tbl_course"(course_id) ON DELETE CASCADE,
	CONSTRAINT "fk_studentId" FOREIGN KEY("student_id") REFERENCES public."tbl_student"(student_id) ON DELETE CASCADE
);


CREATE TABLE tbl_order (
	order_id SERIAL PRIMARY KEY,
	student_id INT NOT NULL,
	course_id INT NOT NULL,
	order_date TIMESTAMP WITH TIME ZONE NOT NULL,
	CONSTRAINT "fk_studentId" FOREIGN KEY("student_id") REFERENCES public."tbl_student"(student_id) ON DELETE CASCADE,
	CONSTRAINT "fk_courseId" FOREIGN KEY("course_id") REFERENCES public."tbl_course"(course_id) ON DELETE CASCADE
);

CREATE TABLE tbl_favorites (
	student_id INT NOT NULL REFERENCES tbl_student(student_id) ON DELETE CASCADE,
	course_id INT NOT NULL REFERENCES tbl_course(course_id) ON DELETE CASCADE ,
	primary key(student_id,course_id)
);




CREATE OR REPLACE PROCEDURE add_person(
	firstname text,
	lastname text,
	email text,
	password text,
	bday timestamp without time zone,
	address text,
	phone varchar(11),
	uniid integer,
	person_type varchar(3))
LANGUAGE 'plpgsql'

AS $$
BEGIN

IF person_type = 'STU' THEN
   WITH new_student as (
            INSERT INTO public.tbl_person(first_name, last_name, email, password, date_of_birth, address, phone, person_type)
            VALUES ( firstName, lastName, email, password, bDay, address, phone, 'STU') returning person_id )
            INSERT INTO tbl_student(student_id, university_id) SELECT person_id, uniId FROM new_student;

ELSIF person_type = 'LEC' THEN
	WITH new_lecturer as (
            INSERT INTO public.tbl_person(first_name, last_name, email, password, date_of_birth, address, phone, person_type)
            VALUES ( firstName, lastName, email, password, bDay, address, phone, 'LEC') returning person_id )
            INSERT INTO tbl_lecturer(lecturer_id, university_id) SELECT person_id, uniId FROM new_lecturer; 

ELSE
	WITH new_supervisor as (
            INSERT INTO public.tbl_supervisor(first_name, last_name, email, password, date_of_birth, address, phone, person_type)
            VALUES ( firstName, lastName, email, password, bDay, address, phone, 'SUP') returning person_id )
            INSERT INTO tbl_supervisor(supervisor_id) SELECT person_id FROM new_supervisor; 
END IF;

 
    COMMIT;
END;
$$;


CREATE OR REPLACE VIEW users AS
SELECT person_id, first_name, last_name, email, password, date_of_birth, address, phone, person_type, U.university_id, university_name
FROM tbl_person P
INNER JOIN tbl_student S
ON S.student_id = P.person_id
INNER JOIN tbl_university U
ON S.university_id = U.university_id
UNION
SELECT person_id, first_name, last_name, email, password, date_of_birth, address, phone, person_type, U.university_id, university_name
FROM tbl_person P
INNER JOIN tbl_lecturer L
ON L.lecturer_id = P.person_id
INNER JOIN tbl_university U
ON L.university_id = U.university_id



INSERT INTO public.tbl_university(university_name, university_location)
	VALUES ('Dokuz Eylül Üniversitesi', 'İzmir'),
	('Ege Üniversitesi', 'İzmir');


CALL add_person('Deniz','Yürekdeler','dyurekdeler@live.com','12345678','01.01.1970','izmir','0554413061',2,'STU');
CALL add_person('Semih','Utku','semihutku@mail.com','12345678','01.01.1970','izmir','0554413061',1,'LEC');

INSERT INTO public.tbl_course(
	title, description, price, video_link, category, lecturer_id, thumbnail)
	VALUES ('android','this course teaches android applications',15,'https://www.youtube.com/embed/KpwoBlDLxq0','software',2,'https://image.shutterstock.com/image-photo/beautiful-water-drop-on-dandelion-260nw-789676552.jpg'),
	 ('web','this course teaches how to develop web pages',15,'https://www.youtube.com/embed/KpwoBlDLxq0','software',2,'https://image.shutterstock.com/image-photo/beautiful-water-drop-on-dandelion-260nw-789676552.jpg'),
	 ('database','this course focuses on database design',15,'https://www.youtube.com/embed/KpwoBlDLxq0','software',2,'https://image.shutterstock.com/image-photo/beautiful-water-drop-on-dandelion-260nw-789676552.jpg');


INSERT INTO public.tbl_order(
	student_id, course_id, order_date)
	VALUES (1,1,'12.05.2010'),
	(1,2,'15.05.2010');

INSERT INTO public.tbl_comment(
	person_id, description, title, course_id, post_date)
	VALUES (1,'This course is very helpful', 'Nice Course', 1, '24.12.2019'),
	(1,'Teacher is fluent in English', 'Understanding', 1, '29.12.2019');

INSERT INTO public.tbl_favorites(
	student_id, course_id)
	VALUES (1,1);

INSERT INTO public.tbl_report(
	student_id, description, course_id, report_date)
	VALUES (1,'It is not teaching what the title says',2,'05.05.2018');


CREATE USER nisakko WITH PASSWORD '123456';
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO nisakko;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO nisakko;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO nisakko;

select pg_terminate_backend(pid) from pg_stat_activity where datname='Online_Course_Platform'



SELECT tbl_course.course_id,  count(comment_id) FROM tbl_course 
LEFT OUTER JOIN tbl_comment 
ON tbl_course.course_id = tbl_comment.course_id 
GROUP BY tbl_course.course_id 

SELECT tbl_course.course_id,  count(comment_id) FROM tbl_course 
LEFT OUTER JOIN tbl_comment 
ON tbl_course.course_id = tbl_comment.course_id 
WHERE tbl_course.course_id = 2
GROUP BY tbl_course.course_id 


ALTER SEQUENCE tbl_course_course_id_seq RESTART WITH 1;

LOGGGGGG ::: https://jackworthen.com/2018/03/19/creating-a-log-table-to-track-changes-to-database-objects-in-sql-server/





