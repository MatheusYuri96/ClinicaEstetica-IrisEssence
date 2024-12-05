from datetime import datetime, timedelta  #Utilizamos timedelta para representar a diferença entre duas datas/horas

# Classe Serviço
class Servico:
    def __init__(self, codigo, nome, preco):
        self.codigo = codigo
        self.nome = nome
        self.preco = preco

    def __str__(self):
        return f"{self.codigo:<7} {self.nome:<22} {self.preco:>10.2f}"    #alinhamento a caracteres

# Classe Cliente
class Cliente:
    def __init__(self, nome, telefone, email):
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.agendamentos = []

    def adicionar_agendamento(self, servico, data_hora, pagamento):

        # Verifica se já existe agendamento no mesmo horário
        for agendamento in self.agendamentos:
            if agendamento["data_hora"] == data_hora:
                print(f"Já existe um agendamento para {self.nome} nesse horário.")
                return
            # Verifica se o novo agendamento entra em conflito com outro
            if abs(agendamento["data_hora"] - data_hora) < timedelta(hours=1):   #Só pode agendamentos fora de 1 hora.
                print(f"Não é possível agendar esse serviço. Já existe um agendamento nas proximidades.")
                return
        # Adiciona o agendamento
        self.agendamentos.append({"servico": servico.nome, "data_hora": data_hora, "preco": servico.preco, "pagamento": pagamento})
        print(f"Serviço '{servico.nome}' agendado para {self.nome} em {data_hora.strftime('%d/%m/%Y %H:%M')}, forma de pagamento: {pagamento}.")

    def remover_agendamento(self, data_hora):
        for agendamento in self.agendamentos:
            if agendamento["data_hora"] == data_hora:
                self.agendamentos.remove(agendamento)
                print(f"Agendamento de {self.nome} em {data_hora.strftime('%d/%m/%Y %H:%M')} removido com sucesso!")
                return
        print(f"Não foi encontrado agendamento para {self.nome} nesta data.")

    def visualizar_agendamentos(self):
        if not self.agendamentos:
            print(f"{self.nome} não tem agendamentos.")
        else:
            print("\n--- Agendamentos ---")
            for i, agendamento in enumerate(self.agendamentos, 1):   #Ele é útil quando você precisa tanto do índice (posição) quanto do valor de cada item ao percorrer um iterável.
                print(f"{i}. Serviço: {agendamento['servico']} | Data/Hora: {agendamento['data_hora'].strftime('%d/%m/%Y %H:%M')} | Preço: R${agendamento['preco']:.2f} | Pagamento: {agendamento['pagamento']}")

# Classe Clínica
class ClinicaEstetica:
    def __init__(self):
        self.servicos = {
            "1": Servico("1", "Botox", 500.00),
            "2": Servico("2", "Massagem Modeladora", 120.00),
            "3": Servico("3", "Massagem Relaxante", 80.00),
            "4": Servico("4", "Limpeza de Pele", 150.00),
            "5": Servico("5", "Design de Sobrancelhas", 50.00),
            "6": Servico("6", "Tratamento para acne", 200.00),
            "7": Servico("7", "Reconstrução capilar", 100.00),
            "8": Servico("8", "Depilação a laser", 250.00),
            "9": Servico("9", "Depilação a cera", 100.00),
            "10": Servico("10", "Drenagem linfática", 200.00),
        }
        self.clientes = []

    def cadastrar_cliente(self, nome, telefone, email):
        cliente = Cliente(nome, telefone, email)
        self.clientes.append(cliente)
        print(f"Cliente {nome} cadastrado com sucesso!")

    def exibir_servicos(self):
        print("\n--- Serviços Disponíveis ---")
        print("Código | Serviço                | Preço (R$)")
        print("-" * 40)
        for servico in self.servicos.values():
            print(servico)
        print("-" * 40)

    def buscar_cliente(self, nome):
        for cliente in self.clientes:
            if cliente.nome.lower() == nome.lower():
                return cliente
        return None

    def agendar_servico(self, nome_cliente):
        cliente = self.buscar_cliente(nome_cliente)
        if cliente:
            self.exibir_servicos()
            codigo_servico = input("Escolha o código do serviço desejado: ")
            if codigo_servico in self.servicos:
                servico = self.servicos[codigo_servico]
                data_str = input("Digite a data e hora do agendamento (dd/mm/aaaa hh:mm): ")
                try:
                    data_hora = datetime.strptime(data_str, "%d/%m/%Y %H:%M")
                    if data_hora < datetime.now():
                        print("Não é possível agendar para uma data/hora no passado!")
                        return
                except ValueError:
                    print("Formato de data/hora inválido! Tente novamente.")
                    return
                pagamento = input("Digite a forma de pagamento (Dinheiro, Cartão, Pix): ")
                cliente.adicionar_agendamento(servico, data_hora, pagamento)
            else:
                print("Código de serviço inválido!")
        else:
            print("Cliente não encontrado!")

    def visualizar_agendamentos(self, nome_cliente):
        cliente = self.buscar_cliente(nome_cliente)
        if cliente:
            cliente.visualizar_agendamentos()
        else:
            print("Cliente não encontrado!")

    def editar_agendamento(self, nome_cliente):
        cliente = self.buscar_cliente(nome_cliente)
        if cliente:
            cliente.visualizar_agendamentos()
            try:
                indice = int(input("Digite o número do agendamento a ser editado: ")) - 1
                self.exibir_servicos()
                codigo_servico = input("Escolha o novo código do serviço: ")
                if codigo_servico in self.servicos:
                    servico = self.servicos[codigo_servico]
                    nova_data_str = input("Digite a nova data e hora (dd/mm/aaaa hh:mm): ")
                    nova_data_hora = datetime.strptime(nova_data_str, "%d/%m/%Y %H:%M")
                    cliente.agendamentos[indice] = {"servico": servico.nome, "data_hora": nova_data_hora, "preco": servico.preco, "pagamento": cliente.agendamentos[indice]["pagamento"]}
                    print(f"Agendamento de {cliente.nome} editado com sucesso!")
                else:
                    print("Código de serviço inválido!")
            except ValueError:
                print("Número do agendamento inválido!")
        else:
            print("Cliente não encontrado!")

    def excluir_agendamento(self, nome_cliente):
        cliente = self.buscar_cliente(nome_cliente)
        if cliente:
            cliente.visualizar_agendamentos()
            try:
                indice = int(input("Digite o número do agendamento a ser excluído: ")) - 1
                del cliente.agendamentos[indice]
                print("Agendamento excluído com sucesso!")
            except ValueError:
                print("Número do agendamento inválido!")
        else:
            print("Cliente não encontrado!")

# Função para exibir o menu
def menu():
    clinica = ClinicaEstetica()

    while True:
        print("\n--- Menu da Clínica ---")
        print("1. Cadastrar Cliente")
        print("2. Agendar Serviço")
        print("3. Visualizar Agendamentos")
        print("4. Editar Agendamento")
        print("5. Excluir Agendamento")
        print("6. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Digite o nome do cliente: ")
            telefone = input("Digite o telefone do cliente: ")
            email = input("Digite o e-mail do cliente: ")
            clinica.cadastrar_cliente(nome, telefone, email)
        elif opcao == "2":
            nome_cliente = input("Digite o nome do cliente: ")
            clinica.agendar_servico(nome_cliente)
        elif opcao == "3":
            nome_cliente = input("Digite o nome do cliente: ")
            clinica.visualizar_agendamentos(nome_cliente)
        elif opcao == "4":
            nome_cliente = input("Digite o nome do cliente: ")
            clinica.editar_agendamento(nome_cliente)
        elif opcao == "5":
            nome_cliente = input("Digite o nome do cliente: ")
            clinica.excluir_agendamento(nome_cliente)
        elif opcao == "6":
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")

# Início do programa
menu()

