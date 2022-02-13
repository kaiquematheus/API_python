
#from pacote import recurso/classe
from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel


app = Flask(__name__)
# O SQLAlchemy funciona independente do banco
# então eu poderia utilizar um postgres ao invez do sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

@app.before_first_request
def cria_banco():
    banco.create_all()




api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')




if __name__ == '__main__':
    from sql_akchemy import banco
    banco.init_app(app)
    app.run(debug=True)

    #http://127.0.0.1:5000/hoteis
    #python3 app.py