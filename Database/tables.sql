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
	select 1 as result;
end $$
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
create function getapikey(userid int)
returns char(87)
	begin
	return(select aKey from apiKeys where userID = userid); 
end $$
delimiter ;
-- trigger, delete old apikeys on a api query. once they are more then 3 hours old.
#create trigger deloldapikeys
#	before select on apiKeys
#		delete from apiKeys
#
#






# create trigger dontbookwhengone
# 13         before insert on bookedflights
# 12         for each row
# 11                 begin
# 10                         declare msg varchar(255);
#  9                         declare currdate date;
#  8             declare flightdate date;
#  7                         set currdate = (select curdate());
#  6                         set flightdate = (select flightDate from flights where flightCode = new.flightCode);
#  5                         if(flightdate < currdate) then
#  4                                 set msg = 'The flight has already left.';
#  3                                 signal sqlstate '45000' set message_text = msg;
#  2                         end if;
#  1                 end $$
#  0 delimiter ;
#
