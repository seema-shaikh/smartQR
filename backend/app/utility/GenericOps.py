from flask import jsonify

def handle_content_type(request):
    content_type = request.content_type
    if content_type == 'application/json':
        data = request.get_json()
        return jsonify({'message': 'JSON data received'}), 200
    else:
        return 'Unsupported Media Type', 415