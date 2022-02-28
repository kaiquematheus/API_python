
#from pacote import recurso/classe
from flask import Flask
import flask
from flask_restful import Api
import flask_restful
from resources.hotel import Hoteis, Hotel
from resources.usuario import User, UserRegister, UserLogin
from flask_jwt_extended import JWTManager



app = Flask(__name__)
# O SQLAlchemy funciona independente do banco
# então eu poderia utilizar um postgres ao invez do sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def cria_banco():
    banco.create_all()




api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/Login')





if __name__ == '__main__':
    from sql_akchemy import banco
    banco.init_app(app)
    app.run(debug=True)

    #http://127.0.0.1:5000/hoteis
    #python3 app.py