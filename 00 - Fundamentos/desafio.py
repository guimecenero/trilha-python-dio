from abc import ABC, abstractmethod
from datetime import datetime

# Classe abstrata para transações
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

# Classe para o histórico de transações
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            'tipo': type(transacao).__name__,
            'valor': transacao.valor,
            'data_hora': datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })

# Classe para saques
class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

# Classe para depósitos
class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

# Classe para o Cliente
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

# Subclasse de Cliente para Pessoa Física
class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

# Classe para a Conta
class Conta:
    def __init__(self, numero, cliente, agencia="0001"):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def sacar(self, valor):
        if valor > self.saldo:
            print("Operação falhou! Saldo insuficiente.")
            return False
        if valor <= 0:
            print("Operação falhou! O valor do saque deve ser positivo.")
            return False
        self.saldo -= valor
        return True

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            return True
        print("Operação falhou! Valor inválido.")
        return False

# Subclasse de Conta para Conta Corrente
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_diarios = 0
        self.data_ultimo_saque = None

    def sacar(self, valor):
        # Verifica se o valor excede o limite de saque
        if valor > self.limite:
            print("Operação falhou! Valor do saque excede o limite de R$500.")
            return False

        # Verifica se os saques diários já atingiram o limite
        data_atual = datetime.now().strftime("%d-%m-%Y")
        if self.data_ultimo_saque != data_atual:
            self.saques_diarios = 0  # Reseta o contador de saques diários

        if self.saques_diarios >= self.limite_saques:
            print("Operação falhou! Limite diário de 3 saques atingido.")
            return False

        # Se as validações passarem, realiza o saque
        if super().sacar(valor):
            self.saques_diarios += 1
            self.data_ultimo_saque = data_atual
            return True
        return False

    def __str__(self):
        return f"""
        Agência: {self.agencia}
        Número da Conta: {self.numero}
        Cliente: {self.cliente.nome}
        Saldo: R$ {self.saldo:.2f}
        """

# Função para criar um novo cliente
def criar_usuario(clientes):
    cpf = input("Informe o CPF (somente números): ")
    for cliente in clientes:
        if isinstance(cliente, PessoaFisica) and cliente.cpf == cpf:
            print("Erro: Já existe um cliente com esse CPF.")
            return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço: ")

    novo_cliente = PessoaFisica(nome, cpf, data_nascimento, endereco)
    clientes.append(novo_cliente)
    print("Cliente criado com sucesso!")

# Função para criar uma nova conta
def criar_conta(clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = next((c for c in clientes if isinstance(c, PessoaFisica) and c.cpf == cpf), None)

    if cliente is None:
        print("Erro: Cliente não encontrado.")
        return

    numero_conta = len(contas) + 1
    nova_conta = ContaCorrente(numero_conta, cliente)
    cliente.adicionar_conta(nova_conta)
    contas.append(nova_conta)
    print(f"Conta {numero_conta} criada com sucesso!")

# Função principal para o menu
def main():
    clientes = []
    contas = []

    while True:
        opcao = input("""
        [nu] Criar novo cliente
        [nc] Criar nova conta
        [d] Depositar
        [s] Sacar
        [e] Exibir extrato
        [q] Sair
        => """)

        if opcao == "nu":
            criar_usuario(clientes)

        elif opcao == "nc":
            criar_conta(clientes, contas)

        elif opcao == "d":
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((c for c in contas if c.numero == numero_conta), None)

            if conta:
                valor = float(input("Informe o valor do depósito: "))
                transacao = Deposito(valor)
                conta.cliente.realizar_transacao(conta, transacao)
            else:
                print("Conta não encontrada.")

        elif opcao == "s":
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((c for c in contas if c.numero == numero_conta), None)

            if conta:
                valor = float(input("Informe o valor do saque: "))
                transacao = Saque(valor)
                conta.cliente.realizar_transacao(conta, transacao)
            else:
                print("Conta não encontrada.")

        elif opcao == "e":
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((c for c in contas if c.numero == numero_conta), None)

            if conta:
                print("\n================ EXTRATO ================")
                for transacao in conta.historico.transacoes:
                    print(f"{transacao['tipo']}: R$ {transacao['valor']:.2f} em {transacao['data_hora']}")
                print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
                print("==========================================")
            else:
                print("Conta não encontrada.")

        elif opcao == "q":
            break

        else:
            print("Operação inválida, tente novamente.")

if __name__ == "__main__":
    main()
