import sqlite3
connection = sqlite3.connect("Database.db")
cursor = connection.cursor()


#foreign key users id in memberships, event_participants
cursor.execute("""CREATE TABLE clubs(
               Club_name TEXT NOT NULL PRIMARY KEY, 
               description TEXT, 
               Coordinator_ID INTEGER NOT NULL UNIQUE FOREIGN KEY REFERENCES Users(ID), 
               Validity_status TEXT CHECK (Validity_status IN ('Approved', 'Pending', 'Rejected')), 
               Created DATE NOT NULL, 
               Updated DATE NOT NULL);""")


cursor.execute("""CREATE TABLE memberships(
               club_name NOT NULL FOREIGN KEY REFERENCES clubs(Club_name),
                member_ID  NOT NULL FOREIGN KEY REFERENCES USers(ID),
                Approval_status NOT NULL TEXT CHECK (Approval_status IN ('Pending', 'Approved', 'Rejected')), Created DATE NOT NULL, Updated DATE NOT NULL)""")

cursor.execute("""CREATE TABLE events(
               Club_name TEXT NOT NULL FOREIGN KEY REFERENCES clubs(Club_name),
               Event_name TEXT,
               Event_description TEXT, Date_and_Time DATE,
               Venue TEXT, Created DATE,
               Updated DATE)""")

cursor.execute("""CREATE TABLE event_participants (
               Event_name TEXT NOT NULL FOREIGN KEY REFERENCES events(Event_name),
               User_ID INTEGER NOT NULL FOREIGN KEY Users(ID),
               Approval_status TEXT NOT NULL CHECK(Approval_status IN('Approved', 'Pending', 'Rejected')),
               Created DATE,
               Updated DATE)""")



cursor.execute("SELECT * FROM USERS;")




print(cursor.fetchall())
connection.commit()
connection.close()

import re

regex = r"[a-z, A-Z]"

test_str = "Ruan's parents are 2 FISH!!!"

matches = re.finditer(regex, test_str, re.MULTILINE)

for matchNum, match in enumerate(matches, start=1):
    
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        
        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))