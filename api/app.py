from flask import Flask
from flask_restful import Api
from routes.projects import Projects
from routes.project import Project
from routes.payments import Payments
from routes.payment import Payment
from routes.log import Log
from routes.log_entry import LogEntry

app = Flask(__name__)
api = Api(app)

api.add_resource(Projects, '/projects')
api.add_resource(Project, '/projects/<project_id>')
api.add_resource(Payments, '/projects/<project_id>/payments')
api.add_resource(Payment, '/projects/<project_id>/payments/<payment_id>')
api.add_resource(Log, '/projects/<project_id>/log')
api.add_resource(LogEntry, '/projects/<project_id>/log/<log_entry_id>')

if __name__ == '__main__':
    app.run(debug=True)