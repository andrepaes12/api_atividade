from models import Pessoas

#Insere dados
def insere_pessoas():
    nome = 'Josafa'
    idade = 37
    pessoa = Pessoas(nome=nome, idade=idade)
    print(f'Vc inseriu o nome {nome} com idade de {idade} anos.')
    pessoa.save()

#Realiza a consulta no BD
def consulta_pessoa():
    pessoas = Pessoas.query.all()
    print(pessoas)
    nome = 'Andre'
    pessoa = Pessoas.query.filter_by(nome=nome).first()
    print(f'Vc filtrou o nome {pessoa.nome}, que tem {pessoa.idade} anos.')

#Altera os dados
def altera_pessoa():
    ex_nome = 'Josafa'
    pessoa = Pessoas.query.filter_by(nome=ex_nome).first()
    ex_idade = pessoa.idade
    pessoa.nome = 'Joao'
    pessoa.idade = 33
    print(f'Vc alterou o nome {ex_nome} de {ex_idade} anos para o nome {pessoa.nome} com {pessoa.idade} anos.')
    pessoa.save()

#Exclui registro
def exclui_pessoa():
    nome = 'Paulo'
    pessoa = Pessoas.query.filter_by(nome=nome).first()
    pessoa.delete()
    print(f'Vc exclui o registro com o nome {nome} de {pessoa.idade} anos.')


if __name__ == '__main__':
    #insere_pessoas()
    consulta_pessoa()
    #altera_pessoa()
    #exclui_pessoa()