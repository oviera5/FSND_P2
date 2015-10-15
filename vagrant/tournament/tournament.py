#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
# import random from randint


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    cur = DB.cursor()
    cur.execute("delete from matches;")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    cur = DB.cursor()
    cur.execute("delete from standings;")
    DB.commit()
    cur.execute("delete from players;")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    cur = DB.cursor()
    cur.execute("select count(playerid) as CountOfPlayers from players;")
    result = cur.fetchone()
    DB.close()
    return result[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    cur = DB.cursor()
    cur.execute("insert into players (playername) values (%s);", (name,))
    DB.commit()
    cur.execute("""insert into standings (playerid,playername,wins,matches)
        (select p.playerid, p.playername, 0, 0 from players p where
        p.playername = %s);""", (name,))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie. For extra credit,
    the left join allows for sorting by opponents matches wins.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    cur = DB.cursor()
    cur.execute("""select s.playerid, s.playername, s.wins, s.matches
       from standings s left join oppmatchwin o on s.playerid = o.playerid
       order by s.wins desc , o.omw desc, s.playerid;""")
    result = cur.fetchall()
    DB.close()
    return result


def reportMatch(winner, loser, rnd=1):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      rnd:  the current round of the tournament (optional)
    """
    DB = connect()
    cur = DB.cursor()
    cur.execute("""insert into matches (round, winplayerid,
                losplayerid) values (%s, %s, %s);""",
                (rnd, winner, loser,))
    DB.commit()
    cur.execute("""update standings set matches = matches + 1 where playerid
        in (%s, %s);""", (winner, loser,))
    DB.commit()
    cur.execute("""update standings set wins = wins + 1
                where playerid = %s;""", (winner,))
    DB.commit()
    DB.close()


def swissPairings(rnd=1):
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings. For extra credit, the left join and null in
    the where clause prevents rematches.

    Args:
      rnd:  the current round of the tournament (optional)

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB = connect()
    cur = DB.cursor()
    cur.execute("""select s1.playerid, s1.playername,
        s2.playerid, s2.playername
        from standings s1
        join standings s2 on s1.playerid < s2.playerid
        and s1.wins = s2.wins
        and s1.matches = s2.matches
        join availablematches a on s1.playerid = a.playera
        and s2.playerid = a.playerb
        where s1.matches = %s and s2.matches = %s
        order by s1.playerid;""", (rnd, rnd,))
    result = cur.fetchall()
    DB.close()
    return result


def checkPairing(winner, loser, rnd):
    """Returns the number of pairings prior to recording a match.

    Check the pairing to prevent empty tuples due to eliminating rematches.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      rnd:  the current round of the tournament

    Returns:
      A number of pairings available if the pairing sent as arguments
      are recorded as a match.

    """
    DB = connect()
    cur = DB.cursor()
    cur.execute("""select count(1)
        from standings s1
        join standings s2 on s1.playerid < s2.playerid
        and s1.wins = s2.wins
        and s1.matches = s2.matches
        join availablematches a on s1.playerid = a.playera
        and s2.playerid = a.playerb
        where s1.matches = %s
          and s2.matches = %s
          and s1.playerid <> %s and s2.playerid <> %s
          and s1.playerid <> %s and s2.playerid <> %s;""",
                (rnd, rnd, winner, loser, loser, winner,))
    result = cur.fetchone()
    DB.close()
    return result[0]


def theWinner():
    """Returns the winning player's name."""
    DB = connect()
    cur = DB.cursor()
    cur.execute("select playername from standings where (wins/matches) = 1")
    result = cur.fetchone()
    DB.close()
    return result[0]
