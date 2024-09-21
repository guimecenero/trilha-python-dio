# Função para sacar dinheiro (keyword-only arguments)
def sacar(*, numero_conta, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if numero_conta not in saldo:
        print("Conta inválida!")
        return saldo, extrato, numero_saques

    if valor > saldo[numero_conta]:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif valor > limite[numero_conta]:
        print("Operação falhou! O valor do saque excede o limite.")
    elif numero_saques[numero_conta] >= limite_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo[numero_conta] -= valor
        extrato[numero_conta] += f"Saque: R$ {valor:.2f}\n"
        numero_saques[numero_conta] += 1
        print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato, numero_saques

# Função para depositar dinheiro (positional-only arguments)
def depositar(saldo, valor, extrato, numero_conta, /):
    if numero_conta not in saldo:
        print("Conta inválida!")
        return saldo, extrato

    if valor > 0:
        saldo[numero_conta] += valor
        extrato[numero_conta] += f"Depósito: R$ {valor:.2f}\n"
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato

# Função para exibir o extrato (positional and keyword-only arguments)
def exibir_extrato(numero_conta, saldo, /, *, extrato):
    if numero_conta not in saldo:
        print("Conta inválida!")
        return

    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato[numero_conta] else extrato[numero_conta])
    print(f"\nSaldo: R$ {saldo[numero_conta]:.2f}")
    print("==========================================")

# Função para criar um novo usuário
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario_existente = [usuario for usuario in usuarios if usuario["cpf"] == cpf]

    if usuario_existente:
        print("Erro: Já existe um usuário com esse CPF.")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("Usuário criado com sucesso!")

# Função para criar uma nova conta
def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("Informe o CPF do usuário: ")
    usuario = [usuario for usuario in usuarios if usuario["cpf"] == cpf]

    if not usuario:
        print("Erro: Usuário não encontrado.")
        return numero_conta

    contas.append({"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario[0]})
    print(f"Conta {numero_conta} criada com sucesso!")
    return numero_conta + 1

def main():
    usuarios = []
    contas = []
    saldo = {}
    extrato = {}
    limite = {}
    numero_saques = {}
    LIMITE_SAQUES = 3
    LIMITE_PADRAO = 500
    AGENCIA = "0001"
    numero_conta = 1

    while True:
        opcao = input("""
        [nu] Criar novo usuário
        [nc] Criar nova conta
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [q] Sair
        => """)

        if opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = criar_conta(AGENCIA, numero_conta, usuarios, contas)
            # Inicializando saldo e limites para a nova conta
            saldo[numero_conta - 1] = 0
            extrato[numero_conta - 1] = ""
            limite[numero_conta - 1] = LIMITE_PADRAO
            numero_saques[numero_conta - 1] = 0

        elif opcao == "d":
            conta = int(input("Informe o número da conta: "))
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato, conta)

        elif opcao == "s":
            conta = int(input("Informe o número da conta: "))
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                numero_conta=conta, saldo=saldo, valor=valor, extrato=extrato,
                limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES
            )

        elif opcao == "e":
            conta = int(input("Informe o número da conta: "))
            exibir_extrato(conta, saldo, extrato=extrato)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, tente novamente.")

if __name__ == "__main__":
    main()
