#!/bin/bash
# MongoDB sharded cluster setup script for Windows (Git Bash / WSL)

# Define base directory
BASE=~/mongodb
mkdir -p "$BASE/configserver" "$BASE/shard1" "$BASE/shard2" "$BASE/router"

# Start Config Server
mongod --configsvr --replSet configReplSet --dbpath "$BASE/configserver" --port 27019 --logpath "$BASE/configserver/config.log" &
sleep 5
mongo --port 27019 --eval 'rs.initiate({_id: "configReplSet", configsvr: true, members: [{_id: 0, host: "localhost:27019"}]})'

# Start Shard 1
mongod --shardsvr --replSet shard1ReplSet --dbpath "$BASE/shard1" --port 27020 --logpath "$BASE/shard1/shard1.log" &
sleep 5
mongo --port 27020 --eval 'rs.initiate({_id: "shard1ReplSet", members: [{_id: 0, host: "localhost:27020"}]})'

# Start Shard 2
mongod --shardsvr --replSet shard2ReplSet --dbpath "$BASE/shard2" --port 27021 --logpath "$BASE/shard2/shard2.log" &
sleep 5
mongo --port 27021 --eval 'rs.initiate({_id: "shard2ReplSet", members: [{_id: 0, host: "localhost:27021"}]})'

# Start Mongos Router
mongos --configdb configReplSet/localhost:27019 --port 27017 --logpath "$BASE/router/mongos.log" &
sleep 5

# Add shards to Mongos
mongo --port 27017 --eval 'sh.addShard("shard1ReplSet/localhost:27020"); sh.addShard("shard2ReplSet/localhost:27021");'
mongo --port 27017 --eval 'sh.enableSharding("social_network")'

# Shard the collections
mongo --port 27017 <<EOF
use social_network;

// Create sharded collections
db.createCollection("posts");
sh.shardCollection("social_network.posts", {userId: 1, createdAt: -1});

db.createCollection("friendships");
sh.shardCollection("social_network.friendships", {userId: 1});

db.createCollection("likes");
sh.shardCollection("social_network.likes", {postId: 1});

db.createCollection("comments");
sh.shardCollection("social_network.comments", {postId: 1});

// Create indexes
db.posts.createIndex({userId: 1, createdAt: -1});
db.posts.createIndex({topicId: 1, createdAt: -1});
db.posts.createIndex({likeCount: -1});
db.posts.createIndex({commentCount: -1});

db.comments.createIndex({userId: 1, createdAt: -1});
db.topics.createIndex({postCount: -1});

db.friendships.createIndex({userId: 1});
db.friendships.createIndex({friendId: 1});
EOF

echo "✅ MongoDB sharded cluster setup complete!"
