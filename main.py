import time

eventos = []
eventos_inscricoes = {}

def confirmar_acao(mensagem):
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta in ["s", "sim"]:
            return True
        elif resposta in ["n", "nao", "não"]:
            return False
        else:
            print("❌ Opção inválida. Digite 'S' para Sim ou 'N' para Não.")

def cadastrar_evento():
    nome = input("\n📌 Nome do evento: ").strip()
    data = input("📅 Data do evento (DD/MM/AAAA): ").strip()
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
    print("\n✅ Evento cadastrado com sucesso!")
    return

def atualizar_evento():
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
                print("\n✅ Evento atualizado com sucesso!")

                if not confirmar_acao("\n📖 Deseja alterar mais alguma coisa neste evento? (S/N): "):
                    return

    print("\n⚠ Evento não encontrado!")

def menu():
    while True:
        print("\n🎭 ===== MENU =====")
        print("1️⃣ Cadastrar Evento")
        print("2️⃣ Atualizar Evento")
        print("3️⃣ Visualizar Eventos")
        print("4️⃣ Me Inscrever em Evento")
        print("5️⃣ Excluir Evento")
        print("6️⃣ Sair")
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