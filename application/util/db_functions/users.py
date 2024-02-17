
from main import Row, Optional, query_db, modify_db


def user_exists(username: str) -> bool:
    """
    Returns True if the given username exists in the database, and
    False otherwise.

    :param username: Username to check the existence of.
    """

    return query_db(f"SELECT username FROM login WHERE username={username!r}", single=True) is not None


def last_user_id() -> Row | None:
    """
    Fetches and returns the id of the last user in the database if present,
    and None otherwise.
    """

    return query_db("SELECT user_id FROM login ORDER BY user_id DESC LIMIT 1", single=True)


def create_user(
        *,
        username: str,
        password: str,
        user_type: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        age: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        gender: Optional[str] = None,
        club_name: Optional[str] = None,
        club_description: Optional[str] = None) -> bool:
    """
    Creates a new user in the database.
    ID is automatically generated. Users are not approved by default.

    :return: True if user is the first on the system, False otherwise.
    """

    # TODO: Club name / description

    age: int | None = int(age) if age is not None else None

    last_user: Row | None = last_user_id()
    user_id: int
    approved: str

    if last_user is None:
        user_id = 1
        user_type = "ADMINISTRATOR"
        approved = "APPROVED"  # Override approval if registration is the first on the system
    else:
        user_id = last_user["user_id"] + 1
        user_type = user_type
        approved = "PENDING"

    modify_db(
        """
        INSERT INTO users 
        (user_id, first_name, last_name, age, email, phone, gender, password, user_type, approved) VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
        user_id, first_name, last_name, age, email, phone, gender, password, user_type, approved
    )

    modify_db(
        """
        INSERT INTO login
        (user_id, username) VALUES
        (?, ?)
        """,
        user_id, username
    )

    if user_type == "ADMINISTRATOR":
        return True

    return False


def get_users_info(
        *,
        user_type: Optional[str] = None,
        unapproved: Optional[bool] = None,
        admin_permission: Optional[bool] = None) -> list[Row] | None:
    """
    Returns a list containing the rows from the users table, if there are any.

    Optional Keyword arguments:
        :param user_type: Should be either "STUDENT", "COORDINATOR", "ADMIN", or None (for all users).
        :param unapproved: Only includes unapproved users.
        :param admin_permission: If true, also includes username in results.
    """

    user_results: list[Row] | None
    login_results: list[Row] | None
    condition: str

    if user_type is None:
        if unapproved:
            condition = "WHERE users.approved='PENDING'"
        else:
            condition = ";"

        if admin_permission:
            user_results = query_db(f"""
                SELECT *
                FROM users
                FULL OUTER JOIN login
                ON users.user_id = login.user_id
                {condition}
            """)
        else:
            user_results = query_db("SELECT * FROM users")
    else:
        join_type: str

        if unapproved:
            condition = " AND users.approved='PENDING';"
        else:
            condition = ";"

        if admin_permission:
            join_type = "FULL OUTER"
        else:
            join_type = "INNER"

        user_results = query_db(f"""
            SELECT *
            FROM users
            {join_type} JOIN login 
            ON users.user_id = login.user_id
            WHERE users.user_type={user_type!r}
            {condition}
        """)

    if user_results is None:
        return None

    return user_results


def get_username_match(username: str) -> Row | None:
    return query_db(f"""
        SELECT * 
        FROM users 
        FULL OUTER JOIN login 
        ON users.user_id = login.user_id
        WHERE login.username={username!r}
    """, single=True)


def get_user_info(user_id: int) -> Row | None:
    return query_db(f"SELECT * FROM users WHERE user_id={user_id}", single=True)


def update_user_info(
        user_id: int,
        *,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        age: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        gender: Optional[str] = None) -> None:

    age: int | None = int(age) if age is not None else None

    modify_db(
        """
        UPDATE users set
        first_name=?,
        last_name=?,
        age=?,
        email=?,
        phone=?,
        gender=?
        WHERE user_id=?;
        """,
        first_name, last_name, age, email, phone, gender, user_id
    )


def approve_user(user_id: int) -> None:
    modify_db(
        """
        UPDATE users set
        approved='APPROVED'
        WHERE user_id=?;
        """,
        user_id
    )


def delete_user(*, username: Optional[str] = None, user_id: Optional[int] = None) -> None:  # noqa
    """
    Deletes a user, specified by either their username or user id, from the users table.

    Keyword Arguments:
        :param username: User's username. If this is given, their id cannot be.
        :param user_id: User's id. Likewise, if this is given, their username cannot be.

    Exactly of the above keyword arguments must be provided.
    """

    raise NotImplementedError()
