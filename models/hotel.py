from sql_alchemy import db


class HotelModel(db.Model):
    __tablename__ = 'hoteis'

    hotel_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(80))
    rating = db.Column(db.Float(precision=1), )
    daily = db.Column(db.Float(precision=2), )
    city = db.Column(db.String(40), )

    def __init__(self, hotel_id, name, rating, daily, city):
        self.hotel_id = hotel_id
        self.name = name
        self.rating = rating
        self.daily = daily
        self.city = city

    def json(self):
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "rating": self.rating,
            "daily": self.daily,
            "city": self.city,
        }

    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first()
        if hotel:
            return hotel
        return None
