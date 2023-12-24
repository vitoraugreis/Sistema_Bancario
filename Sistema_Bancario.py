# Função Criar Usuário (NOVA):
    # Deve armazenar os usuários em uma lista.
    # Usuário: nome, data de nascimento, cpf, endereço
        # endereço: logadouro, número - bairro - cidade/sigla do estado
# -------------------------------------------------------------------------------------
# Função Criar Conta (NOVA):
    # Deve armazenar as contas em uma lista.
    # Conta: Agência, número, usuário.
        # Agência fixa: 0001 e número sequencial -> Começa do 1.
# -------------------------------------------------------------------------------------

import os

MAX_SAQUE_DIARIO = 3
MAX_VALOR_SAQUE = 500
NUM_AGENCIA = "0001"
MENU = """
-------- MENU --------
(1) - Deposito
(2) - Saque
(3) - Extrato
(0) - Sair
----------------------
Insira a operação desejada : """

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

saldo = 500
extrato = ""
saques_diarios = 0

os.system("cls")

while True:
    operacao = int(input(MENU))
    os.system("cls")

    if operacao == 1:
        valor = float(input("Insira o quanto deseja depositar: "))
        saldo, extrato = deposito(saldo, valor, extrato)

    elif operacao == 2:
        valor = float(input("Insira o quanto deseja sacar: "))
        saldo, extrato, saques_diarios = saque(saldo=saldo, valor=valor, extrato=extrato, max_valor_saque=MAX_VALOR_SAQUE, max_saque_diario=MAX_SAQUE_DIARIO, numero_saques=saques_diarios)

    elif operacao == 3:
        historico(saldo, extrato=extrato)

    elif operacao == 0:
        break

    else:
        print("Operação inválida.")