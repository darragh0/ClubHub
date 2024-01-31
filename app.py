from flask import (
    Flask,
    render_template,
    request
)

from modules.user_auth import password_match

app: Flask = Flask(__name__)
users: dict[str, str] = {
    "admin": "243262243132246f6b3835716e6a55446e50304c51675833624962347561566a53646855676179725a61777937706f726d4b73466d6f715975687a75"
}


@app.route("/")
@app.route("/index")
@app.route("/home")
def home() -> str:
    return render_template("index.html")


@app.route("/login")
def login_home() -> str:
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login() -> str:
    username: str = request.form["username"]
    password: str = request.form["password"]
    hashed_pw: str | None = users.get(username)

    if hashed_pw is None:
        app.logger.warning(f"Login fail: {username!r} does not exist")
        return render_template("login.html")

    if not password_match(password, hashed_pw):
        app.logger.info(f"Login fail: Incorrect password for user {username!r}")
        return render_template("login.html")

    app.logger.info(f"Login success: {username!r}")
    return render_template("index.html")


if __name__ == '__main__':
    app.run()






