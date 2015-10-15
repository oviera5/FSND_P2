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
create view trackmatches as
(    
    select a.winplayerid as playerA,
           a.losplayerid as playerB, 
           s.wins
      from matches a 
      left join standings s on a.losplayerId = s.playerId

    union all

    select b.losplayerid, 
           b.winplayerid, 
           s.wins
      from matches b 
      left join standings s on b.winplayerId = s.playerid
);
create view oppmatchwin as 
(
    select playera as playerid,
           sum(wins) as omw
      from trackmatches
     group by playera 
);
create view possiblematches as
(
    select a.playerid playera,
           b.playerid playerb
      from players a
     cross join players b
     where a.playerid <> b.playerid
);
create view availablematches as
(
    select playera,
           playerb
      from possiblematches p
    except
    select playera,
           playerb
      from trackmatches
);