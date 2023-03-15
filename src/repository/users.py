from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def create_user(body: UserModel, db: Session) -> User:
    """
    The create_user function creates a new user in the database.
        Args:
            body (UserModel): The UserModel object containing the data to be inserted into the database.
            db (Session): The SQLAlchemy Session object used to interact with our PostgreSQL database.

    :param body: UserModel: Get the data from the request body
    :param db: Session: Access the database
    :return: A user object
    """
    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function takes in an email and a database session,
    and sets the confirmed field of the user with that email to True.


    :param email: str: Pass in the email address of the user
    :param db: Session: Pass in the database session
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def get_user_by_email(email: str, db: Session) -> User:
    """
    The get_user_by_email function takes in an email and a database session,
    and returns the user associated with that email. If no such user exists,
    it will return None.

    :param email: str: Pass in the email of the user that we want to get from our database
    :param db: Session: Pass in the database session
    :return: The first user in the database with a matching email address
    """
    return db.query(User).filter(User.email == email).first()


async def get_user_by_username(username: str, db: Session) -> User:
    """
    The get_user_by_username function takes a username and returns the user with that username.

    :param username: str: Specify the type of data that will be passed into the function
    :param db: Session: Pass in the database session
    :return: The first user with the given username
    """
    return db.query(User).filter(User.username == username).first()


async def update_avatar(email, url: str, db: Session) -> User:
    """
    The update_avatar function updates the avatar of a user.

    :param email: Find the user in the database
    :param url: str: Tell the function that it will be receiving a string
    :param db: Session: Pass in the database session
    :return: The updated user object
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    The update_token function updates the refresh token for a user.

    :param user: User: Get the user's id, which is used to find the user in the database
    :param token: str | None: Specify that the token parameter can be either a string or none
    :param db: Session: Pass the database session to the function
    :return: Nothing
    """
    user.refresh_token = token
    db.commit()
