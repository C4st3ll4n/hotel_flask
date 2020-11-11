class HotelModel:
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
