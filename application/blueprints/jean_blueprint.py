from flask import render_template, session, Blueprint, request, flash, redirect, url_for

from ..util import db_functions as dbf
from ..util.coordinator import coordinator_functions as cf

import logging

jean_blueprint = Blueprint("jean_blueprint", __name__)


club_id = 0
# coordinator_name = "Jean"


from flask import request, render_template

#-------------------Start of coordinator dashboard--------------------------------------------------------------------------
#***********************************************************
#***********************************************************
@jean_blueprint.route("/cohome", methods=["GET"])
def cohome():

    club_id = request.args.get('club_id', 0)

    if "user" in session:
        user = session["user"]
        return render_template("html/misc/default-home.html", header=f"Hello {user}!")
    
    coordinator_name = cf.get_coordinator_name(club_id)
    club_name = cf.get_club_details(club_id)[0]
    club_description = cf.get_club_details(club_id)[1]
    #***********************************************************

    number_of_active_users = cf.count_active_users(club_id)
    number_of_pending_users = cf.count_pending_users(club_id)

    #***********************************************************
    limited_upcoming_events = cf.limited_view_all_upcoming_events(club_id)
    event_details = []
    if limited_upcoming_events is None:
        limited_upcoming_events = []
    else:
        for event in limited_upcoming_events:
            number_of_pending_participants = cf.count_pending_participants(event["event_id"])
            number_of_approved_participants = cf.count_approved_participants(event["event_id"])
            event_details.append({
                'event_id': event["event_id"],
                'event_name': event["event_name"],
                'event_date': event["date_and_time"],
                'approved_participants': number_of_approved_participants,
                'pending_participants': number_of_pending_participants,
            })


    #***********************************************************

    return render_template("html/coordinator/coordinator-dashboard.html",
                        coordinator_name=coordinator_name,
                        club_id=club_id,
                        active_users=number_of_active_users,
                        pending_users=number_of_pending_users,
                        club_title=club_name,
                        club_description=club_description,
                        limited_events=event_details
                                                              )

#***********************************************************
#***********************************************************


@jean_blueprint.route("/cohome", methods=["POST"])
def save_club_details():
    club_id = request.args.get('club_id', 0)
    club_name = request.form["club_name"]
    club_description = request.form["club_description"]
    cf.save_club_details(club_id, club_name, club_description)
    return redirect(url_for('jean_blueprint.cohome', club_id=club_id))
#***********************************************************
#-------------------end of coordinator dashboard--------------------------------------------------------------------------



#--------------------member_view-----------------------------



@jean_blueprint.route("/memview/<status>", methods=["GET"])
def view_members(status):
    if "user" in session:
        user: str = session["user"]
        return render_template("html/misc/default-home.html", header=f"Hello {user}!")
    status_users = cf.get_all_members(club_id, status)
    return render_template("html/coordinator/member-view.html", status = status, status_users = status_users)


@jean_blueprint.route("/memview", methods=["POST"])
#Note, decided to take status arameter out here, may end up putting it back
def save_member_details():
    global club_id
    for user_id in request.form.getlist("user_id"):
        new_validity = str(request.form.get(f"status_{user_id}")).upper()
        print(f"New Validity: {new_validity}")
        cf.save_member_status(club_id, user_id, new_validity)
        #call delete membershere
    cf.delete_rejected_members(club_id)

    return redirect(url_for('jean_blueprint.cohome', club_id=club_id))





#-----------------------------------------end of member view-----------------------------------------
#---------------------------------------start of participant stuff-----------------------------------
@jean_blueprint.route("/participantview/<status>/<event_id>", methods=["GET"])
def parview(status, event_id):
    if "user" in session:
        user: str = session["user"]
        return render_template("html/misc/default-home.html", header=f"Hello {user}!")
    status_pars = cf.get_all_participants(event_id, status)
    event_name = cf.get_event_details(event_id)["event_name"]
    return render_template("html/coordinator/view-participants.html", status=status, event_id=event_id, status_pars = status_pars, event_name = event_name)


@jean_blueprint.route("/participantview", methods=["POST"])
#Note, decided to take status arameter out here, may end up putting it back
def save_participant_details():
    event_id = request.form.get("event_id")
    for user_id in request.form.getlist("user_id"):
        new_validity = str(request.form.get(f"status_{user_id}")).upper()

        print(f"New Validity: {new_validity}")
        cf.save_participant_status(event_id = event_id, user_id = user_id, new_validity = new_validity)
    cf.delete_rejected_participants(event_id = event_id)

    return redirect(url_for('jean_blueprint.cohome', club_id= club_id))






#---------------------------------------end of participant stuff-----------------------------------

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
@jean_blueprint.route("/new-event", methods=["POST"])



@jean_blueprint.route("/edit-event/<int:event_id>")
def edit_event(event_id):
    if "user" in session:
        user: str = session["user"]
        return render_template("html/misc/default-home.html", header=f"Hello {user}!")
    event_details = cf.get_event_details(event_id)
    return render_template("html/coordinator/single-event-view.html",  event_name = event_details["event_name"], event_date=event_details["date_and_time"],
                            event_location=event_details["venue"], event_description=event_details["event_description"],)


@jean_blueprint.route("/edit-event", methods=["POST"])




#---------------------------------------end of single event--------------------------------------------------
#TODO fix build error
# --------------End of Pages functions-----------------

