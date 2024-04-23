import json
import datetime

"""
Reviews implementation including persistent storage solution.

Classes:
    Review - the review object
    ReviewItem - an individual review element with relevant attributes.
"""


class Review:
    """Review consisting of review items and related methods

    Also contains persistent store methods - JSON.

    Attributes:
        published (list): list of published review items
        drafted (list): list of drafted review items
        reviews (list): list of review items
    """

    def __init__(self):
        self._published = []
        self._drafted = []
        self.reviews = []
        self.topic_manager = Topic(self._published)

        try:
            with open('reviews.json', 'r') as file:
                self.reviews = json.load(file)

            published_reviews = [review for review in self.reviews if review.get('is_published')]
            drafted_reviews = [review for review in self.reviews if not review.get('is_published')]

            for review in published_reviews:
                self._published.append(
                    ReviewItem(topic=review["topic"], content=review["content"], author=review["author"],
                               assignee=review["assignee"], rating=review["rating"],
                               is_published=review["is_published"], is_anonymous=review["is_anonymous"],
                               reactions=review["reactions"], date=review.get("date")))

            for review in drafted_reviews:
                self._drafted.append(
                    ReviewItem(topic=review["topic"], content=review["content"], author=review["author"],
                               assignee=review["assignee"], rating=review["rating"],
                               is_published=review["is_published"], is_anonymous=review["is_anonymous"],
                               reactions=review["reactions"], date=review.get("date")))

        except FileNotFoundError:
            print(f"The file does not exist.")

    def view_published(self):
        """
        Retrieve and return all published reviews from a JSON file.

        :return: list
            A list of dictionaries where each dictionary contains data of a published review.
        """
        return [review.__dict__ for review in self._published]

    def view_drafts(self, username):
        """
        Retrieve and return all unpublished reviews from a JSON file.

        :param username: str
            returns username of user currently in session

        :return: list
            A list of dictionaries where each dictionary contains data of  unpublished review of the user.
        """
        return [review.__dict__ for review in self._drafted if review.author == username]

    def delete_review(self, review, file_path='reviews.json'):

        """
        :param review: review object
            The  review item being deleted from reviews.json

        :param file_path: str, optional
            The path to the JSON file containing the reviews. Defaults to 'review.json'.

        :return:
            returns none if a review item is not passed, 'Review not found.' if review was not found, 'Review
            deleted successfully.' if review was deleted, and 'Could not delete review.' if review could not be deleted.

        :raises:
            TypeError if the review parameter is not a review item.
        """

        if not isinstance(review, ReviewItem):
            raise TypeError("Not a review item")

        with open(file_path, 'r') as file:
            reviews = json.load(file)
            if review not in reviews:
                return "Review not found."
            reviews.remove(review)
        with open(file_path, 'w') as filew:
            if review not in reviews:
                json.dump(reviews, filew, indent=2)
                return "Review deleted successfully."
        # Update topics
        if review:
            remaining_reviews = [r for r in self.reviews if r['topic'] == review.topic]
            if not remaining_reviews:
                self.topic_manager.remove_topic(review.topic)

    def add_review(self, review=None):
        """
        Adds a review into the persistent storage

        Adds a review into the draft list or the published list, and then writes to the
        JSON file reviews.json

        :param review: review object
            The new review item being added to reviews.json

        :return:
            returns only if a review item is not passed

        :raises:
            TypeError if the review parameter is not a review item
        """
        if not isinstance(review, ReviewItem):
            raise TypeError("Not a review item")
        if review.is_published:
            self._published.append(review)
        else:
            self._drafted.append(review)
        try:
            self.reviews.append(review.__dict__)
            with open('reviews.json', 'w') as file:
                json.dump(self.reviews, file, indent=2)
        except FileNotFoundError:
            print(f"The file does not exist.")
        # Update topics
        if review and review.topic not in self.topic_manager.topics:
            self.topic_manager.add_topic(review.topic)

    @staticmethod
    def print_reviews(reviews):
        """
        Print specific fields (date, topic, content, author) of each review.

        :param reviews: list
            A list of review dictionaries to print.
        """
        for review in reviews:
            date = review.get('date')
            topic = review.get('topic')
            content = review.get('content')
            author = review.get('author')

            print(f"Date: {date}")
            print(f"Topic: {topic}")
            print(f"Content: {content}")
            print(f"Author: {author}")
            print("-" * 40)

    @staticmethod
    def search(search_content: str, category=None, file_path='reviews.json'):
        """
        Retrieve and return all reviews that match the search parameters.

        This method reads the JSON file containing reviews and returns a set of reviews that match the strings
        in search_content.

        :param search_content: str
            The text that must match the review(s) being searched for.

        :param category: str, optional
            The category to sort the search results by. Defaults to None, which means no sorting.

        :param file_path: str, optional
            The path to the JSON file containing the reviews. Defaults to 'review.json'.

        :return: set
            A set of reviews that were found.
        """
        found = []
        # while '' in search_content:
        #    search_content.remove('')
        """
        if not search_content:
            raise TypeError("Empty search.")
        """
        with open(file_path, 'r') as file:
            reviews = json.load(file)
            for i in reviews:
                for content in search_content.split():
                    if (content.lower() in i['author'].lower() or content.lower() in i['topic'].lower() or
                    content.lower() in i['content'].lower()) and i['is_published']:
                        if i not in found:
                            found.append(i)
            if not found:
                return []
            if category is not None:
                found = Review.search_sort(category, reviews=found)
            return found

    @staticmethod
    def find_user_reviews(user, file_path="reviews.json"):
        """
        Retrieve and return all reviews of a specific user.

        This method reads the JSON file containing reviews and returns a set of reviews that whose author matches the user
        parameter.

        :param user: str
            The author's name that must match the review(s) being searched for.

        :param file_path: str, optional
            The path to the JSON file containing the reviews. Defaults to 'review.json'.

        :return: set
            A set of reviews that were found.
        """
        user_reviews = []
        with open(file_path, 'r') as file:
            reviews = json.load(file)
            for i in reviews:
                if i['author'].lower() == user.lower() and i['is_published']:
                    user_reviews.append(i)
            return user_reviews

    @staticmethod
    def search_sort(category, reviews=None, file_path='reviews.json'):
        """
        Sort reviews and return list of sorted reviews

        :param category: str
            The category to sort reviews by.

        :param reviews: list, optional
                The list of reviews to sort. Defaults to None, which means all reviews would be sorted.

        :param file_path: str, optional
            The path to the JSON file containing the reviews. Defaults to 'review.json'.

        :return: set
            A set of reviews that were found.
        """
        if reviews is None:
            with open(file_path, 'r') as file:
                reviews = json.load(file)
                for i in reviews:
                    if not i['is_published']:
                        reviews.remove(i)

        if category == 'Newest':
            reviews.sort(key=lambda d: d['date'], reverse=True)
        elif category == 'Oldest':
            reviews.sort(key=lambda d: d['date'])
        elif category == 'A-Z':
            reviews.sort(key=lambda d: d['author'])
        """
        elif category == 'author_descending':
            reviews.sort(key=lambda d: d['author'], reverse=True)
        elif category == 'topic':
            reviews.sort(key=lambda d: d['topic'])
        elif category == 'topic_descending':
            reviews.sort(key=lambda d: d['topic'], reverse=True)
        """
        return reviews


class ReviewItem:
    """Individual ReviewItem for the Review object

    Attributes:
         date (date) : The published date
         topic(str) : Topic of the review item
         content(str) : Content of the review
         author(User) : User of the review
         reactions(list): List of reactions
         is_published(bool) : Boolean value to indicate if the review is published or not
         is_anonymous(bool) : Boolean value to indicate if the review is anonymous or not
         reactions(dict) : Preset to None, initialized to dict

    """

    def __init__(self, topic, content, author, assignee, rating, is_published, is_anonymous, date=None, reactions=None):
        self.date = date if date else str(datetime.datetime.now())
        self.topic = topic
        self.content = content
        self.author = author
        self.assignee = assignee
        self.rating = rating
        self.reactions = reactions if reactions is not None else {"happy": 0, "confused": 0, "sad": 0, "thumbsup": 0, "thumbsdown": 0}
        self.is_published = is_published
        self.is_anonymous = is_anonymous

    def react(self, reaction):
        """
        Add an emoji reaction to a post.
        This function also updates the count of each emoji used.

        :param reaction: str
            Code of the emoji

        :return: none
        """
        if reaction not in self.reactions:
            raise TypeError("Emoji does not exist")
        self.reactions[reaction] += 1


class Topic:
    """
    Class to handle topics of reviews.

    Attributes:
        reviews (list): Reference to the list of reviews or Review object.
        topics (list): A list of unique topics from reviews.
        topics_file (str): Path to the JSON file where topics are stored.
    """

    def __init__(self, reviews, topics_file='topics.json'):
        self.reviews = reviews
        self.topics_file = topics_file
        self.topics = self.load_topics()

    def get_topics(self):
        """
       Returns a list of topics
        :return: list
        """
        return self.topics

    def load_topics(self):
        """
        Load and return unique topics from the topics JSON file.

        :return: list
            A list of unique topics.
        """
        try:
            with open(self.topics_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"The file {self.topics_file} does not exist.")
            return []

    def save_topics(self):
        """
        Save the topics list to the topics JSON file.
        """
        with open(self.topics_file, 'w') as file:
            json.dump(self.topics, file)

    def get_reviews_by_topic(self, topic):
        """
        Returns a list of ReviewItem objects for the given topic.

        :param topic: str
            The topic for which to retrieve reviews.

        :return: list
            A list of ReviewItem objects that match the given topic.
        """
        return [review for review in self.reviews if review["topic"] == topic]

    def add_topic(self, new_topic):
        """
        Add a new topic to the topics list and save it.

        :param new_topic: str
            The new topic to be added.
        """
        if new_topic not in self.topics:
            self.topics.append(new_topic)
            self.save_topics()

    def remove_topic(self, topic):
        """
        Remove a topic from the topics list and save the change.

        :param topic: str
            The topic to be removed.
        """
        if topic in self.topics:
            self.topics.remove(topic)
            self.save_topics()
