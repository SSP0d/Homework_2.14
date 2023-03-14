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
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


# Search contact by fields
@router.get('/search{part_to_search}', response_model=List[ContactResponse])
async def searcher(field: str = Path(min_length=2, max_length=20), db: Session = Depends(get_db)):
    contacts = await repository_contacts.searcher(field, db)
    if len(contacts) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contacts


# Bday contacts
@router.get('/bday', response_model=List[ContactResponse])
async def birthday_list(db: Session = Depends(get_db)):
    contact = await repository_contacts.birthday_list(db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact
