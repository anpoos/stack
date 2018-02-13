
create table employee (id integer(10) auto_increment primary key, first_name varchar(30), last_name varchar(20), emp_no varchar(20) not null, user_name varchar(30), password varchar(100), email varchar(30) not null, is_active varchar(20));
create table issue ( id integer(10) auto_increment primary key, title varchar(200)not null, description varchar(250)not null, created_by varchar(20) references employee(id), created_date date, deleted varchar(50) );
create table solution( id integer(10) auto_increment primary key, issue_id varchar(10) references issue(id), solution varchar(500) not null, created_by varchar(20) references employee(id), created_date date, deleted varchar(20));
insert into employee values(1,'saranya','A',106,'saran',md5('saran'),'saranya111@yahoo.com',0);
insert into employee values(2,'anbu','b',107,'anbu',md5('anbu'),'anbu@gmail.com',1);
-- insert into issue id values(1);	
insert into issue values(1,'test','test case','1','02.02.2018',1);
