create table users(
	user_id int primary key identity (1,1),
	user_name varchar(100) not null,
	user_email varchar(100) unique not null
);

create table projects(
	project_id int primary key identity (1,1),
	project_name varchar(100) not null,
	project_type varchar(50) check (project_type in ('Quest', 'IWO', 'SubK')),
	project_segment varchar(50) check (project_segment in ('AVE', 'C&L', 'DEE', 'PMT', 'ICBM', 'AP')),
	project_supplier varchar(50),
	project_value int, 
	project_priority varchar(50) check (project_priority in ('High', 'Medium', 'Low')),
	project_create_date datetime default getdate(),
	project_due_date date,
	user_id int not null,
	foreign key (user_id) references users(user_id) on delete cascade
);

create table actions(
	action_id int primary key identity (1,1), 
	action_name varchar(100) not null, 
	action_priority varchar(50) check (action_priority in ('High', 'Medium', 'Low')), 
	action_due_date date, 
	action_create_date datetime default getdate(), 
	action_description varchar(250), 
	project_id int not null,
	foreign key (project_id) references projects(project_id) on delete cascade
);

create table subactions(
	subaction_id int primary key identity (1,1), 
	subaction_name varchar(100) not null, 
	subaction_description varchar(250), 
	subaction_create_date datetime default getdate(), 
	subaction_due_date date, 
	subaction_priority varchar(50) check (subaction_priority in ('High', 'Medium', 'Low')),
	action_id int not null,
	foreign key (action_id) references actions(action_id) on delete cascade
);

select @@servername;
