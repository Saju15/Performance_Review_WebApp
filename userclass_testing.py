from unittest import TestCase
from unittest.mock import patch,mock_open
from UserClass import User,Accounts

class TestUserClass(TestCase):
    def setUp(self):
        self.test_account = Accounts()  # Initialize an Accounts object
        self.test_user = User("Jim", "Jones", "JimJones@hotmail.com",
                              "CleverUsername", "StrongPasswordHaha", "Team")

    def test_set_first_name(self):
        failure_value = 123
        with self.assertRaises(TypeError):
            self.test_user.set_first_name(failure_value)

    def test_set_last_name(self):
        failure_value = 123
        with self.assertRaises(TypeError):
            self.test_user.set_last_name(failure_value)

    def test_set_full_name(self):
        failure_value_one = 123
        failure_value_two = 123
        with self.assertRaises(TypeError):
            self.test_user.set_full_name(failure_value_one,failure_value_two)

    def test_set_email(self):
        failure_value = 123
        with self.assertRaises(TypeError):
            self.test_user.set_username(failure_value)

    def test_set_username(self):
        failure_value = 123
        with self.assertRaises(TypeError):
            self.test_user.set_username(failure_value)
    def test_set_password(self):
        failure_value = 123
        with self.assertRaises(TypeError):
            self.test_user.set_team(failure_value)
    def test_set_team(self):
        failure_value = 123
        with self.assertRaises(TypeError):
            self.test_user.set_team(failure_value)

    def test_login_with_invalid_username_type(self):
        failure_username = 123  # Setting the failure instance to integer
        test_password = "StrongPasswordHaha"
        with self.assertRaises(TypeError):
            self.test_user.login(failure_username, test_password)

    def test_login_with_invalid_password_type(self):
        test_username = "CleverUsername"
        failure_password = 123  # Setting the failure instance to integer
        with self.assertRaises(TypeError):
            self.test_user.login(test_username, failure_password)

    def test_add_user(self):
        with patch('builtins.open', mock_open()), patch('json.dump'):
            self.test_account.add_user(self.test_user)
            self.assertEqual(self.test_account.get_users()[-1], self.test_user)

            with self.assertRaises(TypeError):
                self.test_account.add_user("Not a user instance")

    def test_edit_user(self):
        self.test_account.add_user(self.test_user)
        with self.assertRaises(TypeError):
            self.test_user.edit_user(self, "CleverUsername", "Jim", "Jones", "JimJones@hotmail.com",
                                     "CleverUsername", "StrongPasswordHaha", "Team")
            self.test_account.add_user(self.test_user)
            with self.assertRaises(TypeError):
                self.test_user.edit_user("author", 'Jon', 'Janes', 'irrelevantemail', 'bad_username', 'badpsw',
                                         'teamtest')


