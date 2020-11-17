from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from models.hotel import HotelModel
from utils.hotel_filters import path_params, normalize_path_params


class Hoteis(Resource):

    def get(self):
        dados = path_params.parse_args()
        dados_validos = {chave: dados[chave] for chave in dados if dados[chave] is not None}
        params = normalize_path_params(**dados_validos)

        # return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]} #old way
        return {'hoteis': [hotel for hotel in HotelModel.find(**params)]}


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("name", type=str, required=True, help="Name cannot be null")
    argumentos.add_argument("rating", type=float, required=True, help="Rating cannot be null")
    argumentos.add_argument("daily", type=float, required=True, help="Daily cannot be null")
    argumentos.add_argument("city", type=str, required=True, help="City cannot be null")
    argumentos.add_argument("site_id", type=int, required=True, help="Site ID cannot be null")

    """
    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None
    """

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id=hotel_id)
        if hotel:
            return hotel.json(), 200
        return {"message": "Not found"}, 404

    @jwt_required
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id duplicated"}, 400

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)

        try:
            hotel.save_hotel()
        except:
            return {"message": "Fail to save hotel"}, 500

        return hotel.json(), 200

    @jwt_required
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()

        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            try:
                hotel_encontrado.save_hotel()
            except:
                return {"message": "Fail to save hotel"}, 500

            return hotel_encontrado.json(), 200
        else:
            hotel = HotelModel(hotel_id, **dados)
            hotel.save_hotel()
            return hotel.json(), 201

    @jwt_required
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
                return {"message": "Deleted !"}
            except:
                return {"message": "Fail to delete"}, 500
        return {"message": "Not found !"}
