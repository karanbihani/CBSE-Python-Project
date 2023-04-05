create database game;
use game;
create table login (uname varchar(50) not null primary key, pass varchar(50),plct int default 0);
create table plays(uname varchar(50), level int, coinct int, win int default 0, tolp datetime default now());
