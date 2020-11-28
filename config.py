with open('development_cred.json') as arq:
    configs = json.load(arq)

USER = configs.get('user')
PASSWORD = configs.get('password')
HOST = configs.get('host')
PORT = configs.get('port')
DATABASE = configs.get('database')

JWT_TOKEN = configs.get('JWT')
