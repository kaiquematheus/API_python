from ast import arg
from flask_restful import Resource, reqparse
from models.usuarioModel import UserModel
from flask_jwt_extended import create_access_token
from werkzeug.security import safe_str_cmp


atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank")
atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left blank")

class User(Resource):


    # Metodo Get
    # /usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        #Se existir hotel ele vai retornar hotel
        if user:
            return user.json()
        #Se não existir hotel ele retorna o erro 404 not found
        return {'message': 'User not found.'}, 404 # not found

    # Metodo Delete
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An error ocurred trying to delete user.'}, 500 # Internal Server Error
            return {'message': 'User deleted'}

        return {'message': 'User not found.'}, 404
    
class UserRegister(Resource):

    # /cadastro
    def post(self):
        
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {'massage': "The login '{}' already exists.".format(dados['login'])}
            
        user = UserModel(**dados)
        user.save_user()
        return {'message': 'User created successfully!'}, 201 # Created

class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'acces_token': token_de_acesso}, 200
        return{'message': 'The username or password is incorrect'}, 401 # Unauthorize



