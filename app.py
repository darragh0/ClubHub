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


app: Flask = Flask(__name__)
app.config.from_prefixed_env()  # Load environment variables (from .env and .flaskenv)


# Temporary user dictionary with usernames/passwords for login system.
users: dict[str, str] = {
    "admin": "243262243132246f6b3835716e6a55446e50304c51675833624962347561"
             "566a53646855676179725a61777937706f726d4b73466d6f715975687a75"
}


@app.route("/")
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






