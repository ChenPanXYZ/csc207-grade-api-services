from routes.imports import *

team_apis = Blueprint('team_apis', __name__)


# form a team.
@team_apis.route('/team', methods=['POST'])
def form_team():
    name = request.json['name'] if 'name' in request.json else None
    username = get_username_by_api_token(request.headers.get('token'))

    if not name:
        return {
            "status_code": 400,
            "message": "Name are required"
        }, 400

    # check if the name starts with csc207.
    if not name.startswith('csc207'):
        return {
            "status_code": 400,
            "message": "The team name must start with csc207"
        }, 400

    # check if the team already exists.
    the_doc = TEAM.find_one({
        "name": name
    })
    if the_doc:
        return {
            "status_code": 409,
            "message": "Team already exists"
        }, 409

    # check if the utorid is already in a team.
    the_doc = TEAM.find_one({
        "members": {"$in": [username]}
    })
    if the_doc:
        return {
            "status_code": 400,
            "message": "You are already in a team. You can't form a new team until you leave your current team."
        }, 400
    
    # create a team.
    result = TEAM.insert_one({
        "name": name, 
        "members": [username]
    })

    # Retrieve the inserted document using its _id
    new_team = TEAM.find_one({"_id": result.inserted_id})

    # make the_doc a json object with name and members.

    return {
        "status_code": 200,
        "message": f'Team: {name} created successfully',
        "team": json.loads(json_util.dumps(new_team))
    }, 200


# join a team.
@team_apis.route('/team', methods=['PUT'])
def join_team():
    name = request.json['name'] if 'name' in request.json else None
    username = get_username_by_api_token(request.headers.get('token'))

    if not name:
        return {
            "status_code": 400,
            "message": "Name are required"
        }, 400

    # check if the team already exists.
    the_doc = TEAM.find_one({
        "name": name
    })
    if not the_doc:
        return {
            "status_code": 404,
            "message": "Team doesn't exist."
        }, 404

    # check if the utorid is already in a team.
    the_doc = TEAM.find_one({
        "members": {"$in": [username]}
    })
    if the_doc:
        return {
            "status_code": 400,
            "message": "You are already in a team"
        }, 400
    # make the_doc a json object with name and members.
    TEAM.update_one({
        "name": name
    }, {
        "$push": {
            "members": username
        }
    })

    return {
        "status_code": 200,
        "message": f'Joined team: {name} successfully'
    }, 200


# leave a team
@team_apis.route('/leaveTeam', methods=['PUT'])
def leave_team():
    # load utorid.
    username = get_username_by_api_token(request.headers.get('token'))


    # check if the utorid is already in a team.
    the_doc = TEAM.find_one({
        "members": {"$in": [username]}
    })

    if not the_doc:
        return {
            "status_code": 400,
            "message": "You are not in a team"
        }, 400

    # remove the utorid from the team. But if the team only has one member, delete the team.
    if len(the_doc['members']) == 1:
        TEAM.delete_one({
            "_id": the_doc['_id']
        })
    else:
        TEAM.update_one({
            "_id": the_doc['_id']
        }, {
            "$pull": {
                "members": username
            }
        })

    return {
        "status_code": 200,
        "message": "You have left the team"
    }, 200

# get my team members
@team_apis.route('/team', methods=['GET'])
def get_my_team():
    # load utorid from params.
    username = get_username_by_api_token(request.headers.get('token'))


    # check if the utorid is in a team.

    the_doc = TEAM.find_one({
        "members": {"$in": [username]}
    })

    if not the_doc:
        return {
            "status_code": 404,
            "message": "You are not in a team"
        }, 404

    # return the team members.
    return {
        "status_code": 200,
        "message": "Team retrieved successfully",
        "team": json.loads(json_util.dumps(the_doc))
    }, 200