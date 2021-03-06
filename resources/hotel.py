from ast import arg
from flask_restful import Resource, reqparse
from models.hotelModel import HotelModel 
from models.siteModel import SiteModel
from resources.filtros import normalize_path_params, consulta_sem_cidade, consulta_com_cidade
from flask_jwt_extended import jwt_required
import sqlite3

#path /hoteis?cidade=Rio de Janeiro&estrelas_min=4&diaria_max=400

path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)

class Hoteis(Resource):

    def get(self):

        #Conectando com o Banco
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()


        dados = path_params.parse_args()
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)

        #Caso o usuário não tenha definido uma cidade
        if not parametros.get('cidade'):
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_sem_cidade, tupla)
        else:
            #Caso o usuário tenha definido uma cidade
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_com_cidade, tupla)

        hoteis = []
        for linha in resultado:
            hoteis.append({
                'hotel_id': linha[0],
                'nome': linha[1],
                'estrelas': linha[2],
                'diaria': linha[3],
                'cidade': linha[4],
                'site_id': linha[5]
            })

        return {'hoteis': hoteis} # SELECT * FROM hoteis

        #return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]} # SELECT * FROM

class Hotel(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True, help="The field 'name' cannot be left blank.")
    atributos.add_argument('estrelas', type=float, required=True, help="The field 'estrelas' cannot be left blank.")
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')
    atributos.add_argument('site_id', type=int, required=True, help="Every hotel needs to be linked whith sites")

    #Função que consulta se o hotel existe
    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return False

    # Metodo Get
    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        #Se existir hotel ele vai retornar hotel
        if hotel:
            return hotel.json()
        #Se não existir hotel ele retorna o erro 404 not found
        return {'message': 'Hotel not found.'}, 404 # not found
       
    # Metodo post
    @jwt_required()
    def post(self, hotel_id):

        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' alread exists.".format(hotel_id)}, 400 # Bad request

        dados = Hotel.atributos.parse_args() 
        # esse código já vai desempacotar todos os dados definindo chave e valor para cada dado.
        # sendo limitado pelos argumentos setados como atributo da classe
        hotel = HotelModel(hotel_id, **dados) #convertendo o dicionario para json
        
        #if not SiteModel.find_by_id(dados.get('site_id')):
        if not SiteModel.find_by_id(dados['site_id']):
            return {'message': 'The hotel must be associated to a valid site id.'}, 400
        try:
            # salva o hotel no banco de dados.
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500 # Internal Server Error
        return hotel.json(), 201

    # Metodo Put
    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.atributos.parse_args()
        #convertendo o dicionario para json
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200 #OK Atualizado
        # esse código já vai desempacotar todos os dados definindo chave e valor para cada dado.
        # sendo limitado pelos argumentos setados como atributo da classe
        hotel = HotelModel(hotel_id, **dados)
        try:
            # salva o hotel no banco de dados.
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500 # Internal Server Error
        return hotel.json(), 201 # Criado

    # Metodo Delete
    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An error ocurred trying to delete hotel.'}, 500 # Internal Server Error
            return {'message': 'Hotel deleted'}

        return {'message': 'Hotel not found.'}, 404