from abc import ABC, abstractmethod
from datetime import datetime

###################################################################################################
class Pessoa:

    def __init__(self, id_pessoa, nome, data_nascimento):
        self._id_pessoa = id_pessoa
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def id_pessoa(self):
        return self._id_pessoa or None
    
    @id_pessoa.setter
    def id_pessoa(self, id_pessoa):
        self._id_pessoa = id_pessoa
        return None
    @property
    def nome(self):
        return self._nome or None
    
    @nome.setter
    def nome(self, nome):
        self._nome = nome
        return None
    
    @nome.deleter
    def nome(self):
        # nomes "apagados" serão identificados com a string '(apagado)' antecedendo o nome
        self._nome = '(apagado) ' + self._nome
        return None    

    @property
    def data_nascimento(self):
        return self._data_nascimento or None
    
    @data_nascimento.setter
    def data_nascimento(self, data_nascimento):
        self._data_nascimento = data_nascimento
        return None
    
    @data_nascimento.deleter
    def data_nascimento(self):
        # nomes "apagados" serão identificados com a string '(apagado)' antecedendo o nome
        return None   

###################################################################################################
class PessoaFisica(Pessoa):
    def __init__(self, id, nome, data, cpf):
        super().__init__(id, nome, data)
        self._cpf = cpf

    @property
    def cpf(self):
        return self._cpf or None
    
    @cpf.setter
    def cpf(self, nro_cpf):
        self._cpf = nro_cpf
        return None
    
    @cpf.deleter
    def cpf(self):
        # cpf's "apagados" serão identificados com a string '(apagado)' antecedendo o número
        self._cpf = '(apagado) ' + self._cpf
        return None

###################################################################################################
class PessoaJuridica(Pessoa):
    def __init__(self, id, nome, data, cnpj):
        super().__init__(id, nome, data)
        self._cnpj = cnpj

    @property
    def cnpj(self):
        return self._cnpj or None
    
    @cnpj.setter
    def cnpj(self, nro_cnpj):
        self._cnpj = nro_cnpj
        return None
    
    @cnpj.deleter
    def cnpj(self):
        # cpf's "apagados" serão identificados com a string '(apagado)' antecedendo o número
        self._cnpj = '(apagado) ' + self._cnpj
        return None
    
###################################################################################################
################################### TESTE #########################################################
###################################################################################################
print('####### teste criação classe Cliente #######')    
pessoas = []
pessoas.append(PessoaFisica(1, 'zezao manezao', '01/01/2001', 'cpf001'))
pessoas.append(PessoaJuridica(11, 'empresa zezao manezao', '11/11/2011','cnpj0000011'))
print('\n'.join(f"ID cliente: {pessoas[qual].id_pessoa}, Nome: {pessoas[qual].nome}, CPF: {pessoas[qual].cpf}, Data nascimento: {pessoas[qual].data_nascimento}" if pessoas[qual].__class__.__name__ == 'PessoaFisica' else f"ID cliente: {pessoas[qual].id_pessoa}, Nome: {pessoas[qual].nome}, CNPJ: {pessoas[qual].cnpj}, Data nascimento: {pessoas[qual].data_nascimento}" for qual in range(0,len(pessoas))))
###################################################################################################
###################################################################################################
class Historico():
    def __init__(self):
        self.historico = []

    def adicionar_transacao(self, operacao, valor_operacao):
        self.historico.append({datetime.now().strftime('%d/%m/%Y %H:%M:%S'):{operacao:valor_operacao}})
        return True
    
###################################################################################################
class Conta:
    def __init__(self, **kwargs):
    #def __init__(self, agencia, nro_conta, saldo=0):
        self.agencia = kwargs['agencia']
        self.nro_conta = kwargs['nro_conta']
        if 'saldo' in kwargs:
            self._saldoconta = kwargs['saldo']
        else:
            self._saldoconta = 0
        self.historico = Historico()

    @property
    def saldo(self):
        return self._saldoconta
    
    @saldo.setter
    def saldo(self,valor):
        self._saldoconta = valor
    
    def sacar(self, valor):
        self.saldo = self.saldo - valor
        return True
    
    def depositar(self, valor):
        self.saldo = self.saldo + valor
        return True
    
###################################################################################################
class ContaCorrente(Conta):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.limite = kwargs['limite_por_saque']
        self.limite_saques = kwargs['limite_qtd_saques']

    @classmethod
    def nova_conta(cls, **kwargs):
        # uso do **kwargs como exercício
        return cls(agencia=kwargs['agencia'], nro_conta=kwargs['nro_conta'], limite_por_saque=kwargs['limite_por_saque'], limite_qtd_saques=kwargs['limite_qtd_saques'])        
    
    def sacar(self, valor_saque):
        if valor_saque < 0:
            return False
        ok_nok = False
        if valor_saque <= self.limite:
            if self.limite_saques > 0:
                if self.saldo >= valor_saque:
                    ok_nok = super().sacar(valor_saque)
                    self.limite_saques -= 1
        return ok_nok
    
    def depositar(self, valor_deposito):
        if valor_deposito < 0:
            return False
        ok_nok = False
        ok_nok = super().depositar(valor_deposito)
        return ok_nok
###################################################################################################
class Cliente():
    def __init__(self, pessoa, endereco):
        self.pessoa = pessoa
        self.contacorrente = []
        self.endereco = endereco

    def adicionar_conta(self, novaconta):
        self.contacorrente.append(novaconta)

    #def realizar_transacao(self, conta, transacao):
    #    transacao.registrar(conta)
       
###################################################################################################
################################### TESTE #########################################################
###################################################################################################
print()
print('------------ Teste criação de conta --------------')
pessoa1 = pessoas[0]
pessoa2 = pessoas[1]
conta1 = ContaCorrente.nova_conta(agencia=1,nro_conta=1,limite_qtd_saques=3, limite_por_saque=500)
conta2 = ContaCorrente.nova_conta(agencia=1,nro_conta=2,saldo=0, limite_qtd_saques=6, limite_por_saque=1000)
clientes = []
cliente1 = Cliente(pessoa1,endereco='rua aqui numero 0 - Lugar Nenhum - PR')
clientes.append(Cliente(pessoa1,endereco='rua aqui numero 0 - Lugar Nenhum - PR'))
clientes[0].adicionar_conta(conta1)
clientes[0].adicionar_conta(conta2)
cliente1.adicionar_conta(conta1)
cliente1.adicionar_conta(conta2)
cliente2 = Cliente(pessoa2,endereco='rua da empresa - Terra de Ninguém - PR')
clientes.append(Cliente(pessoa2,endereco='rua da empresa - Terra de Ninguém - PR'))
conta3 = ContaCorrente(limite_qtd_saques=10, limite_por_saque=2000,agencia=1,nro_conta=3,saldo=0)
cliente2.adicionar_conta(conta3)
clientes[1].adicionar_conta(conta3)
print(clientes)
print(len(clientes))
print(clientes[0].contacorrente[0].__dict__)
print(clientes[0].contacorrente[0].nro_conta)
print(len(clientes[0].contacorrente))

print('-------------------')
print(cliente1)
print(cliente1.__dict__)
print(cliente2)
print(cliente2.__dict__)
print()
print('-------------------')
print(cliente1.pessoa)
print(cliente1.pessoa.__dict__)
print(cliente1.pessoa.__class__)
print(cliente1.pessoa.__class__.__name__)
print(cliente1.pessoa.nome)
print()
print('-------------------')
print(cliente1.contacorrente)
print(cliente1.contacorrente[0])
print(cliente1.contacorrente[0].__class__)
print(cliente1.contacorrente[0].__class__.__name__)
for aux in range(0, len(cliente1.contacorrente)):
    print(cliente1.contacorrente[aux].__dict__)
###################################################################################################

class Registrar_Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

    @abstractmethod
    def saque(self, valor):
        pass

    @abstractmethod
    def deposito(self,valor):
        pass
###################################################################################################
class Transacao(Registrar_Transacao):
    def __init__(self,conta):
        self.conta = conta

    def registrar(self, tipo_transacao, valor):
        return self.conta.historico.adicionar_transacao(tipo_transacao, valor)
    
    def deposito(self,valor_deposito):
        return self.registrar("deposito", valor_deposito) if self.conta.depositar(valor_deposito) else False
        
    def saque(self,valor_saque):
        return self.registrar("saque", valor_saque) if self.conta.sacar(valor_saque) else False
    
    def extrato(self):
        movimentacoes = self.conta.historico.historico
        for aux in movimentacoes:
            for quando, transac in aux.items():
                for tipo, valor in transac.items():
                    print(f'{quando} -> {tipo} no valor de R$ {valor}')



###################################################################################################
################################### TESTE #########################################################
###################################################################################################
print()
print('----------- Teste movimentação conta -------------')
       
print(f"Saldo atual: {conta1.saldo}")
Transacao(conta1).deposito(1000)
print(f"Saldo atual: {conta1.saldo}")

Transacao(conta1).saque(50)
print(f"Saldo atual: {conta1.saldo}")
print(conta1.__dict__)

Transacao(conta1).saque(800) # não deve ser autorizada pois ultrapassou o limite máx de 500
print(f"Saldo atual: {conta1.saldo}")
print(conta1.__dict__)

Transacao(conta1).saque(10)
print(f"Saldo atual: {conta1.saldo}")
print(conta1.__dict__)

Transacao(conta1).saque(100)
print(f"Saldo atual: {conta1.saldo}")
print(conta1.__dict__)

Transacao(conta1).saque(5) # nao deve ser autorizado pois ultrapassou o limite máximo de 3 saques diários
print(f"Saldo atual: {conta1.saldo}")
print(conta1.__dict__)

print(f"Saldo atual: {conta1.saldo}")
Transacao(conta1).deposito(0.10)
print(f"Saldo atual: {conta1.saldo}")

print()
print(conta1.historico.__dict__)
Transacao(conta1).extrato()
###################################################################################################
def seleciona_cliente_cpf(lista_todos_clientes, cpf_desejado):
    if not(lista_todos_clientes and len(lista_todos_clientes) > 0):
        return False
    if (not cpf_desejado) or cpf_desejado == "":
        return False
    cliente_encontrado = [cliente for cliente in lista_todos_clientes if (cliente.pessoa.__class__.__name__ == 'PessoaFisica') and (cliente.pessoa.cpf == cpf_desejado)] 
    #cliente_encontrado = [cliente for cliente in lista_todos_clientes if ('_cpf' in cliente.pessoa.__dict__) and (cliente.pessoa.cpf == cpf_desejado)] 
    if len(cliente_encontrado) > 0:
        return cliente_encontrado[0] 
    else:
        return None

def seleciona_contacorrente_cliente(cliente_selecionado):
    if len(cliente_selecionado.contacorrente) < 2:
        return cliente_selecionado.contacorrente[0].nro_conta, cliente_selecionado.contacorrente[0] 
    print()
    print('Conta(s) corrente(s) deste cliente: ')
    print('\n'.join(str(cliente_selecionado.contacorrente[aux].nro_conta) for aux in range(0,len(cliente_selecionado.contacorrente))))
    print()
    qual_cc = int(input('Informe a conta corrente desejada: '))
    # cc_selecionada = None
    # for aux in range(0,len(cliente_selecionado.contacorrente)):
    #     if qual_cc == cliente_selecionado.contacorrente[aux].nro_conta:
    #         cc_selecionada = cliente_selecionado.contacorrente[aux]
    #         break
    if qual_cc == None:
        return None, None
    cc_selecionada = [ cliente_selecionado.contacorrente[aux] for aux in range(0,len(cliente_selecionado.contacorrente)) if cliente_selecionado.contacorrente[aux].nro_conta == qual_cc ] or None
    if cc_selecionada == None:
        qual_cc = None 
    return qual_cc, cc_selecionada[0] if cc_selecionada != None else None

###################################################################################################
################################### TESTE #########################################################
###################################################################################################   
print()
print('-------- teste localização cliente específico ----------')
print(clientes)
print(clientes[0])
print(clientes[0].__dict__)
print(clientes[0].pessoa)
print(clientes[0].pessoa.__dict__)
print(clientes[1].pessoa.__dict__)
# lista_cliente_encontrado = seleciona_cliente_cpf(clientes,'cpf001')
# if lista_cliente_encontrado != None:
#     cliente_encontrado = lista_cliente_encontrado[0]
#     print(cliente_encontrado)
#     print(cliente_encontrado.__dict__)
#     print(cliente_encontrado.contacorrente[0].__dict__)
#     print('\n'.join(str(cliente_encontrado.contacorrente[aux].nro_conta) for aux in range(0,len(cliente_encontrado.contacorrente))))
#print(seleciona_cliente_cpf(clientes,'cpf0000000'))
#print()
#print(seleciona_contacorrente_cliente(cliente_encontrado))

print()
print()
print('#####################################################################')
print('############ TESTE DE EXECUÇÃO - MODELO BANCÁRIO COM POO ############')
print('#####################################################################')
print()
opcao_menu = None
cpf_informado = None
cc_informada = None         # número de posição da conta na lista dentro do objeto tipo ContaCorrente
cliente_selecionado = None
cc_selecionada = None       # objeto tipo Conta
id_prox_cliente = 10
id_agencia = 1
id_prox_conta = 10

# Obs.: outras variáveis já inicializadas nos testes acima

menuinicial = f'''
Selecione a opção desejada:
[c]  Selecionar Cliente
[n]  Novo Cliente
[cc] Selecionar Conta-Corrente
[nc] Nova Conta-corrente
[sd] Consulta Saldo
[s]  Saque em conta-corrente
[d]  Depósito em conta-corrente
[e]  Extrato de conta-corrente
[q]  Sair

'''

while opcao_menu != 'q':
    print()
    print('-----------------------------------------------------------------------')
    print(f'Cliente selecionado atual: CPF {cpf_informado if cpf_informado != None else ""}')
    print(f'Conta-corrente selecionada atual: {cc_informada if cc_informada != None else ""}')
    print('-----------------------------------------------------------------------')
    print(menuinicial)
    opcao_menu = input('Seleciona a opção desejada: ')

    match opcao_menu:
        case 'c':
            cpf_informado = input('Informe o cpf do cliente: ')
            cliente_selecionado = seleciona_cliente_cpf(clientes,cpf_informado)
            if cliente_selecionado == None:
                print('Cliente não encontrado. Operação cancelada.')
                cpf_informado = None
                continue
            cc_informada, cc_selecionada = seleciona_contacorrente_cliente(cliente_selecionado)
        case 'n':
            print()
            print('----- Cadastro de novo Cliente -----')
            print()
            novo_nome = input('Nome: ')
            nova_data_nasc = input('Data de nascimento: ')
            novo_cpf = input('CPF: ')
            novo_endereço = input('Endereço: ')
            
            nova_pessoa = PessoaFisica(id_prox_cliente,novo_nome, nova_data_nasc, novo_cpf)
            novo_cliente = Cliente(nova_pessoa,endereco=novo_endereço)
            nova_conta = ContaCorrente(limite_qtd_saques=3, limite_por_saque=500,agencia=id_agencia,nro_conta=id_prox_conta,saldo=0)
            novo_cliente.adicionar_conta(nova_conta)
            
            clientes.append(novo_cliente)

            id_prox_cliente += 1
            id_prox_conta += 1
            cpf_informado = novo_cpf
            cliente_selecionado = novo_cliente  
            cc_selecionada = nova_conta
            cc_informada = id_prox_conta - 1         
            print()

        case 'cc':
            if cliente_selecionado == None:
                print('Necessário selecionar o cliente. Operação cancelda.')
                continue
            cc_informada, cc_selecionada = seleciona_contacorrente_cliente(cliente_selecionado)
            if cc_selecionada == None:
                print('Conta informada é inválida. Tente novamente.')

        case 'nc':
            if cliente_selecionado == None:
                print('Necessário selecionar o cliente. Operação cancelda.')
                continue
            nova_conta = ContaCorrente(limite_qtd_saques=3, limite_por_saque=500,agencia=id_agencia,nro_conta=id_prox_conta,saldo=0)
            cliente_selecionado.adicionar_conta(nova_conta)     
            print(f'Aberta nova conta-corrente para este cliente. Número da nova conta: {id_prox_conta}')   
            id_prox_conta += 1 
            
        case 'sd':
            if cliente_selecionado == None:
                print('Necessário selecionar o cliente. Operação cancelda.')
                continue
            if cc_informada == None:
                print('Necessário selecionar a conta-corrente. Operação cancelda.')
                continue    
            print(f'Saldo atual = R$ {cc_selecionada.saldo:.2f}')           
            continue

        case 's':
            if cliente_selecionado == None:
                print('Necessário selecionar o cliente. Operação cancelda.')
                continue
            if cc_informada == None:
                print('Necessário selecionar a conta-corrente. Operação cancelda.')
                continue  
            valor_saque = float(input('Valor desejado para saque : R$ '))
            print(f'Valor sacado: R$ {valor_saque:.2f}') if Transacao(cc_selecionada).saque(valor_saque) else print('Saque não realizado.')

        case 'd':
            if cliente_selecionado == None:
                print('Necessário selecionar o cliente. Operação cancelda.')
                continue
            if cc_informada == None:
                print('Necessário selecionar a conta-corrente. Operação cancelda.')
                continue  
            valor_deposito = float(input('Valor desejado para depósito : R$ '))
            print(f'Valor depositado: R$ {valor_deposito:.2f}') if Transacao(cc_selecionada).deposito(valor_deposito) else print('Depósito não realizado.')

        case 'e':
            if cliente_selecionado == None:
                print('Necessário selecionar o cliente. Operação cancelda.')
                continue
            if cc_informada == None:
                print('Necessário selecionar a conta-corrente. Operação cancelda.')
                continue    
            print()
            print('------ EXTRATO DE CONTA CORRENTE ------')
            Transacao(cc_selecionada).extrato()
            print()
            print(f'Saldo atual = R$ {cc_selecionada.saldo:.2f}')
            
        case 'q':
            exit