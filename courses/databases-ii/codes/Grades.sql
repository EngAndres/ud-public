create table if not exists test_school.student(
	code INT primary key, 
	name VARCHAR(40) not null
);

create table if not exists test_school.course(
	code INT primary key,
	name VARCHAR(30) not null unique,
	credits INT default 1
);


create table if not exists test_school.grade(
	id SERIAL primary key,
	value DECIMAL default 0.0,
	course_fk INT,
	student_fk INT,
	foreign key (course_fk) 
		references course(code),
	foreign key (student_fk) 
		references student(code)
);

insert into test_school.student(code, name)
values (233, 'Pepita');
insert into test_school.student(code, name)
values (345, 'Pepito');
insert into test_school.student(code, name)
values (987, 'Sutanita');

select * from test_school.student;


insert into test_school.course(code, name, credits)
values(2, 'Bases de Datos', 3);
insert into test_school.course(code, name, credits)
values(1, 'Ciencias de la Computación', 1);
insert into test_school.course(code, name, credits)
values(4, 'Inteligencia Artificial', 4);

select * from test_school.course;

insert into grade(value, student_fk, course_fk)
values(3.5, 233, 1);
insert into grade(value, student_fk, course_fk)
values(4.5, 233, 4);
insert into grade(value, student_fk, course_fk)
values(3.5, 345, 2);
insert into grade(value, student_fk, course_fk)
values(3.0, 987, 4);
insert into grade(value, student_fk, course_fk)
values(3.0, 987, 1);

select * from grade;

-- All students with courses
select student.code, student.name,
		course.name, grade.value
from student
join grade 
	on grade.student_fk = student.code
join course 
	on grade.course_fk = course.code;

-- Average per studient
select student.code, student.name,
		AVG(grade.value) as grade_average
from student
join grade 
	on grade.student_fk = student.code
group by student.code
order by grade_average DESC;

--Average per course
select course.code, course.name,
	   ROUND(AVG(grade.value), 1) as grade_average,
	   MIN(grade.value) as grade_min,
	   MAX(grade.value) as grade_max
from course
join grade 
	on grade.course_fk = course.code
group by course.code
order by grade_average DESC;

with best_grades as (
	select course_fk, AVG(value) as avg_grade
	from grade
	group by course_fk
	order by avg_grade desc
	limit 3
)
select course.name, best_grades.avg_grade
from course
join best_grades
	on course.code = best_grades.course_fk;


-- Get best student per course
with max_ as (
	select course_fk, max(value) as max_grade
	from grade
	group by course_fk
),
best_students as (
	select grade.student_fk, max_.course_fk,
			max_.max_grade
	from grade
	join max_
		on max_.course_fk = grade.course_fk
	where 
		grade.value = max_.max_grade
)
select student.name as student,
		course.name as course,
		best_students.max_grade as grade
from student 
join best_students 
	on best_students.student_fk = student.code
join course
	on best_students.course_fk  = course.code;
