import redis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST= os.getenv("REDIS_HOST","redis")
REDIS_PORT = int(os.getenv("REDIS_PORT","6379"))

client = redis.Redis(host=REDIS_HOST,port=REDIS_PORT,decode_responses=True)

def get_cache(key:str):
    return client.get(key)

def set_cache(key:str,value:str,ttl:int=300):
    client.setex(key,ttl,value)
