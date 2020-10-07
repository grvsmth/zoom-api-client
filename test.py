"""
Test script for accessing the Zoom API
"""

from http.client import HTTPSConnection
from json import dumps
from time import time

import jwt
import config

JWT_ALGORITHM = 'HS256'

def makeJWT(config):
    exp = int(time()) + config.API_EXPIRES_IN

    payload = {
        "iss": config.API_KEY,
        "exp": exp
    }

    encoded = jwt.encode(payload, config.API_SECRET, algorithm=JWT_ALGORITHM)

    return(encoded.decode('utf-8'))

def fetch(endpoint):
    jwt = makeJWT(config)
    conn = HTTPSConnection(config.API_HOST)

    headers = {
        'authorization': "Bearer " + jwt,
        'content-type': "application/json"
    }

    conn.request("GET", endpoint, headers=headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")

users = fetch(config.USERS_ENDPOINT)

print(users)

userId = "-5VUc4eUTliii3rAVfzeIw"

meetings_endpoint = config.MEETINGS_ENDPOINT.format(userId=userId)

meetings = fetch(meetings_endpoint)

print(meetings)
