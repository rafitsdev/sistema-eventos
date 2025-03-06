# 📅 Sistema de Gerenciamento de Eventos com Python

Este projeto é um **sistema de gerenciamento de eventos** que permite a criação, inscrição e administração de eventos de forma eficiente. O sistema possui suporte para **alunos e coordenadores**, garantindo que os eventos sejam organizados e monitorados de maneira adequada.

## 🚀 Funcionalidades
✅ **Registro e autenticação de usuários**: Permite que alunos e coordenadores se cadastrem e façam login.  
✅ **Criação de eventos**: Coordenadores podem cadastrar eventos, definindo nome, data, descrição e número de vagas.  
✅ **Atualização e exclusão de eventos**: Coordenadores podem editar ou excluir eventos cadastrados.  
✅ **Inscrição em eventos**: Alunos podem visualizar e se inscrever em eventos disponíveis.  
✅ **Gerenciamento de inscrições**: Coordenadores podem visualizar e gerenciar as inscrições dos eventos.  
✅ **Persistência de dados**: O sistema salva e carrega os eventos e usuários automaticamente de arquivos JSON.  

## 🛠️ Tecnologias Utilizadas
- **Python**: Implementação do sistema.  
- **JSON**: Para persistência de dados.  
- **OS e RE**: Manipulação de arquivos e validações diversas.  
- **Datetime**: Para validação de datas e atualização automática do status dos eventos.  

## 📂 Estrutura do Projeto
```
/gerenciador-eventos
│── /data
│   ├── eventos.json        # Armazena os eventos e inscrições
│   ├── alunos.json         # Armazena os dados dos alunos
│   ├── coordenadores.json  # Armazena os dados dos coordenadores
│── main.py                 # Código principal do sistema
│── README.md               # Documentação do projeto
│── .gitignore              # Arquivo para ignorar itens desnecessários
```

## 🚀 Como Executar o Projeto
1. **Clone o repositório**:
   ```bash
   git clone https://github.com/rafitsdev/sistema-eventos/
   cd sistema-eventos
   ```
2. **Execute o programa**:
   ```bash
   python main.py
   ```

## 🔎 Como Utilizar
### Para coordenadores:
- Criar, atualizar ou excluir eventos.
- Gerenciar inscrições de alunos.
- Visualizar eventos e status de cada um.

### Para alunos:
- Visualizar eventos disponíveis.
- Inscrever-se e cancelar inscrições em eventos.
- Verificar suas inscrições ativas.

---

## 📌 Contribuições
Se desejar sugerir melhorias ou reportar problemas, fique à vontade para abrir uma _issue_ ou enviar um _pull request_.

---

## 📜 Licença
Este projeto está sob a licença MIT.

---

## 📬 **Contato:**
📧 Email: [rafaelrodrigues.contatoo@gmail.com](mailto:rafaelrodrigues.contatoo@gmail.com)

🔗 LinkedIn: [Rafael Martins Rodrigues](https://www.linkedin.com/in/rafaelmartinsrodrigues/)
