import time
import json
import os
import re
from datetime import datetime

data_dir = "data"
os.makedirs(data_dir, exist_ok=True)

eventos_json = os.path.join(data_dir, "eventos.json")
alunos_json = os.path.join(data_dir, "alunos.json")
coordenadores_json = os.path.join(data_dir, "coordenadores.json")

# Funções de Suporte
def confirmar_acao(mensagem):
    """Funções de Suporte - Confirmar Ação"""
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta in ["s", "sim"]:
            return True
        elif resposta in ["n", "nao", "não"]:
            return False
        else:
            print("❌ Opção inválida. Digite 'S' para Sim ou 'N' para Não.")

def gerar_user_id(usuarios):
    """Funções de Suporte - Gerar IDs para os usuários"""
    return str(max(map(int, usuarios.keys()), default= 0) + 1)

def validar_email(email):
    """Funções de Suporte - Validação de email"""
    padrao = r"[^@]+@[^@]+\.[^@]+"
    return re.match(padrao, email) is not None

def validar_data(data):
    """Funções de Suporte - Validação de Formato de Data"""
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False


# Persistência de Dados
def carregar_eventos():
    """Carregando Eventos no JSON"""

    if not os.path.exists(eventos_json):
        with open(eventos_json, "w") as f:
            json.dump({"eventos": [], "inscricoes": {}}, f)

    with open(eventos_json, "r") as f:
        dados_eventos = json.load(f)

    inscricoes = {k.lower(): v for k, v in dados_eventos.get("inscricoes", {}).items()}
    return dados_eventos.get("eventos", []), inscricoes

def salvar_eventos(eventos, eventos_inscricoes):
    """Salvando Eventos no JSON"""

    with open(eventos_json, "w") as f:
        json.dump({"eventos": eventos, "inscricoes": eventos_inscricoes}, f, indent=4)


def carregar_usuarios():
    """Carregando Usuários no JSON"""

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

def salvar_usuarios(alunos, coordenadores):
    """Salvando Usuários no JSON"""
    with open(alunos_json, "w") as f:
        json.dump(alunos, f, indent=4)
    with open(coordenadores_json, "w") as f:
        json.dump(coordenadores, f, indent=4)

def filtragem_evento():
    """Filtra eventos com base no termo digitado:
    - Se o termo for numérico, retorna o evento correspondente ao índice (enumerate).
    - Se for um trecho do nome, retorna todos os eventos que contenham esse trecho (case-insensitive).
    """
    eventos, _ = carregar_eventos()

    if not eventos:
        print("❌ Nenhum evento econtrado.")
        return []
    
    print("\nEventos disponíveis:")
    for i, evento in enumerate(eventos, 1):
        print(f"{i}. {evento['nome']} - {evento['data']}")


    termo = input("\nDigite o número do evento ou um trecho do nome para filtrar: ").strip()

    if termo.isdigit():
        indice = int(termo)
        if 1 <= indice <= len(eventos):
            return [eventos[indice - 1]]
        else:
            print("⚠ Número inválido")
            return []
    else:
        evento_filtrado = [evento for evento in eventos if termo.lower() in evento["nome"].lower()]
        if not evento_filtrado:
            print("⚠ Nenhum evento encontrado com esse termo.")
        return evento_filtrado


# Funções de Login
def registrar_usuario():
    """Registrando Usuários no Sistema"""
    alunos, coordenadores = carregar_usuarios()

    nome = input("\n🆕 Digite seu nome: ").strip()

    while True:
        email = input("📧 Digite seu email: ").strip().lower()
        if not validar_email(email):
            print("❌Email inválido. Tente novamente com o formato usuario@exemplo.com")
            continue


        email_ja_registrado = False
        for usuario in alunos.values():
            if usuario["email"].strip().lower() == email.strip().lower():
                email_ja_registrado = True
                break
            
        if not email_ja_registrado:
            for usuario in coordenadores.values():
                if usuario["email"].strip().lower() == email.strip().lower():
                    email_ja_registrado = True
                    break
        
        if email_ja_registrado:
            print("⚠ Esse email já está registrado!")
            if confirmar_acao("⚠ Gostaria de tentar outro email? (S/N) "):
                continue
            else:
                return None, None
        else:
            break
    

    while True:
        tipo = input("🎭 Tipo de usuário (Aluno/Coordenador): ").strip().lower()
        if tipo in ["aluno", "coordenador"]:
            break
        print("❌ Tipo inválido! Digite 'Aluno' ou 'Coordenador'. ")

    user_id = gerar_user_id(alunos) if tipo == "aluno" else gerar_user_id(coordenadores)
    curso = input("\n📚 Digite o curso que você está matriculado: ").strip() if tipo == "aluno" else None

    usuario = {"id": user_id, "nome": nome, "email": email, "tipo": tipo, "curso": curso, "inscricoes": []}

    if tipo == "aluno":
        alunos[user_id] = usuario
    else:
        coordenadores[user_id] = usuario

    salvar_usuarios(alunos, coordenadores)
    print(f"\n✅ Registro realizado com sucesso! Seu ID é {user_id}")
    return user_id, tipo

def autenticar_usuario():
    """Autenticando Usuário no Sistema"""
    
    while True:
        alunos, coordenadores = carregar_usuarios()
        email = input("✉ Digite seu email para login: ").strip().lower()
        usuario_encontrado = None
        usuario_id = None

        for key, usuario in alunos.items():
            if usuario["email"].strip().lower() == email:
                usuario_encontrado = usuario
                usuario_id = key
                break
        
        if not usuario_encontrado:
            for key, usuario in coordenadores.items():
                if usuario["email"].strip().lower() == email:
                    usuario_encontrado = usuario
                    usuario_id = key
                    break

        if usuario_encontrado:
            print(f"✅ Login bem-sucedido! Olá, {usuario_encontrado['nome']} ({usuario_encontrado['tipo'].capitalize()})!")
            return usuario_id, usuario_encontrado["tipo"]
        
        if not confirmar_acao("\n❌ Usuário não encontrado. Gostaria de se cadastrar? (s/n) "):
            return None, None
        return registrar_usuario()


# Funções Principais
def cadastrar_evento():
    """Cadastrando Eventos no Sistema"""
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
    eventos_inscricoes[nome.lower()] = []
    salvar_eventos(eventos, eventos_inscricoes)
    print("\n✅ Evento cadastrado com sucesso!")
    return


def atualizar_evento():
    """Atualizando Eventos do Sistema"""
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
                    chave_antiga = None
                    for chave in eventos_inscricoes:
                        if chave.lower() == nome.lower():
                            chave_antiga = chave
                            break
                    if chave_antiga:
                        eventos_inscricoes[novo_nome] = eventos_inscricoes.pop(chave_antiga)
                    else:
                        eventos_inscricoes[novo_nome] = []
                    evento["nome"] = novo_nome

                    nome = novo_nome

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


def visualizar_eventos():
    """Exibe a Lista de Eventos Disponíveis"""
    eventos, _ = carregar_eventos()

    if not eventos:
        print("\n❌ Nenhum evento disponível no momento.")
        return
    print(f"{'ID':<5} 🎫 {'Nome':<20} 📅 {'Data':<12} 📖 {'Status':<12} 🔢 {'Vagas Rest.':<12}")
    for i, evento in enumerate(eventos, 1):
        print(f"{i:<5} {evento['nome']:<23} {evento['data']:<15} {evento.get('status', 'Desconhecido'):<15} {evento['vagas'] - len(evento['inscritos']):<12}")



def excluir_evento():
    """Permite Excluir Evento do Sistema
    
    O usuário (coordenador) consegue pesquisar por parte do nome e recebe uma relação com todos os eventos
    que possuem o termo pesquisado, após selecionar qual deseja excluir ainda recebe uam pergunta confirmando
    se o evento selecionado é o correto, e após confirmação exclui o evento
    """
    eventos, eventos_inscricoes = carregar_eventos()

    nome_parcial = input("🚨 Digite o nome ou parte do nome do evento que deseja excluir: ").strip().lower()

    eventos_filtrados = [evento for evento in eventos if nome_parcial in evento["nome"].lower()]
    if not eventos_filtrados:
        print("⚠ Nenhum evento encontrado com esse termo.")
        return
    
    print("\nEventos encontrados:")
    for i, evento in enumerate(eventos_filtrados, 1):
        print(f"{i}. {evento['nome']}")

    try:
        escolha = int(input("Digite o número do evento que deseja excluir: ").strip())
        if escolha < 1 or escolha > len(eventos_filtrados):
            print("Escolha inválida")
            return
    except ValueError:
        print("Entrada inválida.")
        return

    evento_para_excluir = eventos_filtrados[escolha - 1]

    if not confirmar_acao(f"Você deseja realmente excluir o evento '{evento_para_excluir['nome']}' (S/N) "):
        print("🛑 Operação cancelada")
        return

    eventos = [evento for evento in eventos if evento["nome"].lower() != evento_para_excluir["nome"].lower()]

    key_to_remove = None
    for key in list(eventos_inscricoes.keys()):
        if key.lower() == evento_para_excluir["nome"].lower():
            key_to_remove = key
            break
    if key_to_remove:
        eventos_inscricoes.pop(key_to_remove, None)
    
    salvar_eventos(eventos, eventos_inscricoes)
    print("✅ Evento excluído com sucesso!\n")


def inscricao_evento(usuario_id):
    """Permite que um aluno se inscreva em um evento disponível,
    atualizando também o dicionário de inscrições com um ID para cada inscrição.
    Usa o user_id para identificar o aluno e armazena mais detalhes na lista de inscritos.
    """
    eventos, eventos_inscricoes = carregar_eventos()
    alunos, coordenadores = carregar_usuarios()

    if not eventos:
        print("\n❌ Nenhum evento disponível no momento.")
        return

    print("\nEventos disponíveis:")
    for i, evento in enumerate(eventos, 1):
        vagas_restantes = evento['vagas'] - len(evento['inscritos'])
        print(f"{i}. {evento['nome']} - {evento['data']} (Vagas restantes: {vagas_restantes})")

    while True:
        try:
            escolha = int(input("🔢 Digite o número do evento no qual deseja se inscrever (ou 0 para cancelar): ").strip())
            if escolha == 0:
                print("🛑 Operação cancelada.")
                return
            if escolha < 1 or escolha > len(eventos):
                print("⚠ Escolha inválida. Tente novamente.")
                continue
            break
        except ValueError:
            print("⚠ Entrada inválida. Por favor, insira um número.")

    evento_escolhido = eventos[escolha - 1]
    vagas_restantes = evento_escolhido['vagas'] - len(evento_escolhido['inscritos'])
    if vagas_restantes <= 0:
        print("❌ Esse evento já atingiu o limite de inscrições.")
        return

    if not confirmar_acao(f"Você deseja se inscrever no evento '{evento_escolhido['nome']}'? (S/N) "):
        print("🛑 Operação cancelada.")
        return


    aluno_registrado = alunos.get(usuario_id)
    if not aluno_registrado:
        print("Erro: aluno não encontrado.")
        return


    if evento_escolhido["nome"] in aluno_registrado["inscricoes"]:
        print("Você já está inscrito nesse evento!")
        return


    aluno_info = {
        "id_aluno": usuario_id,
        "aluno_nome": aluno_registrado["nome"],
        "aluno_email": aluno_registrado["email"]
    }
    evento_escolhido["inscritos"].append(aluno_info)
    aluno_registrado["inscricoes"].append(evento_escolhido["nome"])


    chave_evento = evento_escolhido["nome"].strip().lower()
    inscricoes_evento = eventos_inscricoes.get(chave_evento, [])
    
    novo_id = len(inscricoes_evento) + 1
    nova_inscricao = {
        "id_inscricao": novo_id,
        "id_aluno": usuario_id,
        "aluno_nome": aluno_registrado["nome"],
        "aluno_email": aluno_registrado["email"]
    }
    inscricoes_evento.append(nova_inscricao)
    eventos_inscricoes[chave_evento] = inscricoes_evento

    salvar_eventos(eventos, eventos_inscricoes)
    salvar_usuarios(alunos, coordenadores)
    print(f"✅ Inscrição realizada com sucesso no evento '{evento_escolhido['nome']}'!")


def gerenciar_inscricoes_coord():
    """Permite um coordenador visualizar as inscrições por evento"""

    evento_filtrado = filtragem_evento()
    alunos, coordenadores = carregar_usuarios()
    eventos, eventos_inscricoes = carregar_eventos()


    if not evento_filtrado:
        if confirmar_acao("❌ Nenhum evento disponível no momento. Gostaria de cadastrar um evento no sistema? (S/N)"):
            cadastrar_evento()
        return
    
    if len(evento_filtrado) == 1:
        evento_escolhido = evento_filtrado[0]
    else:
        print("\nResultado da busca:\n")
        for i, evento in enumerate(evento_filtrado, 1):
            print(f"{i}. {evento['nome']}")
        try:
            escolha = int(input("Digite o número do evento que deseja visualizar as inscrições: ").strip())
            if escolha < 1 or escolha > len(evento_filtrado):
                if not confirmar_acao("Não encontramos o evento no sistema. Quer pesquisar por outro evento? (S/N) "):
                    print("🛑 Operação Cancelada")
                    return    
            evento_escolhido = evento_filtrado[escolha - 1]
        except ValueError:
            print("❌ Entrada Inválida. Operação cancelada")
            return


    chave = evento_escolhido["nome"].strip().lower()
    inscricoes = eventos_inscricoes.get(chave, [])

    if not inscricoes:
        if not confirmar_acao(f"\nNão há inscrições para o evento '{evento_escolhido['nome']}'. Quer pesquisar por outro evento? (S/N) "):
            print("🛑 Operação Cancelada")
            return
        gerenciar_inscricoes_coord()
    else:
        print(f"\nInscrições para o evento '{evento_escolhido['nome']}':")
        for insc in inscricoes:
            print(f"ID Inscrição: {insc['id_inscricao']}, Aluno ID: {insc['id_aluno']}, Nome:{insc['aluno_nome']}, Email: {insc['aluno_email']}")

    if not confirmar_acao("Deseja excluir alguma incsrição? (S/N) "):
        return
    
    try:
        id_para_excluir = int(input("Digite o ID da inscrição que deseja excluir: ").strip())
    except ValueError:
        print("🛑 Entrada inválida. Opereção cancelada!")
        return
    
    inscricoes_restantes = [insc for insc in inscricoes if insc["id_inscricao"] != id_para_excluir] 
    if len(inscricoes_restantes) == len(inscricoes):
        if not confirmar_acao("Não encontramos a inscrição. Deseja pesquisar por outro ID? (S/N) "):
            return

    eventos_inscricoes[chave] = inscricoes_restantes

    aluno_id_excluir = None
    for insc in inscricoes:
        if insc["id_inscricao"] == id_para_excluir:
            aluno_id_excluir = insc["id_aluno"]
            break

    if aluno_id_excluir:
        aluno_registrado = alunos.get(aluno_id_excluir)
        if aluno_registrado and evento_escolhido["nome"] in aluno_registrado["inscricoes"]:
            aluno_registrado["inscricoes"].remove(evento_escolhido["nome"])
        nova_lista_inscritos = [al for al in evento_escolhido["inscritos"] if al["id_aluno"] != aluno_id_excluir]
        evento_escolhido["inscritos"] = nova_lista_inscritos

    for ev in eventos:
        if ev["nome"].strip().lower() == chave:
            ev["inscritos"] = evento_escolhido["inscritos"]
            break

    salvar_eventos(eventos, eventos_inscricoes)
    salvar_usuarios(alunos, coordenadores)
    print("✅ Inscrição excluída com sucesso!")


def visualizar_inscricoes_aluno(usuario_id):
    """Permite ao aluno visualizar os eventos nos quais está inscrito"""

    alunos, _ = carregar_usuarios()
    aluno = alunos.get(usuario_id)
    
    if not aluno:
        if confirmar_acao("Aluno não encontrado. Deseja se cadastrar? (S/N) "):
            registrar_usuario()
        return
    inscricoes = aluno.get("inscricoes", [])
    if not inscricoes:
        if confirmar_acao("Você ainda não está inscrito em nenhum evento. Gostaria de ver os eventos disponíveis? (S/N) "):
            inscricao_evento(usuario_id)
        return
    else:
        print(f"\n👋 Olá, {aluno['nome']}! Você está inscrito nos seguintes eventos: ")
        for evento in inscricoes:
            print(f" - {evento}")


def menu():
    """Menu do Sistema"""
    carregar_eventos()
    carregar_usuarios()

    usuario_atual, tipo_usuario = None, None
    while not usuario_atual:
        opcao = input("🆕 Deseja [1] Registrar-se ou [2] Fazer Login? ").strip()
        if opcao == "1":
            usuario_atual, tipo_usuario = registrar_usuario()
        elif opcao == "2":
            usuario_atual, tipo_usuario = autenticar_usuario()
        else:
            print("❌ Opção inválida! Registre-se [1] ou Faça Login [2]: ")

    if tipo_usuario == "coordenador":
        while True:
            print("\n🎭 ===== MENU =====")
            print("1️⃣ - Cadastrar Evento")
            print("2️⃣ - Atualizar Evento")
            print("3️⃣ - Visualizar Eventos")
            print("4️⃣ - Visualizar Inscrições")
            print("5️⃣ - Excluir Evento")
            print("6️⃣ - Sair")
            opcao = input("👉 Escolha uma opção: ").strip()
            
            if opcao == "1":
                cadastrar_evento()
            elif opcao == "2":
                atualizar_evento()
            elif opcao == "3":
                visualizar_eventos()
            elif opcao == "4":
                gerenciar_inscricoes_coord()
            elif opcao == "5":
                excluir_evento()
            elif opcao == "6":
                print("\n👋 Saindo...\n")
                break
            else:
                print("❌ Opção inválida, tente novamente.\n")

    else:
        while True:
            print("\n🎭 ===== MENU =====")
            print("1️⃣ - Visualizar Eventos")
            print("2️⃣ - Me inscrever em Evento")
            print("3️⃣ - Minhas Inscrições")
            print("4️⃣ - Sair")
            opcao = input("👉 Escolha uma opção: ").strip()
            if opcao == "1":
                visualizar_eventos()
            elif opcao == "2":
                inscricao_evento(usuario_atual)
            elif opcao == "3":
                visualizar_inscricoes_aluno(usuario_atual)
            elif opcao == "4":
                print("\n👋 Saindo...\n")
                break
            else:
                print("❌ Opção inválida, tente novamente.\n")

menu()