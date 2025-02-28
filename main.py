import time
import json
import os
import re
from datetime import datetime

# ===================================
# Configuração do diretório de dados
# ===================================
data_dir = "data"
os.makedirs(data_dir, exist_ok=True)

eventos_json = os.path.join(data_dir, "eventos.json")
alunos_json = os.path.join(data_dir, "alunos.json")
coordenadores_json = os.path.join(data_dir, "coordenadores.json")

# ===================
# Funções de Suporte
# ===================
def confirmar_acao(mensagem):
    """Solicita confirmação ao usuário."""
    while True:
        resposta = input(mensagem + " ").strip().lower()
        if resposta in ["s", "sim"]:
            return True
        elif resposta in ["n", "nao", "não"]:
            return False
        else:
            print("❌ Opção inválida. Digite 'S' para Sim ou 'N' para Não.")

def gerar_user_id(usuarios):
    """Gera um ID sequencial para os usuários."""
    return str(max(map(int, usuarios.keys()), default=0) + 1)

def validar_email(email):
    """Valida o formato do email."""
    padrao = r"[^@]+@[^@]+\.[^@]+"
    return re.match(padrao, email) is not None

def validar_data(data):
    """Valida o formato da data (DD/MM/AAAA)."""
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False

# ==================================
# Atualização de Status dos Eventos
# ==================================
def atualizar_status_eventos():
    """Atualiza o status dos eventos com base na data.
        Se a data do evento já passou, define 'Finalizado';
        caso contrário, 'Disponível'.
    """
    eventos, eventos_inscricoes = carregar_eventos()
    hoje = datetime.now()
    for evento in eventos:
        try:
            data_evento = datetime.strptime(evento["data"], "%d/%m/%Y")
            if data_evento < hoje:
                evento["status"] = "Finalizado"
            else:
                evento["status"] = "Disponível"
        except Exception:
            evento["status"] = "Desconhecido"
    salvar_eventos(eventos, eventos_inscricoes)

# ============================
# Exibição Tabular de Eventos
# ============================
def exibir_eventos(eventos):
    """Exibe a lista de eventos em formato tabular com cabeçalho."""
    if not eventos:
        print("❌ Nenhum evento disponível.")
        return
    print("\n{:<7} {:<25} {:<12} {:<14} {:<12}".format("🎫 ID", "👤 Nome", "📅 Data", "🟢 Status", "🔢 Vagas Rest."))
    print("-" * 80)
    for i, evento in enumerate(eventos, 1):
        vagas_restantes = evento['vagas'] - len(evento['inscritos'])
        status = evento.get("status", "Desconhecido")
        print("{:<8} {:<26} {:<14} {:<14} {:<12}".format(i, evento['nome'], evento['data'], status, vagas_restantes))

# ===============================
# Função de Filtragem de Evento
# ===============================
def filtragem_evento():
    """Filtra eventos com base no termo digitado.
        - Se o termo for numérico, retorna o evento correspondente pelo índice.
        - Se for um trecho do nome, retorna os eventos que contenham esse trecho (case-insensitive).
    """
    atualizar_status_eventos()
    eventos, _ = carregar_eventos()
    if not eventos:
        print("❌ Nenhum evento encontrado.")
        return []
    print("\nEventos disponíveis:")
    exibir_eventos(eventos)
    termo = input("\nDigite o número do evento ou um trecho do nome para filtrar (ex: '1' ou 'Nome do Evento'): ").strip()
    print("\n⏳ Filtrando eventos...")
    time.sleep(1.5)
    if termo.isdigit():
        indice = int(termo)
        if 1 <= indice <= len(eventos):
            return [eventos[indice - 1]]
        else:
            print("🛑 Número inválido.")
            return []
    else:
        eventos_filtrados = [evento for evento in eventos if termo.lower() in evento["nome"].lower()]
        if not eventos_filtrados:
            print("🛑 Nenhum evento encontrado com esse termo\n")
        return eventos_filtrados
    

# ======================
# Persistência de Dados
# ======================
def carregar_eventos():
    """Carrega os eventos do JSON e normaliza as chaves de inscrições para lowercase."""
    if not os.path.exists(eventos_json):
        with open(eventos_json, "w") as f:
            json.dump({"eventos": [], "inscricoes": {}}, f)
    with open(eventos_json, "r") as f:
        dados_eventos = json.load(f)
    inscricoes = {k.lower(): v for k, v in dados_eventos.get("inscricoes", {}).items()}
    return dados_eventos.get("eventos", []), inscricoes

def salvar_eventos(eventos, eventos_inscricoes):
    """Salva os eventos e inscrições no JSON."""
    with open(eventos_json, "w") as f:
        json.dump({"eventos": eventos, "inscricoes": eventos_inscricoes}, f, indent=4)

def carregar_usuarios():
    """Carrega os usuários dos arquivos JSON."""
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
    """Salva os usuários no JSON."""
    with open(alunos_json, "w") as f:
        json.dump(alunos, f, indent=4)
    with open(coordenadores_json, "w") as f:
        json.dump(coordenadores, f, indent=4)


# ==================
# Funções de Login
# ==================
def registrar_usuario():
    """Registra um novo usuário no sistema, garantindo email único (case-insensitive)."""
    alunos, coordenadores = carregar_usuarios()
    nome = input("\n🆕 Digite seu nome: ").strip()
    while True:
        email = input("📧 Digite seu email: ").strip().lower()
        if not validar_email(email):
            print("❌ Email inválido. Use o formato usuario@exemplo.com")
            continue
        email_ja_registrado = False
        for usuario in alunos.values():
            if usuario["email"].strip().lower() == email:
                email_ja_registrado = True
                break
        if not email_ja_registrado:
            for usuario in coordenadores.values():
                if usuario["email"].strip().lower() == email:
                    email_ja_registrado = True
                    break
        if email_ja_registrado:
            time.sleep(1.5)
            print("🛑 Esse email já está registrado!")
            if confirmar_acao("📧 Gostaria de tentar outro email? (S/N)"):
                continue
            else:
                return None, None
        else:
            break
    while True:
        tipo = input("🎭 Tipo de usuário (Aluno/Coordenador): ").strip().lower()
        if tipo in ["aluno", "coordenador"]:
            break
        print("❌ Tipo inválido! Digite 'Aluno' ou 'Coordenador'.")
    user_id = gerar_user_id(alunos) if tipo == "aluno" else gerar_user_id(coordenadores)
    curso = input("📚 Digite o curso que você está matriculado: ").strip() if tipo == "aluno" else None
    usuario = {"id": user_id, "nome": nome, "email": email, "tipo": tipo, "curso": curso, "inscricoes": []}
    if tipo == "aluno":
        alunos[user_id] = usuario
    else:
        coordenadores[user_id] = usuario
    salvar_usuarios(alunos, coordenadores)
    print("\n⌛ Salvando suas credenciais, aguarde...")
    time.sleep(2)
    print(f"✅ Registro realizado com sucesso! Seu ID é {user_id}")
    time.sleep(1.75)
    return user_id, tipo

def autenticar_usuario():
    """Autentica o usuário e retorna seu user_id e tipo."""
    while True:
        alunos, coordenadores = carregar_usuarios()
        email = input("\n👤 Digite seu email para login: ").strip().lower()
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
            print("\n⌛ Efetuando login, aguarde...")
            time.sleep(2)
            print(f"✅ Login bem-sucedido! Olá, {usuario_encontrado['nome']} ({usuario_encontrado['tipo'].capitalize()})!")
            return usuario_id, usuario_encontrado["tipo"]
        if not confirmar_acao("❌ Usuário não encontrado. Deseja se cadastrar? (S/N)"):
            return None, None
        return registrar_usuario()

# ===================
# Funções Principais
# ===================
def cadastrar_evento():
    """Cadastra um novo evento no sistema, validando duplicidade.
        Se o evento já existir, exibe o evento e interrompe o cadastro.
    """
    while True:
        eventos, eventos_inscricoes = carregar_eventos()
        nome = input("📌 Nome do evento: ").strip()
        data = input("📅 Data do evento (DD/MM/AAAA): ").strip()
        if not validar_data(data):
            print("❌ Data inválida! Use o formato DD/MM/AAAA")
            return
        descricao = input("📖 Descrição do evento: ").strip()
        print("\n🕐 Salvando evento no sistema...")
        time.sleep(1.5)
        while True:
            try:
                vagas = int(input("👥 Agora informe o número máximo de vagas para o evento: "))
                if vagas <= 0:
                    if not confirmar_acao("🛑 O número de vagas deve ser maior que zero. Tentar novamente? (S/N) "):
                        return
                    continue
                break
            except ValueError:
                print("❌ Valor inválido. Insira um número.")
                continue

        novo_evento = {
            'nome': nome,
            'data': data,
            'descricao': descricao,
            'vagas': vagas,
            'inscritos': []
        }

        evento_existente = None
        for evento in eventos:
            if (evento['nome'].strip().lower() == novo_evento['nome'].strip().lower() and
                evento['data'].strip() == novo_evento['data'].strip() and
                evento['descricao'].strip().lower() == novo_evento['descricao'].strip().lower() and
                evento['vagas'] == novo_evento['vagas']):
                evento_existente = evento

        if evento_existente:
            print("\n🛑 Evento já existe no sistema.")
            exibir_eventos([evento])
            time.sleep(1.5)
            if confirmar_acao("\n❓ Gostaria de cadastrar outro evento? (S/N) "):
                continue
            else:
                return
        else:
            eventos.append(novo_evento)
            eventos_inscricoes[nome.lower()] = []
            salvar_eventos(eventos, eventos_inscricoes)
            print("✅ Evento cadastrado com sucesso!")


def atualizar_evento():
    """Atualiza os dados de um evento existente utilizando filtragem."""
    atualizar_status_eventos()
    while True:
        eventos_filtrados = filtragem_evento()
        if not eventos_filtrados:
            if not confirmar_acao("Gostaria de pesquisar por outro evento? (S/N) "):
                return
            continue
        if len(eventos_filtrados) > 1:
            print("\n\nEventos filtrados:")
            exibir_eventos(eventos_filtrados)
            try:
                escolha = int(input("\nDigite o número do evento que deseja atualizar: ").strip())
                if escolha < 1 or escolha > len(eventos_filtrados):
                    print("❌ Número inválido. Operação cancelada.")
                    return
                evento_escolhido = eventos_filtrados[escolha - 1]
            except ValueError:
                print("❌ Entrada inválida. Operação cancelada.")
                return
        else:
            evento_escolhido = eventos_filtrados[0]
        
        eventos, eventos_inscricoes = carregar_eventos()
        chave_evento = evento_escolhido["nome"].strip().lower()
        for evento in eventos:
            if evento["nome"].strip().lower() == chave_evento:
                print("\n✅ Evento encontrado para atualização!")
                while True:
                    alteracao = input("\n📝 O que deseja alterar? (Nome, Data, Descrição ou Qtde de vagas): ").strip().lower()
                    if alteracao == "nome":
                        novo_nome = input("\n📌 Novo nome: ").strip()
                        chave_antiga = None
                        for chave in eventos_inscricoes:
                            if chave == chave_evento:
                                chave_antiga = chave
                                break
                        if chave_antiga:
                            eventos_inscricoes[novo_nome.lower()] = eventos_inscricoes.pop(chave_antiga)
                        else:
                            eventos_inscricoes[novo_nome.lower()] = []
                        evento["nome"] = novo_nome
                        chave_evento = novo_nome.strip().lower()
                    elif alteracao == "data":
                        evento["data"] = input("\n📅 Nova data (DD/MM/AAAA): ").strip()
                    elif alteracao in ["descricao", "descrição"]:
                        evento["descricao"] = input("\n📖 Nova descrição: ").strip()
                    elif alteracao in ["qtde", "qtde de vagas"]:
                        while True:
                            try:
                                evento["vagas"] = int(input("\n👥 Nova quantidade de vagas: "))
                                if evento["vagas"] <= 0:
                                    if not confirmar_acao("🛑 Número de vagas deve ser maior que zero. Tentar novamente? (S/N) "):
                                        return
                                    continue
                                break
                            except ValueError:
                                print("🛑 Valor inválido. Opereção cancelada.")
                                continue
                    else:
                        print("🛑 Opção inválida. Escolha entre Nome, Data, Descrição ou Qtde de vagas.")
                        continue
                    print("\n⏳ Atualizando evento...")
                    time.sleep(2)
                    salvar_eventos(eventos, eventos_inscricoes)
                    print("✅ Evento atualizado com sucesso!\n")
                    if not confirmar_acao("📝 Deseja alterar mais algo neste evento? (S/N)"):
                        print("\n⏪ Retornando ao menu")
                        time.sleep(1.5)
                        return
                    break
        else:
            if not confirmar_acao("🙁 Evento não encontrado. Deseja cadastrar um novo evento? (S/N) "):
                print("\n⏪ Retornando ao menu")
                time.sleep(1.5)
                return


def visualizar_eventos_coord():
    """Exibe a lista de eventos disponíveis em formato tabular."""
    atualizar_status_eventos()
    print("\n🔎 Trazendo informações de eventos no sistema...")
    time.sleep(2)
    eventos, _ = carregar_eventos()
    if not eventos:
        print("❌ Nenhum evento disponível.")
        return
    print("\n🎭 Eventos Disponíveis:")
    exibir_eventos(eventos)
    time.sleep(1.5)
    print("\n❔ O que deseja fazer:\n")
    print("1️⃣ - Atualizar Evento")
    print("2️⃣ - Excluir Evento")
    print("3️⃣ - Gerenciar Inscrições")
    print("4️⃣ - Voltar ao menu principal")
    opcao = input("👉 Escolha uma opção: ").strip()
    if opcao == "1":
        atualizar_evento()
    elif opcao == "2":
        excluir_evento()
    elif opcao == "3":
        gerenciar_inscricoes_coord()
    elif opcao == "4":
        print("\n⏪ Retornando ao menu")
        time.sleep(1.5)
        return
    else:
        print("❌ Opção inválida. Retornando ao menu principal.")
        time.sleep(1)
        return


def visualizar_eventos_alunos():
    """Exibe a lista de eventos disponíveis em formato tabular para os alunos"""
    atualizar_status_eventos()
    eventos, _ = carregar_eventos()
    print("\n🔎 Trazendo informações de eventos no sistema...")
    time.sleep(2)
    if not eventos:
        print("❌ Nenhum evento disponível.")
        return
    exibir_eventos(eventos)


def excluir_evento():
    """Exclui um evento utilizando filtragem."""
    eventos_filtrados = filtragem_evento()
    if not eventos_filtrados:
        print("🙁 Nenhum evento encontrado para exclusão.")
        return
    if len(eventos_filtrados) > 1:
        print("\nEventos filtrados:")
        exibir_eventos(eventos_filtrados)
        try:
            escolha = int(input("\n Digite o número do evento que deseja excluir: ").strip())
            if escolha < 1 or escolha > len(eventos_filtrados):
                print("🛑 Número inválido. Operação cancelada.")
                return
            evento_para_excluir = eventos_filtrados[escolha - 1]
        except ValueError:
            print("❌ Entrada inválida. Operação cancelada.")
            return
    else:
        evento_para_excluir = eventos_filtrados[0]
    if not confirmar_acao(f"\n❓ Tem certeza de que deseja ecluir o evento '{evento_para_excluir['nome']}'? (S/N)"):
        print("🛑 Operação cancelada.")
        print("\n⏪ Retornando ao menu")
        time.sleep(1.5)
        return
    eventos, eventos_inscricoes = carregar_eventos()
    eventos = [evento for evento in eventos if evento["nome"].strip().lower() != evento_para_excluir["nome"].strip().lower()]
    chave = evento_para_excluir["nome"].strip().lower()
    if chave in eventos_inscricoes:
        eventos_inscricoes.pop(chave, None)
    print("\n🚮 Excluindo evento do sistema, aguarde...")
    time.sleep(1.5)
    salvar_eventos(eventos, eventos_inscricoes)
    print("✅ Evento excluído com sucesso!")
    print("\n⏪ Retornando ao menu")
    time.sleep(1.5)


def gerenciar_inscricoes_coord():
    """Permite ao coordenador visualizar e gerenciar inscrições de um evento."""
    while True:
        eventos_filtrados = filtragem_evento()
        alunos, coordenadores = carregar_usuarios()
        eventos, eventos_inscricoes = carregar_eventos()
        if not eventos_filtrados:
            if confirmar_acao("❌ Nenhum evento encontrado. Deseja cadastrar um evento? (S/N)"):
                cadastrar_evento()
            return
        if len(eventos_filtrados) > 1:
            print("\nEventos filtrados:")
            exibir_eventos(eventos_filtrados)
            try:
                escolha = int(input("\nDigite o número do evento para ver inscrições: ").strip())
                if escolha < 1 or escolha > len(eventos_filtrados):
                    print("🛑 Número inválido. Operação cancelada.")
                    continue
                evento_escolhido = eventos_filtrados[escolha - 1]
            except ValueError:
                print("❌ Entrada inválida. Operação cancelada.")
                return
        else:
            evento_escolhido = eventos_filtrados[0]
        chave = evento_escolhido["nome"].strip().lower()
        inscricoes = eventos_inscricoes.get(chave, [])
        if not inscricoes:
            if confirmar_acao(f"🛑 Não há inscrições para '{evento_escolhido['nome']}'. Deseja pesquisar outro evento? (S/N)"):
                gerenciar_inscricoes_coord()
            else:
                print("🛑 Operação cancelada. Retornando ao menu")
                time.sleep(1.5)
            return
        print(f"\n📋 Inscrições para '{evento_escolhido['nome']}':\n")
        print("{:<15} {:<10} {:<25} {:<30}".format("🔖 ID Inscrição", "👤 Aluno ID", "👥 Nome", "📧 Email"))
        print("-" * 80)
        for insc in inscricoes:
            print("{:<15} {:<10} {:<25} {:<30}".format(insc['id_inscricao'], insc['id_aluno'], insc['aluno_nome'], insc['aluno_email']))
        time.sleep(2)
        if not confirmar_acao("\n❓ Deseja excluir alguma inscrição? (S/N)"):
            return
        try:
            id_para_excluir = int(input("\nDigite o ID da inscrição a excluir: ").strip())
        except ValueError:
            print("❌ Entrada inválida. Operação cancelada!")
            return
        inscricoes_restantes = [insc for insc in inscricoes if insc["id_inscricao"] != id_para_excluir]
        if len(inscricoes_restantes) == len(inscricoes):
            if not confirmar_acao("🛑 Inscrição não encontrada. Pesquisar outro ID? (S/N)"):
                return
        for idx, insc in enumerate(inscricoes_restantes, start = 1):
            insc["id_inscricao"] = idx
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
    """Permite ao aluno visualizar os eventos nos quais está inscrito e cancelar sua inscrição, se desejar."""

    eventos_completos, eventos_inscricoes = carregar_eventos()
    alunos, _ = carregar_usuarios()
    aluno = alunos.get(usuario_id)
    
    print("\n🔎 Buscando suas inscrições...")
    time.sleep(2.5)
    
    inscricoes = aluno.get("inscricoes", [])
    if not inscricoes:
        if confirmar_acao("\n😞 Você não está inscrito em nenhum evento. Deseja ver os eventos disponíveis e se inscrever? (S/N)"):
            print("\n🔎 Buscando eventos disponíveis...")
            time.sleep(2.5)
            inscricao_evento(usuario_id)
        print("\n⏪ Retornando ao menu...")
        time.sleep(1.5)
        return


    eventos_inscritos = [evento for evento in eventos_completos if evento["nome"] in inscricoes]
    print(f"\n👋 Olá, {aluno['nome']}! Você está inscrito nos seguintes eventos:")
    exibir_eventos(eventos_inscritos)
    
    
    if confirmar_acao("\n❓ Deseja cancelar sua inscrição em algum evento? (S/N) "):
        try:
            escolha = int(input("\nDigite o número do evento para cancelar sua inscrição: ").strip())
            if escolha < 1 or escolha > len(eventos_inscritos):
                print("🛑 Número inválido. Operação cancelada.")
                print("⏪ Retornando ao menu")
                time.sleep(1.5)
                return
        except ValueError:
            print("🛑 Entrada inválida. Operação cancelada.")
            print("⏪ Retornando ao menu")
            time.sleep(1.5)
            return
        
        evento_cancelar = eventos_inscritos[escolha - 1]
        chave = evento_cancelar["nome"].strip().lower()
        
        print("\n⏳ Processando cancelamento...")
        time.sleep(2)
        if evento_cancelar["nome"] in aluno["inscricoes"]:
            aluno["inscricoes"].remove(evento_cancelar["nome"])
        
        for evento in eventos_completos:
            if evento["nome"].strip().lower() == chave:
                evento["inscritos"] = [insc for insc in evento["inscritos"] if insc["id_aluno"] != usuario_id]
                break
        
        inscricoes_evento = eventos_inscricoes.get(chave, [])
        novas_inscricoes = [insc for insc in inscricoes_evento if insc["id_aluno"] != usuario_id]
        for idx, insc in enumerate(novas_inscricoes, start=1):
            insc["id_inscricao"] = idx
        eventos_inscricoes[chave] = novas_inscricoes
        

        salvar_eventos(eventos_completos, eventos_inscricoes)
        salvar_usuarios(alunos, _)
        print("✅ Sua inscrição foi cancelada com sucesso!")
        print("⏪ Retornando ao menu")
        time.sleep(1.5)
    else:
        print("\n✅ Nenhuma alteração realizada.\n")
        print("⏪ Retornando ao menu")
        time.sleep(1.5)



def inscricao_evento(usuario_id):
    """Permite que um aluno se inscreva em um evento disponível."""
    atualizar_status_eventos()
    eventos, eventos_inscricoes = carregar_eventos()
    alunos, coordenadores = carregar_usuarios()

    if not eventos:
        print("❌ Nenhum evento disponível.")
        return

    print("\nEventos disponíveis:")
    exibir_eventos(eventos)
    time.sleep(1.5)
    
    while True:
        try:
            escolha = int(input("\n🔢 Número do evento para inscrição (ou 0 para cancelar): ").strip())
            if escolha == 0:
                print("🛑 Operação cancelada.")
                print("⏪ Retornando ao menu")
                time.sleep(1.5)
                return
            if escolha < 1 or escolha > len(eventos):
                time.sleep(1.5)
                print("🛑 Escolha inválida. Tente novamente.")
                continue
            break
        except ValueError:
            time.sleep(1.5)
            print("🛑 Entrada inválida. Insira um número.")

    evento_escolhido = eventos[escolha - 1]
    vagas_restantes = evento_escolhido['vagas'] - len(evento_escolhido['inscritos'])
    if vagas_restantes <= 0:
        print("❌ Limite de inscrições atingido.")
        print("⏪ Retornando ao menu")
        time.sleep(1.5)
        return

    if not confirmar_acao(f"❓ Confirmar inscrição no evento '{evento_escolhido['nome']}'? (S/N)"):
        print("🛑 Operação cancelada.")
        print("⏪ Retornando ao menu")
        time.sleep(1.5)
        return

    aluno_registrado = alunos.get(usuario_id)
    if evento_escolhido["nome"] in aluno_registrado["inscricoes"]:
        print("🛑 Você já está inscrito neste evento!")
        visualizar_inscricoes_aluno(usuario_id)
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
    print("⏪ Retornando ao menu")
    time.sleep(1.5)


# ===============
# Menu Principal
# ===============
def menu():
    """Menu do Sistema"""
    carregar_eventos()
    carregar_usuarios()
    usuario_atual, tipo_usuario = None, None
    print("😁 Olá, Seja bem-vindo! Escolha uma das opções abaixo\n")
    time.sleep(1.75)
    while not usuario_atual:
        opcao = input("🆕 [1] Registrar-se ou [2] Fazer Login? ").strip()
        if opcao == "1":
            usuario_atual, tipo_usuario = registrar_usuario()
        elif opcao == "2":
            usuario_atual, tipo_usuario = autenticar_usuario()
        else:
            print("❌ Opção inválida! Registre-se [1] ou Faça Login [2].")
    if tipo_usuario == "coordenador":
        while True:
            print("\n" + "="*50)
            print("          MENU COORDENADOR          ")
            print("="*50)
            print("1️⃣ - Cadastrar Evento")
            print("2️⃣ - Atualizar Evento")
            print("3️⃣ - Visualizar Eventos")
            print("4️⃣ - Gerenciar Inscrições de Alunos")
            print("5️⃣ - Excluir Evento")
            print("6️⃣ - Sair")
            opcao = input("👉 Escolha uma opção: ").strip()
            if opcao == "1":
                cadastrar_evento()
            elif opcao == "2":
                atualizar_evento()
            elif opcao == "3":
                visualizar_eventos_coord()
            elif opcao == "4":
                gerenciar_inscricoes_coord()
            elif opcao == "5":
                excluir_evento()
            elif opcao == "6":
                print("\n👋 Saindo...\n")
                break
            else:
                print("❌ Opção inválida, tente novamente.")
    else:
        while True:
            print("\n" + "="*40)
            print("            MENU ALUNO             ")
            print("="*40)
            print("1️⃣ - Visualizar Eventos")
            print("2️⃣ - Me inscrever em Evento")
            print("3️⃣ - Minhas Inscrições")
            print("4️⃣ - Sair")
            opcao = input("👉 Escolha uma opção: ").strip()
            if opcao == "1":
                visualizar_eventos_alunos()
            elif opcao == "2":
                inscricao_evento(usuario_atual)
            elif opcao == "3":
                visualizar_inscricoes_aluno(usuario_atual)
            elif opcao == "4":
                print("\n👋 Saindo...\n")
                break
            else:
                print("❌ Opção inválida, tente novamente.")

menu()