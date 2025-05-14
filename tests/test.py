import sys
import os
import time
import pprint
from bson.objectid import ObjectId

# Add parent directory to path so we can import the query modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from queries.query1 import (
    get_all_posts_by_user,
    get_top_k_most_liked_posts_by_user,
    get_top_k_most_commented_posts_by_user,
    get_all_comments_by_user
)

from queries.query2 import (
    get_all_posts_on_topic,
    get_top_k_popular_topics,
    get_friend_posts_last_24_hours
)

# Load sample IDs from file
sample_user_id = None
sample_topic_id = None
sample_post_id = None

try:
    with open("C:\\Users\\NEW MMC\\Documents\\8th Semester\\DDE\\A02\\Social-network-feed-management_MngoDB\\scripts\\sample_ids.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            if "Sample User ID" in line:
                sample_user_id = line.split(": ")[1].strip()
            elif "Sample Topic ID" in line:
                sample_topic_id = line.split(": ")[1].strip()
            elif "Sample Post ID" in line:
                sample_post_id = line.split(": ")[1].strip()
except FileNotFoundError:
    print("Sample IDs file not found. Please run data generator first.")
    exit(1)

pp = pprint.PrettyPrinter(indent=2)

# Test all queries
print("\n=== Testing Query 1: All posts of a user ===")
start_time = time.time()
user_posts = get_all_posts_by_user(sample_user_id)
query_time = time.time() - start_time
print(f"Found {len(user_posts)} posts for user {sample_user_id}")
print(f"Query execution time: {query_time:.4f} seconds")
if user_posts:
    print("\nSample post:")
    pp.pprint(user_posts[0])

print("\n=== Testing Query 2: Top k most liked posts of a user ===")
k = 5
start_time = time.time()
top_liked_posts = get_top_k_most_liked_posts_by_user(sample_user_id, k)
query_time = time.time() - start_time
print(f"Found {len(top_liked_posts)} top liked posts for user {sample_user_id}")
print(f"Query execution time: {query_time:.4f} seconds")
if top_liked_posts:
    print("\nSample post:")
    pp.pprint(top_liked_posts[0])

print("\n=== Testing Query 3: Top k most commented posts of a user ===")
k = 5
start_time = time.time()
top_commented_posts = get_top_k_most_commented_posts_by_user(sample_user_id, k)
query_time = time.time() - start_time
print(f"Found {len(top_commented_posts)} top commented posts for user {sample_user_id}")
print(f"Query execution time: {query_time:.4f} seconds")
if top_commented_posts:
    print("\nSample post:")
    pp.pprint(top_commented_posts[0])

print("\n=== Testing Query 4: All comments of a user ===")
start_time = time.time()
user_comments = get_all_comments_by_user(sample_user_id)
query_time = time.time() - start_time
print(f"Found {len(user_comments)} comments by user {sample_user_id}")
print(f"Query execution time: {query_time:.4f} seconds")
if user_comments:
    print("\nSample comment:")
    pp.pprint(user_comments[0])

print("\n=== Testing Query 5: All posts on a topic ===")
start_time = time.time()
topic_posts = get_all_posts_on_topic(sample_topic_id)
query_time = time.time() - start_time
print(f"Found {len(topic_posts)} posts on topic {sample_topic_id}")
print(f"Query execution time: {query_time:.4f} seconds")
if topic_posts:
    print("\nSample post:")
    pp.pprint(topic_posts[0])

print("\n=== Testing Query 6: Top k most popular topics ===")
k = 5
start_time = time.time()
popular_topics = get_top_k_popular_topics(k)
query_time = time.time() - start_time
print(f"Found {len(popular_topics)} most popular topics")
print(f"Query execution time: {query_time:.4f} seconds")
if popular_topics:
    print("\nPopular topics:")
    for i, topic in enumerate(popular_topics, 1):
        print(f"{i}. Topic: {topic['name']}, Post Count: {topic['postCount']}")

print("\n=== Testing Query 7: Posts of all friends in last 24 hours ===")
start_time = time.time()
friend_recent_posts = get_friend_posts_last_24_hours(sample_user_id)
query_time = time.time() - start_time
print(f"Found {len(friend_recent_posts)} recent posts by friends of user {sample_user_id}")
print(f"Query execution time: {query_time:.4f} seconds")
if friend_recent_posts:
    print("\nSample friend recent post:")
    pp.pprint(friend_recent_posts[0])

print("\nAll query tests completed successfully!")