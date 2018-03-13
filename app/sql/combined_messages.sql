create table combined_messages
(
	email varchar(100) not null,
	mobile varchar(10) not null,
	primary key (email, mobile),
	carrier varchar(3) not null,
	alert_time time not null,
	index alert_index(alert_time),
	email_alert tinyint(1) not null,
	sms_alert tinyint(1) not null,
	message varchar(160) not null
);


