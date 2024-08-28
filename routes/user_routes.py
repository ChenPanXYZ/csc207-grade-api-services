from routes.imports import *

user_apis = Blueprint('user_apis', __name__)

@user_apis.route('/signUp', methods=['GET'])
@limiter.limit("3600/minute")
def sign_up():
    # get parameters from request
    username = request.args.get('username') if 'username' in request.args else None
    print(username)

    # generate a random api token.
    # generate deployment api token.

    # first, see if this utorid is associated with a token.
    the_doc = USER.find_one({
        "username": username
    })
    if the_doc:
        return {
            "status_code": 409,
            "message": "Someone took this username. If you are not the owner of this username or you forgot your password, please sign up with a different username and use the new password instead."
        }, 409
    def generate_password(length=32):
        # Define the characters that can be used in the password
        characters = string.ascii_letters + string.digits

        # Generate a random password using the specified length
        password = ''.join(random.choice(characters) for _ in range(length))

        return password

    password = generate_password()

    # save to DB.
    USER.insert_one({
        "username": username,
        "password": password,
        "token": password
    })

    # return with token
    return {
        "status_code": 200,
        "message": "User signed up successfully. Please copy and paste the environment_variables into your intelij java running environment variables.",
        "token": password, 
        "environment_variables": f'token={password}'
    }


@user_apis.route('/getMyData', methods=['GET'])
def get_my_data():
    # load utorid from params.
    username = get_username_by_api_token(request.headers.get('token'))

    # get all grades.
    grades = GRADE.find({
        "username": username
    })
    team = TEAM.find_one({
        "members": {"$in": [username]}
    })

    # get team members' grades.
    team_members = team['members']

    team_info = []

    for team_member in team_members:
        the_doc = USER.find_one({
            "username": team_member
        })
        team_info.append({
            "teammate": team_member,
            "grades": GRADE.find({
                "username": team_member
            })
        })



    # return the team members.
    return {
        "status_code": 200,
        "grades": json.loads(json_util.dumps(grades)),
        "team_info": json.loads(json_util.dumps(team_info)),
    }, 200



# For TAs or instructors to get all data.
# See the SUPER_TOKEN from config.py. By default it is ilovecsc207
@user_apis.route('/getAllData', methods=['GET'])
def get_all_data():
    from config import SUPER_TOKEN
    token = request.headers.get('token') if 'token' in request.headers else None
    # check if token equals to SUPER_TOKEN

    if token != SUPER_TOKEN:
        return {
            "status_code": 401,
            "message": "Unauthorized access"
        }, 401

    # get all grades.
    grades = GRADE.find({
    })
    teams = TEAM.find({
    })

    # return the team members.
    return {
        "status_code": 200,
        "grades": json.loads(json_util.dumps(grades)),
        "teams": json.loads(json_util.dumps(teams)),
    }, 200