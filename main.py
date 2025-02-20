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
            print("Você escolheu a opção 'Cadastrar Evento'")
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

# 🚀 Iniciar o sistema
menu()
