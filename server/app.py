from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    db_messages = Message.query.all()
    if db_messages:
        if request.method == 'GET':
            messages = [message.to_dict() for message in db_messages]
            response = make_response(messages, 200)
            return response
        elif request.method == 'POST':
            message = Message(username=request.json.get("username"), 
                               body=request.json.get("body"))
            db.session.add(message)
            db.session.commit()
            message_dict = message.to_dict()
            response = make_response(message_dict, 201)
            return response
    else:
        message = {'message': 'error retrieving messages from db'}
        return make_response(message, 200)
    

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id): 
    message = Message.query.filter_by(id=id).first()
    if message:
        if request.method == 'PATCH':
            for attr in request.json:
                setattr(message, attr, request.json.get(attr))
            db.session.add(message)
            db.session.commit()
            message_dict = message.to_dict()
            response = make_response(message_dict, 200)
            return response
        elif request.method == 'DELETE':
            db.session.delete(message)
            db.session.commit()
            message = {"message": "message succesfully deleted"}
            response = make_response(message, 200)
    else:
        body = {"Error": f"error retreiving message at {id}"}
        response = make_response(body, 200)
        return response

    return ''

if __name__ == '__main__':
    app.run(port=5555)
