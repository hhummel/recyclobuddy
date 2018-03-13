create table messages
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
	service varchar(10) not null,
	carrier varchar(3) not null,
	primary key (email, mobile, service),
	alert_time time not null,
	alert_day int(11) not null,
	email_alert tinyint(1) not null,
	sms_alert tinyint(1) not null
);


