import bottle
from beaker.middleware import SessionMiddleware
from bottle import route, request, run, template, redirect, static_file
from review import Review, ReviewItem, Topic
from UserClass import Accounts, User
import json

hostName = "localhost"
serverPort = 8080

reviewsObj = Review()
accountsObj = Accounts()

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 1800,
    'session.cookie_secure': True,
    'session.data_dir': './data',
    'session.auto': True
}

app = SessionMiddleware(bottle.app(), session_opts)


@route('/', method="GET")
def login():
    return static_file('html/login.html', ".")


@route('/profile', method="GET")
def load_profile():
    s = bottle.request.environ.get('beaker.session')
    if 'username' not in s:
        redirect('/')
    else:
        author = s['username']
        topic_obj = Topic(reviewsObj.view_published())
        user = accountsObj.view_user(author)
        draft = reviewsObj.view_drafts(user["username"])
        all_users = accountsObj.get_users()
        all_topics = topic_obj.get_topics()
        template_data = {
            "user": user,
            "drafts": draft,
            "all_users": all_users,
            "all_topics": all_topics
        }
    return template('html/profile.html', **template_data)


@route('/index.html', method="GET")
def load_homepage():
    s = bottle.request.environ.get('beaker.session')
    if 'username' not in s:
        redirect('/')
    else:
        author = s['username']
        user = accountsObj.view_user(author)
        topic_obj = Topic(reviewsObj.view_published())
        reviews = reviewsObj.view_published()
        all_users = accountsObj.get_users()
        all_topics = topic_obj.get_topics()
        template_data = {
            "reviews": reviews,
            "user": user,
            "all_users": all_users,
            "all_topics": all_topics
        }
    return template('html/index.html', **template_data)


@route('/load-reviews-by-topic', method="POST")
def load_reviews_by_topic():
    s = bottle.request.environ.get('beaker.session')
    if 'username' not in s:
        redirect('/')
    else:
        author = s['username']
        topic_obj = Topic(reviewsObj.view_published())
        topic = request.forms.get('topic')
        if topic == 'all':
            reviews = reviewsObj.view_published()
        else:
            reviews = topic_obj.get_reviews_by_topic(topic)
        user = accountsObj.view_user(author)
        all_users = accountsObj.get_users()
        all_topics = topic_obj.get_topics()
        template_data = {
            "reviews": reviews,
            "user": user,
            "all_users": all_users,
            "all_topics": all_topics
        }
    return template('html/index.html', **template_data)


@route('/add-topic', method='POST')
def add_topic():
    s = bottle.request.environ.get('beaker.session')
    if 'username' not in s:
        redirect('/')
    new_topic = request.forms.get('new_topic')
    topic_obj = Topic(reviewsObj.view_published())
    if new_topic and new_topic not in topic_obj.get_topics():
        topic_obj.add_topic(new_topic)
    redirect('/index.html')


@route('/viewdrafts', method="GET")
def load_draft():
    s = bottle.request.environ.get('beaker.session')
    if 'username' not in s:
        redirect('/')
    else:
        reviews = reviewsObj.view_drafts(s["username"])
        topic_obj = Topic(reviewsObj.view_published())
        all_users = accountsObj.get_users()
        all_topics = topic_obj.get_topics()
        template_data = {
            "reviews": reviews,
            "all_users": all_users,
            "all_topics": all_topics
        }
    return template('html/index.html', **template_data)


@route('/signup', method="POST")
def sign_up():
    #db = request.db
    firstname = request.forms.get('firstname')
    lastname = request.forms.get('lastname')
    email = request.forms.get('email')
    username = request.forms.get('username')
    password = request.forms.get('password')
    team = request.forms.get('team')
    accountsObj.add_user(User(firstname, lastname, email, username, password, team))
    redirect("/")


@route('/edit_user',method="POST")
def edit_account():
    s = bottle.request.environ.get('beaker.session')
    if 'username' not in s:
        redirect('/')
    else:
        author = s['username']
        user = accountsObj.view_user(author)
        userObj = accountsObj.find_user(author)
        first_name = request.forms.get('first')
        last_name = request.forms.get('last')
        username = request.forms.get('username')
        password = request.forms.get('psw')
        if user["first_name"] == first_name:
            raise Exception('You cannot change your first name to your previously chosen name.')
        if user["last_name"] == last_name:
            raise Exception('You cannot change your last name to your previously chosen name.')
        if user["username"] == username:
            raise Exception("You cannot change your username to a preexisting username.")
        if user["password"] == password:
            raise Exception("You cannot change your password to your previous password.")
        userObj.edit_user(username,first_name,last_name,username,password)
        redirect('/index.html')


@route('/login', method="POST")
def login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    user = accountsObj.find_user(username)
    if not user:
        return "User not found"
    if password == user.get_password():
        s = bottle.request.environ.get('beaker.session')
        s['username'] = username
        s.save()
        redirect("/index.html")
    else:
        return "Password Incorrect Please try Again"


@route('/signout', method="GET")
def sign_out():
    s = bottle.request.environ.get('beaker.session')
    s.delete()
    redirect('/')


@route('/about_me', method="GET")
def reviews_about_me():
    s = bottle.request.environ.get('beaker.session')
    if 'username' not in s:
        redirect('/')
    else:
        author = s['username']
        topic_obj = Topic(reviewsObj.view_published())
        user = accountsObj.view_user(author)
        user_obj = accountsObj.find_user(author)
        all_users = accountsObj.get_users()
        all_topics = topic_obj.get_topics()
        reviews = user_obj.get_user_reviews()
        template_data = {
            "user": user,
            "drafts": reviews,
            "all_users": all_users,
            "all_topics": all_topics
        }
    return template('html/profile.html', **template_data)


@route('/by_me', method="GET")
def reviews_about_me():
    s = bottle.request.environ.get('beaker.session')
    if 'username' not in s:
        redirect('/')
    else:
        author = s['username']
        topic_obj = Topic(reviewsObj.view_published())
        user = accountsObj.view_user(author)
        user_obj = accountsObj.find_user(author)
        all_users = accountsObj.get_users()
        all_topics = topic_obj.get_topics()
        reviews = user_obj.get_reviews_by_user()
        template_data = {
            "user": user,
            "drafts": reviews,
            "all_users": all_users,
            "all_topics": all_topics
        }
    return template('html/profile.html', **template_data)


@route('/add', method="POST")
def write_review():
    s = bottle.request.environ.get('beaker.session')
    if 'username' not in s:
        redirect('/')
    else:
        author = s['username']
        assignee = request.forms.get('assignee')
        topic = request.forms.get('topic')
        content = request.forms.get('content')
        rating = request.forms.get('rating')
        is_anonymous = True if request.forms.get('anonymous') == 'on' else False
        is_published = not request.forms.get('draft')
        reviewsObj.add_review(ReviewItem(topic=topic, content=content, author=author, assignee=assignee, rating=rating,
                                         is_anonymous=is_anonymous, is_published=is_published))
        redirect('/index.html')


@route('/edit_review', method="POST")
def edit_review():
    s = bottle.request.environ.get('beaker.session')
    if 'username' not in s:
        redirect('/')
    author = s['username']
    assignee = request.forms.get('assignee')
    topic = request.forms.get('topic')
    content = request.forms.get('content')
    rating = request.forms.get('rating')
    is_published = not request.forms.get('draft')
    newReview = ReviewItem(topic=topic, content=content, author=author, assignee=assignee, rating=rating,
                                     is_published=is_published)
    reviewsObj = newReview

    print(reviewsObj)
    redirect('/index.html')


@route('/search_review', method="POST")
def find_review():
    search_results = request.forms.get('search_string')
    found_reviews = Review.search(search_results)
    print(type(found_reviews))
    s = bottle.request.environ.get('beaker.session')
    if 'username' not in s:
        redirect('/')
    else:
        author = s['username']
        user = accountsObj.view_user(author)
        topic_obj = Topic(reviewsObj.view_published())
        all_users = accountsObj.get_users()
        all_topics = topic_obj.get_topics()
        template_data = {
            "all_users": all_users,
            "reviews": found_reviews,
            "user": user,
            "all_topics": all_topics
        }
    return template('html/index.html', **template_data)


@route('/filter_review', method="POST")
def filter_review():
    category = request.forms.get('filter')
    sorted_reviews = Review.search_sort(category)
    s = bottle.request.environ.get('beaker.session')
    if 'username' not in s:
        redirect('/')
    else:
        author = s['username']
        user = accountsObj.view_user(author)
        topic_obj = Topic(reviewsObj.view_published())
        all_users = accountsObj.get_users()
        all_topics = topic_obj.get_topics()
        template_data = {
            "all_users": all_users,
            "reviews": sorted_reviews,
            "user": user,
            "all_topics": all_topics
        }
    print("Before template rendering:", type(sorted_reviews))
    return template('html/index.html', **template_data)


@route('/add_reaction', method='POST')
def add_reaction():
    topic = request.forms.get('topic')
    author = request.forms.get('author')
    date = request.forms.get('date')
    emoji = request.forms.get('emoji')

    for review_item in reviewsObj.reviews:
        if review_item['topic'] == topic and review_item['author'] == author and review_item['date'] == date:
            print(review_item)
            review = ReviewItem(**review_item)
            review.react(emoji)
            review_item.update(review.__dict__)

            with open('reviews.json', 'w') as file:
                json.dump(reviewsObj.reviews, file, indent=2)

            redirect('/index.html')
            return

    return "Review not found"


@route('/style.css', method="GET")
def css():
    return static_file('./style.css', root=".")


@route('/logo.png', method="GET")
def photo():
    return static_file('/logo.png', root=".")


@route('/profile.css', method="GET")
def css_profile():
    return static_file('./profile.css', root=".")


if __name__ == "__main__":
    run(app, host=hostName, port=serverPort, debug=True)
