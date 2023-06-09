from random import randint

from faker import Faker
from sqlalchemy.orm import Session

from src.database.db import SessionLocal
from src.database.models import Contact, User
from src.schemas import ContactModel, UserModel

fake = Faker('uk_UA')
database = SessionLocal()


def create_contacts(data: ContactModel, db: Session = database):
    """
    The create_contacts function creates a new contact in the database.
        Args:
            data (ContactModel): The contact to be created.
            db (Session, optional): A database session object. Defaults to None.

    :param data: ContactModel: Pass in the contact data to be added to the database
    :param db: Session: Pass the database session to the function
    :return: The contact that was created
    """
    contact = Contact(**data.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def create_users(data: UserModel, db: Session = database):
    """
    The create_users function creates a new user in the database.
        Args:
            data (UserModel): The UserModel object to be created.
            db (Session, optional): SQLAlchemy Session instance. Defaults to database.

    :param data: UserModel: Specify the type of data that will be passed to the function
    :param db: Session: Pass a database session to the function
    :return: The user object
    """
    user = User(**data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)


if __name__ == '__main__':
    for _ in range(100):
        random_contact = ContactModel(
            name=fake.first_name(),
            surname=fake.last_name(),
            email=fake.email(),
            phone=fake.phone_number(),
            birthday=fake.date(),
            description=fake.text(),
            user_id=randint(1, 20)
        )
        create_contacts(data=random_contact, db=database)

    for _ in range(20):
        random_user = UserModel(
            username=fake.first_name(),
            email=fake.email(),
            password=fake.password(),
        )
