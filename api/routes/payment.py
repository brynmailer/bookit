from flask import request
from flask_restful import Resource
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
from bson.objectid import ObjectId
from datetime import date, datetime
from database import db

class Payment(Resource):
    def put(self, project_id, payment_id):
        # update payment with parsed payment_id
        if ObjectId(payment_id) in db.projects.find_one({'_id': ObjectId(project_id)})['payments']:
            req_body = request.get_json(force=True)
            db.payments.update_one({'_id': ObjectId(payment_id)}, {'$set': {
                'amount': req_body['amount'],
                'date': datetime.strptime(req_body['date'], '%m/%d/%Y'),
                'status': req_body['staus'],
                'description': req_body['description']
            }})
            return dumps(db.payments.find({'_id': ObjectId(payment_id)}), json_options=RELAXED_JSON_OPTIONS), 200
        return f"Payment with id {payment_id} does not exist on project with id {project_id}"
    
    def delete(self, project_id, payment_id):
        # delete payment with parsed payment_id
        if ObjectId(payment_id) in db.projects.find_one({'_id': ObjectId(project_id)})['payments']:
            db.payments.delete_one({'_id': ObjectId(payment_id)})
            return f"Payment with id {payment_id} deleted from project with id {project_id}", 204
        return f"Payment with id {payment_id} does not exist on project with id {project_id}"