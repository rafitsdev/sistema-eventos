import time
import json
import os

data_dir = "data"
os.makedirs(data_dir, exist_ok=True)

eventos_json = os.path.join(data_dir, "eventos.json")
alunos_json = os.path.join(data_dir, "alunos.json")
coordenadores_json = os.path.join(data_dir, "coordenadores.json")


def confirmar_acao(mensagem):
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta in ["s", "sim"]:
            return True
        elif resposta in ["n", "nao", "não"]:
            return False
        else:
            print("❌ Opção inválida. Digite 'S' para Sim ou 'N' para Não.")

def gerar_user_id(usuarios):
    return str(len(usuarios) + 1)

def validar_email(email):
    import re
    padrao = r"[^@]+@[^@]+\.[^@]+"
    return re.match(padrao, email) is not None

def validar_data(data):
    from datetime import datetime
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False



def carregar_eventos():

    if not os.path.exists(eventos_json):
        with open(eventos_json, "w") as f:
            json.dump({"eventos": [], "inscricoes": {}}, f)

    with open(eventos_json, "r") as f:
        dados_eventos = json.load(f)

    return dados_eventos.get("eventos", []), dados_eventos.get("inscricoes", {})

def carregar_usuarios():

    if not os.path.exists(alunos_json):
        with open(alunos_json, "w") as f:
            json.dump({}, f)

    if not os.path.exists(coordenadores_json):
        with open(coordenadores_json, "w") as f:
            json.dump({}, f)


    with open(alunos_json, "r") as f:
        alunos = json.load(f)

    with open(coordenadores_json, "r") as f:
        coordenadores = json.load(f)
    return alunos, coordenadores


def salvar_eventos(eventos, eventos_inscricoes):

    with open(eventos_json, "w") as f:
        json.dump({"eventos": eventos, "inscricoes": eventos_inscricoes}, f, indent=4)


def salvar_usuarios(alunos, coordenadores):
    with open(alunos_json, "w") as f:
        json.dump(alunos, f, indent=4)
    with open(coordenadores_json, "w") as f:
        json.dump(coordenadores, f, indent=4)


def registrar_usuario():
    alunos, coordenadores = carregar_usuarios()

    nome = input("\n🆕 Digite seu nome: ").strip()
    email = input("📧 Digite seu email: ").strip()
    if not validar_email(email):
        print("❌Email inválido. Tente novamente com o formato usario@exemplo.com")
        return None, None
    
    while True:
        tipo = input("🎭 Tipo de usuário (Aluno/Coordenador): ").strip().lower()
        if tipo in ["aluno", "coordenador"]:
            break
        print("❌ Tipo inválido! Digite 'Aluno' ou 'Coordenador'. ")

    if email in alunos or email in coordenadores:
        print("⚠ Esse email já está registrado!")
        if not confirmar_acao("⚠ Esse email já está registrado! Gostaria de tentar outro email? (S/N) "):
            return None, None

    user_id = gerar_user_id(alunos) if tipo == "aluno" else gerar_user_id(coordenadores)
    curso = input("\n📚 Digite o curso que você está matriculado: ").strip() if tipo == "aluno" else None

    usuario = {"id": user_id, "nome": nome, "email": email, "tipo": tipo, "curso": curso, "inscricoes": []}

    if tipo == "aluno":
        alunos[user_id] = usuario
    else:
        coordenadores[user_id] = usuario

    salvar_usuarios(alunos, coordenadores)
    print(f'\n✅ Registro realizado com sucesso! Seu ID é {user_id}')
    return user_id, tipo

def cadastrar_evento():
    eventos, eventos_inscricoes = carregar_eventos()

    nome = input("\n📌 Nome do evento: ").strip()
    data = input("📅 Data do evento (DD/MM/AAAA): ").strip()
    if not validar_data(data):
        print("❌ Data inválida! Tente novamente com o formato DD/MM/AAAA")
        return
    descricao = input("📖 Descrição do evento: ").strip()

    while True:
        try:
            vagas = int(input("👥 Número máximo de participantes: "))

            if vagas <= 0:
                if not confirmar_acao("\n❌ O número de vagas deve ser maior que zero.\n Gostaria de tentar novamente? (s/n) "):
                    return
                continue
            break
        except ValueError:
            print("❌ Erro: O número de vagas deve ser um valor numérico. \n")
            continue

    evento = {'nome': nome, 'data': data, 'descricao': descricao, 'vagas': vagas, 'inscritos': []}
    eventos.append(evento)
    eventos_inscricoes[nome] = []
    salvar_eventos(eventos, eventos_inscricoes)
    print("\n✅ Evento cadastrado com sucesso!")
    return


def atualizar_evento():
    eventos, eventos_inscricoes = carregar_eventos()

    nome = input("\n🔎 Digite o nome do evento que deseja atualizar: ").strip()
    print("\n🔍 Procurando no sistema, aguarde...")
    time.sleep(2)

    for evento in eventos:
        if evento["nome"].lower() == nome.lower():
            print("\n✅ EVENTO ENCONTRADO!")

            while True:
                alteracao = input("🛠 O que você deseja alterar no evento? (Nome, Data, Descrição ou Qtde de vagas): ").strip().lower()

                if alteracao == "nome":
                    novo_nome = input("📌 Novo nome do evento: ").strip()
                    eventos_inscricoes[novo_nome] = eventos_inscricoes.pop(nome, [])
                    evento["nome"] = novo_nome
                elif alteracao == "data":
                    evento["data"] = input("📅 Nova data do evento (DD/MM/AAAA): ").strip()
                elif alteracao in ["descricao", "descrição"]:
                    evento["descricao"] = input("📖 Nova descrição do evento: ").strip()
                elif alteracao in ["qtde", "qtde de vagas"]:
                    while True:
                        try:
                            evento["vagas"] = int(input("👥 Novo número de vagas: "))
                            if evento["vagas"] <= 0:
                                if not confirmar_acao("\n❌ O número de vagas deve ser maior que zero.\nGostaria de tentar novamente? (S/N): "):
                                    return
                                continue
                            break
                        except ValueError:
                            print("❌ Erro: O número de vagas deve ser um valor numérico. \n")
                            continue
                else:
                    print("❌ Opção inválida. Escolha entre Nome, Data, Descrição ou Qtde de Vagas.")
                    continue

                print("\n⏳ Atualizando dados do evento, aguarde... ")
                time.sleep(2)
                salvar_eventos(eventos, eventos_inscricoes)
                print("\n✅ Evento atualizado com sucesso!")

                if not confirmar_acao("\n📖 Deseja alterar mais alguma coisa neste evento? (S/N): "):
                    return

    print("\n⚠ Evento não encontrado!")

def menu():
    carregar_eventos()
    carregar_usuarios()
    usuario_atual, tipo_usuario = None, None
    while not usuario_atual:
        opcao = input("🆕 Deseja 1️⃣ Registrar-se ou 2️⃣ Fazer Login? ").strip()
        if opcao == "1":
            usuario_atual, tipo_usuario = registrar_usuario()
        elif opcao == "2":
            print("Você escolheu fazer login")
        else:
            print("❌ Opção inválida! Escolha 1️⃣ ou 2️⃣: ")

    while True:
        print("\n🎭 ===== MENU =====")
        print("1️⃣  Cadastrar Evento")
        print("2️⃣  Atualizar Evento")
        print("3️⃣  Visualizar Eventos")
        print("4️⃣  Me Inscrever em Evento")
        print("5️⃣  Excluir Evento")
        print("6️⃣  Sair")
        opcao = input("👉 Escolha uma opção: ").strip()
        
        if opcao == "1":
            cadastrar_evento()
        elif opcao == "2":
            atualizar_evento()
        elif opcao == "3":
            print("Você escolheu a opção 'Visualizar Evento'")
        elif opcao == "4":
            print("Você escolheu a opção 'Me Inscrever em Evento'")
        elif opcao == "5":
            print("Você escolheu a opção 'Excluir Evento'")
        elif opcao == "6":
            print("\n👋 Saindo...\n")
            break
        else:
            print("❌ Opção inválida, tente novamente.\n")

menu()