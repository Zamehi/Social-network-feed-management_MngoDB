from data_models_generator import SocialNetworkDB
from query_implementation import SocialNetworkQueries
from bson.objectid import ObjectId
import time
import pprint

def test_social_network_implementation():
    """Test the complete social network implementation"""
    print("=" * 50)
    print("SOCIAL NETWORK FEED MANAGEMENT TEST")
    print("=" * 50)
    
    # Step 1: Initialize the database and generate test data
    print("\nStep 1: Initializing database and generating test data...")
    db = SocialNetworkDB()
    sample_ids = db.generate_data(
        num_users=100,  # Adjust these numbers based on your testing needs
        num_topics=20,
        max_friends_per_user=20,
        max_posts_per_user=30,
        max_likes_per_post=25,
        max_comments_per_post=10
    )
    
    # Get sample IDs for testing
    sample_user_id = sample_ids["sample_user_id"]
    sample_topic_id = sample_ids["sample_topic_id"]
    
    # Step 2: Initialize the queries object
    queries = SocialNetworkQueries()
    
    # Step 3: Test each query
    print("\nStep 3: Testing all required queries...")
    pp = pprint.PrettyPrinter(indent=2)
    
    # Test Query 1: All posts of a user
    print("\n--- Query 1: All posts of a user ---")
    start_time = time.time()
    user_posts = queries.get_all_posts_by_user(sample_user_id)
    query_time = time.time() - start_time
    print(f"Found {len(user_posts)} posts for user {sample_user_id}")
    print(f"Query execution time: {query_time:.4f} seconds")
    if user_posts:
        print("Sample post:")
        pp.pprint(user_posts[0])
    
    # Test Query 2: Top k most liked posts of a user
    print("\n--- Query 2: Top k most liked posts of a user ---")
    k = 5
    start_time = time.time()
    top_liked_posts = queries.get_top_k_most_liked_posts_by_user(sample_user_id, k)
    query_time = time.time() - start_time
    print(f"Found {len(top_liked_posts)} top liked posts for user {sample_user_id}")
    print(f"Query execution time: {query_time:.4f} seconds")
    if top_liked_posts:
        print("Top liked posts:")
        for i, post in enumerate(top_liked_posts[:3], 1):
            print(f"{i}. Likes: {post['likeCount']}, Content: {post['content'][:50]}...")
    
    # Test Query 3: Top k most commented posts of a user
    print("\n--- Query 3: Top k most commented posts of a user ---")
    k = 5
    start_time = time.time()
    top_commented_posts = queries.get_top_k_most_commented_posts_by_user(sample_user_id, k)
    query_time = time.time() - start_time
    print(f"Found {len(top_commented_posts)} top commented posts for user {sample_user_id}")
    print(f"Query execution time: {query_time:.4f} seconds")
    if top_commented_posts:
        print("Top commented posts:")
        for i, post in enumerate(top_commented_posts[:3], 1):
            print(f"{i}. Comments: {post['commentCount']}, Content: {post['content'][:50]}...")
    
    # Test Query 4: All comments of a user
    print("\n--- Query 4: All comments of a user ---")
    start_time = time.time()
    user_comments = queries.get_all_comments_by_user(sample_user_id)
    query_time = time.time() - start_time
    print(f"Found {len(user_comments)} comments by user {sample_user_id}")
    print(f"Query execution time: {query_time:.4f} seconds")
    if user_comments:
        print("Sample comment:")
        pp.pprint(user_comments[0])
    
    # Test Query 5: All posts on a topic
    print("\n--- Query 5: All posts on a topic ---")
    start_time = time.time()
    topic_posts = queries.get_all_posts_on_topic(sample_topic_id)
    query_time = time.time() - start_time
    print(f"Found {len(topic_posts)} posts on topic {sample_topic_id}")
    print(f"Query execution time: {query_time:.4f} seconds")
    if topic_posts:
        print("Sample topic post:")
        pp.pprint(topic_posts[0])
    
    # Test Query 6: Top k most popular topics
    print("\n--- Query 6: Top k most popular topics ---")
    k = 5
    start_time = time.time()
    popular_topics = queries.get_top_k_popular_topics(k)
    query_time = time.time() - start_time
    print(f"Found {len(popular_topics)} most popular topics")
    print(f"Query execution time: {query_time:.4f} seconds")
    if popular_topics:
        print("Popular topics:")
        for i, topic in enumerate(popular_topics, 1):
            print(f"{i}. Topic: {topic['name']}, Post Count: {topic['postCount']}")
    
    # Test Query 7: Posts of all friends in last 24 hours
    print("\n--- Query 7: Posts of all friends in last 24 hours ---")
    start_time = time.time()
    friend_recent_posts = queries.get_friend_posts_last_24_hours(sample_user_id)
    query_time = time.time() - start_time
    print(f"Found {len(friend_recent_posts)} recent posts by friends of user {sample_user_id}")
    print(f"Query execution time: {query_time:.4f} seconds")
    if friend_recent_posts:
        print("Sample friend recent post:")
        pp.pprint(friend_recent_posts[0])
    
    print("\n" + "=" * 50)
    print("Testing complete! All queries executed successfully.")
    print("=" * 50)

if __name__ == "__main__":
    test_social_network_implementation()