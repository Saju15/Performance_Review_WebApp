
from unittest import TestCase
import shutil
from review import Review, ReviewItem, Topic


class TestReview(TestCase):
    """
        Test for the Review class.

        This test class covers functionalities of the Review class, including
        initialization, viewing published reviews and drafts, deleting reviews, and searching for reviews.
        It utilizes the actual 'reviews.json' file for testing and ensures that the original data is
        preserved by backing up before tests and restoring it afterward using the shutil module.
        """
    @classmethod
    def setUpClass(cls):
        # Making a copy of the original review persistence storage
        shutil.copy('reviews.json', 'reviews_backup.json')

    @classmethod
    def tearDownClass(cls):
        # Restoring the original reviews.json file
        shutil.move('reviews_backup.json', 'reviews.json')

    def setUp(self):
        self.test_review_1 = ReviewItem('Performance Review: Test 1', 'Test1 Content...', 'brightestwitch', 'Harry Potter', '5', True, False, {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5})
        self.test_review_2 = ReviewItem('Performance Review: Test 2', 'Test2 Content...', 'brightestwitch', 'Harry Potter', '3', False, False, {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5})

        self.review = Review()

        self.review.add_review(self.test_review_1)
        self.review.add_review(self.test_review_2)

    def test_init(self):
        self.assertGreaterEqual(len(self.review._published), 1)
        self.assertGreaterEqual(len(self.review._drafted), 1)

    def test_view_published(self):
        published = self.review.view_published()
        self.assertIn(self.test_review_1.__dict__, published)

    def test_view_drafts(self):
        drafts = self.review.view_drafts('brightestwitch')
        self.assertIn(self.test_review_2.__dict__, drafts)

    def test_delete_review(self):
        self.review.delete_review(self.test_review_1)
        self.assertNotIn(self.test_review_1.__dict__, self.review._published)

    def test_search(self):
        found_reviews = self.review.search("Test1 Content")
        self.assertTrue(any(review['content'] == 'Test1 Content...' for review in found_reviews))

    # Negative test cases
    def test_delete_non_existing_review(self):
        non_existing_review = ReviewItem('Non-Existing Review', 'Non-Existing Content', 'unknown', 'Nobody', '1', False, False, {})
        delete_result = self.review.delete_review(non_existing_review)
        self.assertNotEqual(delete_result, "Review deleted successfully.")

    def test_view_drafts_for_non_existing_user(self):
        drafts = self.review.view_drafts('non_existing_user')
        self.assertEqual(len(drafts), 0)

    def test_add_invalid_review(self):
        with self.assertRaises(TypeError):
            self.review.add_review("This is not a ReviewItem object")


class TestTopic(TestCase):
    """
        Tests for the Topic class in the review module.

        This test class covers functionalities of the Topic class, including loading topics,
        adding and removing topics, and retrieving reviews by topic.
        It interacts with the 'topics.json' file and ensures data integrity by backing up and restoring
        the file using the shutil module.
        """
    @classmethod
    def setUpClass(cls):
        # Backup the original topics.json file
        shutil.copy('topics.json', 'topics_backup.json')

    @classmethod
    def tearDownClass(cls):
        # Restore the original topics.json file
        shutil.move('topics_backup.json', 'topics.json')

    def setUp(self):
        self.review = Review()
        self.topic = Topic(self.review.reviews, 'topics.json')

    def test_load_topics(self):
        topics = self.topic.load_topics()
        self.assertIsInstance(topics, list)

    def test_add_topic(self):
        new_topic = "New Test Topic"
        self.topic.add_topic(new_topic)
        self.assertIn(new_topic, self.topic.topics)

    def test_remove_topic(self):
        new_topic = "New Test Topic"
        self.topic.add_topic(new_topic)
        self.topic.remove_topic(new_topic)
        self.assertNotIn(new_topic, self.topic.topics)

    def test_get_reviews_by_topic(self):
        test_review = ReviewItem('Test Topic', 'Content...', 'Author', 'Assignee', '5', True, False, {})
        self.review.add_review(test_review)
        reviews_by_topic = self.topic.get_reviews_by_topic('Test Topic')
        self.assertTrue(any(review['content'] == 'Content...' for review in reviews_by_topic))