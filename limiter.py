from flask_limiter import Limiter
from flask import request, abort
from config import APIS_WITHOUT_TOKENS

# implement rate limit.
def get_client_key():
    # check if it is signUp or not. If it is, use get_remote_address instead.
    client_key = None
    if request.endpoint in APIS_WITHOUT_TOKENS: 
        client_key = 'global'
    else: 
        client_key = request.headers.get('token')

    return client_key

limiter = Limiter(
    key_func=get_client_key,
    default_limits=["60/minute"]
)