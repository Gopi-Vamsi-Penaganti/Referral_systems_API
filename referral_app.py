from flask import Flask
from flask import Flask, request, jsonify
app = Flask(__name__)
from queries import createNewUser, get_value, update_referer, withdraw

@app.route('/')
def hello_world():
    return 'Welcome to referral system!'

@app.route('/login', methods=["POST"])
def login():
    '''
        input_json fields ["phonenum", "name", "referral_code": optional]
    '''
    input_json = request.get_json(force=True) 
    print(input_json)
    #  if no referral code --> create user
    if "referral_code" not in input_json.keys():
        response = createNewUser(data=input_json)
        return response 
    else:
        response = get_value(value_name= "ReferralCode", value= input_json["referral_code"])
        if response["success"]:
            
            create_user_response = createNewUser(data=input_json)
            if not create_user_response["success"]:
                return create_user_response
            update_response = update_referer(params= response["row"], phone=input_json["phonenum"])
            if not update_response["success"]:
                return update_response["success"]
        
            return {
                "updated_response": update_response,
                "create_user_response": create_user_response
            }

        else:
            return response



@app.route('/withdraw-user', methods=["POST"])
def withdraw_user():
    '''
        input fields ["phonenum"]
    '''
    input_json = request.get_json(force=True) 
    response = withdraw(value=input_json["phonenum"])
    return response


@app.route('/get-user-details', methods=["get"])
def get_user_details():
    '''
        input fields ["phonenum"]
    '''
    input_json = request.get_json(force=True) 
    response = get_value(value_name= "PhoneNumber", value= input_json["phonenum"])
    if response["success"]:
        return{
            "success": True,
            "user-details": {
                                'PhoneNumber': response["row"][0],
                                'FullName': response["row"][1],
                                'ReferralCode': response["row"][2],
                                'ReferredNum': response["row"][3],
                                "ReferredContacts": response["row"][4],
                                'Balance': response["row"][5]

                            }
        }
    else:
        return response


if __name__=="__main__":
    app.run(debug=True)

    
