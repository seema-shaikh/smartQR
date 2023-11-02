from json import dumps
from flask import jsonify, make_response, send_file

def emailRequiredResponse():
    return jsonify({'message': 'Email is required'}), 400

def unsuccessfulResponse():
    response = {'Status': '400', 'Response': 'Unsuccessful!'}
    return jsonify(response), 400

def existingUserResponse():
    response = {'Status': '400', 'Response': 'Already existing user! Try Logging in.'}
    return jsonify(response), 400

def successLoginResponse():
    response = {'Status': '200', 'Response': 'Logged in successfully!'}
    return jsonify(response)

def successSignupResponse():
    response = {'Status': '200', 'Response': 'Signed up successfully!'}
    return jsonify(response)

def failureLoginResponse():
    response = {'Status': '400', 'Response': 'Invalid credentials!'}
    return jsonify(response), 400

def userNotFoundResponse():
    response = {'Status': 400, "Response": "We cannot find an account with this email address!"}
    return jsonify(response), 400

def invalidRequestResponse():
    response = {'Status': '400', 'Response': 'Bad Request'}
    return jsonify(response), 400

def incompleteResponse(message):
    response = {'Status': '400', 'Response': 'Incomplete request! Missing param:'+str(message)}
    return jsonify(response), 400

def errorResponse(e,status=400):
    response = {'Status': status, 'Response': str(e)}
    return jsonify(response), status

def databaseErrorResponse():
    response = {'Status': '400', 'Response': 'Error occured with Database. Please try again!'}
    return jsonify(response), 400

def customResponse(keys_values,status=200):
    return jsonify(keys_values), status

def successUpdate(updated='Profile'):
    response = {'Status': '200', 'Response': updated.title()+' updated successfully!','updated':updated}
    return jsonify(response), 200

def successLogout():
    response = {'Status': '200', 'Response': 'Logged out successfully!'}
    return jsonify(response), 200

def validationError(error):
    response = {'Status': '400', 'Response': 'Error in validating input'}
    return jsonify(response), 400

def emailVerificationSent():
    response = {'Status': '200', 'Response': 'Verification link sent to registered email'}
    return jsonify(response)

def successUpload(document_name):
    response = {'Status': '200', 'Response': document_name.title() + ' uploaded successfully!'}
    return jsonify(response)

def successAddToCart():
    response = {'Status': '200', 'Response': 'Added to cart successfully!'}
    return jsonify(response)

def returnJSONArray(data,status=200,content_type='application/json'):
    return make_response(dumps(data)),status,{'Content-Type': content_type+'; charset=utf-8'}

def insufficientbalance():
    response = {'Status': '400', 'Response': 'Insufficient wallet balance! Add funds and try again.'}
    return jsonify(response), 400

def invalidFileFormat():
    response = {'Status' : '400' , 'Response' : 'File format is not allowed!'}
    return jsonify(response), 400

def unknownuser():
    response = {'Status': '403', 'Response': 'Unknown user'}
    return jsonify(response), 403

def unknownAgent():
    response = {'Status': '400', 'Response': 'Unknown agent'}
    return jsonify(response), 400

def emailVerificationSuccess():
    response = {'Status': '200', 'Response': 'Email verified successfully!'}
    return jsonify(response)


def expiredTokenResponse():
    response = {'Status': '400', 'Response': 'The token seems to have expired or already verified!'}
    return jsonify(response), 400


def schemaNotvalid():
    response = {'Status': '400', 'Response': 'Invalid schema of the input request! Please re-check the parameters.'}
    return jsonify(response), 400

def passwordNotFound():
    response = {'Status': '400', 'Response': 'Please fill in the password field'}
    return jsonify(response)

def customerAlreadyPresent():
    response = {'Status': '400', 'Response': 'You have already added this customer!'}
    return jsonify(response)

def sendFile(path):
    file= send_file(path, as_attachment=True, cache_timeout=0, attachment_filename="RFQ - Bulk Upload Template.xlsx")
    response= make_response(file, 200)
    return response
