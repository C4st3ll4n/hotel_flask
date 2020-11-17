import sqlite3

from werkzeug.debug.repr import dump

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

    def save_hotel(self):
        db.session.add(self)
        db.session.commit()

    def update_hotel(self, name, rating, daily, city):
        self.name = name
        self.rating = rating
        self.daily = daily
        self.city = city

    def delete_hotel(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find(cls, **kwargs):
        params = kwargs
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        if not params.get("cidade"):

            consulta = """
                       SELECT * FROM hoteis
                       where (rating >= ? and rating <= ?)
                       and (daily >= ? and daily <= ?)
                       LIMIT ? OFFSET ?
                       """
            cond = tuple([params[chave] for chave in params])
            # result = cursor.execute(consulta, (rating_min, rating_max, daily_min, daily_max, limit, offset))
            result = cursor.execute(consulta, cond)
        else:
            consulta = """
                       SELECT * FROM hoteis
                       where (rating >= ? and rating <= ?) 
                       and (daily >= ? and daily <= ?)
                       and city like ?
                       LIMIT ? OFFSET ?
                       """

            cond = tuple([params[chave] for chave in params])
            result = cursor.execute(consulta, cond)

        hoteis = []

        for linha in result:
            hoteis.append({
                "hotel_id": linha[0],
                "name": linha[1],
                "rating": linha[2],
                "daily": linha[3],
                "city": linha[4],
            })

        return hoteis
