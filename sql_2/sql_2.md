```sql
select * from instructor;
```
![1](./1.png)

```sql
select * from course;
```
![2](./2.png)

```sql
update instructor
set salary = salary * 1.1
where dept_name = 'Comp. Sci.';
```
![3](./3.png)

```sql
delete from course
where course_id not in (
    select course_id
    from section
);
```
![4](./4.png)

```sql
insert into instructor 
    select id, name, dept_name, 10000
    from student
    where tot_cred > 100;
```
![5](./5.png)

```sql
select * from instructor;
```
![6](./6.png)

```sql
select * from course;
```
![7](./7.png)

```sql
select id, person_name, city, street
from employee natural join works
where company_name = 'First Bank Corporation';

select id, person_name, city, street
from employee
where id in (
    select id from works
    where company_name = 'First Bank Corporation'
);
```
![8](./8.png)

```sql
select id, person_name, city, street
from employee natural join works
where company_name = 'First Bank Corporation' and salary > 10000;
```
![9](./9.png)

```sql
select id
from employee 
where id not in (
    select id
    from works
    where company_name = 'First Bank Corporation'
);

select id
from works
where company_name <> 'First Bank Corporation';
```
![10](./10.png)

```sql
select id
from works
where salary > (select max(salary)
                from works
                where company_name = 'Small Bank Corporation');
```
![11](./11.png)

```sql
select company_name
from company
where city in (select city
                from company
                where company_name = 'Small Bank Corporation');
```
![12](./12.png)

```sql
select company_name
from works
group by company_name
having count(id) >= all (select count(id)
                        from works
                        group by company_name);
```
![13](./13.png)

```sql
select company_name
from works
group by company_name
having avg(salary) > (select avg(salary)
                        from works
                        where company_name = 'First Bank Corporation');
```
![14](./14.png)
