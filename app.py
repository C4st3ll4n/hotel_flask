from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.hotel import Hoteis, Hotel
from resources.user import User, UserRegister, UserLogin

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///banco.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "ISAIDTHEHIPHOPTHEHIP"
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def init_banco():
    db.create_all()


api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/users/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')

if __name__ == "__main__":
    from sql_alchemy import db
    db.init_app(app)
    app.run(debug=True)
