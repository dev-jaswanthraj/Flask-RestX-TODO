from core import api, db
from flask_restx import Resource, marshal
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from .models import User, Todo
from .parser import login_data, todo_data
from .serializer import todo_resource
import datetime


class Login(Resource):
    def get(self):
        data = login_data.parse_args()
        user = User.query.filter_by(name = data['name']).first()
        if user:
            if user.password == data['password']:
                access_token = create_access_token(identity=data['name'])
                return {'token': access_token}, 200
            return {'msg': "Incorrect Username or Password"}, 305
        return {'msg': "User Not Found"}, 404

class VTodo(Resource):
    @jwt_required() 
    def get(self):
        cur_user = get_jwt_identity()
        cur_user = User.query.filter_by(name = cur_user).first()
        todo_items = Todo.query.filter_by(user_id = cur_user.id).all()
        return marshal(todo_items, todo_resource), 200
    @jwt_required() 
    def post(self):
        cur_user = get_jwt_identity()
        cur_user = User.query.filter_by(name = cur_user).first()
        req = todo_data.parse_args()
        todo_item = Todo(
            content = req['content'],
            user_id = cur_user.id,
            date = datetime.date.today()
        )
        db.session.add(todo_item)
        db.session.commit()
        return marshal(todo_item, todo_resource), 201

class SVTodo(Resource):
    @jwt_required()
    def get(self, id):
        todo_item = Todo.query.get(id)
        if not todo_item:
            return {"msg": "Item Not Found"}, 404
        user = User.query.get(todo_item.user_id)
        if user.name == get_jwt_identity():
            return marshal(todo_item, todo_resource), 200
        return {"msg": "Not Allowed"}, 403

    @jwt_required()
    def delete(self, id):
        todo_item = Todo.query.get(id)
        if not todo_item:
            return {"msg": "Item Not Found"}, 404
        user = User.query.get(todo_item.user_id)
        if user.name == get_jwt_identity():
            db.session.delete(todo_item)
            db.session.commit()
            return marshal(todo_item, todo_resource), 200
        return {"msg": "Not Allowed"}, 403
    
    @jwt_required()
    def put(self, id):
        todo_item = Todo.query.get(id)
        if not todo_item:
            return {"msg": "Item Not Found"}, 404
        if todo_item.completed:
            return {"msg": "Task Already Completed"}, 200
        user = User.query.get(todo_item.user_id)
        if user.name == get_jwt_identity():
            todo_item.completed = True
            db.session.commit()
            return marshal(todo_item, todo_resource), 201
        return {"msg": "Not Allowed"}, 403

class CVTodo(Resource):
    @jwt_required() 
    def get(self):
        cur_user = get_jwt_identity()
        cur_user = User.query.filter_by(name = cur_user).first()
        todo_items = Todo.query.filter_by(user_id = cur_user.id, completed = True).all()
        return marshal(todo_items, todo_resource), 200

class UCVTodo(Resource):
    @jwt_required() 
    def get(self):
        cur_user = get_jwt_identity()
        cur_user = User.query.filter_by(name = cur_user).first()
        todo_items = Todo.query.filter_by(user_id = cur_user.id, completed = False).all()
        return marshal(todo_items, todo_resource), 200

api.add_resource(Login, "/login")
api.add_resource(VTodo, "/Todo")
api.add_resource(SVTodo, "/Todo/<int:id>")
api.add_resource(CVTodo, "/Todo/Completed")
api.add_resource(UCVTodo, "/Todo/Uncompleted")