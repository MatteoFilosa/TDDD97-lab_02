from flask import Flask, jsonify, request
import database_helper

app = Flask(__name__)

app.debug = True

@app.teardown_request
def after_request(exception):
    database_helper.disconnect_db()

@app.route('/user/signup', methods = ['PUT'])
def sign_up():
    json = request.get_json()
    if "email" in json and "password" in json and "firstname" in json and "familyname" in json and "gender" in json and "city" in json and "country" in json:
        if len(json['email']) < 100 and len(json['password']) < 100 and len(json['firstname']) < 100 and len(json['familyname']) < 100 and len(json['gender']) < 100 and len(json['city']) < 100 and len(json['country']) < 100:
            result = database_helper.create_user(json['email'], json['password'], json['firstname'], json['familyname'], json['gender'], json['city'], json['country'])
            if result == True:
                return "{}", 201
            else:
                return "{}", 500
        else:
            return "{}", 400
    else:
        return "{}", 400
