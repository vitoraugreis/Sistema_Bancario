# Função Criar Conta (NOVA):
    # Deve armazenar as contas em uma lista.
    # Conta: Agência, número, usuário.
        # Agência fixa: 0001 e número sequencial -> Começa do 1.
# -------------------------------------------------------------------------------------

import os
def menu():
    menu = """
-------- MENU --------
(1) - Cadastrar usuário
(2) - Cadastrar conta
(3) - Deposito
(4) - Saque
(5) - Extrato
(0) - Sair
----------------------
Insira a operação desejada : """

    return int(input(menu))

def cadastrar_usuario(*, usuarios: list):
    cpf = input("Informe o cpf do usuário: ")

    if cpf == "adm":
        listar_usuarios(usuarios=usuarios)
        return

    verificacao_cpf = validar_cpf(cpf)
    if verificacao_cpf:
        verificacao_usuario = not procurar_usuario(usuarios, cpf)
        if verificacao_usuario:
            nome = input("Informe o nome do usuário: ")
            data_nascimento = input("Informe a data de nascimento do usuário (DD/MM/AAAA): ")
            endereco = input("Informe o endereço do usuário (logadouto, número - bairro - cidade/sigla do estado): ")
            usuarios.append({"CPF" : cpf, "Nome" : nome, "Data de nascimento" : data_nascimento, "Endereço": endereco})
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

def procurar_usuario(usuarios: list, cpf, /):
    for usuario in usuarios:
        if cpf in usuario.values():
            return True

    return False

def listar_usuarios(*, usuarios: list):
    for usuario in usuarios:
        print(usuario)

def cadastrar_conta(agencia, numero_conta, /, *, usuarios: list, contas: list):
    cpf = input("Insira o cpf do proprietário: ")

    if cpf == "adm": 
        listar_contas(contas=contas)
        return False
    
    verificacao_cpf = validar_cpf(cpf)
    if verificacao_cpf:
        verificacao_usuario = procurar_usuario(usuarios, cpf)
        if verificacao_usuario:
            contas.append({"Agencia":agencia, "Número":numero_conta, "Proprietário":cpf})
            print("Conta criada com sucesso.")
            return True
        else:
            print("ERRO: cpf não cadastrado.")
            return False
    else:
        return False

def listar_contas(*, contas: list):
    for conta in contas:
        print(conta)

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

    saldo = 500
    extrato = ""
    saques_diarios = 0
    usuarios = list()
    contas = list()
    numero_conta = 1
    
    os.system("cls")
    
    while True:
        operacao = menu()
        os.system("cls")
    
        if operacao == 1:
            cadastrar_usuario(usuarios=usuarios)
        
        elif operacao == 2:
            cadastro = cadastrar_conta(NUM_AGENCIA, numero_conta, usuarios=usuarios, contas=contas)
            if cadastro: numero_conta += 1
        
        elif operacao == 3:
            valor = float(input("Insira o quanto deseja depositar: "))
            saldo, extrato = deposito(saldo, valor, extrato)
    
        elif operacao == 4:
            valor = float(input("Insira o quanto deseja sacar: "))
            saldo, extrato, saques_diarios = saque(saldo=saldo, valor=valor, extrato=extrato, max_valor_saque=MAX_VALOR_SAQUE, max_saque_diario=MAX_SAQUE_DIARIO, numero_saques=saques_diarios)
    
        elif operacao == 5:
            historico(saldo, extrato=extrato)
    
        elif operacao == 0:
            break
    
        else:
            print("Operação inválida.")

main()
