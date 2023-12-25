import os

def menu(primeiro_menu):
    if not primeiro_menu: print()

    menu = " MENU "
    print(menu.center(30, '-'))
    print("(1) - Cadastrar usuário")
    print("(2) - Listar usuários")
    print("(3) - Cadastrar conta")
    print("(4) - Listar contas")
    print("(5) - Deposito")
    print("(6) - Saque")
    print("(7) - Extrato")
    print("(0) - Sair")
    print('-'*30)
    print("Insira a operação desejada :", end = " ")

    return int(input())

def cadastrar_usuario(*, usuarios: list):
    cpf = input("Informe o cpf do usuário: ")

    verificacao_cpf = validar_cpf(cpf)
    if verificacao_cpf:
        verificacao_usuario = not procurar_usuario(usuarios, cpf, False)
        if verificacao_usuario:
            nome = input("Informe o nome do usuário: ")
            data_nascimento = input("Informe a data de nascimento do usuário (DD/MM/AAAA): ")
            endereco = input("Informe o endereço do usuário (logadouto, número - bairro - cidade/sigla do estado): ")
            usuarios.append({"cpf" : cpf, "nome" : nome, "data_nascimento" : data_nascimento, "endereco": endereco})
        else:
            print("ERRO: cpf já cadastrado.")

def validar_cpf(cpf, /):
    if not cpf.isnumeric():
        print("ERRO: cpf deve conter apenas números.")
        return False
    if len(cpf) != 11:
        print("ERRO: cpf informado é inválido.\nO cpf deve conter 11 números.")
        return False
    
    return True

def procurar_usuario(usuarios: list, cpf, retornar_usuario, /):
    for usuario in usuarios:
        if cpf in usuario.values():
            if retornar_usuario == True: return usuario
            else: return True
    return False

def listar_usuarios(*, usuarios: list):
    titulo = " USUÁRIOS "
    print(titulo.center(60, '='))
    if not usuarios: print("Nenhum usuário foi cadastrado.", '='*60, sep = '\n')
    else:
        for usuario in usuarios:
            print(f"Nome: {usuario['nome']}")
            print(f"CPF: {usuario['cpf']}")
            print(f"Data de nascimento: {usuario['data_nascimento']}")
            print(f"Endereço: {usuario['endereco']}")
            print('='*60)

def cadastrar_conta(agencia, numero_conta, /, *, usuarios: list, contas: list):
    cpf = input("Insira o cpf do proprietário: ")

    if cpf == "adm": 
        listar_contas(contas=contas)
        return False
    
    verificacao_cpf = validar_cpf(cpf)
    if verificacao_cpf: usuario = procurar_usuario(usuarios, cpf, True)
    else: return False
    if usuario:
        contas.append({"agencia":agencia, "numero":numero_conta, "dono":usuario})
        print("Conta criada com sucesso.")
        return True
    else:
        print("ERRO: cpf não cadastrado.")
        return False

def listar_contas(*, contas: list):
    titulo = " CONTAS "
    print(titulo.center(60, '='))
    if not contas: print("Não há contas registradas", '='*60, sep='\n')
    else:
        for conta in contas:
            print(f"Agência: {conta['agencia']}")
            print(f"Número da conta: {conta['numero']}")
            print(f"Dono: {conta['dono'].get('nome')}")
            print('='*60)

def saque(*, saldo, valor, extrato, max_valor_saque, max_saque_diario, numero_saques):
    if numero_saques == max_saque_diario:
        print("Operacao invalida. Limite de saques diarios atingido.")
    elif valor > max_valor_saque:
        print("Valor invalido. O limite de valor de saque eh de R$ 500.00")
    elif valor <= 0:
        print("Valor invalido. O valor de saque deve ser maior que zero.")
    elif valor > saldo:
        print("Valor invalido. O valor inserido eh maior que o saldo da conta.")
    else:
        saldo -= valor
        numero_saques += 1
        extrato += f"- Saque: R$ {valor : .2f}\n"
        print("Saque feito com sucesso!")

    return saldo, extrato, numero_saques

def deposito(saldo, valor, extrato, /):
    if valor <= 0:
        print("Valor invalido. O valor inserido deve ser maior que 0.")
    else:
        saldo += valor
        extrato += f"+ Deposito: R$ {valor : .2f}\n"
        print("Depósito feito com sucesso!")

    return saldo, extrato

def historico(saldo, /, *,  extrato):
    print("=============== EXTRATO ===============")
    print("A conta não possui extrato\n" if not extrato else extrato)
    print(f"Saldo: R$ {saldo : .2f}")
    print("=======================================")

def main():
    MAX_SAQUE_DIARIO = 3
    MAX_VALOR_SAQUE = 500
    NUM_AGENCIA = "0001"

    primeiro_menu = True
    saldo = 500
    extrato = ""
    saques_diarios = 0
    usuarios = list()
    contas = list()
    numero_conta = 1
    
    os.system("cls")
    
    while True:
        operacao = menu(primeiro_menu)
        primeiro_menu = False
        os.system("cls")
    
        if operacao == 1:
            cadastrar_usuario(usuarios=usuarios)
        
        elif operacao == 2:
            listar_usuarios(usuarios=usuarios)

        elif operacao == 3:
            cadastro = cadastrar_conta(NUM_AGENCIA, 
                                       numero_conta, 
                                       usuarios=usuarios, 
                                       contas=contas)
            if cadastro: numero_conta += 1
        
        elif operacao == 4:
            listar_contas(contas=contas)

        elif operacao == 5:
            valor = float(input("Insira o quanto deseja depositar: "))
            saldo, extrato = deposito(saldo, valor, extrato)
    
        elif operacao == 6:
            valor = float(input("Insira o quanto deseja sacar: "))
            saldo, extrato, saques_diarios = saque(saldo=saldo, 
                                                   valor=valor, 
                                                   extrato=extrato, 
                                                   max_valor_saque=MAX_VALOR_SAQUE, 
                                                   max_saque_diario=MAX_SAQUE_DIARIO, 
                                                   numero_saques=saques_diarios)
    
        elif operacao == 7:
            historico(saldo, extrato=extrato)
    
        elif operacao == 0:
            break
    
        else:
            print("Operação inválida.")

main()
