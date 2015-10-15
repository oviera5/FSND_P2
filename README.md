FSND_P2
=============

Project 2 for Full Stack Web Developer Nanodegree

Introduction

    This python database application was created by Orlando Viera for Project 2 of the Full Stack Web Developer Nanodegree.

Create date
    
    October 15, 2015

File location

    https://github.com/oviera5/FSND_P2

Installation instructions

    To run this python project, please follow the steps listed below:

        01 - Have Python 2 installed on your machine.
        02 - Install Vagrant: http://vagrantup.com/
        03 - Install VirtualBox: https://www.virtualbox.org/
        04 - Fork the fullstack-nanodegree-vm repository:
             http://github.com/udacity/fullstack-nanodegree-vm
        05 - Clone the fullstack-nanodegree-vm repository to your local machine
        06 - Copy the following files from this repository over the existing files
             in /fullstack-nanodegree-vm/vagrant/tournament:
        
             a) tournament.sql
             b) tournament.py
             c) tournament_test.py
    
        07 - Make your present working directory: 
             /fullstack-nanodegree-vm/vagrant/tournament
        08 - Then type the following on the command line:

             a) vagrant up
             b) vagrant ssh
             c) cd /vagrant
             d) cd tournament
             e) psql

        09 - Type the following to import schema and exit the database: 

             a) \i tournament.sql
             b) \q

        10 - Run the application by entering the following at the prompt:

             python tournament_test.py

        11 - The test cases will run first, then you will be prompted to 
             to run a full tournament by entering 4 or 8 or 16 players.

        12 - The tournament will display the winner and you will be
             prompted to run another tournament or to exit.

Notes to evaluator

        For extra credit this application does the following:

            1) Prevents rematches between players by incorporating the
               following views in the database:

               a) trackmatches
               b) possiblematches
               c) availablematches

            2) Rank players according to Opponent Match Wins(OMW) by 
               incorporating the 'oppmatchwin' view.

Contact information

    Email: orlando.g.viera@gmail.com