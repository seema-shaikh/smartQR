from flask import jsonify

def emailRequiredResponse():
    return jsonify({'message': 'Email is required'}), 400

def existingUserResponse():
    response = {'Status': '400', 'Response': 'Already existing user! Try Logging in.'}
    return jsonify(response), 400

def errorResponse(e,status=400):
    response = {'Status': status, 'Response': str(e)}
    return jsonify(response), status
