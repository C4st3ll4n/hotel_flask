from flask_restful import reqparse

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


consulta_sem_cidade = """
                       SELECT * FROM hoteis
                       where (rating >= %s and rating <= %s)
                       and (daily >= %s and daily <= %s)
                       LIMIT %s OFFSET %s
                       """

consulta_com_cidade = """
                       SELECT * FROM hoteis
                       where (rating >= %s and rating <= %s) 
                       and (daily >= %s and daily <= %s)
                       and city like %s
                       LIMIT %s OFFSET %s
                       """