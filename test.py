"""
Test script for accessing the Zoom API
"""

from http.client import HTTPSConnection
from json import loads, dumps
from random import randint
from time import time

import jwt
from config import API_CONFIG, API_ENDPOINT

JWT_ALGORITHM = 'HS256'
PAGE_SIZE = 30

"""
Create a new Javascript Web Token (JWT) for authenticating to the
Zoom API servers, based on the information in a config dict
"""
def makeJWT(config):
    exp = int(time()) + config["jwt_expires_in"]

    payload = {
        "iss": config["key"],
        "exp": exp
    }

    encoded = jwt.encode(payload, config["secret"], algorithm=JWT_ALGORITHM)

    return(encoded.decode('utf-8'))


"""
Given a config dict (with a hostname and JWT info) an API endpoint, fetch the 
"""
def fetch(config, endpoint):
    jwt = makeJWT(config)
    conn = HTTPSConnection(config["host"])

    headers = {
        'authorization': "Bearer " + jwt,
        'content-type': "application/json"
    }

    conn.request("GET", endpoint, headers=headers)

    res = conn.getresponse()
    data = res.read()

    return loads(data.decode("utf-8"))


"""
Example queries
"""

# Get a page of users
response = fetch(API_CONFIG, API_ENDPOINT["users"].format(page_size=PAGE_SIZE))
print(response["users"])

# Get the meetings for a user
# test_index = randint(0, PAGE_SIZE-1)
test_index = 25
test_user = response["users"][test_index]

print(
    "Showing meetings for user {test_index}: {first_name} {last_name}".format(
        test_index=test_index,
        first_name=test_user["first_name"],
        last_name=test_user["last_name"]
    )
)

meetings_endpoint = API_ENDPOINT["meetings"].format(userId=test_user["id"])
user_meetings = fetch(API_CONFIG, meetings_endpoint)
print(user_meetings)


# Get a page of the daily meetings report
meetings_report = fetch(API_CONFIG, API_ENDPOINT["dashboard_meetings"])

print(meetings_report)
