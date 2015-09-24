-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
drop database if exists tournament;
create database tournament;
\c tournament;
create table players
(
    playerId serial primary key,
    playerName varchar(40)
);
create table matches
(
    matchId serial primary key,
    round integer,
    playerA integer references players,
    playerB integer references players,
    winPlayerId integer,
    losPlayerId integer
);
create table standings
(
    playerId integer references players,
    playerName varchar(40),
    wins integer,
    matches integer
);