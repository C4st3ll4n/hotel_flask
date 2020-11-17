from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from werkzeug.debug.repr import dump

from models.hotel import HotelModel

path_params = reqparse.RequestParser()
path_params.add_argument("cidade", type=str)
path_params.add_argument("estrelas_min", type=float)
path_params.add_argument("estrelas_max", type=float)
path_params.add_argument("diarias_min", type=float)
path_params.add_argument("diarias_max", type=float)
path_params.add_argument("limit", type=int)
path_params.add_argument("offset", type=int)


def normalize_path_params(cidade=None, estrelas_min=0, estrelas_max=5, diaria_min=0, diaria_max=10000, limit=50,
                          offset=0):
    if not cidade:
        args = {
            "estrelas_min": estrelas_min,
            "estrelas_max": estrelas_max,
            "diaria_min": diaria_min,
            "diaria_max": diaria_max,
            "limit": limit,
            "offset": offset
        }
    else:
        args = {
            "estrelas_min": estrelas_min,
            "estrelas_max": estrelas_max,
            "diaria_min": diaria_min,
            "diaria_max": diaria_max,
            "cidade": cidade,
            "limit": limit,
            "offset": offset
        }

    return args


class Hoteis(Resource):

    def get(self):
        dados = path_params.parse_args()
        dados_validos = {chave: dados[chave] for chave in dados if dados[chave] is not None}
        params = normalize_path_params(**dados_validos)

        #return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

        return {'hoteis': [hotel for hotel in HotelModel.find(**params)]}


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("name", type=str, required=True, help="Name cannot be null")
    argumentos.add_argument("rating", type=float, required=True, help="Rating cannot be null")
    argumentos.add_argument("daily", type=float, required=True, help="Daily cannot be null")
    argumentos.add_argument("city", type=str, required=True, help="City cannot be null")

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
