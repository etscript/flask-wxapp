# -*- coding: UTF-8 -*-
from app import app, db, models, api
from flask_restful import reqparse, Resource, fields, marshal_with
from models import Address as AddressModel
from datetime import datetime 

class Address(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required = True,
                                    help='name information is missing')
        self.parser.add_argument('tel', type=str, required = True,
                                    help='tel information is missing')
        self.parser.add_argument('province', type=str, required = True,
                                    help='province information is missing')
        self.parser.add_argument('city', type=str, required = True,
                                    help='city information is missing')
        self.parser.add_argument('area', type=str, required = True,
                                    help='area information is missing')
        self.parser.add_argument('address', type=str, required = True,
                                    help='address information is missing')
        super(Address, self).__init__()

    def get(self, id):
        address = AddressModel.query.filter_by(id=id).first()
        retaddress = address.to_dict() if address else []
        return retaddress, 200

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
            setattr(sql_address,'updated_time',datetime.now())
            db.session.commit()
        else:
            return {'message':'no data'},400
        return address, 200

class Addresses(Resource):
    
    def get(self, openid):
        address = AddressModel.query.filter_by(openid=openid)
        retaddress = [u.to_dict() for u in address]
        return retaddress, 200
        #return {'address': openid}, 200

class AddressList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('mid', type=str, required = True,
                                    help='mid information is missing')
        self.parser.add_argument('name', type=str, required = True,
                                    help='name information is missing')
        self.parser.add_argument('tel', type=str, required = True,
                                    help='tel information is missing')
        self.parser.add_argument('province', type=str, required = True,
                                    help='province information is missing')
        self.parser.add_argument('city', type=str, required = True,
                                    help='city information is missing')
        self.parser.add_argument('area', type=str, required = True,
                                    help='area information is missing')
        self.parser.add_argument('address', type=str, required = True,
                                    help='address information is missing')
        super(AddressList, self).__init__()

    def get(self):
        # return TODOS
        address = AddressModel.query.all()
        retaddress = [u.to_dict() for u in address]
        return {'addresses': retaddress}, 200

    def post(self):
        address = self.parser.parse_args()
        sql_body = models.Address(openid=address['mid'], 
                    name=address['name'], 
                    tel=address['tel'],
                    province=address['province'], 
                    city=address['city'], 
                    area=address['area'],
                    address=address['address'],
                    created_time=datetime.now(), 
                    updated_time=datetime.now())
        db.session.add(sql_body)
        db.session.commit()
        return address, 200


api.add_resource(AddressList, '/api/addresses')
api.add_resource(Addresses, '/api/addresses/<string:openid>')
api.add_resource(Address, '/api/address/<int:id>')

