'''1.Desenvolva um Sistema de Gerenciamento de Biblioteca Digital que integre 
todos os conceitos fundamentais do Python: 
O sistema deve permitir: 

-- Cadastro e gerenciamento de livros 

-- Cadastro e gerenciamento de usuários 

-- Sistema de empréstimos e devoluções 

-- Busca avançada com filtros 

-- Relatórios e estatísticas 

-- Persistência de dados em arquivos 

-- Interface interativa com menus paginados
'''
#import time
import math
import json
ddd = ("68", "96", "92", "97", "91", "93",
       "94", "69", "95", "63", "82", "71",
       "73", "74", "75", "77", "85", "88",
       "98", "99", "83", "81", "87", "86",
       "89", "84", "79", "61", "62", "64",
       "65", "66", "67", "27", "28", "31",
       "32", "33", "34", "35", "37", "38",
       "21", "22", "24", "11", "12", "13",
       "14", "15", "16", "17", "18", "19",
       "41", "42", "43", "44", "45", "46",
       "51", "53", "54", "55", "47", "48", "49")
def save(nome, lista):
    with open (nome, "w", encoding="utf-8") as arquivo:
        json.dump(lista, arquivo, indent=4, ensure_ascii=False)
def load(nome):
    try:
        with open (nome, "r", encoding="utf-8") as arquivo:
            f = json.load(arquivo)
    except FileNotFoundError:
        print("Arquivo não encontrado, gerando novo arquivo.")
        return []
    return f
def showbooks(criterio, busca):
    results = []
    if criterio and busca:
        for i in library:
            if busca in i[criterio]:
                results.append(i)
            else:
                return False
    else:
        results = library
    print(f"Resultados encontrados: {len(results)}:")  
    for i in results:
        status = "Disponível" if i["disponivel"] else "Emprestado"
        print(f"Título: {i['titulo']} | Gênero: {i['genero']} | Ano: {i['ano']} | Editora: {i['editora']} | ID: {i['id']} | Status: {status}", sep=";\n") 
    return        
def registerbook():
    title = input("Título do Livro: ")
    ident = len(library) + 1
    while True:
        try:
            genre = input("Gênero: ")
            valid = genre.strip().lower().replace("-"," ")
            if valid not in genres:
                raise ValueError
            else:
                genre = genre.strip().lower().replace("-"," ").capitalize()
                print("Livro cadastrado com sucesso!")
                break
        except ValueError:
            print("Por favor, selecione apenas opções válidas. " \
            "Considere utilizar um dos gêneros válidos abaixo:")
            for i in genres:
                print(i.capitalize(), end=";\n")
            continue
    while True:
        try:  
            year = input("Caso não saiba ou a obra seja muito antiga, " \
            "deixe em branco\nAno de publicação: ")
            if year == "":
                year = "N/A"
                break
            elif year.isdigit():
                if (len(year) > 4):
                    raise ValueError
                else:
                    break
            else:
                raise ValueError
        except ValueError:
            print("Utilize um ano válido.")
            continue
    ed = input("Caso não saiba, deixe em branco\nEditora: ")
    if ed == "":
        ed = "N/A"
    newbook = {"titulo" : title,
            "id" : ident,
            "genero" : genre,
            "ano" : year,
            "editora" : ed,
             "disponivel" : True,
             "emprestado" : None, 
             "vezes emprestado" : 0}
    library.append(newbook)
    save("biblioteca.json", library)
def registeruser():
    while True:
        try:
            name = input("Por favor, insira seu nome completo: ").title()
            if not name.isalpha():
                raise ValueError
            else:
                break
        except ValueError:
            print("Por favor, insira um nome válido.")
            continue
    while True:
        try:
            login = input("Crie um usuário para login: ")
            if len(login) < 5:
                print("Login muito pequeno! Crie um usuário com ao menos 5 caracteres.")
                raise ValueError
            elif login in [u['login'] for u in users]:
                print("Login já existente, tente novamente.")
                raise ValueError
            else:
                break
        except ValueError:
            continue
    while True:
        try:
            password = input("Crie sua senha: ")  
            if len(password) < 8:
                print("Senha muito curta! Crie uma senha com ao menos 8 caracteres.")
                raise ValueError
            elif password.isdigit() or password.isalpha() or password.isalnum():
                print("Para sua segurança, sua senha precisa conter ao menos uma letra, número e um caracter especial.")
                raise ValueError
            else:
                break
        except ValueError:
            continue       
    ident = len(users) + 1       
    while True:
        try:
            cell = input("Por favor, insira seu número de celular: ").strip().replace("-", "")
            if not cell.isdigit() or len(cell) != 11 or cell.startswith("0") or cell[0:2] not in ddd or cell[2] != "9":
                print("Algo deu errado, tente novamente. Utilize um número válido.")
                raise ValueError
            else:
                break
        except ValueError:
            continue
    print("Usuário cadastrado com sucesso! Bem-vindo(a)!")
    newuser = {"nome" : name, 
           "login": login, 
           "senha": password, 
           "id" : ident, 
           "tel" : cell, 
           "livrosemprestados" : [],
           "tipo" : "Usuário"}
    users.append(newuser)
    save("usuarios.json", users)
def report():
    #livros atualmente emprestados
    #mais emprestados do período
    pass
def lendsys(criterio, busca, nome):
    results = []
    for i in library:
        if busca in i[criterio] and i["disponivel"]:
            results.append(i)
    if len(results) == 0:
        print("Sem resultados disponíveis.")
    else:
        print(f"Resultados disponíveis para empréstimo: {len(results)}.") 
        for i in results:
            print(f"Título: {i['titulo']} | Gênero: {i['genero']} | Ano: {i['ano']} | Editora: {i['editora']} | ID: {i['id']}", sep=";\n")
        while True:
            try:
                borrow = input("Gostaria de solicitar um empréstimo? (sim/não)").lower().strip()
                if borrow == "sim":
                    while True:
                        try:
                            borrow = int(input("Digite o ID da edição desejada: "))
                            for i in results:
                                if i['id'] == borrow:
                                    i['disponivel'] = False
                                    i['vezes emprestado'] += 1
                                    i['emprestado'] = nome
                                    for j in users:
                                        if nome == j['nome']:
                                            j['livrosemprestados'].append(i['id'])
                                break
                            print("Boa leitura!")
                            return
                        except TypeError:
                            print("Utilize apenas o id informado.")
                            continue
                elif borrow == "não":
                    return
                else:
                    raise ValueError
            except ValueError:
                print("Por favor, digite apenas uma das opções válidas!")
                continue    
    save("biblioteca.json", library)
    save("usuarios.json", users)
load("biblioteca.json")
load ("usuarios.json")
library = []
users = [{"nome": "Admin",
          "login" : "admin",
          "senha" : "adminlib777",
          "tipo" : "Administrador"}]
genres = ("romance", "terror", "horror", "mistério", "ficção científica", 
          "fantasia", "suspense", "comédia", "drama", "não ficção"
          "técnico", "educação", "conto", "ficção histórica", "aventura", "poesia", "história",
          "autoajuda")
menu = None
useradmin = "acesso a registro de novos livros"
