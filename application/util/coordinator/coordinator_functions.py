
from flask import redirect, url_for, flash
import application.util.db_functions as dbf


#Header setup
def get_coordinator_name(club_id):
    coordinator_info = dbf.query_db("""
    select u.first_name, u.last_name
    from users u join clubs c on u.user_id = c.creator
    where c.club_id = {club_id};
    """.format(club_id=club_id))
    if coordinator_info:
        return f"{coordinator_info[0]['first_name']} {coordinator_info[0]['last_name']}"
    else:
        return "Coordinator not found"



#-------viewing and editing club details----------------------

def get_club_details(club_id):
    club_details = dbf.query_db("""
    select *
    from clubs
    where club_id = {club_id};
    """.format(club_id=club_id))[0]
    club_name = club_details["club_name"]
    club_description = club_details["club_description"]
    return club_name, club_description

def save_club_details(club_id, new_name, new_description):
    try:
        dbf.modify_db("""
        update  clubs
        set club_name = '{new_name}', club_description = '{new_description}', updated = CURRENT_TIMESTAMP
        Where club_id = {club_id};
        """.format(club_id=club_id, new_name=str(new_name), new_description=str(new_description)))

        flash("Club details successfully updated", "success")
    except:
        flash("An error occurred while updating the club details", "error")
    return redirect(url_for('jean_blueprint.cohome', club_id=club_id))



#-------viewing members and participants----------------------
def count_active_users(club_id):
    number_of_active_users = dbf.query_db("""
    select count(user_id)
    from club_memberships
    where club_id ={club_id} and validity = 'APPROVED'
    """.format(club_id=club_id))[0][0]
    return number_of_active_users

def count_pending_users(club_id):
    number_of_pending_users = dbf.query_db("""
    select count(user_id)
    from club_memberships
    where club_id ={club_id} and validity = 'PENDING'
    """.format(club_id=club_id))[0][0]
    return number_of_pending_users

def get_all_members(club_id, status):
    status_users = dbf.query_db( """
    select users.*
    from users join club_memberships on users.user_id = club_memberships.user_id
    where club_memberships.validity = '{status}' and club_memberships.club_id = {club_id};
    """.format(status=status.upper(), club_id = club_id))
    return status_users

def save_member_status(club_id, user_id, new_validity):
    dbf.modify_db("""
    update club_memberships
    set validity = '{NEW_VALIDITY}'
    where user_id = {user_id} and club_id = {club_id}
    """.format(user_id=user_id, club_id=club_id, NEW_VALIDITY=new_validity.upper()))

def delete_rejected_members(club_id):
    dbf.modify_db("""
    delete 
    from club_memberships
    where validity = 'Rejected' and club_id = {club_id};
    """.format(club_id=club_id))

    #to be continued
#-------viewing events----------------------
def limited_view_all_upcoming_events(club_id):
    return (dbf.query_db("""
    select *
    from events
    where club_id = {club_id} and date_and_time >= CURRENT_TIMESTAMP
    order by date_and_time
    limit {limit};
    """.format(club_id=club_id, limit =5)))

def count_pending_participants(event_id):
    return (dbf.query_db("""
    select count(user_id)
    from event_participants
    where event_id ={event_id} and validity = 'PENDING'
    """.format(event_id=event_id))[0][0])

def count_approved_participants(event_id):
    return (dbf.query_db("""
    select count(user_id)
    from event_participants
    where event_id ={event_id} and validity = 'APPROVED'
    """ .format(event_id=event_id))[0][0])

def get_all_participants(event_id, status):
    return (dbf.query_db("""
    select users.*
    from users join event_participants on users.user_id = event_participants.user_id 
    where event_participants.validity = '{status}' and event_participants.event_id = {event_id};
    """.format(status=status.upper(), event_id = event_id)))

def save_participant_status(event_id, user_id, new_validity):
    dbf.modify_db("""
    update event_participants
    set validity = '{NEW_VALIDITY}', updated = CURRENT_TIMESTAMP
    where user_id = {user_id} and event_id = {event_id};
    """.format(user_id=user_id, event_id=event_id, NEW_VALIDITY=new_validity.upper()))

def delete_rejected_participants(event_id):
    dbf.modify_db("""
    delete 
    from event_participants
    where validity = 'Rejected' and event_id = {event_id};
    """.format(event_id=event_id))
#-----------editing events---------------------
def get_event_details(event_id):
    event_details = dbf.query_db("""
    select *
    from events
    where event_id = {event_id};
    """.format(event_id=event_id))[0]
    return event_details
