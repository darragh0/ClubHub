from flask import (
    Blueprint,
    render_template,
    session,
    flash,
    redirect,
    request,
    url_for
)
from werkzeug import Response

from ..util.database import user_exists, create_new_user
from ..util.user_auth import hash_password

registration: Blueprint = Blueprint("registration", __name__)


def validate_password(password: str) -> None | str:
    errors: list[str] = []
    error_msg_prefix: str = "Password must contain"
    error_msg: str

    lower: bool = False
    upper: bool = False
    digit: bool = False

    for char in password:
        code: int = ord(char)

        if code in range(48, 58):
            digit = True
        elif code in range(65, 91):
            upper = True
        elif code in range(97, 122):
            lower = True

    if not upper:
        errors.append("a lowercase character")
    if not lower:
        errors.append("an uppercase character")
    if not digit:
        errors.append("a digit")

    if not errors:
        return None

    if len(errors) == 1:
        error_msg = errors[0]
    elif len(errors) == 2:
        error_msg_prefix += ":"
        error_msg = f"{errors[0]} and {errors[1]}"
    else:
        error_msg_prefix += ":"
        error_msg = f"{errors[0]}, {errors[1]}, and {errors[2]}"

    return f"{error_msg_prefix} {error_msg}"


@registration.route("/register")
def register_get() -> Response | str:
    """
    Loads the registration page.
    """

    if "user" in session:
        flash("You must log out before creating a new account", category="error")
        return redirect("/profile")

    username: str = request.args.get("username", None)
    user_type: str = request.args.get("user_type", None)

    first_name: str = request.args.get("first_name", None)
    last_name: str = request.args.get("last_name", None)
    age: str = request.args.get("age", None)
    email: str = request.args.get("email", None)
    phone: str = request.args.get("phone", None)
    gender: str = request.args.get("gender", None)

    return render_template(
        template_name_or_list="html/register.html",
        username=username, user_type=user_type, first_name=first_name,
        last_name=last_name, age=age, email=email, phone=phone, gender=gender
    )


@registration.route("/register", methods=["POST"])
def register_post() -> Response:

    def map_to_none(value: str) -> str | None:
        """
        Maps a string to None if it is an empty string.
        """

        return None if not value or value is None else value

    # Required inputs
    username: str = map_to_none(request.form["register-username"])
    password: str = map_to_none(request.form["register-password"])
    confirm_password: str = map_to_none(request.form["register-confirm-password"])
    captcha_response: str = map_to_none(request.form["g-recaptcha-response"])
    user_type: str = request.form.get("register-user-type", None)

    # Non required inputs
    first_name: str = map_to_none(request.form["register-first-name"])
    last_name: str = map_to_none(request.form["register-first-name"])
    age: str = map_to_none(request.form["register-age"])
    email: str = map_to_none(request.form["register-email"])
    phone: str = map_to_none(request.form["register-phone"])
    gender: str = request.form.get("register-gender", None)

    page: Response = redirect(
        url_for(endpoint=".register_get", username=username, user_type=user_type,
                first_name=first_name, last_name=last_name, age=age, email=email,
                phone=phone, gender=gender)
    )

    if user_exists(username):
        flash(f"Sorry, the username {username!r} is taken!", category="error")
        return page

    if not captcha_response:
        flash("Please complete the CAPTCHA before form submission", category="error")
        return page

    if user_type is None:
        flash("Please select a user type for your account", category="error")
        return page

    password_error_msg: None | str = validate_password(password)

    if password_error_msg is not None:
        flash(password_error_msg, category="error")
        return page

    if confirm_password != password:
        flash("Passwords do not match", category="error")
        return page

    hashed_pw: str = hash_password(password=password)

    flash(f"Registration ticket opened. Awaiting administrator approval for: {username!r}", category="info")

    create_new_user(
        username=username, password=hashed_pw, user_type=user_type, first_name=first_name,
        last_name=last_name, age=age, email=email, phone=phone, gender=gender
    )

    return redirect("/home")


@registration.route("/privacy-policy")
def privacy_policy() -> str:
    return render_template("html/privacy-policy.html")


@registration.route("/terms-and-conditions")
def terms_and_conditions() -> str:
    return render_template("html/terms-and-conditions.html")
