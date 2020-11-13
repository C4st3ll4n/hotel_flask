from sql_alchemy import db


class UserModel(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    login = db.Column(db.String(40))
    password = db.Column(db.String(40))

    def __init__(self, name, login, password):
        self.name = name
        self.login = login
        self.password = password

    def json(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "login": self.login,
        }

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def update_user(self, nome, login, password):
        self.name = nome
        self.login = login
        self.password = password

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()


