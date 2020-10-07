
API_CONFIG = {
    "host": "api.zoom.us",
    "key": "",
    "secret": "",
    "jwt_expires_in": 60
}

API_ENDPOINT = {
    "users": "/v2/users?status=active&page_size={page_size}&page_number=1",
    "meetings": "/v2/report/users/{userId}/meetings",
    "dashboard_meetings": "/v2/metrics/meetings"
}
