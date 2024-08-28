from connection import USER
# Helper function to get the username by api token.
def get_username_by_api_token(api_token):
    the_doc = USER.find_one({
        "token": api_token
    })
    if the_doc:
        return the_doc['username']
    return None