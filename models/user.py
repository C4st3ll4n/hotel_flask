from flask import url_for, request
from requests import post

from sql_alchemy import db
from utils.mailgun import *


class UserModel(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    login = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(40), nullable=False)
    status = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(150), nullable=False, unique=True)

    def __init__(self, name, login, password, email, status=False):
        self.name = name
        self.login = login
        self.password = password
        self.status = status
        self.email = email

    def json(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "login": self.login,
            "email":self.email,
            "status": self.status
        }

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return

    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
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

    def send_email_confirm(self):
        base_url = request.url_root[:-1]
        url = url_for('userconfirm', user_id=self.user_id)
        link_confirmacao = str(base_url + url)
        url_post = f"https://api.mailgun.net/v3/{mailgun_domain}/messages"
        return post(
            url_post,
            auth=("api", mailgun_api_key),
            data={"from": "NÃO RESPONDA <henrique.souza@elostecnologia.com.br>",
                  "to": self.email,
                  "subject": "Confirmar cadastro",
                  "text": f"Clique no link, e confirme seu cadastro\n {link_confirmacao}",
                  'html': confirm_template(link_confirmacao)
                  },
        )
