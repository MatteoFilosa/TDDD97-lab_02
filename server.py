from flask import Flask, jsonify, request
import binascii
import os
import database_helper

app = Flask(__name__)

app.debug = True

tokenDic = {
    "token": "",
    "email": ""
 }

@app.teardown_request
def after_request(exception):
    database_helper.disconnect_db()

@app.route('/user/signup', methods = ['PUT'])
def sign_up():
    json = request.get_json()
    if "email" in json and "password" in json and "firstname" in json and "familyname" in json and "gender" in json and "city" in json and "country" in json:
        if len(json['email']) < 30 and len(json['password']) > 5 and len(json['password']) < 30 and len(json['firstname']) < 30 and len(json['familyname']) < 30 and len(json['gender']) < 30 and len(json['city']) < 30 and len(json['country']) < 30:
            result = database_helper.create_user(json['email'], json['password'], json['firstname'], json['familyname'], json['gender'], json['city'], json['country'])
            if result == True:
                return "{}", 201
            else:
                return "{}", 500
        else:
            return "{}", 400
    else:
        return "{}", 400

@app.route('/user/signin', methods = ['POST'])
def sign_in():

    json = request.get_json()
    if "email" in json and "password" in json:
        if len(json['email']) < 30 and len(json['password']) < 30:
            result = database_helper.find_user(json['email'], json['password'])
            if result == True:
                token = binascii.hexlify(os.urandom(20)).decode()
                tokenDic["token"] = token
                tokenDic["email"] = json['email']
                print(tokenDic)
                database_helper.send_token(token)
                #jsonify token
                return jsonify({"token" : token}), 200
            else:
                return "{}", 500
        else:
            return "{}", 400
    else:
        return "{}", 400

@app.route('/user/signout', methods = ['POST'])
def sign_out():

    json = request.get_json()
    if "token" in json:
        if json['token']==tokenDic['token'] and tokenDic['email']!="":
            tokenDic['token'] = ""
            tokenDic['email'] = ""
            return "{}", 200
        else:
            return "{}", 400
    else:
        return "{}", 400

@app.route('/user/changepassword', methods = ['PUT'])
def change_password():

    json = request.get_json()
    if "token" in json and "password" in json and "newpassword" in json:
        if len(json['token'])< 30 and len(json['password']) < 30 and len(json['newpassword']) < 30:
            result = database_helper.new_password(tokenDic['token'], json['password'], json['newpassword'])
            if result == True:
                return "{}", 201
            else:
                return "{}", 500
        else:
            return "{}", 400
    else:
        return "{}", 400

@app.route('/user/postmessage', methods = ['PUT'])
def post_message():

    json = request.get_json()
    if "token" in json and "message" in json and "email" in json:
        if json['token']==tokenDic['token'] and len(json['message']) < 150:
            result = database_helper.message_help(json['token'], json['message'], json['email'])
            if result == True:
                return "{}", 201
            else:
                return "{}", 500
        else:
            return "{}", 400
    else:
        return "{}", 400

@app.route('/user/getuserdatabytoken', methods = ['GET'])
def get_user_data_by_token():

    json = request.headers.get("token")
    print(json)
    if json==tokenDic['token']:
        rows = database_helper.retrieve_data_token(json)
        if rows != False:
            result = []
            for row in rows:
                result.append({"email": row[0], "firstname" : row[1], "lastname" : row[2], "gender" : row[3], "city" : row[4], "country" : row[5]})
            return jsonify(result), 200
        else:
            return "{}", 500
    else:
        return "{}", 400

@app.route('/user/getuserdatabyemail', methods = ['GET'])
def get_user_data_by_email():

    jsonToken = request.headers.get("token")
    jsonEmail = request.get_json()
    if jsonToken==tokenDic['token'] and "email" in jsonEmail and len(jsonEmail) < 30:
        rows = database_helper.retrieve_data_email(jsonToken, jsonEmail['email'])
        if rows != False:
            result = []
            for row in rows:
                result.append({"email": row[0], "firstname" : row[1], "lastname" : row[2], "gender" : row[3], "city" : row[4], "country" : row[5]})
            return jsonify(result), 200
        else:
            return "{}", 500
    else:
        return "{}", 400

@app.route('/user/getusermessagesbytoken', methods = ['GET'])
def get_user_messages_by_token():

    json = request.headers.get("token")
    if json==tokenDic['token']:
        result = database_helper.retrieve_messages_token(json)
        if result != False:
            return jsonify({"result" : result}), 200
        else:
            return "{}", 500
    else:
        return "{}", 400

@app.route('/user/getusermessagesbyemail', methods = ['GET'])
def get_user_messages_by_email():

    jsonToken = request.headers.get("token")
    jsonEmail = request.get_json()
    if jsonToken==tokenDic['token'] and "email" in jsonEmail and len(jsonEmail) < 30:
        result = database_helper.retrieve_messages_email(jsonToken, jsonEmail['email'])
        if result != False:
            return jsonify({"result" : result}), 200
        else:
            return "{}", 500
    else:
        return "{}", 400
