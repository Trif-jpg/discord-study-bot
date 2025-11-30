# Gary, a Discord study bot

### Purpose
**Gary** was created to make studying with friends more fun and interesting.
The whole purpose of **Gary** was to be able to compete with your friends while also studying for your midterms, an exam, etc. 

### Commands
**Gary** currently has 6 commands:
1. **-helpme** which displays, on Discord, all commands that currently exist.
2. **-log** which takes in two arguments (<time> <date>) and then later logs them in a *.csv* file alongside the user's id.
    - The argument <time> is expected to be *minutes* and the argument <date> in the format of *DD-MM-YY*.
    - In case *no date* is added while executing the command, **Gary** will log the current date, at the time the command is executed.
3. **-history** which displays all of the users past logs which are saved in the *.csv* file from most recent to oldest.
4. **-stats** which display the user's *total time* that has been logged at that time. 
5. **-leaderboard** which sorts the total time from all users from highest to lowest.
6. **clear** is an Admin only command which deletes all data stored in the *.csv* file.

### Future plans
In the future I plan to make **Gary** a bit more interesting rather than a bunch of simple commands that track time.
Some of the things I want to add in the near future:
- *Slash commands*
- *Better looking interface*
- *Time*
- *Data visualization*
- *Schedule system*


