import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel
from src.repository.users import (
    create_user,
    confirmed_email,
    get_user_by_email,
    get_user_by_username,
    update_avatar,
    update_token
)


class TestUser(unittest.IsolatedAsyncioTestCase):

    def SetUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.body = UserModel(
            username="Serhii",
            email="sspod@ukr.net",
            password="0987654321"
        )

    async def test_create_user(self):
        body = self.body
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)
        self.assertTrue(hasattr(result, 'id'))

    async def test_confirmed_email(self):
        await create_user(body=self.body, db=self.session)
        await confirmed_email(email=self.body.email, db=self.session)
        result = await get_user_by_email(email=self.body.email, db=self.session)
        self.assertEqual(result.confirmed, True)
