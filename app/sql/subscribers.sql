create table subscribers
(
	prefix varchar(3) not null,
	first_name varchar(35) not null,
	middle_name varchar(35) null,
	last_name varchar(35) not null,
	suffix varchar(5) null,
	address varchar(100) not null,
	address2 varchar(100) null,
	city varchar(100) not null,
	state varchar(2) not null,
	zip varchar(5) not null,
	municipality varchar(25) not null,
	email varchar(100) not null,
	mobile varchar(10) not null,
	primary key (email, mobile),
	carrier varchar(3) not null,
	recycle_zone varchar(10) not null,
	trash_zone varchar(10) not null,
	yard_zone varchar(10) not null,
	recycle_day int(11) not null,
	trash_day int(11) not null,
	yard_day int(11) not null,
	alert_time time not null,
	alert_day int(11) not null,
	email_alert tinyint(1) not null,
	sms_alert tinyint(1) not null,
	subscribe tinyint(1) not null,
	creation datetime not null
);


