from routes.imports import *

grade_apis = Blueprint('grade_apis', __name__)

# # An API that returns a grade document, it's a get request with the following path: grade/course/utorid
# # The response body should be a JSON object with the following fields:
# # status: a code
# # message: "Grade retrieved successfully" if the grade document is retrieved successfully, "Error retrieving grade" otherwise
# # grade: the grade of the student
@grade_apis.route('/grade', methods=['GET'])
def get_grade():
    try:
        username = request.args.get('username') if 'username' in request.args else None
        if not username or username == "":
            username = get_username_by_api_token(request.headers.get('token'))

        course = request.args.get('course') if 'course' in request.args else None

        if not course:
            grades = GRADE.find({
                "username": username
            })
            return {
                "status_code": 200,
                "message": "Grades retrieved successfully",
                "grades": json.loads(json_util.dumps(grades))
            }, 200
        else:
            the_doc = GRADE.find_one({
                "username": username,
                "course": course
            })
            if not the_doc:
                return {
                    "status_code": 404,
                    "message": "Grade not found or at least one of your teammates doesn't have the grade for this course (double check with your teammates on what course names they used to log)"
                }, 404
            return {
                "status_code": 200,
                "message": "Grade retrieved successfully",
                "grade": json.loads(json_util.dumps(the_doc))
            }, 200
    except PyMongoError as e:
        print(e)
        return {
            "status_code": 500,
            "message": "Error retrieving grade"
        }, 500
    except Exception as e:
        print("error")
        print(e)
        return {
            "status_code": 500,
            "message": "Error retrieving grade"
        }, 500



# An API that creates a grade document.
# The request body should be a JSON object with the following fields:
# utorid: the utorid of the student
# course: the course code
# grade: the grade of the student
# The response body should be a JSON object with the following fields:
# status: a code
# message: "Grade created successfully" if the grade document is created successfully, "Error creating grade" otherwise
# id: the id of the grade document created
@grade_apis.route('/grade', methods=['POST'])
def create_grade():
    try:
        course = request.json['course'] if 'course' in request.json else None
        grade = request.json['grade'] if 'grade' in request.json else None
        print(request.headers.get('token'))
        username = get_username_by_api_token(request.headers.get('token'))
        print(username)

        if not username or not course or not grade:
            return {
                "status_code": 400,
                "message": "username, course, and grade are required"
            }, 400

        def is_integer(s):
            try:
                int(s)
                return True
            except ValueError:
                return False
        
    
        the_doc = USER.find_one({
            "username": username
        })
        # check if exist, if not, return 403.

        if not the_doc:
            return {
                "status_code": 403,
                "message": "Invalid token or username"
            }, 403
        
        # check if the grade is valid.
        if not is_integer(grade) or int(grade) < 0 or int(grade) > 100:
            return {
                "status_code": 400,
                "message": "grade must be an integer between 0 and 100"
            }, 400
        grade = int(grade)

        # check if the grade document already exists

        the_doc = GRADE.find_one({
            "username": username,
            "course": course
        })
        if the_doc:
            return {
                "status_code": 409,
                "message": "Grade already exists"
            }, 409
        grade_id = GRADE.insert_one({
            "username": username,
            "course": course,
            "grade": grade
        }).inserted_id
        return {
            "status_code": 200,
            "message": "Grade created successfully",
            "id": str(grade_id)
        }, 200
    except PyMongoError as e:
        print(e)
        return {
            "status_code": 500,
            "message": "Error creating grade"
        }, 500


