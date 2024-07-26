import sys

message: str = sys.argv[1]
location: str = ""
for word in message.split():
    location += word[0]
print(location)
