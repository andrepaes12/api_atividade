from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades, Usuarios
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

#dic password
# USUARIOS = {
#     'andre': '123',
#     'andreia': '321'
# }     #criação da tabela usuarios via models.py

@auth.verify_password   #exigir acesso com login/senha
def verificacao(login, senha):
    if not (login, senha):
        return False
    #return USUARIOS.get(login) == senha
    return Usuarios.query.filter_by(login=login, senha=senha).first()


class ListaPessoas(Resource):
    def get(self):
        pessoas = Pessoas.query.all()
        response = [
            {'id': i.id,
             'nome': i.nome,
             'idade': i.idade}
            for i in pessoas
        ]
        return response

    @auth.login_required  # executará a função se estiver logado
    def post(self):
        dados = request.json    #passar os dados no body do json via Postman
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()
        response = {
            'id': pessoa.id,
            'nome': pessoa.nome,
            'idade': pessoa.idade
        }
        return response


class Pessoa(Resource):
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        response = {
            'nome': pessoa.nome,
            'idade': pessoa.idade,
            'id': pessoa.id
        }
        return response

    @auth.login_required
    def put(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        dados = request.json
        if 'nome' in dados:
            pessoa.nome = dados['nome']
        if 'idade' in dados:
            pessoa.idade = dados['idade']
        pessoa.save()
        response = {
            'id': pessoa.id,
            'nome': pessoa.nome,
            'idade': pessoa.idade
        }
        return response

    @auth.login_required
    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        mensagem = f'Pessoa {pessoa.nome} excluída com sucesso'
        pessoa.delete()
        return {'status': 'sucesso', 'mensagem': mensagem}


class ListaAtividades(Resource):
    def get(self):
        atividades = Atividades.query.all() #evitar o uso do all(), conforme o tamanho do BD
        response = [{'id': i.id, 'nome': i.nome, 'pessoa': i.pessoa.nome} for i in atividades]
        return response

    @auth.login_required  # executará a função se estiver logado
    def post(self):
        dados = request.json    #passar os dados no body do json via Postman
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(nome=dados['nome'], pessoa=pessoa)
        atividade.save()
        response = {
            'pessoa': atividade.pessoa.nome,
            'nome': atividade.nome,
            'id': atividade.id
        }
        return response


api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(ListaAtividades, '/atividades/')


if __name__ == '__main__':
    app.run(debug=True)