import unittest
from unittest.mock import MagicMock, patch

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
        self.user = UserModel(
            username='Serhii',
            email='sspod@ukr.net',
            password='0987654321'
        )
        self.test_email = 'test_email@test.com'

    async def test_create_user(self):
        with patch.object(self.session, "add") as mock_add, \
                patch.object(self.session, "commit") as mock_commit, \
                patch.object(self.session, "refresh") as mock_refresh:
            user = create_user(self.user, self.session)
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, self.user.username)
        self.assertEqual(user.email, self.user.email)
        self.assertEqual(user.password, self.user.password)
        self.assertTrue(hasattr(user, 'id'))
        mock_add.assert_called_once_with(user)
        mock_commit.assert_called_once()
        mock_refresh.assert_called_once_with(user)

    async def test_get_user_by_email(self):
        user = User()
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email=self.user.email, db=self.session)
        self.assertEqual(result, user)

    async def test_get_user_by_email_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(email=self.test_email, db=self.session)
        self.assertIsNone(result)

    async def test_user_by_username(self):
        user = User(username=self.user.username)
        self.session.query().filter().first.return_value = user
        result = await get_user_by_username(username=self.user.username, db=self.session)
        self.assertEqual(result, user)

    async def test_user_by_username_not_found(self):
        user = User(username=self.user.username)
        self.session.query().filter().first.return_value = None
        result = await get_user_by_username(username=self.user.username, db=self.session)
        self.assertIsNone(result)

    async def test_confirmed_email(self):
        await create_user(body=self.user, db=self.session)
        await confirmed_email(email=self.user.email, db=self.session)
        result = await get_user_by_email(email=self.user.email, db=self.session)
        self.assertEqual(result.confirmed, True)

    async def test_update_avatar(self):
        user = User(email=self.user.email)
        self.session.query().filter().first.return_value = user
        result = await update_avatar(user.email, "avatar_url", self.session)
        self.assertEqual(result.avatar, user.avatar)

    async def test_update_token(self):
        self.user.refresh_token = 'old_token'
        token = 'new_token'

        with patch.object(self.session, "commit") as mock_commit:
            await update_token(self.user, token, self.session)

        self.assertEqual(self.user.refresh_token, token)
        mock_commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
