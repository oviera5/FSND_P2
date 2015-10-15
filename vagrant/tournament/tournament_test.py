#!/usr/bin/env python
#
# Start of test cases for tournament.py

from tournament import *
import random
import math


def testDeleteMatches():
    # Delete all previous matches held in the database.
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    # Delete all previous matches and players held in the database.
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    # Test the number of players in the database.
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    # Test the number of players after registering one player.
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    # Test the number of players after registering four players.
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    # Test the standings before any matches have been recorded.
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even "
                         "before they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in "
                         "standings, even if they have no matches played.")
    print ("6. Newly registered players appear in the standings with no "
           "matches.")


def testReportMatches():
    # Test the standings after recording two matches.
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    # print(id1, id2, id3, id4)
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins "
                             "recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    # Test the pairings after recording two matches.
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


# End of test cases for tournament.py

# The following three functions provide the algorithm for the tournament.

def enterPlayer():
    # Prompt the user to enter player names for the tournament.

    print "Please enter 4 or 8 or 16 players."
    print
    p = 'y'
    x = countPlayers()
    while x < 16:

        if x == 4 or x == 8 or x == 16:
            p = raw_input("Would you like to enter more players? y/n: ")

        if p.strip() == 'y' or p.strip() == 'y':
            pname = raw_input("Enter player's name :")
            registerPlayer(pname)
        else:
            break
        x = countPlayers()

    return x


def generateRounds(p):
    # Provides the number of rounds based on the number players entered.

    r = int(math.log(p, 2))
    return r


def playtour():
    # Loops through rounds, records results, and displays winner.

    numOfPlayers = enterPlayer()
    numOfRounds = generateRounds(numOfPlayers)
    matchesPerRound = numOfPlayers/2

    for rnd in range(0, numOfRounds):

        if rnd == 0:
            standings = playerStandings()
            listOfPlayers = [row[0] for row in standings]
            random.shuffle(listOfPlayers)
            x = listOfPlayers

            for match in zip(x[0::2], x[1::2]):
                flip = random.randint(0, 1)
                if flip == 0:
                    winer = match[0]
                    loser = match[1]
                else:
                    winer = match[1]
                    loser = match[0]
                reportMatch(winer, loser, rnd+1)
        else:

            for match in range(0, matchesPerRound):

                pairings = swissPairings(rnd)
                a = [row[0] for row in pairings]
                b = [row[2] for row in pairings]

                y = 0

                # Check pairs for empty tuples due to eliminating rematches

                for pair in range(0, len(a)):
                    x = checkPairing(a[pair], b[pair], rnd)
                    if x > y:
                        y = x
                        w = a[pair]
                        l = b[pair]

                if y == 0:
                    w = a[0]
                    l = b[0]

                # add some randomness to outcome
                flip = random.randint(0, 1)
                if flip == 0:
                    winer = w
                    loser = l
                else:
                    winer = l
                    loser = w

                reportMatch(winer, loser, rnd+1)

    print "The winner is " + theWinner()


if __name__ == '__main__':
    # To start the test cases, call the following 8 functions.
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "Success!  All tests pass!"
    # Ends the calls to the test case functions.
    print
    # Ask the user if they want to start a tournament.
    while True:
        n = raw_input("Would you like to Start A New Tournamemnt? y/n: ")
        if n.strip() == 'n' or n.strip() == 'N':
            break
        elif n.strip() == 'y' or n.strip() == 'Y':
            deleteMatches()
            deletePlayers()
            playtour()
        else:
            print 'You did not press y or n'
