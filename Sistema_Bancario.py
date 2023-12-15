import os

MAX_SAQUE_DIARIO = 3
MAX_VALOR_SAQUE = 500
MENU = """
-------- MENU --------
(1) - Deposito
(2) - Saque
(3) - Extrato
(0) - Sair
----------------------
Insira a operação desejada : """

saldo = 500
extrato = ""
saques_diarios = 0

os.system("cls")

while True:
    operacao = int(input(MENU))
    os.system("cls")
    if operacao == 1:
        deposito = float(input("Insira o quanto deseja depositar: "))
        if deposito <= 0:
            print("Valor invalido. O valor inserido deve ser maior que 0.")
        else:
            saldo += deposito
            extrato += f"+ Deposito: R$ {deposito : .2f}\n"

    elif operacao == 2:
        if saques_diarios == MAX_SAQUE_DIARIO:
            print("Operacao invalida. Limite de saques diarios atingido.")
        else:
            saque = float(input("Insira o quanto deseja sacar: "))
            if saque > MAX_VALOR_SAQUE:
                print("Valor invalido. O limite de valor de saque eh de R$ 500.00")
            elif saque <= 0:
                print("Valor invalido. O valor de saque deve ser maior que zero.")
            elif saque > saldo:
                print("Valor invalido. O valor inserido eh maior que o saldo da conta.")
            else:
                saldo -= saque
                saques_diarios += 1
                extrato += f"- Saque: R$ {saque : .2f}\n"

    elif operacao == 3:
        print("=============== EXTRATO ===============")
        print("A conta não possui extrato\n" if not extrato else extrato)
        print(f"Saldo: R$ {saldo : .2f}")
        print("=======================================")

    elif operacao == 0:
        break

    else:
        print("Operação inválida.")