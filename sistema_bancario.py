
"""
Sistema Bancário com Menu Interativo
POO: Classe Abstrata, Herança e Polimorfismo
Execução: python sistema_bancario.py
"""

from abc import ABC, abstractmethod


# ============================================================
# 1. CLASSE ABSTRATA
# ============================================================
class ContaBancaria(ABC):
    def __init__(self, numero, titular, saldo_inicial):
        self._numero = numero
        self._titular = titular
        self._saldo = saldo_inicial
        self._extrato = []

    # Método concreto: depósito é igual para todas as contas
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            self._extrato.append(f"Depósito: +R$ {valor:.2f}")
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
        else:
            print("Valor de depósito inválido.")

    # Método abstrato: cada tipo de conta saca de um jeito
    @abstractmethod
    def sacar(self, valor):
        pass

    def exibir_extrato(self):
        print("\n========== EXTRATO ==========")
        print(f"Titular: {self._titular.nome} (CPF: {self._titular.cpf})")
        print(f"Conta nº: {self._numero}")
        print("-----------------------------")
        if not self._extrato:
            print("Nenhuma movimentação.")
        else:
            for mov in self._extrato:
                print(mov)
        print("-----------------------------")
        print(f"Saldo atual: R$ {self._saldo:.2f}")
        print("=============================\n")

    @property
    def numero(self):
        return self._numero

    @property
    def titular(self):
        return self._titular

    @property
    def saldo(self):
        return self._saldo


# ============================================================
# 2. CONTA CORRENTE (com limite de cheque especial)
# ============================================================
class ContaCorrente(ContaBancaria):
    def __init__(self, numero, titular, saldo_inicial, limite):
        super().__init__(numero, titular, saldo_inicial)
        self._limite_cheque_especial = limite

    def sacar(self, valor):
        saldo_disponivel = self._saldo + self._limite_cheque_especial
        if valor > 0 and valor <= saldo_disponivel:
            self._saldo -= valor
            self._extrato.append(f"Saque: -R$ {valor:.2f}")
            print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
        else:
            print("Saque negado. Saldo + limite insuficiente.")


# ============================================================
# 3. CONTA POUPANÇA (com rendimento)
# ============================================================
class ContaPoupanca(ContaBancaria):
    def __init__(self, numero, titular, saldo_inicial):
        super().__init__(numero, titular, saldo_inicial)

    def sacar(self, valor):
        if valor > 0 and valor <= self._saldo:
            self._saldo -= valor
            self._extrato.append(f"Saque: -R$ {valor:.2f}")
            print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
        else:
            print("Saque negado. Saldo insuficiente.")

    def aplicar_rendimento(self, taxa):
        rendimento = self._saldo * taxa
        self._saldo += rendimento
        self._extrato.append(f"Rendimento ({taxa*100:.2f}%): +R$ {rendimento:.2f}")
        print(f"Rendimento de {taxa*100:.2f}% aplicado! (+R$ {rendimento:.2f})")


# ============================================================
# 4. CLIENTE
# ============================================================
class Cliente:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf


# ============================================================
# 5. MENU INTERATIVO
# ============================================================
def buscar_conta(contas, numero):
    for c in contas:
        if c.numero == numero:
            return c
    return None


def menu():
    contas = []
    proximo_numero = 1

    # Contas de exemplo para demonstração
    cliente1 = Cliente("Ana Souza", "111.222.333-44")
    cliente2 = Cliente("Bruno Lima", "555.666.777-88")
    contas.append(ContaCorrente(proximo_numero, cliente1, 1000.0, 500.0))
    proximo_numero += 1
    contas.append(ContaPoupanca(proximo_numero, cliente2, 2000.0))
    proximo_numero += 1

    while True:
        print("\n========= BANCO LOVABLE =========")
        print("1 - Criar Conta Corrente")
        print("2 - Criar Conta Poupança")
        print("3 - Depositar")
        print("4 - Sacar")
        print("5 - Aplicar Rendimento (Poupança)")
        print("6 - Exibir Extrato")
        print("7 - Listar Contas")
        print("0 - Sair")
        print("=================================")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Nome do titular: ")
            cpf = input("CPF: ")
            saldo = float(input("Saldo inicial: R$ "))
            limite = float(input("Limite do cheque especial: R$ "))
            cliente = Cliente(nome, cpf)
            contas.append(ContaCorrente(proximo_numero, cliente, saldo, limite))
            print(f"Conta Corrente nº {proximo_numero} criada para {nome}.")
            proximo_numero += 1

        elif opcao == "2":
            nome = input("Nome do titular: ")
            cpf = input("CPF: ")
            saldo = float(input("Saldo inicial: R$ "))
            cliente = Cliente(nome, cpf)
            contas.append(ContaPoupanca(proximo_numero, cliente, saldo))
            print(f"Conta Poupança nº {proximo_numero} criada para {nome}.")
            proximo_numero += 1

        elif opcao == "3":
            numero = int(input("Número da conta: "))
            conta = buscar_conta(contas, numero)
            if conta:
                valor = float(input("Valor do depósito: R$ "))
                conta.depositar(valor)
            else:
                print("Conta não encontrada.")

        elif opcao == "4":
            numero = int(input("Número da conta: "))
            conta = buscar_conta(contas, numero)
            if conta:
                valor = float(input("Valor do saque: R$ "))
                conta.sacar(valor)  # Polimorfismo
            else:
                print("Conta não encontrada.")

        elif opcao == "5":
            numero = int(input("Número da conta poupança: "))
            conta = buscar_conta(contas, numero)
            if isinstance(conta, ContaPoupanca):
                taxa = float(input("Taxa de rendimento (ex: 0.05 para 5%): "))
                conta.aplicar_rendimento(taxa)
            else:
                print("Conta inválida ou não é poupança.")

        elif opcao == "6":
            numero = int(input("Número da conta: "))
            conta = buscar_conta(contas, numero)
            if conta:
                conta.exibir_extrato()
            else:
                print("Conta não encontrada.")

        elif opcao == "7":
            print("\n--- Contas Cadastradas ---")
            for c in contas:
                tipo = "Corrente" if isinstance(c, ContaCorrente) else "Poupança"
                print(f"Nº {c.numero} | {tipo} | {c.titular.nome} | Saldo: R$ {c.saldo:.2f}")

        elif opcao == "0":
            print("Encerrando o sistema. Até logo!")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
