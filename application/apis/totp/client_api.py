from datetime import datetime
from http import client

from flask import request
from flask_jwt_extended import jwt_required
from flask_restplus import Namespace, Resource, reqparse

from application import db
from application.core.db.models.client_model import (ClientData,
                                                     ClientDataSchema)
from application.core.db.models.finger_print import FingerPrintData
from application.core.decorators import limiter
from application.core.totp import get_current_totp

nsApi = Namespace('client', description=' operations')

@nsApi.route('/fetch-data')
class GetClientDataList(Resource):
    @nsApi.doc('fetch list from database')
    @jwt_required()
    def get(self):
        schema = ClientDataSchema(many=True)
        data = ClientData.query.all()
        return schema.dump(data)
    
@nsApi.route('/get-data/<pk>')
class GetClientData(Resource):
    @nsApi.doc('fetch list from database')
    @jwt_required()
    def get(self, pk):
        schema = ClientDataSchema()
        data = ClientData.query.filter_by(id=pk).first()
        return schema.dump(data)

@nsApi.route('/current-totp/<clientId>')
class GetCurrentTotp(Resource):
    @nsApi.doc('get current totp code')
    @jwt_required()
    def post(self, clientId):
        data = ClientData.query.filter_by(client_id=clientId).first()
        fp = FingerPrintData(client_id=clientId, api_updated_at=datetime.utcnow())
        db.session.add(fp)
        db.session.commit()
        key = data.totp_key
        current_totp = get_current_totp(key)
        return current_totp
    
@nsApi.route('/add-data')
class AddNewClientData(Resource):
    @limiter
    @nsApi.doc('add new data in database')
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_id', type=str)
        parser.add_argument('totp_key', type=str)
        args = parser.parse_args()
        result = ClientData(client_id=args.client_id, totp_key=args.totp_key)
        db.session.add(result)
        db.session.commit()
        return {"status":True, "msg":"data has uploaded successfully!"}
    
@nsApi.route('/update-data/<pk>')
class UpdateClientData(Resource):
    @nsApi.doc('update data in database')
    @jwt_required()
    def put(self, pk):
        parser = reqparse.RequestParser()
        parser.add_argument('client_id', type=str)
        parser.add_argument('totp_key', type=str)
        args = parser.parse_args()
        result = ClientData.query.filter_by(client_id=pk).first()
        result.client_id = args.client_id
        result.totp_key = args.totp_key
        db.session.commit()
        return {"msg":"data has been updated successfully"}
    
@nsApi.route('/delete-data/<pk>')
class DeleteClientData(Resource):
    @nsApi.doc('delete data')
    @jwt_required()
    def delete(self, pk):
        result = ClientData.query.filter_by(id=pk).delete()
        db.session.commit()
        return {"msg":"data has been deleted successfully"}
    
