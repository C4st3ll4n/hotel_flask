from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from models.user import UserModel


class User(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("name", type=str, required=True, help="Name cannot be null")
    argumentos.add_argument("login", type=float, required=True, help="Rating cannot be null")

    def get(self, user_id):
        user = UserModel.find_user(user_id=user_id)
        if user:
            return user.json(), 200
        return {"message": "Not found"}, 404

    @jwt_required
    def put(self, user_id):
        dados = User.argumentos.parse_args()

        user_found = UserModel.find_user(user_id)
        if user_found:
            user_found.update_user(**dados)
            try:
                user_found.save_user()
            except:
                return {"message": "Fail to save user"}, 500

            return user_found.json(), 200
        else:
            user = UserModel(user_id, **dados)
            user.save_user()
            return user.json(), 201

    @jwt_required
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
                return {"message": "Deleted !"}
            except:
                return {"message": "Fail to delete"}, 500
        return {"message": "Not found !"}


class UserRegister(Resource):
    def post(self):
        argumentos = reqparse.RequestParser()
        argumentos.add_argument("name", type=str, required=True, help="Name cannot be null")
        argumentos.add_argument("login", type=str, required=True, help="Login cannot be null")
        argumentos.add_argument("password", type=str, required=True, help="Password cannot be null")
        dados = argumentos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {"message": "User already exists"}

        user = UserModel(**dados)

        try:
            user.save_user()
            return {"message": "User created sucessfully"}, 201
        except:
            return {"message": "Failed to create a user"}, 500


class UserLogin(Resource):
    def post(self):
        argumentos = reqparse.RequestParser()
        argumentos.add_argument("login", type=str, required=True, help="Login cannot be null")
        argumentos.add_argument("password", type=str, required=True, help="Password cannot be null")
        dados = argumentos.parse_args()

        try:
            user = UserModel.find_by_login(dados['login'])
            if user:
                if safe_str_cmp(user.password, dados['password']):
                    token_acesso = create_access_token(identity=user.user_id)
                    return {"message": "Sucessfully logged", "access_token":token_acesso}, 200
                else:
                    return {"message": "Password dont match"}, 403

        except Exception as e:
            return {"message": "Failed to return a user", "exception": e.__str__()}, 500

        return {"message": "User does not exists"}, 401
