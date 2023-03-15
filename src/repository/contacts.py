from datetime import datetime, timedelta

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(user: User, db: Session):
    """
    The get_contacts function returns a list of contacts for the user with the given id.


    :param user: User: Get the user from the database
    :param db: Session: Access the database
    :return: A list of contacts for the specified user
    """
    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    return contacts


async def get_contact(contact_id: int, user: User, db: Session):
    """
    The get_contact function takes in a contact_id and user, and returns the contact with that id.
        Args:
            contact_id (int): The id of the desired Contact object.
            user (User): The User object associated with this request.

    :param contact_id: int: Get the contact with that id from the database
    :param user: User: Check if the user is authorized to access the contact
    :param db: Session: Pass the database session to the function
    :return: A contact object
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    return contact


async def create_contact(body: ContactModel, user: User, db: Session):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactModel: Specify the type of data that is expected to be passed into the function
    :param user: User: Get the user_id from the user object
    :param db: Session: Access the database
    :return: The created contact
    """
    contact = Contact(**body.dict(), user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(body: ContactModel, contact_id: int, user: User, db: Session):
    """
    The update_contact function updates a contact in the database.
        Args:
            body (ContactModel): The updated contact information.
            contact_id (int): The id of the contact to update.
            user (User): The current user, used for authorization purposes.

    :param body: ContactModel: Pass the contact information to the function
    :param contact_id: int: Identify the contact that is to be deleted
    :param user: User: Get the user from the database
    :param db: Session: Access the database
    :return: The updated contact
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.description = body.description
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session):
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            user (User): The user who is removing the contact. This is used to ensure that only contacts belonging to this
                user are deleted, and not contacts belonging to other users with similar IDs.

    :param contact_id: int: Identify the contact to be removed
    :param user: User: Get the user_id from the database
    :param db: Session: Pass the database session to the function
    :return: The contact that was removed
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def searcher(field: str, db: Session):
    """
    The searcher function takes a string and a database session as arguments.
    It then searches the database for contacts that have the string in their name, surname, email or phone number.
    The function returns a list of all contacts found.

    :param field: str: Specify the field that we want to search for
    :param db: Session: Connect to the database
    :return: A list of contacts that match the search field
    """
    contact_list = []
    contacts_all = db.query(Contact).all()
    for contact in contacts_all:
        if field.lower() in contact.name.lower() and contact not in contact_list:
            contact_list.append(contact)
        if field.lower() in contact.surname.lower() and contact not in contact_list:
            contact_list.append(contact)
        if field.lower() in contact.email.lower() and contact not in contact_list:
            contact_list.append(contact)
        if field.lower() in contact.phone and contact not in contact_list:
            contact_list.append(contact)

    return contact_list


async def birthday_list(db: Session):
    """
    The birthday_list function returns a list of contacts whose birthday is within the next 7 days.
        The function takes in a database session and queries all contacts from the database.
        It then iterates through each contact, replacing their birth year with the current year,
        and subtracting that date from today's date to get a timedelta object. If that timedelta object
        is between -7 days and 0 days (i.e., if it's less than 0 but greater than -7), then we know their birthday
        falls within this week.

    :param db: Session: Pass the database session to the function
    :return: A list of contacts whose birthday is in the next week
    """
    contacts_list = []
    dt_now = datetime.now()
    now_year = datetime.now().strftime('%Y')
    contacts = db.query(Contact).all()
    for contact in contacts:
        delta = contact.birthday.replace(year=int(now_year)) - dt_now
        if timedelta(days=-1) < delta < timedelta(days=7):
            contacts_list.append(contact)
    return contacts_list
