from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta

class SocialNetworkQueries:
    def __init__(self, connection_string="mongodb://localhost:27017/"):
        """Initialize connection to MongoDB"""
        self.client = MongoClient(connection_string)
        self.db = self.client["social_network"]
        
        # Access collections
        self.users = self.db["users"]
        self.friendships = self.db["friendships"]
        self.topics = self.db["topics"]
        self.posts = self.db["posts"]
        self.likes = self.db["likes"]
        self.comments = self.db["comments"]
    
    def get_all_posts_by_user(self, user_id):
        """
        Query 1: Get all posts of a user
        :param user_id: ObjectId of the user
        :return: List of posts
        """
        user_posts = list(self.posts.find(
            {"userId": ObjectId(user_id) if isinstance(user_id, str) else user_id},
            {"_id": 1, "content": 1, "createdAt": 1, "likeCount": 1, "commentCount": 1}
        ).sort("createdAt", -1))
        
        return user_posts
    
    def get_top_k_most_liked_posts_by_user(self, user_id, k=10):
        """
        Query 2: Get top k most liked posts of a user
        :param user_id: ObjectId of the user
        :param k: Number of posts to return
        :return: List of top k most liked posts
        """
        top_liked_posts = list(self.posts.find(
            {"userId": ObjectId(user_id) if isinstance(user_id, str) else user_id},
            {"_id": 1, "content": 1, "createdAt": 1, "likeCount": 1}
        ).sort("likeCount", -1).limit(k))
        
        return top_liked_posts
    
    def get_top_k_most_commented_posts_by_user(self, user_id, k=10):
        """
        Query 3: Get top k most commented posts of a user
        :param user_id: ObjectId of the user
        :param k: Number of posts to return
        :return: List of top k most commented posts
        """
        top_commented_posts = list(self.posts.find(
            {"userId": ObjectId(user_id) if isinstance(user_id, str) else user_id},
            {"_id": 1, "content": 1, "createdAt": 1, "commentCount": 1}
        ).sort("commentCount", -1).limit(k))
        
        return top_commented_posts
    
    def get_all_comments_by_user(self, user_id):
        """
        Query 4: Get all comments of a user
        :param user_id: ObjectId of the user
        :return: List of comments with post information
        """
        # Find all comments by the user
        user_comments = list(self.comments.find(
            {"userId": ObjectId(user_id) if isinstance(user_id, str) else user_id},
            {"_id": 1, "postId": 1, "content": 1, "createdAt": 1}
        ).sort("createdAt", -1))
        
        # Enhance comments with post information
        for comment in user_comments:
            post = self.posts.find_one({"_id": comment["postId"]}, {"content": 1, "userId": 1})
            if post:
                comment["postContent"] = post["content"][:50] + "..." if len(post["content"]) > 50 else post["content"]
                comment["postAuthorId"] = post["userId"]
        
        return user_comments
    
    def get_all_posts_on_topic(self, topic_id):
        """
        Query 5: Get all posts on a topic
        :param topic_id: ObjectId of the topic
        :return: List of posts on the topic
        """
        topic_posts = list(self.posts.find(
            {"topicId": ObjectId(topic_id) if isinstance(topic_id, str) else topic_id},
            {"_id": 1, "userId": 1, "content": 1, "createdAt": 1, "likeCount": 1, "commentCount": 1}
        ).sort("createdAt", -1))
        
        # Enhance posts with user information
        for post in topic_posts:
            user = self.users.find_one({"_id": post["userId"]}, {"username": 1})
            if user:
                post["username"] = user["username"]
        
        return topic_posts
    
    def get_top_k_popular_topics(self, k=10):
        """
        Query 6: Get top k most popular topics in terms of posts
        :param k: Number of topics to return
        :return: List of top k popular topics
        """
        top_topics = list(self.topics.find(
            {},
            {"_id": 1, "name": 1, "postCount": 1}
        ).sort("postCount", -1).limit(k))
        
        return top_topics
    
    def get_friend_posts_last_24_hours(self, user_id):
        """
        Query 7: Get posts of all friends in last 24 hours
        :param user_id: ObjectId of the user
        :return: List of posts by friends in the last 24 hours
        """
        # Find all friends of the user
        friends = list(self.friendships.find(
            {"userId": ObjectId(user_id) if isinstance(user_id, str) else user_id},
            {"friendId": 1}
        ))
        
        friend_ids = [friend["friendId"] for friend in friends]
        
        # Find recent posts by these friends
        last_24_hours = datetime.now() - timedelta(hours=24)
        
        recent_friend_posts = list(self.posts.find(
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
        for post in recent_friend_posts:
            user = self.users.find_one({"_id": post["userId"]}, {"username": 1})
            if user:
                post["username"] = user["username"]
            
            topic = self.topics.find_one({"_id": post["topicId"]}, {"name": 1})
            if topic:
                post["topicName"] = topic["name"]
        
        return recent_friend_posts

# Example usage
if __name__ == "__main__":
    from bson.objectid import ObjectId
    
    queries = SocialNetworkQueries()
    
    # Use a valid user ID from your database
    sample_user_id = ObjectId("your_user_id_here")
    sample_topic_id = ObjectId("your_topic_id_here")
    
    # Example calls
    print("1. User posts:", queries.get_all_posts_by_user(sample_user_id))
    print("2. Top liked posts:", queries.get_top_k_most_liked_posts_by_user(sample_user_id, 5))
    print("3. Top commented posts:", queries.get_top_k_most_commented_posts_by_user(sample_user_id, 5))
    print("4. User comments:", queries.get_all_comments_by_user(sample_user_id))
    print("5. Topic posts:", queries.get_all_posts_on_topic(sample_topic_id))
    print("6. Popular topics:", queries.get_top_k_popular_topics(5))
    print("7. Friend recent posts:", queries.get_friend_posts_last_24_hours(sample_user_id))