from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['social_network']

def get_all_posts_by_user(user_id):
    """Query 1: Get all posts of a user"""
    if isinstance(user_id, str):
        user_id = ObjectId(user_id)
    
    posts = list(db.posts.find(
        {"userId": user_id},
        {"_id": 1, "content": 1, "createdAt": 1, "likeCount": 1, "commentCount": 1}
    ).sort("createdAt", -1))
    
    return posts

def get_top_k_most_liked_posts_by_user(user_id, k=10):
    """Query 2: Get top k most liked posts of a user"""
    if isinstance(user_id, str):
        user_id = ObjectId(user_id)
    
    posts = list(db.posts.find(
        {"userId": user_id},
        {"_id": 1, "content": 1, "createdAt": 1, "likeCount": 1}
    ).sort("likeCount", -1).limit(k))
    
    return posts

def get_top_k_most_commented_posts_by_user(user_id, k=10):
    """Query 3: Get top k most commented posts of a user"""
    if isinstance(user_id, str):
        user_id = ObjectId(user_id)
    
    posts = list(db.posts.find(
        {"userId": user_id},
        {"_id": 1, "content": 1, "createdAt": 1, "commentCount": 1}
    ).sort("commentCount", -1).limit(k))
    
    return posts

def get_all_comments_by_user(user_id):
    """Query 4: Get all comments of a user"""
    if isinstance(user_id, str):
        user_id = ObjectId(user_id)
    
    comments = list(db.comments.find(
        {"userId": user_id},
        {"_id": 1, "postId": 1, "content": 1, "createdAt": 1}
    ).sort("createdAt", -1))
    
    # Enhance comments with post information
    for comment in comments:
        post = db.posts.find_one({"_id": comment["postId"]}, {"content": 1, "userId": 1})
        if post:
            comment["postContent"] = post["content"][:50] + "..." if len(post["content"]) > 50 else post["content"]
            comment["postAuthorId"] = post["userId"]
    
    return comments