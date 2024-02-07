# Third party libraries
from werkzeug import Response
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session
)

# Local modules
from modules.user_auth import password_match
from jinja2 import Environment


app: Flask = Flask(__name__)
app.config.from_prefixed_env()  # Load environment variables (from .env and .flaskenv)


# Temporary user dictionary with usernames/passwords for login system.
users: dict[str, str] = {
    "admin": "243262243132246f6b3835716e6a55446e50304c51675833624962347561"
             "566a53646855676179725a61777937706f726d4b73466d6f715975687a75"
}


@app.route("/cohome")
def cohome():
    if "user" in session:
        user: str = session["user"]
        return render_template("index.html", header=f"Hello {user}!")
    return render_template("Coordinator/coordinator_dashboard.html", coordinator_name = "John Doe", active_users = 40, pending_users = 3, club_title = "Club 1", club_description = "Description 1")

@app.route("/menview/<status>")
def parview(status):
    if "user" in session:
        user: str = session["user"]
        return render_template("index.html", header=f"Hello {user}!")
    return render_template("Coordinator/Coordinator_participant_view.html", status = status)


@app.route("/participantview/<status>")
def memview(status):
    if "user" in session:
        user: str = session["user"]
        return render_template("index.html", header=f"Hello {user}!")
    return render_template("Coordinator/view_members.html", status = status)

@app.route("/eventview/<timeline>")
def see_events(timeline):
    if "user" in session:
        user: str = session["user"]
        return render_template("index.html", header=f"Hello {user}!")
    return render_template("Coordinator/coordinators_events.html", timeline = timeline)

@app.route("/singleeventview")
def edit_event():
    if "user" in session:
        user: str = session["user"]
        return render_template("index.html", header=f"Hello {user}!")
    return render_template("Coordinator/single_event_view.html", event_name = 'Event 1', event_date = '2021-10-10', event_time = '10:00', event_location = 'Location 1', event_description = 'Description 1')

@app.route("/index")
@app.route("/home")
def home() -> str:
    """
    Loads the home (default) page.
    """

    if "user" in session:
        user: str = session["user"]
        return render_template("index.html", header=f"Hello {user}!")

    return render_template("index.html")


@app.route("/login")
def login() -> str:
    """
    Loads the login page.
    """

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post() -> str | Response:
    """
    Function called when login button (from the login page) is pressed.
    """

    username: str = request.form["username"]
    password: str = request.form["password"]

    if "user" in session:
        current_user: str = session["user"]
        app.logger.warning(f"Login fail: {current_user!r} is already logged in")
        return render_template("login.html", error_message=f"You are already logged in as {current_user!r}")

    if not username:
        app.logger.warning("Login fail: Empty username")
        return render_template("login.html", error_message="Please enter a username")

    if username not in users:
        app.logger.warning(f"Login fail: User {username!r} does not exist")
        return render_template("login.html", error_message="User not found")

    hashed_pw: str = users[username]

    if not password_match(password, hashed_pw):
        app.logger.warning(f"Login fail: Incorrect password for user {username!r}")
        return render_template("login.html", error_message="Incorrect password")

    app.logger.info(f"Login success: {username!r}")

    # Create a user session
    session["user"] = username

    return redirect("/home")


if __name__ == '__main__':
    app.run()






