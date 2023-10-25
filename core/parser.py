from flask_restx import reqparse

#For login request data
login_data = reqparse.RequestParser()
login_data.add_argument("name", type = str)
login_data.add_argument("password", type = str)

#Request Pasrser for Todo
todo_data = reqparse.RequestParser()
todo_data.add_argument("content", type = str)
todo_data.add_argument("completed", type = bool)
