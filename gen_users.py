import bcrypt
import os
import socket
from pymongo import MongoClient

# Get the hostname using socket.gethostname()
hostname = socket.gethostname()
url = f'mongodb://{hostname}:7000'
db_name = 'userauth'  # Update with your database name
collection_name = 'users'

async def generate_random_users(count):
    users = []

    for i in range(count):
        username = f'user_{i}'
        password = f'pass_{i}'

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10))

        users.append({
            'username': username,
            'password': hashed_password.decode('utf-8'),
        })

    return users

async def insert_users_into_db(users):
    client = MongoClient(url, connect=True)

    try:
        db = client[db_name]
        collection = db[collection_name]

        result = collection.insert_many(users)
        
        if result.acknowledged:
            print(f"{len(result.inserted_ids)} users inserted into the database.")
        else:
            print("Insert operation not acknowledged.")
    finally:
        client.close()

async def main():
    number_of_users = 100

    users = await generate_random_users(number_of_users)
    await insert_users_into_db(users)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
