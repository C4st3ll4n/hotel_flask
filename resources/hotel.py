from flask_restful import Resource, reqparse

from models.hotel import HotelModel


class Hoteis(Resource):
    def get(self):
        return {}


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("name")
    argumentos.add_argument("rating")
    argumentos.add_argument("daily")
    argumentos.add_argument("city")

    """
    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None
    """

    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id=hotel_id)
        if hotel is None:
            return {"message": "Not found"}, 404
        else:
            return hotel

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id duplicated"}, 400

        dados = Hotel.argumentos.parse_args()
        hotel_obj = HotelModel(hotel_id, **dados)
        new_hotel = hotel_obj.json()

        """
        new_hotel = {
            "hotel_id": hotel_id, **dados
        }"""

        hoteis.append(new_hotel)

        return new_hotel, 200

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()

        hotel = HotelModel(hotel_id, **dados)
        new_hotel = hotel.json()

        hotel = Hotel.find_hotel(hotel_id)

        if hotel:
            hotel.update(new_hotel)
            return new_hotel, 200
        else:
            hoteis.append(new_hotel)
            return new_hotel, 201

    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {"message": "Deleted !"}
