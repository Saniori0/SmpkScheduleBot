from config import redis
from modules import parser

redis.delete("groups")

group = parser.parseGroupSchedule("cg63.htm")

print(group)