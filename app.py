from flask import Flask, request, jsonify, send_file
from mongo import client
from bson import Binary
from bson.objectid import ObjectId
import base64
import io

app = Flask(__name__)

@app.route('/')
def apiStatus():
    result = "Hi! Welcome to Quickie backend"
    return jsonify(result)

@app.route('/create', methods=['POST'])
def createUser():

    dbs = client.quickie
    collection = dbs.users

    email = request.args.get('email')
    password = request.args.get('password')

    if(email is None or password is None):
        data = {'status': False, 'message': 'Invalid data'}
        return jsonify(data)
    elif (len(email) <= 0 or len(password) <= 0):
        data = {'status': False, 'message': 'Length is too short'}
        return jsonify(data)
    elif (checkExistence(email) is False):
        query = {
            'email': email,
            'password': password
        }
        collection.insert_one(query)
        data = {"status" : True, "message" : "User created successfully"}
        return jsonify(data)
    else:
        data = {"status" : False, "message" : "User already exists"}
        return jsonify(data)
    
@app.route('/authenticate', methods=['GET'])
def authenticateUser():
    
    dbs = client.quickie
    collection = dbs.users

    email = request.args.get('email')
    password = request.args.get('password')
    print(email + " " + password)
    query = {"email": email, "password": password}

    result = collection.find_one(query)
    if result is None:
        data = {"status" : False, "message": "user not found"}
        return jsonify(data)
    else :
        data = {"status" : True, "message": "user found"}
        return jsonify(data)

@app.route('/upload', methods=['POST'])
def upload_image():

    dbs = client.quickie
    collection = dbs.users

    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            # Convert image to binary format
            image_binary = Binary(image.read())

            # Save image to MongoDB
            image_id = str(collection.insert_one({'image': image_binary}).inserted_id)

            return jsonify({'status': 'success', 'image_id': image_id})
    
    return jsonify({'status': 'failed', 'message': 'Image upload failed.'})

@app.route('/api/images/<image_id>', methods=['GET'])
def get_image(image_id):

    dbs = client.quickie
    collection = dbs.users

    image_data = collection.find_one({'_id': ObjectId(image_id)})
    if image_data:
        image_binary = image_data['image']
        return send_file(io.BytesIO(image_binary), mimetype='image/jpeg')
    
    return jsonify({'status': 'failed', 'message': 'Image not found.'})

def checkExistence(email):
    dbs = client.cleanHires
    collection = dbs.users

    query = {"email" : email}
    response = collection.count_documents(query)
    if(response == 0):
        return False
    else :
        return True
    
if __name__ == '__main__':
    app.run(debug=True)
