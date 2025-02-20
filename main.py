eventos = []
eventos_incricoes = {}

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
    eventos_incricoes[nome] = []
    print("\n✅ Evento cadastrado com sucesso!")
    return

def menu():
    while True:
        print("\n🎭 ===== MENU =====")
        print("1️⃣ - Cadastrar Evento")
        print("2️⃣ - Atualizar Evento")
        print("3️⃣ - Visualizar Eventos")
        print("4️⃣ - Me Inscrever em Evento")
        print("5️⃣ - Excluir Evento")
        print("6️⃣ - Sair")
        opcao = input("👉 Escolha uma opção: ").strip()
        
        if opcao == "1":
            cadastrar_evento()
        elif opcao == "2":
            print("Você escolheu a opção 'Atualizar Evento'")
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