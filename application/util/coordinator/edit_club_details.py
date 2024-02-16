
#-------------Start of making tables-------------------#
create_club_table = """
Create table if not exists clubs(
  club_id Integer primary key AUTOINCREMENT,
  club_name varchar(400),
  club_description varchar(1000),
  coordinator_id integer,
  validity varchar(20) check (validity in ('Pending', 'Approved', 'Rejected')) default 'Pending',
  created datetime default CURRENT_TIMESTAMP,
  updated datetime DEFAULT CURRENT_TIMESTAMP,
  FOREIGN key (coordinator_id) REFERENCES coordinators(coordinator_id));
"""


create_memberships_table = """
  Create table if not exists club_memberships(
  club_id Integer,
  user_id Integer,
  validity varchar(20) check (validity in ('Pending', 'Approved', 'Rejected')),
  created datetime default CURRENT_TIMESTAMP,
  updated datetime DEFAULT CURRENT_TIMESTAMP,
  Primary key (club_id, user_id),
  FOREIGN key (club_id) REFERENCES clubs(club_id));
"""



#NOTE: this may not work, its erroing on sqlite online, need to check if this is correct bc I got help ~online~
restrict_number_of_clubs_per_user = """
  CREATE TRIGGER check_max_clubs
  BEFORE INSERT ON club_memberships
  BEGIN
      SELECT CASE
          WHEN (SELECT COUNT(*) FROM club_memberships WHERE user_id = NEW.user_id) >= 3
          THEN
              RAISE(ABORT, 'Cannot add more than 3 clubs for a user');
      END;
  END;
"""



create_events_table = """
 Create table if not exists events(
  event_id Integer primary key AUTOINCREMENT,
  club_id integer,
  event_name varchar(300),
  event_description varchar(1000),
  date_and_time datetime,
  venue varchar(400),
  created datetime default CURRENT_TIMESTAMP,
  updated datetime DEFAULT CURRENT_TIMESTAMP,
  FOREIGN key (club_id) REFERENCES clubs(club_id))
"""


create_participants_table = """ 
  Create table if not exists event_participants(
  event_id Integer,
  user_id integer,
  validity varchar(20) check (validity in ('Pending', 'Approved', 'Rejected')),
  created datetime default CURRENT_TIMESTAMP,
  updated datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY key (event_id, user_id),
  FOREIGN key (user_id) REFERENCES users(user_id)
  FOREIGN key (event_id) REFERENCES events(event_id));
"""
# create_venues_table = """
#   Create table if not exists venues(
#   venue_id Integer primary key AUTOINCREMENT,
#   venue_name varchar(400),
#   created datetime default CURRENT_TIMESTAMP,
#   updated datetime DEFAULT CURRENT_TIMESTAMP);
#  """

#-------------End of making tables-------------------#
#-------------Start of button functions-------------------#



##NOTE: these strings are intended to be used with formatting eg:
# insert_new_club = """
# INsert into clubs(club_name, club_description, coordinator_id)
# values({club_name}, {club_description}, {Coordinator_id});
# """.format(club_name = 'Archery', club_description = 'Big cool club', coordinator_id = 45)
#OR INSERT VARIABLES RATHER THAN STRINGS


insert_new_club = """
INSERT into clubs(club_name, club_description, coordinator_id)
values('{club_name}', '{club_description}', {coordinator_id});
"""

save_club_details = """
update  clubs
set club_name = '{new_name}', club_description = '{new_description}', updated = CURRENT_TIMESTAMP
Where club_id = {club_id};
"""
#Member commands
#Here we can call this command in a for loop for all members, so its not excecuted until save is clicked. On save it can read the box for each user/participant and delete where relevant.
# so save and delete are called together.

save_members = """
update club_memberships
set validity = '{NEW_VALIDITY}'   
where user_id = {user_id} and club_id = {club_id}, updated = CURRENT_TIMESTAMP;
"""#new_validity will be read from the form on save.

#called after save has been called for each member
delete_members = """
delete 
from club_memberships
where validity = 'Rejected' and club_id = {club_id};
"""

view_pending_members = """
select users.*
from users join club_memberships on users.user_id = club_memberships.user_id
where club_memberships.validity = 'Pending' and club_memberships.club_id = {club_id};
"""
view_members = """
select users.*
from users join club_memberships on users.user_id = club_memberships.user_id
where club_memberships.validity = '{status}' and club_memberships.club_id = {club_id};
"""
add_member = """
insert into club_memberships(club_id, user_id)
values ({club_id}, {user_id});
"""

view_pending_participants = """
select users.*
from users join event_participants on users.user_id = event_participants.user_id 
where event_participants.validity = 'Pending' and event_participants.event_id = {event_id};
"""
view_approved_participants = """
select users.*
from users join event_participants on users.user_id = event_participants.user_id join events on events.event_id = event_participants.event_id
where event_participants.validity = 'Approved' and event_participants.event_id = {event_id};
"""

save_participants = """
update club_memberships
set validity = '{NEW_VALIDITY}', updated = CURRENT_TIMESTAMP
where user_id = {user_id} and event_id = {event_id};
"""
delete_participants = """
delete 
from event_participants
where validity = 'Rejected' and event_id = {event_id};
"""

add_participant_member = """
insert into event_participants(event_id, user_id, validity)
values ({event_id}, {user_id}, 'Approved');
"""
add_participant_non_member = """
insert into event_participants(event_id, user_id)
values ({event_id}, {user_id});"""


insert_new_event = """
insert into events(club_id, event_name, event_description, date_and_time)
values({club_id}, '{event_name}', '{event_description}}', '{timestamp}');
"""

save_event_details = """
update events
set event_name = '{event_name}', event_description = '{event_description}', date_and_time = '{timestamp}', venue = '{venue}', updated = CURRENT_TIMESTAMP
where event_id = 7;
"""
view_past_events = """
select *
from events
where club_id = {club_id} and date_and_time < CURRENT_TIMESTAMP
order by date_and_time DESC;
"""
view_all_upcoming_events = """
select *
from events
where club_id = {club_id} and date_and_time > CURRENT_TIMESTAMP
order by date_and_time;
"""
limited_view_all_upcoming_events = """
select *
from events
where club_id = {club_id} and date_and_time >= CURRENT_TIMESTAMP
order by date_and_time
limit {limit};
"""
view_single_event = """
select *
from events
where event_id = {event_id};
"""

count_approved_members = """
select count(user_id)
from club_memberships
where club_id ={club_id} and validity = 'APPROVED'
"""
count_pending_members = """
select count(user_id)
from club_memberships
where club_id ={club_id} and validity = 'PENDING'
"""
count_pending_participants = """
select count(user_id)
from event_participants
where event_id ={event_id} and validity = 'PENDING'
"""

count_approved_participants = """
select count(user_id)
from event_participants
where event_id ={event_id} and validity = 'APPROVED'
"""
get_club_details="""
select *
from clubs
where club_id = {club_id};
"""

get_coordinator_name = """
select u.first_name, u.last_name
from users u join clubs c on u.user_id = c.creator
where c.club_id = {club_id};
"""


count_upcoming_events= """
select count(event_id)
from events
where club_id = {club_id} and date_and_time > CURRENT_TIMESTAMP;
"""
count_past_events= """
select count(event_id)
from events
where club_id = {club_id} and date_and_time < CURRENT_TIMESTAMP;"""


#TODO I've done this with string formatting, ask Darragh what the original idea was again as I have forgotten.