```sql
select title 
from course
where dept_name='Comp. Sci.' and credits=3;
```
![1_a](./1_a.png)

```sql
select distinct student.ID
from (student join takes using(ID)) 
join (instructor join teaches using(ID)) 
using(course_id, sec_id, semester, year) 
where instructor.name = 'Srinivasan';
```
![1_b](./1_b.png)

```sql
select max(salary) 
from instructor;
```
![1_c](./1_c.png)

```sql
select course_id, sec_id, count(ID) 
from section natural join takes 
where semester = 'Fall' and year = 2017
group by course_id, sec_id;
```
![1_d](./1_d.png)

```sql
create table grade_points (
    grade varchar(20) primary key,
    points numeric(2,1) not null
);
```
![2_1](./2_1.png)

```sql
insert into grade_points (grade, points) values
('A+', 4.3),
('A', 4.0),
('A-', 3.7),
('B+', 3.3),
('B', 3.0),
('B-', 2.7),
('C+', 2.3),
('C', 2.0),
('C-', 1.7),
('D+', 1.3),
('D', 1.0),
('D-', 0.7),
('F', 0.0);
```
![2_2](./2_2.png)

```sql
alter table takes
add constraint takes_grade_fkey
foreign key (grade) references grade_points(grade);
```
![2_3](./2_3.png)

```sql
select sum(credits * points) as Scored
from takes natural join course natural join grade_points
where ID='12345';
```
![2_a](./2_a.png)

```sql
select sum(credits * points) / sum(credits) as GPA
from takes natural join course natural join grade_points
where ID='12345'; 
```
![2_b](./2_b.png)

```sql
select ID, sum(credits * points) / sum(credits) as GPA
from takes natural join course natural join grade_points
group by ID;
```
![2_c](./2_c.png)

```sql
select ID, sum(credits * points) / sum(credits) as GPA
from takes natural join course natural join grade_points
group by ID
having sum(credits * points) / sum(credits) > 3.0;
```
![2_d](./2_d.png)