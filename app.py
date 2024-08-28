from flask import Flask, make_response
from flask import jsonify
from pymongo.errors import PyMongoError
from flask import request, abort
import json
from bson import json_util
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime
import random
import string

from routes.grade_routes import grade_apis
from routes.team_routes import team_apis
from routes.user_routes import user_apis
from routes.user_password_routes import user_password_apis

from connection import USER, GRADE, TEAM
from config import APIS_WITHOUT_TOKENS

app = Flask(__name__)


from limiter import limiter

limiter.init_app(app)
# Initialize the limiter
app.register_blueprint(grade_apis)
app.register_blueprint(team_apis)
app.register_blueprint(user_apis)
app.register_blueprint(user_password_apis)



@app.errorhandler(429)
def ratelimit_handler(e):
    return {
        "status_code": 429,
        "message": "Too many requests! Please check your code to make sure you are not sending more than 50 requests per minutes. Or wait a little bit for the server to come up."
    }, 429


# This function will be called before each request.
def api_key_middleware():
    if request.endpoint in APIS_WITHOUT_TOKENS: return # for these endpoints, no need to check the token.
    # for these endpoints, just need to check if the 
    token = request.headers.get("token")

    if not token:
        return {
            "status_code": 401,
            "message": "Authorization header is required"
        }, 401

    the_doc = USER.find_one({
        "token": token
    })

    if not the_doc:
        return {
            "status_code": 401,
            "message": "Invalid token."
        }, 401


    elif request.endpoint in ['grade_apis.get_grade', 'grade_apis.get_grades']:
        myUsername = the_doc['username']
        username = request.args.get('username') if 'username' in request.args else myUsername
        if username == myUsername:
            return
        else:
            # check if in the same team.
            the_doc = TEAM.find_one({
                "members": {"$in": [myUsername]}
            })

            if not the_doc or username not in the_doc['members']:
                return {
                    "status_code": 401,
                    "message": "You are not in the same team"
                }, 401
            else:
                return
    else:
        return
        
@app.before_request
def before_request():
    response = api_key_middleware()
    if response is not None:
        return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=20112, debug=True, threaded=True)
