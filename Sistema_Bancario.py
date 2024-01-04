import os, colorama
from abc import ABC, abstractmethod, abstractproperty
from colorama import Fore

colorama.init(autoreset=True)
VERMELHO = Fore.LIGHTRED_EX
VERDE = Fore.GREEN
AMARELO = Fore.YELLOW
RESET = Fore.RESET

class SistemaGeral:
    def __init__(self):
        self._pessoas_fisicas = SistemaPessoasFisicas()

    @property
    def pessoas_fisicas(self):
        return self._pessoas_fisicas
    
    def busca_geral_cliente(self, chave):
        for sistema in self.__dict__.values():
            cliente = sistema.buscar(chave)
            if cliente: return cliente
        
        return False
    
    def busca_geral_conta(self, numero):
        for sistema in self.__dict__.values():
            for cliente in sistema.clientes:
                for conta in cliente.contas:
                    if conta.numero == numero: return conta # Talvez não seja muito bom por nivel de complexidade.

    def listagem_geral_clientes(self):
        for sistema in self.__dict__.values():
            sistema.listar()
        
        return False
    
    def listagem_geral_contas(self):
        tem_conta = False
        titulo = " TODAS AS CONTAS "
        print(titulo.center(60, '='))
        for sistema in self.__dict__.values():
            for cliente in sistema.clientes:
                for conta in cliente.contas:
                    print(conta, '='*60, sep='\n')
                    tem_conta = True
        
        if not tem_conta: print("Não há contas registradas.", '='*60, sep='\n')

class SistemaPessoasFisicas:
    def __init__(self):
        self._clientes = []
    
    @property
    def clientes(self):
        return self._clientes
    
    def cadastrar(self):
        cpf = input("Digite o cpf: ")
        if not self.validar_cpf(cpf): return False

        if self.buscar(cpf):
            print(VERMELHO + "ERRO: CPF já existente no sistema.")
            return False
        
        nome = input("Digite o nome: ")
        data_nascimento = input("Digite a data de nascimento: ") # VERIFICAR DEPOIS
        endereco = input("Digite o endereço: ")
        self._clientes.append(PessoaFisica(nome, cpf, data_nascimento, endereco))
        print(VERDE + "Cliente cadastrado com sucesso.")
        return True

    def validar_cpf(self, cpf):
        if not cpf.isnumeric():
            print(VERMELHO + "ERRO: cpf deve conter apenas números.")
            return False
        if len(cpf) != 11:
            print(VERMELHO + "ERRO: cpf informado é inválido.\nO cpf deve conter 11 números.")
            return False
        
        return True

    def buscar(self, cpf):
        for cliente in self._clientes:
            if cliente.cpf == cpf: return cliente

        return False
    
    def listar(self):
        titulo = " PESSOAS FÍSICAS "
        print(titulo.center(60, '='))
        if not self._clientes: print("Nenhuma pessoa física foi cadastrada.", '='*60, sep='\n')
        else:
            for cliente in self._clientes:  print(cliente, '='*60, sep='\n')

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    @property
    def endereco(self):
        return self._endereco
    
    @property
    def contas(self):
        return self._contas
    
    def adicionar_conta(self, conta): # Veridicação da condição da conta feita em outro lugar.
        self._contas.append(conta)
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def listar_contas(self):
        titulo = " CONTAS "
        print(titulo.center(60, '='))
        if not self._contas: print("Não há contas registradas.", '='*60, sep='\n')
        else:
            for conta in self._contas: print(conta, '='*60, sep='\n')
        
class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento

    @property
    def nome(self):
        return self._nome
    
    @property
    def cpf(self):
        return self._cpf
    
    @property
    def data_nascimento(self):
        return self._data_nascimento
    
    def __str__(self):
        return f"Nome: {self._nome}\nCpf: {self._cpf}\nData de nascimento: {self._data_nascimento}\nEndereço: {self._endereco}\nNúmero de contas: {len(self._contas)}"

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)

    def sacar(self, valor):
        if valor > self._saldo:
            print("ERRO: O valor informado é maior que o saldo da conta.")
            return False
        
        if valor <= 0:
            print("ERRO: O valor informado é menor ou igual a zero.")
            return False
        
        self._saldo -= valor
        print("Saque realizado com sucesso.")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("ERRO: O valor do depósito deve ser maior que zero.")
            return False
        
        self._saldo += valor
        print("Depósito realizado com sucesso.")
        return True
    
    def __str__(self):
        return f"Proprietário: {self._cliente.nome}\nNúmero: {self._numero}\tAgência: {self._agencia}\nSaldo: {self._saldo : .2f}\nNúmero de Operações: {len(self._historico.transacoes)}"

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite_valor_saque = limite
        self._numero_saque = 0
        self._limite_saques = limite_saques
    
    @property
    def limite_valor_saque(self):
        return self._limite_valor_saque
    
    @property
    def limite_saques(self):
        return self._limite_saques
    
    @property
    def numero_saque(self):
        return self._numero_saque
    
    def sacar(self, valor):
        if self._numero_saque == self._limite_saques:
            print("ERRO: Limite de saque diário atingido.")
            return False
        
        if valor > self._limite_valor_saque:
            print("ERRO: Valor informado supera o limite de dinheiro que pode ser sacado.")
            return False

        if valor > self._saldo:
            print("ERRO: O valor informado é maior que o saldo da conta.")
            return False
        
        if valor <= 0:
            print("ERRO: O valor informado é menor ou igual a zero.")
            return False
        
        self._saldo -= valor
        self._numero_saque += 1
        print("Saque realizado com sucesso.")
        return True

    def __str__(self):
        return f"Tipo: {AMARELO+'Corrente'+RESET}\nProprietário: {self._cliente.nome}\nNúmero: {self._numero}\tAgência: {self._agencia}\nSaldo: {self._saldo : .2f}\nNúmero de Operações: {len(self._historico.transacoes)}"

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)

    def listar(self):
        titulo = " TRANSAÇÕES "
        print(titulo.center(60, '='))
        for transacao in self._transacoes: print(transacao)

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        operacao = conta.sacar(self._valor)
        if operacao: 
            conta.historico.adicionar_transacao(self)
            return True
        
        return False

    def __str__(self):
        return f"- Saque: R${self._valor : .2f}"

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        operacao = conta.depositar(self._valor)
        if operacao:
            conta.historico.adicionar_transacao(self)
            return True
    
        return False
    
    def __str__(self):
        return f"+ Depósito: R${self._valor : .2f}"

def menu(primeiro_menu):
    if not primeiro_menu: print()

    menu = " MENU "
    print(menu.center(30, '-'))
    print("(1) - Cadastrar cliente")
    print("(2) - Listar clientes")
    print("(3) - Cadastrar conta")
    print("(4) - Listar contas")
    print("(5) - Depositar")
    print("(6) - Sacar")
    print("(7) - Extrato")
    print("(0) - Sair")
    print('-'*30)
    print("Insira a operação desejada :", end = " ")

    return int(input())

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

def cadastrar_cliente(sistema):
    titulo_menu = " TIPOS DE CLIENTE "
    print(titulo_menu.center(30, '-'))
    print("(1) - Pessoa Física")
    print("(0) - Cancelar")
    print('-'*30)
    opcao = int(input("Insira o tipo de cliente desejado: "))

    if opcao == 1: sistema.pessoas_fisicas.cadastrar()
    elif opcao != 0: print(VERMELHO + "Operação inválida.")

    return

def criar_conta(sistema):
    titulo_menu = " TIPOS DE CONTA "
    print(titulo_menu.center(30, '-'))
    print("(1) - Conta Corrente")
    print("(0) - Cancelar")
    print('-'*30)
    opcao = int(input("Insira o tipo de cliente desejado: "))

    if opcao == 1:
        cpf = input("Digite o CPF: ")
        cliente = sistema.busca_geral_cliente(cpf)
        if not cliente:
            print(VERMELHO + "ERRO: Cpf inválido.")
            return False
        
        numero = input("Digite o número da nova conta: ")
        busca_conta = sistema.busca_geral_conta(numero)
        if busca_conta:
            print(VERMELHO + "ERRO: Número de conta já existente.")
            return False
        
        conta = ContaCorrente.nova_conta(numero, cliente)
        cliente.adicionar_conta(conta)
        print(VERDE + "Conta criada com sucesso.")
        return True
    
    elif opcao != 0: print(VERMELHO + "Operação inválida.")

    return

def listar_contas(sistema):
    titulo_menu_lista = " OPÇÕES "
    print(titulo_menu_lista.center(30, '-'))
    print("(1) - Listar todas as contas")
    print("(2) - Listar todas as contas de um cliente")
    print("(0) - Cancelar")
    print('-'*30)
    opcao_lista = int(input("Insira o tipo de cliente desejado: "))
    os.system("cls")

    if opcao_lista == 1: sistema.listagem_geral_contas()
    elif opcao_lista == 2:
        titulo_menu_cliente = " TIPOS DE CLIENTE "
        print(titulo_menu_cliente.center(30, '-'))
        print("(1) - Pessoa Física")
        print("(0) - Cancelar")
        print('-'*30)
        opcao_cliente = int(input("Insira o tipo de cliente desejado: "))
        os.system("cls")

        if opcao_cliente == 1:
            cpf = input("Insira o cpf do cliente desejado: ")
            cliente = sistema.busca_geral_cliente(cpf)
            if cliente: 
                print()
                cliente.listar_contas()
            else: print(VERMELHO + "ERRO: Cliente inexistente.")
        elif opcao_cliente != 0: print(VERMELHO + "Operação inválida.")


    elif opcao_lista != 0: print(VERMELHO + "Operação inválida.")

    return

def main():
    sistema = SistemaGeral()
    primeiro_menu = True
    
    os.system("cls")
    
    while True:
        operacao = menu(primeiro_menu)
        primeiro_menu = False
        os.system("cls")
    
        if operacao == 1:
            cadastrar_cliente(sistema)
        
        elif operacao == 2:
            sistema.listagem_geral_clientes()

        elif operacao == 3:
            criar_conta(sistema)
        
        elif operacao == 4:
            listar_contas(sistema)

        elif operacao == 5:
            pass
    
        elif operacao == 6:
            pass
    
        elif operacao == 7:
            pass
    
        elif operacao == 0:
            break
    
        else:
            print(VERMELHO + "Operação inválida.")


def testes():
    sistema = SistemaGeral()
    sistema.pessoas_fisicas.cadastrar()
    criar_conta(sistema)

    cpf = input()
    numero = input()
    conta = sistema.busca_geral_conta(numero)
    cliente = sistema.busca_geral_cliente(cpf)

    valor = float(input())
    transacao = Deposito(valor)
    cliente.realizar_transacao(conta, transacao)

    valor = float(input())
    transacao = Saque(valor)
    cliente.realizar_transacao(conta, transacao)

    cliente.listar_contas()
    print('-'*100)
    conta.historico.listar()


main()
#testes()