import json


class Accounts:
    """
    Account consisting of user methods and related methods

    Also contains persistent store methods - JSON.

    Attributes:
        user (list): list of user items
        userdicts (list): list of user items as a dictionary
    """

    def __init__(self):
        self._users = []
        self._userdicts = []
        try:
            with open('users.json', 'r') as file:
                self._userdicts = json.load(file)

            for user in self._userdicts:
                self._users.append(User(user["first_name"], user["last_name"], user["email"], user["username"],
                                        user["password"], user["team"]))

        except FileNotFoundError:
            print(f"The file does not exist.")

    def add_user(self, user):
        """
        This function adds a review into the persistent storage
        Arguments:
            Takes a user parameter, a user class item.
        Returns:
            This function returns only if an incorrect item is passed in the function
        Raises:
            This function raises a TypeError if the name is not a review item.
        """
        if not isinstance(user, User):
            raise TypeError("Not a user item")
            return
        self._users.append(user)
        try:
            self._userdicts.append(user.__dict__)
            with open('users.json', 'w') as file:
                json.dump(self._userdicts, file, indent=2)
        except FileNotFoundError:
            print(f"The file does not exist.")

    def get_users(self):
        """
        This function returns the list of users
        Arguments:
            Takes no parameters
        Returns:
            This function returns a list of user items
        Raises:
            This function does not raise any errors
        """
        return self._users

    def view_user(self, user):
        """
        This function returns a dictionary values of a certain user
        Arguments:
            user: the account the dictionary is wanted for
        Returns:
            This function returns a dictionary for the user
        Raises:
            This function does not raise any errors
        """
        for account in self._userdicts:
            if account['username'] == user:
                return account

    def find_user(self, username):
        """
        This function finds if a user attempting to sign in exists
        Arguments:
            Asks for parameter username, the string 'username' submitted by the user attempting to sign in
        Returns:
            This function returns a user item if found, none otherwise
        Raises:
            This function does not raise any errors
        """
        for user in self._users:
            if username == user.get_username():
                return user
        return None


class User:

    def __init__(self, first_name, last_name, email, username, password, team):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = password
        self.full_name = self.first_name + " " + self.last_name
        self.team = team

    def edit_review(self, topic, content, file_path='reviews.json'):
        """
        This edits a user's unpublished review.
        Returns:
             This function returns the user's review.
        Arguments:
            This function takes the self keyword, topic, content, and file_path with 'reviews.json' as a default argument as arguments.
        Raises:
            This function raises an exception if the review is not found.
        """

        with open(file_path, 'r+') as file:
            reviews = json.load(file)
        for i in reviews:
            if i['author'] == self.full_name and i['topic'] == topic and i['is_published'] == False:
                i['content'] = content

                with open('reviews.json', 'w') as file:
                    json.dump(reviews, file, indent=2)
                return i

        raise Exception("Review not found.")

    def get_first_name(self):
        """
        This function returns the user's first name.
        Returns:
             This function returns the user's first name.
        Arguments:
            This function only takes the self keyword as an argument.
        Raises:
            This function does not raise any errors.
        """

        return self.first_name

    def set_first_name(self, first_name):
        """
        This function sets the first_name variable to a new first name.
        Returns:
            This function does not return anything.
        Arguments:
            This function takes a string called first_name as an argument.
        Raises:
            This function raises a TypeError if it is not a string.
        """
        if isinstance(first_name, str):
            self.first_name = first_name
        else:
            raise TypeError("You have entered a value that is not a string.")

    def get_last_name(self):
        """
        This function returns the user's last_name
        Arguments:
            This functon takes no arguments, only the self keyword.
        Returns:
            This function returns the user attribute of self.last_name
        Raises:
            This function raises a TypeError if the name is not a string.
        """
        if isinstance(self.last_name, str):
            return self.last_name
        else:
            raise TypeError("The last name provided is of an invalid datatype. Names must be strings.")

    def set_last_name(self, last_name):
        """
        THis function sets the self.last_name to a string argument called last_name.
        Arguments:
            This function takes a string last_name as its argument.
        Returns:
            This function odes not return any values.
        Raises:
            This function raises a TypeError if the last_name variable is not a string.
        """
        if isinstance(last_name, str):
            self.last_name = last_name
        else:
            raise TypeError("The last name provided is of an invalid datatype. Names must be strings.")

    def get_full_name(self):
        """
        This function returns the user's last_name
        Arguments:
            This functon takes no arguments, only the self keyword.
        Returns:
            This function returns the user attribute of self.full_name
        Raises:
            This function raises a TypeError if the name is not a string.
        """
        if isinstance(self.full_name, str):
            return self.full_name
        else:
            raise TypeError("The full name is not a string. Names must be strings.")

    def set_full_name(self, first_name, last_name):
        """
        This function returns the user's last_name
        Arguments:
            This functon takes no arguments, only the self keyword.
        Returns:
            This function returns the user attribute of self.full_name
        Raises:
            This function raises a TypeError if the name is not a string.
        """
        if isinstance(first_name, str) and isinstance(last_name, str):
            self.full_name = first_name + " " + last_name
        else:
            raise TypeError("The first_name or last_name variable is not a string. Names must be strings.")

    def get_username(self):
        """
        This function gets the username of the user object
        Arguments:
            This function takes no arguments
        Returns:
            This function returns self.username.
        Raises:
            Does not raise any errors
        """
        return self.username

    def set_username(self, new_username):
        """
        This function allows the user to set a new username
        Arguments:
            This function takes a string variable (new_username) as an argument
        Returns:
            This function does not return a value.
        Raises:
            Raises a TypeError if the username is not a string.
        """
        if isinstance(new_username, str):
            self.username = new_username
        else:
            raise TypeError("The provided username is not a string. Usernames must be strings.")

    def get_password(self):
        """
        This function gets the password of the user object
        Arguments:
            This function takes no arguments
        Returns:
            This function returns self.password.
        Raises:
            Does not raise any errors
        """
        return self.password

    def set_password(self, new_password):
        # Must be altered to make sure that length and character inclusion is appropriate
        """
        This function allows the user to set a new pasword.
        Arguments:
            This function takes a string variable (new_password) as an argument
        Returns:
            This function does not return a value.
        Raises:
            In the future implementation, this function will act more like an actual password authenticator.
            If the password does not meet the predetermined standards, a custom error will be raised,
        """
        if isinstance(new_password, str):
            self.password = new_password
        else:
            raise TypeError("The provided password is not a string. Passwords must be strings.")

    def get_team(self):
        """
        This function returns the user's assigned team.
        Arguments:
            This function does not take any arguments. It only takes the self keyword.
        Returns:
            This function returns the self.team string variable.
        Raises:
            This function raises a TypeError if the self.team attribute is not a string.
        """
        if isinstance(self.team, str):
            return self.team
        else:
            raise TypeError("This team name is invalid. Team names must be strings.")

    def set_team(self, team_name):
        """
        This function sets the self.team variable to a new string variable called team_name.
        Arguments:
            This function takes a string argument called team_name.
        Returns:
            This function does not return any values.
        Raises:
            THis function raises a TypeError if the value is not a string.
        """
        if isinstance(team_name, str):
            self.team = team_name
        else:
            raise TypeError("The provided team name of an invalid type. Team names must be a string.")

    def login(self, username, password):
        """
        This function allows the user to log into their account on the webpage.
        Arguments:
            This function takes two strings, username and password as arguments.
        Returns:
            This function does not return anything.
        Raises:
            This function raises a TypeError if the username or password is not a string.
            This function also raises a TypeError if the username does not equal self.username
            or if password does not equal self.password.
        """
        if not isinstance(username, str):
            raise (TypeError("The username invalid. You must input a string as a username."))
        if not isinstance(password, str):
            raise (TypeError("The password is invalid. You must input a string as a password."))
        if not username.equals(self.username):
            raise TypeError("The username does not match your recorded username.")
        if not password.equals(self.password):
            raise TypeError("The password does not match your recorded password.")

    def edit_user(self, author, new_first_name, new_last_name, new_username, new_password, file_path='users.json'):
        """
       This edits a user's username.
       Returns:
           This function returns a user's new profile after editing their details.
       Arguments:
           This function takes the self keyword, author for authentication, a new first name, last name,
           username, and password.
       Raises:
           This function raises an exception if the user does not exist.
       """

        with open(file_path, 'r+') as file:
            users = json.load(file)
        for i in users:
            if self.username == i['username']:
                user = i
                user['first_name'] = new_first_name
                user['last_name'] = new_last_name
                user['username'] = new_username
                user['password'] = new_password
                user['fullname'] = new_last_name + " " + new_last_name
                with open('users.json', 'w') as file:
                    json.dump(users, file, indent=2)
                return user

        raise Exception("User not found.")

    def get_user_reviews(self):
        """
        Retrieve and return all reviews assigned to a specific user from a JSON file.

        :return: list
            A list of dictionaries containing review items assigned to the user.
        """
        try:
            with open('reviews.json', 'r') as file:
                reviews = json.load(file)

            user_reviews = [review for review in reviews if review.get('assignee') == self.full_name]

            return user_reviews

        except FileNotFoundError:
            print(f"The file reviews.json does not exist.")
            return []

    def get_reviews_by_user(self):
        """
        Retrieve and return all reviews posted by the specific user from a JSON file.

        :return: list
            A list of dictionaries containing review items published by the user
        """
        try:
            with open('reviews.json', 'r') as file:
                reviews = json.load(file)

            user_reviews = [review for review in reviews if review.get('author') == self.username
                            and review.get('is_published') == True]

            return user_reviews

        except FileNotFoundError:
            print(f"The file reviews.json does not exist.")
            return []


def main():
    user = User("Draco", "Malfoy", "draco@hogwarts.com", "purebloodprince", "slytherin", "Slytherin")
    # print(user.edit_review("Hogwarts", "Edit Review Test"))
    # print(user.get_user_reviews())


main()
