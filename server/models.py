from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


# "body": String.
# "username": String.
# "created_at": DateTime.
# "updated_at": DateTime.
# Don't forget to add default values for "created_at" and "updated_at"!
# (Hint - we discussed this in the Phase 3 Many-to-Many Relationships reading and gave an 
#  example in the Phase 4 Building a Get API Reading.)

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    username = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'Username: {self.username}, body:{self.body}'

