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
	university_location TEXT NOT NULL,
	discount_info INT DEFAULT 0 NOT NULL,
	CONSTRAINT "discountRange" CHECK (discount_info in (0,10,25,50))
);

CREATE TABLE tbl_student(
	student_id INT NOT NULL PRIMARY KEY,
	family_id INT,
	university_id INT,
	CONSTRAINT "fk_universityId" FOREIGN KEY("university_id") REFERENCES public."tbl_university"(university_id),
	CONSTRAINT "fk_studentId" FOREIGN KEY("student_id") REFERENCES public."tbl_person"(person_id)
);

CREATE TABLE tbl_lecturer(
	lecturer_id INT NOT NULL PRIMARY KEY,
	university_id INT NOT NULL,
	CONSTRAINT "fk_lecturerId" FOREIGN KEY("lecturer_id") REFERENCES public."tbl_person"(person_id),
	CONSTRAINT "fk_universityId" FOREIGN KEY("university_id") REFERENCES public."tbl_university"(university_id)
);

CREATE TABLE tbl_supervisor(
	supervisor_id INT NOT NULL PRIMARY KEY,
	authority_level INT DEFAULT 0 NOT NULL,
	CONSTRAINT "fk_supervisorId" FOREIGN KEY("supervisor_id") REFERENCES public."tbl_person"(person_id)
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
	CONSTRAINT "fk_lecturerId" FOREIGN KEY("lecturer_id") REFERENCES public."tbl_lecturer"(lecturer_id)
);

CREATE TABLE tbl_comment (
	comment_id SERIAL PRIMARY KEY,
	student_id INT NOT NULL,
	description TEXT NOT NULL,
	title TEXT NOT NULL,
	course_id INT NOT NULL,
	post_date TIMESTAMP WITH TIME ZONE NOT NULL,
	CONSTRAINT "fk_courseId" FOREIGN KEY("course_id") REFERENCES public."tbl_course"(course_id),
	CONSTRAINT "fk_studentId" FOREIGN KEY("student_id") REFERENCES public."tbl_student"(student_id)
);

CREATE TABLE tbl_report (
	report_id SERIAL PRIMARY KEY,
	student_id INT NOT NULL,
	description TEXT NOT NULL,
	course_id INT NOT NULL,
	report_date TIMESTAMP WITH TIME ZONE NOT NULL,
	CONSTRAINT "fk_courseId" FOREIGN KEY("course_id") REFERENCES public."tbl_course"(course_id),
	CONSTRAINT "fk_studentId" FOREIGN KEY("student_id") REFERENCES public."tbl_student"(student_id)
);

CREATE TABLE tbl_family (
	family_id SERIAL PRIMARY KEY,
	student1_id INT NOT NULL UNIQUE,
	student2_id INT NOT NULL UNIQUE,
	creation_date TIMESTAMP WITH TIME ZONE NOT NULL,
	CONSTRAINT "fk_studentId1" FOREIGN KEY("student1_id") REFERENCES public."tbl_student"(student_id),
	CONSTRAINT "fk_studentId2" FOREIGN KEY("student2_id") REFERENCES public."tbl_student"(student_id),
	CONSTRAINT "check_students" CHECK(student1_id != student2_id)
);

CREATE TABLE tbl_order (
	order_id SERIAL PRIMARY KEY,
	student_id INT NOT NULL,
	course_id INT NOT NULL,
	order_date TIMESTAMP WITH TIME ZONE NOT NULL,
	CONSTRAINT "fk_studentId" FOREIGN KEY("student_id") REFERENCES public."tbl_student"(student_id),
	CONSTRAINT "fk_courseId" FOREIGN KEY("course_id") REFERENCES public."tbl_course"(course_id)
);

CREATE TABLE tbl_favorites (
	student_id INT NOT NULL REFERENCES tbl_student(student_id),
	course_id INT NOT NULL REFERENCES tbl_course(course_id),
	primary key(student_id,course_id)
);

CREATE TABLE tbl_supervised (
	supervisor_id INT NOT NULL REFERENCES tbl_supervisor(supervisor_id),
	course_id INT NOT NULL REFERENCES tbl_course(course_id),
	approved BOOL NOT NULL,
	primary key(supervisor_id,course_id)
);

INSERT INTO public.tbl_university(university_name, university_location, discount_info)
	VALUES ('Dokuz Eylül Üniversitesi', 'İzmir',0),
	('Ege Üniversitesi', 'İzmir',0);

INSERT INTO public.tbl_person(
	first_name, last_name, email, password, date_of_birth, address, phone, person_type)
	VALUES ('Semih','Utku','semihutku@mail.com',12345678,'01.01.1970','izmir','0554413061','LEC');

INSERT INTO public.tbl_lecturer(lecturer_id, university_id)
	VALUES (1,'1');
INSERT INTO public.tbl_course(
	title, description, price, video_link, category, lecturer_id, thumbnail)
	VALUES ('android','desc',15,'https://www.youtube.com/watch?v=aT-kWWPDZmo','software',1,'https://image.shutterstock.com/image-photo/beautiful-water-drop-on-dandelion-260nw-789676552.jpg'),
	 ('web','desc',15,'https://www.youtube.com/watch?v=aT-kWWPDZmo','software',1,'https://image.shutterstock.com/image-photo/beautiful-water-drop-on-dandelion-260nw-789676552.jpg'),
	 ('database','desc',15,'https://www.youtube.com/watch?v=aT-kWWPDZmo','software',1,'https://image.shutterstock.com/image-photo/beautiful-water-drop-on-dandelion-260nw-789676552.jpg');

INSERT INTO public.tbl_order(
	student_id, course_id, order_date)
	VALUES (1,1,'12.05.2010'),
	(1,2,'12.05.2010');
CREATE USER nisakko WITH PASSWORD '123456';
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO nisakko;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO nisakko;