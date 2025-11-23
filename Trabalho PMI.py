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
import time
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
def updateuser():
    login = input("Digite o login do usuário que deseja editar: ").strip()
    user = None
    for u in users:
        if u["login"] == login:
            user = u
            break
    if not user:
        print("Usuário não encontrado.")
        return
    for campo in ["nome", "tel"]:
        novo = input(f"{campo.capitalize()} atual: {user[campo]}. Digite novo ou deixe vazio para manter: ").strip()
        if novo:
            user[campo] = novo
    save("usuarios.json", users)
    print("Usuário atualizado com sucesso.")
def deleteuser():
    login = input("Digite o login do usuário que deseja remover: ").strip()
    for u in users:
        if u["login"] == login:
            users.remove(u)
            save("usuarios.json", users)
            print("Usuário removido com sucesso.")
            return
    print("Usuário não encontrado.")
def updatebook():
    id = input("Digite o ID do livro que deseja editar: ").strip()
    if not id.isdigit():
        print("ID inválido.")
        return
    id = int(id)
    book = None
    for i in library:
        if i["id"] == id:
            book = i
            break
    if not book:
        print("Livro não encontrado.")
        return
    for campo in ["titulo", "genero", "ano", "editora"]:
        novo = input(f"{campo.capitalize()} atual: {book[campo]}. Digite novo ou deixe vazio para manter: ").strip()
        if novo:
            if campo == "genero" and novo.lower() not in genres:
                print("Gênero inválido.")
                return
            book[campo] = novo if campo != "genero" else novo.lower()
    save("biblioteca.json", library)
    print("Livro atualizado com sucesso.")
def deletebook():
    id = input("Digite o ID do livro que deseja remover: ").strip()
    if not id.isdigit():
        print("ID inválido.")
        return
    id = int(id)
    for i in library:
        if i["id"] == id:
            library.remove(i)
            for u in users:
                if id in u["livrosemprestados"]:
                    u["livrosemprestados"].remove(id)
                    save("usuarios.json", users)
            save("biblioteca.json", library)
            print("Livro removido com sucesso.")
            return
    print("Livro não encontrado.")
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
def showbooks_multiple():
    tamanhpag = 10
    print("Filtros disponíveis: título, genero, ano, editora, status (disponível/emprestado). Deixe em branco para ignorar.")
    filtro = {}
    for crit in ["titulo", "genero", "ano", "editora"]:
        val = input(f"{crit.capitalize()}: ").strip()
        if val:
            filtro[crit] = val.lower()
    status = input("Status (disponível/emprestado, deixe em branco p/ ambos): ").lower().strip()
    results = []
    for i in library:
        match = True
        for crit in filtro:
            if filtro[crit] not in str(i[crit]).lower():
                match = False
        if status:
            if status == "disponível" and not i["disponivel"]:
                match = False
            if status == "emprestado" and i["disponivel"]:
                match = False
        if match:
            results.append(i)
    inicio = 0
    while True:
        fim = inicio + tamanhpag
        pagina = results[inicio:fim]
        print(f"Páginal {(inicio // tamanhpag)+1}")
        for idx, i in enumerate(pagina, start=inicio +1):
            statusmsg = "Disponível" if i["disponivel"] else "Emprestado"
            print(f"{idx}. Título: {i['titulo']} | Gênero: {i['genero']} | Ano: {i['ano']} | Editora: {i['editora']} | ID: {i['id']} | Status: {statusmsg}", end=";\n")
        print("-" *20)
        print("[A]Avançar | [V]Voltar | [S]Sair")
        opc = input("").lower().strip()
        if opc == "s":
            return
        elif opc == "a":
            if fim < len(results):
                inicio += tamanhpag
            else:
                print("Você já está na última página!")
        elif opc == "v":
            if inicio - tamanhpag >= 0:
                inicio -= tamanhpag
            else:
                print("Você está na primeira página.")  
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
            name = input("Por favor, insira seu nome completo: ").lower()
            val = name.strip()
            if not val.isalpha():
                raise ValueError
            else:
                name = name.title()
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
    print("Usuário cadastrado com sucesso!")
    return
def reportlibrary():
    total = len(library)
    emprestados = [i for i in library if not i['disponivel']]
    disponiveis = [i for i in library if i['disponivel']]
    print(f"Total de livros: {total}")
    print(f"Disponíveis: {len(disponiveis)}")
    print(f"Emprestados: {len(emprestados)}")
    print("------ Livros mais emprestados ------")
    ranking = sorted(library, key=lambda x: x["vezes emprestado"], reverse=True)[:5]
    for idx, i in enumerate(ranking, start=1):
        print(f"{idx}. {i['titulo']} | Vezes emprestado: {i['vezes emprestado']}")
    print("------ Usuários com mais empréstimos ------")
    topusers = sorted(users, key=lambda u: len(u.get("livrosemprestados", [])), reverse=True)[:5]
    for idx, u in enumerate(topusers, start=1):
        print(f"{idx}. {u['nome']} | Livros emprestados: {len(u['livrosemprestados'])}")
    print("------ Livros por gênero ------")
    conta_generos = {}
    for i in library:
        g = i["genero"]
        conta_generos[g] = conta_generos.get(g, 0) + 1
    for g, qt in conta_generos.items():
        print(f"{g.capitalize()}: {qt}")
def lendsys(usuario):
    print("1. Solicitar Empréstimo\n2. Fazer Devolução")
    try:
        escolha = int(input("Escolha a opção: ").strip())
        if escolha not in (1,2):
            print("Opção inválida.")
            return
    except ValueError:
        print("Entrada inválida.")
        return
    criterios_validos = {"titulo", "genero", "ano", "editora"}
    criterio = input("Escolha o critério (titulo/genero/ano/editora): ").lower().strip()
    if criterio not in criterios_validos:
        print("Critério inválido.")
        return
    busca = input(f"Digite o valor para busca ({criterio}): ").lower().strip()
    nome = usuario['nome']
    results = []
    ndisponivel = []
    for i in library:
        if busca in str(i.get(criterio, "")).lower() and i["disponivel"]:
            results.append(i)
        if busca in str(i.get(criterio, "")).lower() and not i["disponivel"] and nome == i['emprestado']:
            ndisponivel.append(i)
    if escolha == 2:
        print(f"Opções para devolução: {len(ndisponivel)}")
        for i in ndisponivel:
            print(f"Título: {i['titulo']} | Gênero: {i['genero']} | Ano: {i['ano']} | Editora: {i['editora']} | ID: {i['id']}", sep=";\n")
        while True:
            try:
                id = int(input("Digite o id do livro para devolução, (0 para voltar ao menu): "))
            except ValueError:
                print("Id inválido, digite apenas números.")
                continue
            if id == 0:
                return
            found = False
            for i in ndisponivel:
                if i['id'] == id:
                    found = True
                    i['disponivel'] = True
                    i['emprestado'] = None
                    for j in users:
                        if nome == j['nome']:
                            if id in j['livrosemprestados']:
                                j['livrosemprestados'].remove(id)
                    save("biblioteca.json", library)
                    save("usuarios.json", users)
                    print("Livro devolvido com sucesso.")
                    return
            if not found:
                print("Id incorreto, tente novamente.")
                continue
    elif len(results) == 0:
        print("Sem resultados disponíveis para empréstimo.")
    else:
        print(f"Resultados disponíveis para empréstimo: {len(results)}.") 
        for i in results:
            print(f"Título: {i['titulo']} | Gênero: {i['genero']} | Ano: {i['ano']} | Editora: {i['editora']} | ID: {i['id']}", sep=";\n")
        while True:
            borrow = input("Gostaria de solicitar um empréstimo? (sim/não)").lower().strip()
            if borrow == "sim":
                try:
                    borrow_id = int(input("Digite o ID da edição desejada: "))
                except ValueError:
                    print("Id inválido, digite apenas números.")
                    continue
                found = False
                for i in results:
                    if i['id'] == borrow_id:
                        found = True
                        i['disponivel'] = False
                        i['vezes emprestado'] += 1
                        i['emprestado'] = nome
                        for j in users:
                            if nome == j['nome']:
                                j['livrosemprestados'].append(i['id'])
                        save("biblioteca.json", library)
                        save("usuarios.json", users)
                        print("Boa leitura!")
                        return
                if not found:
                    print("Id incorreto, tente novamente.")
                    continue
            elif borrow == "não":
                return
            else:
                print("Por favor, digite apenas uma das opções válidas!")
library = load("biblioteca.json")
users = load ("usuarios.json")
genres = ("romance", "terror", "horror", "mistério", "ficção científica", 
          "fantasia", "suspense", "comédia", "drama", "não ficção", "técnico", "educação", "conto", "ficção histórica", "aventura", "poesia", "história",
          "autoajuda")
loginmenu = "Bem-vindo(a)! Por favor, escolha uma opção abaixo:\n1. Login;\n2. Registrar novo usuário."
def login():
    while True:
        print(loginmenu)
        try:
            option = int(input(""))
            if option not in (1, 2):
                raise ValueError
            else:
                if option == 1:
                    tentativas = 0
                    while tentativas < 3:
                        user = None
                        login = input("Usuário: ")
                        for i in users:
                            if login == i['login']:
                                user = i
                                break
                        if user:
                            senha = input("Senha: ")
                            if senha == user['senha']:
                                    acess = i
                                    return acess
                            else:
                                print("Usuário ou senha incorretos, tente novamente em alguns segundos.")
                                time.sleep(10)
                                tentativas += 1 
                                continue
                        if not user: 
                            print("Usuário não encontrado. Tente novamente.")
                            tentativas += 1
                            continue
                else:
                    registeruser()
        except ValueError:
            print("Selecione apenas uma das opções disponíveis, por favor.")
            continue
acess = login() 
def menu_principal(acess):
    while True:
        print("\n----- Biblioteca Digital -----")
        print("[1] Buscar livros")
        print("[2] Empréstimos/Devoluções")
        print("[3] Relatórios")
        print("[4] Cadastro de livro")
        print("[5] Cadastro de usuário")
        print("[6] Editar livro")
        print("[7] Remover livro")
        print("[8] Editar usuário")
        print("[9] Remover usuário")
        print("[S] Sair")
        escolha = input("Escolha uma opção: ").strip().lower()
        if escolha == "1":
            showbooks_multiple()
        elif escolha == "2":
            lendsys(acess)
        elif escolha == "3":
            reportlibrary()
        elif escolha == "4":
            if acess.get("id") == 0:
                registerbook()
            else:
                print("Somente administradores podem cadastrar livros.")
        elif escolha == "5":
            if acess.get("id") == 0:
                registeruser()
            else:
                print("Somente administradores podem cadastrar usuários.")
        elif escolha == "6":
            if acess.get("id") == 0:
                updatebook()
            else:
                print("Apenas administradores podem editar livros.")
        elif escolha == "7":
            if acess.get("id") == 0:
                deletebook()
            else:
                print("Apenas administradores podem remover livros.")
        elif escolha == "8":
            if acess.get("id") == 0:
                updateuser()
            else:
                print("Apenas administradores podem editar usuários.")
        elif escolha == "9":
            if acess.get("id") == 0:
                deleteuser()
            else:
                print("Apenas administradores podem remover usuários.")
        elif escolha == "s":
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")
menu_principal(acess)
