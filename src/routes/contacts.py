from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.repository import contacts as repository_contacts
from src.schemas import ContactModel, ContactResponse
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=['contacts'])


# Create contact
@router.post(
    '/create',
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
    description='5 requests per minute limit'
)
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.
        The function takes a ContactModel object as input, which is validated by pydantic.
        The function also takes an optional db Session object and current_user User object as inputs,
            both of which are provided by dependency injection via FastAPI's Depends decorator.

    :param body: ContactModel: Get the data from the request body
    :param db: Session: Get the database session
    :param current_user: User: Get the user from the database
    :return: The contact that was created
    """
    contact = await repository_contacts.create_contact(body, current_user, db)
    return contact


# Get all contacts
@router.get(
    '/all',
    response_model=List[ContactResponse],
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
    description='5 requests per minute limit'
)
async def get_contacts(db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contacts function returns a list of contacts for the current user.

    :param db: Session: Get the database session
    :param current_user: User: Get the current user
    :return: A list of contacts
    """
    contacts = await repository_contacts.get_contacts(current_user, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    return contacts


# Get contact by id
@router.get(
    '/{contact_id}',
    response_model=ContactResponse,
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
    description='5 requests per minute limit'
)
async def get_contact(contact_id: int = Path(1, ge=1), db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact function is a GET request that returns the contact with the given ID.
    The function takes in an optional contact_id parameter, which defaults to 1 if not provided.
    It also takes in a db Session object and current_user User object as parameters, both of which are injected by FastAPI's dependency injection system.

    :param contact_id: int: Specify the id of the contact to be retrieved
    :param ge: Set a minimum value for the contact_id
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the auth_service
    :return: A contact object
    """
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    return contact


# Update contact
@router.put(
    '/update/{contact_id}',
    response_model=ContactResponse,
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
    description='5 requests per minute limit'
)
async def update_contact(body: ContactModel, contact_id: int = Path(1, ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        The function takes an id, body and db as parameters.
        It returns the updated contact if successful.

    :param body: ContactModel: Get the data from the request body
    :param contact_id: int: Get the contact id from the url
    :param ge: Specify that the contact_id must be greater than or equal to 1
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the auth_service
    :return: The updated contact
    """
    contact = await repository_contacts.update_contact(body, contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not Found')
    return contact


# Delete contact
@router.delete(
    '/delete/{contact_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
    description='5 requests per minute limit'
)
async def remove_contact(contact_id: int = Path(1, ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_contact function removes a contact from the database.
        The function takes in an integer representing the id of the contact to be removed,
        and returns a dictionary containing information about that contact.

    :param contact_id: int: Specify the contact id of the contact to be updated
    :param ge: Specify that the parameter must be greater than or equal to 1
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the database
    :return: The removed contact
    """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


# Search contact by fields
@router.get('/search{part_to_search}', response_model=List[ContactResponse])
async def searcher(field: str = Path(min_length=2, max_length=20), db: Session = Depends(get_db)):
    """
    The searcher function searches for contacts in the database.
        It takes a field as an argument and returns all contacts that match the field.

    :param field: str: Search for a contact in the database
    :param max_length: Limit the length of the field
    :param db: Session: Get the database session
    :return: A list of contacts that match the search criteria
    """
    contacts = await repository_contacts.searcher(field, db)
    if len(contacts) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contacts


# Bday contacts
@router.get('/bday', response_model=List[ContactResponse])
async def birthday_list(db: Session = Depends(get_db)):
    """
    The birthday_list function returns a list of contacts with birthdays in the current month.

    :param db: Session: Get the database session
    :return: A list of contacts with a birthday today
    """
    contact = await repository_contacts.birthday_list(db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact
