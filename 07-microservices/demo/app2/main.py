from datetime import datetime
import requests
import pymysql
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from google.cloud import pubsub_v1

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:app2123@127.0.0.1:3309/app_post'
db = SQLAlchemy(app)

project = 'sacred-highway-197822'
topic_name = 'new_user'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    user_id = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Post %r>' % self.title


db.create_all()

def serialize(post):
    return {
        'title':post.title,
        'body':post.body,
        'author': post.user_id
    }

@app.route("/")
def hello():
    posts = Post.query.all()
    data = []
    for item in posts:
        data.append(serialize(item))
    print(data)
    create_push_subscription()
    return jsonify(json_list = data)

@app.route("/authors")
def authors():
    data = requests.get('http://localhost:8080').json()
    print(data)
    return jsonify(data)

@app.route("/webhook")
def webhook(request):
    print(request)

def create_subscription():
    """Create a new pull subscription on the given topic."""
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = subscriber.topic_path(project, topic_name)
    subscription_path = subscriber.subscription_path(
        project, "app2_subscription")

    subscription = subscriber.create_subscription(
        subscription_path, topic_path)

    print('Subscription created: {}'.format(subscription))

def create_push_subscription():
    """Create a new push subscription on the given topic.
    For example, endpoint is
    "https://my-test-project.appspot.com/push".
    """
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = subscriber.topic_path(project, topic_name)
    subscription_path = subscriber.subscription_path(
        project, "app2_push_subscription")

    push_config = pubsub_v1.types.PushConfig(
        push_endpoint="https://us-central1-sacred-highway-197822.cloudfunctions.net/helloHttp")

    subscription = subscriber.create_subscription(
        subscription_path, topic_path, push_config)

    print('Push subscription created: {}'.format(subscription))
    print('Endpoint for subscription is: {}'.format(endpoint))

def receive_messages():
    """Receives messages from a pull subscription."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project, "app2_subscription")

    def callback(message):
        print('Received message: {}'.format(message))
        message.ack()

    subscriber.subscribe(subscription_path, callback=callback)

    # The subscriber is non-blocking, so we must keep the main thread from
    # exiting to allow it to process messages in the background.
    print('Listening for messages on {}'.format(subscription_path))
    while True:
        time.sleep(60)
    

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8085, debug=True)