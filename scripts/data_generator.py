from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import random
import string

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['social_network']

# Clear existing collections
db.users.delete_many({})
db.friendships.delete_many({})
db.topics.delete_many({})
db.posts.delete_many({})
db.likes.delete_many({})
db.comments.delete_many({})

# Configuration
NUM_USERS = 100
NUM_TOPICS = 20
MAX_FRIENDS_PER_USER = 20
MAX_POSTS_PER_USER = 30
MAX_LIKES_PER_POST = 25
MAX_COMMENTS_PER_POST = 10

print("Generating test data...")

# Generate users
user_ids = []
print(f"Creating {NUM_USERS} users...")
for i in range(NUM_USERS):
    username = f"user{i+1}"
    email = f"user{i+1}@example.com"
    date_joined = datetime.now() - timedelta(days=random.randint(1, 365))
    
    result = db.users.insert_one({
        "username": username,
        "email": email,
        "dateJoined": date_joined,
        "lastActive": datetime.now() - timedelta(days=random.randint(0, 30))
    })
    user_ids.append(result.inserted_id)

# Generate topics
topic_ids = []
print(f"Creating {NUM_TOPICS} topics...")
for i in range(NUM_TOPICS):
    topic_name = f"Topic{i+1}"
    result = db.topics.insert_one({
        "name": topic_name,
        "postCount": 0
    })
    topic_ids.append(result.inserted_id)

# Generate friendships
print("Creating friendship connections...")
for user_id in user_ids:
    num_friends = random.randint(5, MAX_FRIENDS_PER_USER)
    possible_friends = [uid for uid in user_ids if uid != user_id]
    friends = random.sample(possible_friends, min(num_friends, len(possible_friends)))
    
    for friend_id in friends:
        db.friendships.insert_one({
            "userId": user_id,
            "friendId": friend_id,
            "createdAt": datetime.now() - timedelta(days=random.randint(1, 300))
        })

# Generate posts
post_ids = []
print("Creating posts...")
for user_id in user_ids:
    num_posts = random.randint(1, MAX_POSTS_PER_USER)
    for _ in range(num_posts):
        content = ''.join(random.choices(string.ascii_letters + string.digits + " ", k=random.randint(50, 256)))
        topic_id = random.choice(topic_ids)
        created_at = datetime.now() - timedelta(days=random.randint(0, 60))
        
        result = db.posts.insert_one({
            "userId": user_id,
            "content": content,
            "topicId": topic_id,
            "createdAt": created_at,
            "likeCount": 0,
            "commentCount": 0
        })
        post_ids.append(result.inserted_id)
        
        # Update topic post count
        db.topics.update_one(
            {"_id": topic_id},
            {"$inc": {"postCount": 1}}
        )

# Generate likes
print("Creating likes...")
for post_id in post_ids:
    num_likes = random.randint(0, MAX_LIKES_PER_POST)
    likers = random.sample(user_ids, min(num_likes, len(user_ids)))
    
    for user_id in likers:
        db.likes.insert_one({
            "userId": user_id,
            "postId": post_id,
            "createdAt": datetime.now() - timedelta(hours=random.randint(1, 24*60))
        })
        
        # Update post like count
        db.posts.update_one(
            {"_id": post_id},
            {"$inc": {"likeCount": 1}}
        )

# Generate comments
print("Creating comments...")
for post_id in post_ids:
    num_comments = random.randint(0, MAX_COMMENTS_PER_POST)
    commenters = random.sample(user_ids, min(num_comments, len(user_ids)))
    
    for user_id in commenters:
        comment_content = ''.join(random.choices(string.ascii_letters + string.digits + " ", k=random.randint(10, 100)))
        db.comments.insert_one({
            "userId": user_id,
            "postId": post_id,
            "content": comment_content,
            "createdAt": datetime.now() - timedelta(hours=random.randint(1, 24*60))
        })
        
        # Update post comment count
        db.posts.update_one(
            {"_id": post_id},
            {"$inc": {"commentCount": 1}}
        )

print("Data generation complete!")
print(f"Created {len(user_ids)} users, {len(topic_ids)} topics, {len(post_ids)} posts")

# Save a sample user ID to a file for testing
with open("sample_ids.txt", "w") as f:
    f.write(f"Sample User ID: {user_ids[0]}\n")
    f.write(f"Sample Topic ID: {topic_ids[0]}\n")
    f.write(f"Sample Post ID: {post_ids[0]}\n")