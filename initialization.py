from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import random
import string

class SocialNetworkDB:
    def __init__(self, connection_string="mongodb://localhost:27017/"):
        """Initialize connection to MongoDB"""
        self.client = MongoClient(connection_string)
        self.db = self.client["social_network"]
        
        # Create collections
        self.users = self.db["users"]
        self.friendships = self.db["friendships"]
        self.topics = self.db["topics"]
        self.posts = self.db["posts"]
        self.likes = self.db["likes"]
        self.comments = self.db["comments"]
        
        # Ensure indexes (in addition to those created in setup script)
        self._create_indexes()
    
    def _create_indexes(self):
        """Create indexes for efficient querying"""
        # Most indexes were created in the setup script, but we can add more here if needed
        self.users.create_index("username", unique=True)
        self.topics.create_index("name", unique=True)
    
    def generate_data(self, num_users=100, num_topics=20, 
                     max_friends_per_user=20, max_posts_per_user=50,
                     max_likes_per_post=30, max_comments_per_post=15):
        """Generate test data for the social network"""
        print("Generating test data...")
        
        # Clear existing data
        self.users.delete_many({})
        self.friendships.delete_many({})
        self.topics.delete_many({})
        self.posts.delete_many({})
        self.likes.delete_many({})
        self.comments.delete_many({})
        
        # Generate users
        user_ids = []
        print(f"Creating {num_users} users...")
        for i in range(num_users):
            username = f"user{i+1}"
            email = f"user{i+1}@example.com"
            date_joined = datetime.now() - timedelta(days=random.randint(1, 365))
            
            result = self.users.insert_one({
                "username": username,
                "email": email,
                "dateJoined": date_joined,
                "lastActive": datetime.now() - timedelta(days=random.randint(0, 30))
            })
            user_ids.append(result.inserted_id)
        
        # Generate topics
        topic_ids = []
        print(f"Creating {num_topics} topics...")
        topics = [f"Topic{i+1}" for i in range(num_topics)]
        for topic in topics:
            result = self.topics.insert_one({
                "name": topic,
                "postCount": 0
            })
            topic_ids.append(result.inserted_id)
        
        # Generate friendships (follows)
        print("Creating friendship connections...")
        for user_id in user_ids:
            # Each user follows a random number of other users
            num_friends = random.randint(5, max_friends_per_user)
            possible_friends = [uid for uid in user_ids if uid != user_id]
            if len(possible_friends) > num_friends:
                friends = random.sample(possible_friends, num_friends)
            else:
                friends = possible_friends
                
            for friend_id in friends:
                self.friendships.insert_one({
                    "userId": user_id,
                    "friendId": friend_id,
                    "createdAt": datetime.now() - timedelta(days=random.randint(1, 300))
                })
        
        # Generate posts
        post_ids = []
        print("Creating posts...")
        for user_id in user_ids:
            num_posts = random.randint(5, max_posts_per_user)
            for _ in range(num_posts):
                # Generate random post content (256 bytes max)
                content = ''.join(random.choices(string.ascii_letters + string.digits + " ", k=random.randint(50, 256)))
                topic_id = random.choice(topic_ids)
                created_at = datetime.now() - timedelta(days=random.randint(0, 60))
                
                result = self.posts.insert_one({
                    "userId": user_id,
                    "content": content,
                    "topicId": topic_id,
                    "createdAt": created_at,
                    "likeCount": 0,
                    "commentCount": 0
                })
                post_ids.append(result.inserted_id)
                
                # Update topic post count
                self.topics.update_one(
                    {"_id": topic_id},
                    {"$inc": {"postCount": 1}}
                )
        
        # Generate likes
        print("Creating likes...")
        for post_id in post_ids:
            num_likes = random.randint(0, max_likes_per_post)
            likers = random.sample(user_ids, min(num_likes, len(user_ids)))
            
            for user_id in likers:
                self.likes.insert_one({
                    "userId": user_id,
                    "postId": post_id,
                    "createdAt": datetime.now() - timedelta(hours=random.randint(1, 24*60))
                })
                
                # Update post like count
                self.posts.update_one(
                    {"_id": post_id},
                    {"$inc": {"likeCount": 1}}
                )
        
        # Generate comments
        print("Creating comments...")
        for post_id in post_ids:
            num_comments = random.randint(0, max_comments_per_post)
            commenters = random.sample(user_ids, min(num_comments, len(user_ids)))
            
            for user_id in commenters:
                comment_content = ''.join(random.choices(string.ascii_letters + string.digits + " ", k=random.randint(10, 100)))
                self.comments.insert_one({
                    "userId": user_id,
                    "postId": post_id,
                    "content": comment_content,
                    "createdAt": datetime.now() - timedelta(hours=random.randint(1, 24*60))
                })
                
                # Update post comment count
                self.posts.update_one(
                    {"_id": post_id},
                    {"$inc": {"commentCount": 1}}
                )
        
        print("Data generation complete!")
        print(f"Created {len(user_ids)} users, {len(topic_ids)} topics, {len(post_ids)} posts")
        
        # Return some sample IDs for testing
        return {
            "sample_user_id": user_ids[0],
            "sample_topic_id": topic_ids[0],
            "sample_post_id": post_ids[0]
        }

# Example usage of data generation
if __name__ == "__main__":
    db = SocialNetworkDB()
    sample_ids = db.generate_data()
    print(f"Sample user ID: {sample_ids['sample_user_id']}")
    print(f"Sample topic ID: {sample_ids['sample_topic_id']}")
    print(f"Sample post ID: {sample_ids['sample_post_id']}")