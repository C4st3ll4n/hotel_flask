from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from models.site import SiteModel


class Sites(Resource):
    def get(self):
        return {"sites": [site.json() for site in SiteModel.query.all()]}


class Site(Resource):
    def get(self, url):

        site = SiteModel.find_site(url)
        if site:
            return site.json()

        return {"message": "Not found"}, 404

    @jwt_required
    def post(self, url):
        path_params = reqparse.RequestParser()
        path_params.add_argument("name", type=str, required=True, help="Name cannot be null")
        dados = path_params.parse_args()

        if SiteModel.find_site(url):
            return {"message": "Already exists a site with this URL"}, 400

        try:
            site = SiteModel(url=url, name=dados['name'])
            site.save_site()
            return site.json()
        except Exception as e:
            return {"message": "Something went wrong", "exception":e.__str__()}, 500

    @jwt_required
    def delete(self, url):
        site: SiteModel = SiteModel.find_site(url)

        if site:
            try:
                site.delete_site()
                return {"message": "deleted"},200
            except Exception:
                return {"message": "Something went wrong"}, 500

        return {"message": "Does not exists a site with this URL"}, 400
