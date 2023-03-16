import unittest
from datetime import date, timedelta, datetime
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User, Contact
from src.repository.contacts import (
    create_contact,
    get_contact,
    update_contact,
    remove_contact,
    birthday_list,
    get_contacts,
    searcher
)
from src.schemas import ContactModel, UserModel


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    def SetUp(self):
        self.session = MagicMock(spec=Session)
        self.user = UserModel(
            username='Serhii',
            email='sspod@ukr.net',
            password='0987654321'
        )
        self.contact = ContactModel(
            usernnameame='Serhii',
            surname='sspod@ukr.net',
            email='0987654321',
            phone='0631234567',
            birthday=date.today(),
        )
        self.test_contact1 = ContactModel(
            usernnameame='Jon',
            surname='Smit',
            email='Jon.smit@test.com',
            phone='0630987654',
            birthday=date.today(),
        )
        self.test_contact2 = ContactModel(
            usernnameame='lina',
            surname='Norington',
            email='Lina.Norington@test.com',
            phone='0630987653',
            birthday=date.today(),
        )
        self.test_contact3 = ContactModel(
            usernnameame='Will',
            surname='Scot',
            email='Will.scot@test.com',
            phone='0630987634',
            birthday=date.today(),
        )

    async def test_create_contact(self):
        body = self.contact
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)
        self.assertTrue(hasattr(result, "id"))

    async def test_get_contact(self):
        contact = Contact()
        self.session.query(Contact).filter.return_value.first.return_value = contact
        result = await get_contact(contact.id, self.user, self.session)
        self.assertEqual(result, contact)

    async def test_get_contacts(self):
        contacts = [Contact(user_id=1), Contact(user_id=1), Contact(user_id=1)]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts(user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_not_found(self):
        contact = Contact()
        self.session.query(Contact).filter.return_value.first.return_value = None
        result = await get_contact(contact.id, self.user, self.session)
        self.assertIsNone(result)

    async def test_update_contact(self):
        contact_id = 1
        body = self.contact
        new_body = self.test_contact1
        contact = Contact(
            id=contact_id,
            name=new_body.name,
            surname=new_body.surname,
            email=new_body.email,
            phone=new_body.phone,
            birthday=date.today(),
            )
        self.session.query(Contact).filter.return_value.first.return_value = contact
        result = await update_contact(body, contact_id, self.user, self.session)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact(self):
        contact_id = 1
        contact = Contact(id=contact_id)
        self.session.query(Contact).filter.return_value.first.return_value = contact
        result = await remove_contact(contact_id, self.user, self.session)
        self.assertEqual(result, contact)

    async def test_get_birthday_list(self):
        contacts = [Contact(birthday=datetime.now() + timedelta(days=1)),
                    Contact(birthday=datetime.now() + timedelta(days=2)),
                    Contact(birthday=datetime.now() + timedelta(days=3)),
                    Contact(birthday=datetime.now() + timedelta(days=4)),
                    Contact(birthday=datetime.now() + timedelta(days=5)),
                    Contact(birthday=datetime.now() + timedelta(days=6)),
                    Contact(birthday=datetime.now() + timedelta(days=7)),
                    Contact(birthday=datetime.now() + timedelta(days=8)),
                    Contact(birthday=datetime.now() + timedelta(days=9)),
                    Contact(birthday=datetime.now() + timedelta(days=10)),
                    ]
        self.session.query().all.return_value = contacts
        result = await birthday_list(db=self.session)
        self.assertEqual(result, contacts[0:7])

    async def test_searcher(self):
        contact1 = Contact(
            name=self.test_contact1.name,
            surname=self.test_contact1.surname,
            email=self.test_contact1.email
        )
        contact2 = Contact(
            name=self.test_contact2.name,
            surname=self.test_contact2.surname,
            email=self.test_contact2.email
        )
        contact3 = Contact(
            name=self.test_contact3.name,
            surname=self.test_contact3.surname,
            email=self.test_contact3.email
        )
        self.session.query.return_value.all.return_value = [contact1, contact2, contact3]
        results = await searcher('Will', self.session)

        assert contact1 not in results
        assert contact2 not in results
        assert contact3 in results


if __name__ == '__main__':
    unittest.main()
