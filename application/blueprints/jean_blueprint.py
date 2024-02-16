from flask import render_template, session, Blueprint, request, flash, redirect, url_for

from ..util import db_functions as dbf
from ..util.coordinator import edit_club_details as ecd

import logging

jean_blueprint = Blueprint("jean_blueprint", __name__)


club_id = 0
# coordinator_name = "Jean"


from flask import request, render_template

#-------------------Start of coordinator dashboard--------------------------------------------------------------------------

@jean_blueprint.route("/cohome", methods=["GET"])
def cohome():

    club_id = request.args.get('club_id', 0)

    if "user" in session:
        user = session["user"]
        return render_template("html/misc/default-home.html", header=f"Hello {user}!")
    
    coordinator_info = dbf.query_db(ecd.get_coordinator_name.format(club_id=0))

    if coordinator_info:
        coordinator_name = f"{coordinator_info[0]['first_name']} {coordinator_info[0]['last_name']}"
    else:
        coordinator_name = "Coordinator not found"

    club_details = dbf.query_db(ecd.get_club_details.format(club_id=club_id))[0]
    club_name = club_details["club_name"]
    club_description = club_details["club_description"]

    number_of_active_users = dbf.query_db(ecd.count_approved_members.format(club_id=club_id))[0][0]
    number_of_pending_users = dbf.query_db(ecd.count_pending_members.format(club_id=club_id))[0][0]


    
    limited_upcoming_events = dbf.query_db(ecd.limited_view_all_upcoming_events.format(club_id=club_id, limit =3))
    event_details = []
    if limited_upcoming_events is None:
        limited_upcoming_events = []
    else:
        for event in limited_upcoming_events:
            number_of_approved_participants = dbf.query_db(ecd.count_approved_participants.format(event_id=event["event_id"]))[0][0]
            number_of_pending_participants = dbf.query_db(ecd.count_pending_participants.format(event_id=event["event_id"]))[0][0]
            event_details.append({
                'event_id': event["event_id"],
                'event_name': event["event_name"],
                'event_date': event["date_and_time"],
                'approved_participants': number_of_approved_participants,
                'pending_participants': number_of_pending_participants,
            })




    return render_template("html/coordinator/coordinator-dashboard.html",
                        coordinator_name=coordinator_name,
                        club_id=club_id,
                        active_users=number_of_active_users,
                        pending_users=number_of_pending_users,
                        club_title=club_name,
                        club_description=club_description,
                        limited_events=event_details
                                                              )

@jean_blueprint.route("/cohome", methods=["POST"])
def save_club_details():
    club_id = request.args.get('club_id', 0)
    club_name = request.form["club_name"]
    club_description = request.form["club_description"]

    
    try:
        # Update the database
        dbf.modify_db(ecd.save_club_details.format(club_id=club_id, new_name=str(club_name), new_description=str(club_description)))

        # Print a message for debugging
        print("Database updated successfully")

        # Flash a success message
        flash("Club details successfully updated", "success")

    except Exception as e:
        # Print an error message for debugging
        logging.warning(f"Error updating database: {e}")
        print(f"Error updating database: {e}")

    # Redirect to the /cohome route after processing the form
    return redirect(url_for('jean_blueprint.cohome', club_id=club_id))

#-------------------end of coordinator dashboard--------------------------------------------------------------------------



#--------------------member_view-----------------------------



@jean_blueprint.route("/memview/<status>", methods=["GET"])
def view_members(status):
    if "user" in session:
        user: str = session["user"]
        return render_template("html/misc/default-home.html", header=f"Hello {user}!")
    status_users = dbf.query_db(ecd.view_members.format(status=status.upper(), club_id = club_id))
    return render_template("html/coordinator/member-view.html", status = status, status_users = status_users)


@jean_blueprint.route("/memview/<status>", methods=["POST"])
#Note, decided to take status arameter out here, may end up putting it back
def save_member_details():
    club_id = club_id
    for user in status_users:
        user_id = request.form["user_id"]
        new_validity = request.form["validity"]
        dbf.modify_db(ecd.save_members.format(user_id=user_id, club_id=club_id, NEW_VALIDITY=new_validity))






#-----------------------------------------end of member view-----------------------------------------
@jean_blueprint.route("/participantview/<status>")
def parview(status):
    if "user" in session:
        user: str = session["user"]
        return render_template("html/misc/default-home.html", header=f"Hello {user}!")

    return render_template("html/coordinator/view-participants.html", status=status)


@jean_blueprint.route("/eventview/<timeline>")
def see_events(timeline):
    if "user" in session:
        user: str = session["user"]
        return render_template("html/misc/default-home.html", header=f"Hello {user}!")

    return render_template("html/coordinator/multi-event-view.html", timeline=timeline)

# ----------------------------Start of single event--------------------------------------------
@jean_blueprint.route("/new-event")
def new_event():
    if "user" in session:
        user: str = session["user"]
        return render_template("html/misc/default-home.html", header=f"Hello {user}!")

    return render_template("html/coordinator/single-event-view.html")

#TODO have this write to database, probably will encounter same problem as before



@jean_blueprint.route("/edit-event/<int:event_id>")
def edit_event(event_id):
    if "user" in session:
        user: str = session["user"]
        return render_template("html/misc/default-home.html", header=f"Hello {user}!")
    event_details = dbf.query_db(ecd.view_single_event.format(event_id=event_id))[0]
    return render_template("html/coordinator/single-event-view.html",  event_name = event_details["event_name"], event_date=event_details["date_and_time"],
                            event_location=event_details["venue"], event_description=event_details["event_description"],)

#---------------------------------------end of single event--------------------------------------------------
#TODO fix build error
# --------------End of Pages functions-----------------

