from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['social_network']

def get_all_posts_on_topic(topic_id):
    """Query 5: Get all posts on a topic"""
    if isinstance(topic_id, str):
        topic_id = ObjectId(topic_id)
    
    posts = list(db.posts.find(
        {"topicId": topic_id},
        {"_id": 1, "userId": 1, "content": 1, "createdAt": 1, "likeCount": 1, "commentCount": 1}
    ).sort("createdAt", -1))
    
    # Enhance posts with user information
    for post in posts:
        user = db.users.find_one({"_id": post["userId"]}, {"username": 1})
        if user:
            post["username"] = user["username"]
    
    return posts

def get_top_k_popular_topics(k=10):
    """Query 6: Get top k most popular topics in terms of posts"""
    topics = list(db.topics.find(
        {},
        {"_id": 1, "name": 1, "postCount": 1}
    ).sort("postCount", -1).limit(k))
    
    return topics

def get_friend_posts_last_24_hours(user_id):
    """Query 7: Get posts of all friends in last 24 hours"""
    if isinstance(user_id, str):
        user_id = ObjectId(user_id)
    
    # Find all friends of the user
    friends = list(db.friendships.find(
        {"userId": user_id},
        {"friendId": 1}
    ))
    
    friend_ids = [friend["friendId"] for friend in friends]
    
    # Find recent posts by these friends
    last_24_hours = datetime.now() - timedelta(hours=24)
    
    posts = list(db.posts.find(
        {
            "userId": {"$in": friend_ids},
            "createdAt": {"$gte": last_24_hours}
        },
        {
            "_id": 1, "userId": 1, "content": 1, "createdAt": 1, 
            "likeCount": 1, "commentCount": 1, "topicId": 1
        }
    ).sort("createdAt", -1))
    
    # Enhance posts with user and topic information
    for post in posts:
        user = db.users.find_one({"_id": post["userId"]}, {"username": 1})
        if user:
            post["username"] = user["username"]
        
        topic = db.topics.find_one({"_id": post["topicId"]}, {"name": 1})
        if topic:
            post["topicName"] = topic["name"]
    
    return posts