from sql_alchemy import db


class SiteModel(db.Model):
    __tablename__ = 'sites'

    site_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    url = db.Column(db.String(180))
    hoteis = db.relationship('HotelModel')

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def json(self):
        return {
            "site_id": self.site_id,
            "name": self.name,
            "url": self.url,
            "hoteis": [hotel.json() for hotel in self.hoteis]
        }

    @classmethod
    def find_site(cls, url):
        site = cls.query.filter_by(url=url).first()
        if site:
            return site

        return None

    @classmethod
    def find_by_id(cls, site_id):
        site = cls.query.filter_by(site_id=site_id).first()
        if site:
            return site

        return None

    def save_site(self):
        db.session.add(self)
        db.session.commit()

    def delete_site(self):

        [hotel.delete_hotel() for hotel in self.hoteis]

        db.session.delete(self)
        db.session.commit()
