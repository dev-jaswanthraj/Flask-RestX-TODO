from flask_restx import fields

class datefun(fields.Raw):
    def format(self, date):
        return date.strftime("%d | %m | %Y")

user_resource = {
    "id": fields.Integer,
    "name": fields.String
}
todo_resource = {
    "content": fields.String,
    "id": fields.Integer,
    "completed": fields.Boolean,
    "date": datefun,
    "user": fields.Nested(user_resource)
}

