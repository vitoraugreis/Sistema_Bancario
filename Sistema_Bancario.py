import os
from abc import ABC, abstractmethod, abstractproperty

class SistemaGeral:
    def __init__(self):
        self._pessoas_fisicas = SistemaPessoasFisicas()

    @property
    def pessoas_fisicas(self):
        return self._pessoas_fisicas
    
    def busca_geral(self, chave):
        for sistema in self.__dict__.values():
            cliente = sistema.buscar(chave)
            if cliente: return cliente
        
        return False

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
            print("ERRO: CPF já existente no sistema.")
            return False
        
        nome = input("Digite o nome: ")
        data_nascimento = input("Digite a data de nascimento: ") # VERIFICAR DEPOIS
        endereco = input("Digite o endereço: ")
        self._clientes.append(PessoaFisica(nome, cpf, data_nascimento, endereco))
        print("Cliente cadastrado com sucesso.")
        return True

    def validar_cpf(self, cpf):
        if not cpf.isnumeric():
            print("ERRO: cpf deve conter apenas números.")
            return False
        if len(cpf) != 11:
            print("ERRO: cpf informado é inválido.\nO cpf deve conter 11 números.")
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
        return self.contas
    
    def adicionar_conta(self, conta): # Veridicação da condição da conta feita em outro lugar.
        self._contas.append(conta)
    
    def realizar_transacao(conta, transacao):
        pass
        
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
    def __init__(self, numero, agencia, cliente, historico):
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
    def nova_conta(cls, cliente, numero):
        pass

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().nova_conta(cliente, numero)
        self._limite = limite
        self._limite_saques = limite_saques
    
    @property
    def limite(self):
        return self._limite
    
    @property
    def limite_saques(self):
        return self._limite_saques

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

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

    def registrar(self, conta): # IMPLEMENTAR
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta): # IMPLEMENTAR
        pass

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

def testes():
    sistema = SistemaGeral()

# main()
testes()