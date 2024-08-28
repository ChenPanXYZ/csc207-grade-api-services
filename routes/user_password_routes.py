from routes.imports import *

user_password_apis = Blueprint('user_password_apis', __name__)

# An API that creates a student document.
# The request body should be a JSON object with the following fields:
# username: the username of the student
# password: the password code
# additionalInformation: the additional information of the student

@user_password_apis.route('/user', methods=['POST'])
@limiter.limit("3600/minute")
def create_user():
    try:
        username = request.json['username'] if 'username' in request.json else None
        password = request.json['password'] if 'password' in request.json else None
        creation_time = request.json['creation_time'] if 'creation_time' in request.json else None

        if not username or not password:
            return {
                "status_code": 400,
                "message": "username, password, and creation_time are required."
            }, 400

        # check if the student document already exists
        # if exists, then modify.

        the_doc = USER.find_one({
            "username": username
        })

        if the_doc:
            return {
                "status_code": 409,
                "message": "User already exists."
            }, 409
        user_id = USER.insert_one({
            "username": username,
            "password": password,
            "additionalInformation": {}, # added createdAt
            "creation_time": creation_time
        }).inserted_id

        return {
            "status_code": 200,
            "message": "User created successfully."
        }, 200

    except PyMongoError as e:
        print(e)
        return {
            "status_code": 500,
            "message": "Error creating user."
        }, 500


@user_password_apis.route('/user', methods=['PUT'])
def change_password():
    try:
        username = request.json['username'] if 'username' in request.json else None
        password = request.json['password'] if 'password' in request.json else None

        if not username or not password:
            return {
                "status_code": 400,
                "message": "username, password are required."
            }, 400

        # check if the student document already exists
        # if exists, then modify.

        the_doc = USER.find_one_and_update({
            "username": username
        }, 
        {
            "$set": {
                "password": password
            }
        })
        return {
            "status_code": 200,
            "message": "User updated successfully."
        }, 200

    except PyMongoError as e:
        print(e)
        return {
            "status_code": 500,
            "message": "Error creating user."
        }, 500


@user_password_apis.route('/checkIfUserExists', methods=['GET'])
def check_if_user_exists():
    username = request.args.get('username') if 'username' in request.args else None

    # check if a user object with this username exist.

    the_doc = USER.find_one({
        "username": username
    })

    if the_doc:
        return {
            "status_code": 200,
            "message": "User exists"
        }, 200
    else:
        return {
            "status_code": 404,
            "message": "User does not exist"
        }, 404


# An API that returns a student document, it's a get request with the following path: grade/course/utorid
# The response body should be a JSON object with the following fields:
# status: a code
# message: "Student retrieved successfully" if the grade document is retrieved successfully, "Error retrieving grade" otherwise
# grade: the grade of the student
@user_password_apis.route('/user', methods=['GET'])
def get_user():
    try:
        username = request.args.get('username') if 'username' in request.args else None
        print(request.headers)
        the_doc = USER.find_one({
            "username": username,
        })
        if not the_doc:
            return {
                "status_code": 404,
                "message": "User not found."
            }, 404
        return {
            "status_code": 200,
            "message": "User retrieved successfully",
            "user": json.loads(json_util.dumps(the_doc))
        }, 200
    except PyMongoError as e:
        print(e)
        return {
            "status_code": 500,
            "message": "Error retrieving user"
        }, 500
    except Exception as e:
        print("error")
        print(e)
        return {
            "status_code": 500,
            "message": "Error retrieving user"
        }, 500
    