drop database if exists notes;
create database notes character set = 'utf8' collate = 'utf8_general_ci';
use notes;
create table users(
	id int not null auto_increment,
	username varchar(255) not null unique,
	hash char(87) not null,
	fullname varchar(255),
	constraint users_PK primary key(id),
	constraint userID_unique unique(id)
);
create table notes(
	id int not null auto_increment unique,
	userID int not null,
	content text not null,
	added TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
	lastEdited TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	active int default 1,  
	-- constraints
	constraint notes_PK primary key(id),
	constraint notes_userid_FK foreign key(userID) references users(id)
);
create table apiKeys(
	userID int not null,
	aKey char(255) not null,
	issued timestamp default current_timestamp,
	eternalKey int(1) default 0,
	-- constraints
	constraint apikeys_PK primary key(aKey),
	constraint apikeys_FK foreign key(userID) references users(id),
	constraint apikeys_akey_unique unique(aKey),
	constraint apikeys_userID_unique unique(userID) -- This is dont to force good key control, no user can have two keys. 
	
);	

-- SP, function, triggers. 

-- Adding a user
delimiter $$
create procedure adduser(user_name varchar(255), hash_ char(87), fullName varchar(255)) 
begin
	INSERT INTO users(username, hash, fullname) VALUES (user_name, hash_, fullname);
end $$
delimiter ;

-- Adding a user;
#delimiter $$
#create function adduser(user_name varchar(255), hash_ char(87), fullName varchar(255))
#return int determanistic
#	begin	
#		return(INSERT INTO users(username, hash, fullname) VALUES (user_name, hash_, fullname);  select count(*) from users where username = user_name;);
#end $$
delimiter ;
-- Adding a note
delimiter $$
create procedure addnote(userid_ int, content_ text)
begin 
	INSERT INTO notes(userID,content)VALUES (userid_, content_);
end $$
delimiter ;
-- adding an apikey
delimiter $$
create procedure addapikey(userid_ int, akey_ char(87))
begin
	insert into apiKeys(userID, aKey) VALUES (userid_, akey_);
end $$
delimiter ;
-- Deleting a note
delimiter $$
create procedure deletenote(id_ int, userid_ int)
begin
	delete from notes where id = id_ and userID = userid_;
end $$
delimiter ;
-- Archive a note 
delimiter $$
create procedure archivenote(id_ int, userid int)
begin
	update notes set active = 0 where id = id_ and userID = userid;
end $$
delimiter ;
-- gettting apikeys from authenticated user. 
delimiter $$
create function getapikey(userid_ int)
returns char(87)
	begin
	return(select aKey from apiKeys where userID = userid_ and issued > date_sub(now(), interval 3 hour)); 
end $$
delimiter ;
-- trigger, delete old apikeys on a api query. once they are more then 3 hours old.
-- not working out. instead the select will limit to only three hour old keys. 


