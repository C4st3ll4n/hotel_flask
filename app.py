from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from deniallist import DENIALLIST

from resources.hotel import Hoteis, Hotel
from resources.user import User, UserRegister, UserLogin, UserLogout
from resources.site import Sites, Site

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///banco.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "ISAIDTHEHIPHOPTHEHIP"
app.config["JWT_BLACKLIST_ENABLED"] = True
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def init_banco():
    db.create_all()


@jwt.token_in_blacklist_loader
def check_deniallist(token):
    return token['jti'] in DENIALLIST


@jwt.revoked_token_loader
def token_invalido():
    return jsonify({"message": "revoked token"}), 401


api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/users/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Sites, '/sites')
api.add_resource(Site, '/sites/<string:url>')

if __name__ == "__main__":
    from sql_alchemy import db
    db.init_app(app)
    app.run(debug=True)
