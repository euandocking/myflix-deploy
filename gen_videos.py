import pymongo
import os
import random
import socket
from faker import Faker

# Install the required libraries using:
# pip install pymongo faker

hostname = socket.gethostname()

# Connect to the video catalog MongoDB instance
video_client = pymongo.MongoClient(f'mongodb://{hostname}:7000')
video_database = video_client["videocatalog"]
video_collection = video_database["videos"]

# Connect to the user MongoDB instance (replace with your actual connection details)
user_client = pymongo.MongoClient(f'mongodb://{hostname}:7000')
user_database = user_client["userauth"]
user_collection = user_database["users"]

# Create a Faker instance
fake = Faker()

# List of thumbnail URLs
thumbnail_urls = [
    "https://images.pexels.com/photos/9162803/pexels-photo-9162803.jpeg?auto=compress&cs=tinysrgb&w=800&lazy=load",
    "https://images.pexels.com/photos/2167039/pexels-photo-2167039.jpeg?auto=compress&cs=tinysrgb&w=800&lazy=load",
    "https://images.pexels.com/photos/16861541/pexels-photo-16861541/free-photo-of-arbres.jpeg?auto=compress&cs=tinysrgb&w=800&lazy=load",
    "https://images.pexels.com/photos/18898418/pexels-photo-18898418/free-photo-of-close-up-of-a-branch-with-green-and-yellow-leaves.jpeg?auto=compress&cs=tinysrgb&w=800&lazy=load",
    "https://images.pexels.com/photos/5391172/pexels-photo-5391172.jpeg?auto=compress&cs=tinysrgb&w=800&lazy=load",
    "https://images.pexels.com/photos/17848880/pexels-photo-17848880/free-photo-of-close-up-of-flower-in-woman-hand.jpeg?auto=compress&cs=tinysrgb&w=800&lazy=load",
    "https://images.pexels.com/photos/19738565/pexels-photo-19738565/free-photo-of-grand-central-madison.jpeg?auto=compress&cs=tinysrgb&w=800&lazy=load",
    "https://images.pexels.com/photos/19869392/pexels-photo-19869392/free-photo-of-dolomiti.jpeg?auto=compress&cs=tinysrgb&w=800&lazy=load",
    "https://images.pexels.com/photos/19877105/pexels-photo-19877105/free-photo-of-mong-c.jpeg?auto=compress&cs=tinysrgb&w=800&lazy=load"
]

# List of video URLs
video_urls = [
    "https://player.vimeo.com/progressive_redirect/playback/885476389/rendition/360p/file.mp4?loc=external&oauth2_token_id=1747418641&signature=7476713e9d7f227590b2aeb7509d6a9be5810c497dcbe559bd1e8899b4a9a902",
    "https://player.vimeo.com/progressive_redirect/playback/901565269/rendition/360p/file.mp4?loc=external&oauth2_token_id=1747418641&signature=6b7519440b4697a6c1f9f955c0c9a2349f4431c842e3b5a8e39567c1e993ea08",
    "https://player.vimeo.com/progressive_redirect/playback/885329387/rendition/360p/file.mp4?loc=external&oauth2_token_id=1747418641&signature=17f9f99525ffd5c64c254c8a1383ef0b29a0653eb9d0833e9439a10832f17ac2",
    "https://player.vimeo.com/external/625578943.sd.mp4?s=b5d0014fc8a58da88476401eb41637c461a9ac28&profile_id=164&oauth2_token_id=57447761",
    "https://player.vimeo.com/progressive_redirect/playback/899246570/rendition/540p/file.mp4?loc=external&oauth2_token_id=1747418641&signature=40dde4d43100a4ef1b77b713dee18a003757a7748ffab1cfbddce2818c818283",
    "https://player.vimeo.com/progressive_redirect/playback/839110727/rendition/360p/file.mp4?loc=external&oauth2_token_id=57447761&signature=b70e971443f1e948b459b3d6c4608c959301182875cdde7e88cd449445defcda",
    "https://player.vimeo.com/external/559095856.sd.mp4?s=e26678dab640522393c262d670ab497d1fd31585&profile_id=165&oauth2_token_id=57447761",
    "https://player.vimeo.com/external/499163955.sd.mp4?s=0c89bc5df95d06724809fc2161e8310966b0eb45&profile_id=165&oauth2_token_id=57447761",
    "https://player.vimeo.com/external/656924687.hd.mp4?s=287dedde8ba9a99e9fd193edaad02921b4d660fb&profile_id=174&oauth_token_id=57447761",
    "https://player.vimeo.com/progressive_redirect/playback/895130985/rendition/360p/file.mp4?loc=external&oauth2_token_id=1747418641&signature=d6a3bf71a0c2ac4c18493963410a63386c894aba941c1e1211dac9cc7e1e2d7c",

    # Add more video URLs as needed
]

# Function to generate fake video data with a random number of user ratings
def generate_fake_video_data(index, users):
    title = f"title_{index}"
    description = fake.paragraph()
    
    # Randomly select a thumbnail URL
    thumbnail_url = random.choice(thumbnail_urls)
    
    # Randomly select a video URL from the list
    video_url = random.choice(video_urls)
    
    categories = random.sample(["Action", "Comedy", "Romance", "Drama", "Sci-Fi", "Thriller"], k=random.randint(1, 3))

    # Generate a random subset of users and corresponding ratings for the video
    num_ratings = random.randint(1, len(users))
    user_ratings = random.sample(users, k=num_ratings)
    user_ratings = [{"user": user["_id"], "rating": random.randint(1, 5)} for user in user_ratings]

    video_data = {
        "title": title,
        "description": description,
        "thumbnailUrl": thumbnail_url,
        "videoUrl": video_url,
        "categories": categories,
        "userRatings": user_ratings
    }

    return video_data

# Number of videos to generate
num_videos = 100

# Retrieve users from the user collection
users = list(user_collection.find({}, {"_id": 1}))

# Populate the video catalog MongoDB collection with fake video data and a random number of user ratings
for i in range(num_videos):
    video_data = generate_fake_video_data(i, users)
    video_collection.insert_one(video_data)

print(f"{num_videos} fake videos with a random number of user ratings inserted into the video catalog MongoDB.")