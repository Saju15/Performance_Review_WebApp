# Code Reviews

**Important Note:** 
**This is our code review from Sprint 1 which was not implemented as expected. Our code review for sprint 2 is conducted during pull requests where members presented their code and others gave their suggestions which lead to creating new ideas/ bringing issues to attention.**

Unfortunately we did not realize the SCRUM master should have been making code reviews
                    every meeting. We will be implementing this for the next sprint. This means we only
                    have a code review for our final implementation, which is not ideal.
                    As a team we went through our code for spint 1 and wrote down reviews for each component.

---

## October 20th, 2023

| Class : Review             | Reviews                                      |
|----------------------------|----------------------------------------------|
| --init--                   | Readable,Has PEP8 errors                     |
| view_published(self)       | Readable                                     |
| view_drafts(self,username) | Readable                                     |
| add_review(self,review)    | line 85 - does not need the return statement |
| print_reviews(reviews)     | test function, can be removed                |
| get_topics(filepath)       | PEP8 error                                   |
| write_review(self, review) | Stub, needs to be removed                    |

| Class : ReviewItem         | Reviews   |
|----------------------------|-----------|
| --init--                   | Readable  |

| Class : Accounts         | Reviews                                  |
|--------------------------|------------------------------------------|
| --init--                 | PEP8 errors, Docstring is not articulate |
| add_user(self,user)      | line 40 - deos not return statement      |
| get_user(self)           | Readable                                 |
| find_user(self,username) | Readable                                 |

| Class : User                             | Reviews                                                              |
|------------------------------------------|----------------------------------------------------------------------|
| --init--                                 | No docstring                                                         |
| edit_review()                            | No docstring, unused variable temp, local variable is not referenced |
| get_first_name(self)                     | PEP8 error                                                           |
| set_first_name(self, first_name)         | PEP8 error                                                           |
| get_last_name(self)                      | PEP8 error                                                           |
| set_last_name(self, last_nam             | PEP8 error                                                           |
| set_full_name(self,first_name,last_name) | PEP8 error                                                           |
| get_username(self)                       | No docstring                                                         |
| set_username(self, new_username)         | PEP8 error                                                           |
| get_password(self)                       | No docstring                                                         |
| set_password(self, new_password)         | PEP8 error, Functionality is not fully implemented                   |
| get_team(self)                           | PEP8 error, Functionality is not fully implemented                   |
| set_team(self,team_name)                 | PEP8 error                                                           |
| login(self, username, password)          | PEP8 errors, Unresolved attribute reference                          |

| Module - Server | Reviews                                                                                    |
|-----------------|--------------------------------------------------------------------------------------------|
| login('/')      | PEP8 error, Duplicated function with different url exist                                   |
| load_homepage() | Local variable 'template_data' might be referenced before assignment                       |
| load_draft()    | PEP8 error                                                                                 |
| sign_up()       | PEP8 error, Functionality is not fully implemented - doesn't check if user already exists. |
| login()         | Works as intended                                                                          |
| write_review()  | Works as intended                                                                          |
| css()           | Works as intended                                                                          |






