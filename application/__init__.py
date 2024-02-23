﻿from typing import Optional
from logging import DEBUG
from sqlite3 import Connection
from os.path import exists
from colorama import Fore

from flask import Flask, g

from .blueprints import register_all_blueprints
from .util.db_functions import get_db, DB_PATH
from .util import get_boolean_input

app: Flask = Flask(__name__, template_folder="templates", static_folder="static")
app.config.from_prefixed_env()
app.logger.setLevel(DEBUG)

register_all_blueprints(app)


def initialise_db(*, populate: Optional[bool] = None) -> None:
    """
    Initialises the database with the 'schema.sql' script.

    This function is only intended to be called once, to create the actual database file.

    Optional Keyword Arguments:
        :param populate: If true, populates the database with the 'populate.sql' script.
    """

    with app.app_context():
        db: Connection = get_db()

        with app.open_resource("database/schema.sql", "r") as file:
            db.cursor().executescript(file.read())

        if populate:
            with app.open_resource("database/populate.sql", "r") as file:
                db.cursor().executescript(file.read())

        db.commit()


def db_prompt() -> None:
    """
    If the database does not exist, asks the user whether or not to populate it,
    then creates it.
    """

    if exists(DB_PATH):
        return None

    print(
        f"{Fore.LIGHTYELLOW_EX}~=~=~=~=~=~=~ {Fore.RESET}"
        f"{Fore.LIGHTBLUE_EX}Welcome to our ClubHub application! {Fore.RESET}"
        f"{Fore.LIGHTYELLOW_EX}~=~=~=~=~=~=~{Fore.RESET}\n"
    )

    print("Would you like to populate the database with sample data?")

    populate: bool = get_boolean_input(prompt="(yes/no) > ")
    print()

    print(f"{Fore.LIGHTGREEN_EX}✔{Fore.RESET} Successfully created database "
          f"{'with sample data' if populate else ''}\n"
    )

    initialise_db(populate=populate)


@app.teardown_appcontext
def close_connection(_exception) -> None:
    """
    Closes the database connection.
    This function is invoked automatically.
    """

    db: Connection = getattr(g, "_database", None)

    if db is not None:
        db.close()
