from flask_restx import fields

user_resource = {
    "id": fields.Integer,
    "name": fields.String
}
todo_resource = {
    "content": fields.String,
    "id": fields.Integer,
    "completed": fields.Boolean,
    "user": fields.Nested(user_resource)
}

