# -*- coding: UTF-8 -*-
from app import app, db, models, api
from flask_restful import reqparse, Resource
from models import User as UserModel
from models import Address as AddressModel
from wxapp import create_token

# Todo
# shows a single todo item and lets you delete a todo item
class User(Resource):
    def get(self, openid):
        user = UserModel.query.filter_by(id=openid).first()
        retuser = user.to_dict() if user else ''
        return {'user': retuser}, 200

    def delete(self, openid):
        # abort_if_todo_doesnt_exist(todo_id)
        # del TODOS[todo_id]
        # return '', 204
        pass

    def put(self, openid):
        # args = parser.parse_args()
        # task = {'task': args['task']}
        # TODOS[todo_id] = task
        # return task, 201
        pass


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class UserList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user', type=dict, required = True,
                                    help='user information is missing')
        super(UserList, self).__init__()

    def get(self):
        # return TODOS
        user = UserModel.query.all()
        retuser = [u.to_dict() for u in user]
        return {'users': retuser}, 200

    def post(self):
        args = self.parser.parse_args()
        user = args['user']
        sql_body = models.User(id=user['id'], nickname=user['nickname'], 
                    default_region=user['default_region'])
        db.session.add(sql_body)
        db.session.commit()
        return {'user': user}, 201

class Address(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('consignee_phone', type=str, required = True,
                                    help='consignee_phone is missing')
        self.parser.add_argument('consignee_address', type=str, required = True,
                                    help='consignee_address is missing')
        self.parser.add_argument('consignee_name', type=str, required = True,
                                    help='consignee_name is missing')
        super(Address, self).__init__()

    def get(self, id):
        address = AddressModel.query.filter_by(id=id).first()
        retaddress = address.to_dict() if address else ''
        return {'address': retaddress}, 200

    def delete(self, id):
        address = AddressModel.query.filter_by(id=id).first()
        if address:
            db.session.delete(address)
            db.session.commit()
        return '', 204

    def put(self, id):
        address = self.parser.parse_args()
        sql_address = AddressModel.query.filter_by(id=id).first()
        if sql_address:
            for k,v in address.items():
                setattr(sql_address,k,v)
            db.session.commit()
        else:
            return {'message':'no data'},400
        return {'address': address}, 200

class Addresses(Resource):
    def get(self, openid):
        address = AddressModel.query.filter_by(openid=openid)
        retaddress = [u.to_dict() for u in address]
        return {'address': retaddress}, 200

class AddressList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('address', type=dict, required = True,
                                    help='address information is missing')
        super(AddressList, self).__init__()

    def get(self):
        # return TODOS
        address = AddressModel.query.all()
        retaddress = [u.to_dict() for u in address]
        return {'addresses': retaddress}, 200

    def post(self):
        args = self.parser.parse_args()
        address = args['address']
        sql_body = models.Address(openid=address['openid'], 
                    consignee_address=address['consignee_address'], 
                    consignee_phone=address['consignee_phone'],
                    consignee_name=address['consignee_name'])
        db.session.add(sql_body)
        db.session.commit()
        return {'address': address}, 201


class AuthToken(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('code', type=str, required = True,
                                    help='address information is missing')
        self.parser.add_argument('username', type=str, required = True,
                                    help='address information is missing')
        self.parser.add_argument('password', type=str, required = True,
                                    help='address information is missing')
        self.parser.add_argument('grant_type', type=str, required = True,
                                    help='address information is missing')
        self.parser.add_argument('auth_approach', type=str, required = True,
                                    help='address information is missing')
        super(AuthToken, self).__init__()

    # def get(self):
    #     # return TODOS
    #     address = AddressModel.query.all()
    #     retaddress = [u.to_dict() for u in address]
    #     return {'addresses': retaddress}, 200

    def post(self):
        args = self.parser.parse_args()
        is_validate, token = create_token(args)
        if not is_validate:
            return {'unauthorized':'Invalid token'}, 401
        return token, 201



api.add_resource(UserList, '/api/users')
api.add_resource(User, '/api/user/<string:openid>')
api.add_resource(AddressList, '/api/addresses')
api.add_resource(Addresses, '/api/addresses/<string:openid>')
api.add_resource(Address, '/api/address/<int:id>')

api.add_resource(AuthToken, '/api/auth/token')
