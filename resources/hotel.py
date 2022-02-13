from ast import arg
from flask_restful import Resource, reqparse
from models.hotel import HotelModel


class Hoteis(Resource):
    
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]} # SELECT * FROM

class Hotel(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True, help="The field 'name' cannot be left blank.")
    atributos.add_argument('estrelas', type=float, required=True, help="The field 'estrelas' cannot be left blank.")
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')

    #Função que consulga se o hotel existe
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
       
    # Metodo Post
    def post(self, hotel_id):

        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' alread exists.".format(hotel_id)}, 400 # Bad request

        dados = Hotel.atributos.parse_args() 
        # esse código já vai desempacotar todos os dados definindo chave e valor para cada dado.
        # sendo limitado pelos argumentos setados como atributo da classe
        hotel = HotelModel(hotel_id, **dados)
        #convertendo o dicionario para json
        try:
            # salva o hotel no banco de dados.
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500 # Internal Server Error
        return hotel.json()

    # Metodo Put
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
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An error ocurred trying to delete hotel.'}, 500 # Internal Server Error
            return {'message': 'Hotel deleted'}

        return {'message': 'Hotel not found.'}, 404