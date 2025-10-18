"""
SISTEMA BANCÁRIO MODULAR
========================

Este é um sistema bancário simples desenvolvido em Python para fins educacionais.
O sistema permite criar usuários, contas bancárias e realizar operações básicas
como depósitos, saques e consulta de extrato.

COMO USAR:
----------
1. Execute o programa
2. Escolha uma opção do menu digitando o número correspondente
3. Siga as instruções na tela para cada operação

FUNCIONALIDADES:
----------------
- Criar usuários com CPF único
- Criar contas bancárias vinculadas a usuários
- Realizar depósitos (ilimitados)
- Realizar saques (até 3 por dia, limite de R$ 500 por saque)
- Consultar extrato com histórico de movimentações
- Listar todas as contas cadastradas

REGRAS DE NEGÓCIO:
------------------
- Cada usuário é identificado por um CPF único (11 dígitos)
- Cada conta possui uma agência fixa (0001) e número sequencial
- Limite de saque: R$ 500,00 por operação
- Limite de saques diários: 3 saques
- Não é possível sacar mais que o saldo disponível
"""

# ============================================================================
# FUNÇÕES DE OPERAÇÕES BANCÁRIAS
# ============================================================================

def depositar(saldo, valor, extrato, /):
    """
    Realiza um depósito na conta.
    
    Parâmetros posicionais (não podem ser passados por nome):
    - saldo: float - Saldo atual da conta
    - valor: float - Valor a ser depositado
    - extrato: str - Histórico de movimentações
    
    Retorna:
    - tuple: (novo_saldo, novo_extrato)
    
    Regras:
    - O valor deve ser positivo
    - Não há limite de valor ou quantidade de depósitos
    """
    if valor > 0:
        saldo += valor  # Adiciona o valor ao saldo
        extrato += f"Depósito: R$ {valor:.2f}\n"  # Registra no extrato
        print("\n✓ Depósito realizado com sucesso!")
    else:
        print("\n✗ Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """
    Realiza um saque da conta.
    
    Parâmetros nomeados (devem ser passados por nome):
    - saldo: float - Saldo atual da conta
    - valor: float - Valor a ser sacado
    - extrato: str - Histórico de movimentações
    - limite: float - Limite máximo por saque
    - numero_saques: int - Quantidade de saques já realizados hoje
    - limite_saques: int - Limite máximo de saques diários
    
    Retorna:
    - tuple: (novo_saldo, novo_extrato, novo_numero_saques)
    
    Regras:
    - O valor deve ser positivo
    - O valor não pode exceder o saldo disponível
    - O valor não pode exceder o limite por saque (R$ 500)
    - Não pode exceder o limite de saques diários (3 saques)
    """
    # Verifica as condições que impedem o saque
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    # Valida cada condição e exibe mensagem apropriada
    if excedeu_saldo:
        print("\n✗ Operação falhou! Saldo insuficiente.")
    elif excedeu_limite:
        print(f"\n✗ Operação falhou! O valor do saque excede o limite de R$ {limite:.2f}.")
    elif excedeu_saques:
        print(f"\n✗ Operação falhou! Número máximo de saques diários ({limite_saques}) excedido.")
    elif valor > 0:
        saldo -= valor  # Deduz o valor do saldo
        extrato += f"Saque:    R$ {valor:.2f}\n"  # Registra no extrato
        numero_saques += 1  # Incrementa o contador de saques
        print("\n✓ Saque realizado com sucesso!")
    else:
        print("\n✗ Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    """
    Exibe o extrato bancário com todas as movimentações e saldo atual.
    
    Parâmetros:
    - saldo: float (posicional) - Saldo atual da conta
    - extrato: str (nomeado) - Histórico de movimentações
    
    Retorna:
    - None (apenas exibe informações na tela)
    """
    print("\n" + "=" * 50)
    print(" " * 18 + "EXTRATO")
    print("=" * 50)
    
    # Verifica se há movimentações registradas
    if extrato == "":
        print("\nNão foram realizadas movimentações.")
    else:
        print(extrato)
    
    # Sempre exibe o saldo atual
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("=" * 50)


# ============================================================================
# FUNÇÕES DE GERENCIAMENTO DE USUÁRIOS E CONTAS
# ============================================================================

def validar_cpf(cpf):
    """
    Valida se o CPF contém apenas números e tem 11 dígitos.
    
    Parâmetros:
    - cpf: str - CPF a ser validado
    
    Retorna:
    - bool: True se válido, False caso contrário
    """
    # Remove espaços em branco
    cpf = cpf.strip()
    
    # Verifica se contém apenas dígitos e tem 11 caracteres
    if cpf.isdigit() and len(cpf) == 11:
        return True
    
    print("\n✗ CPF inválido! Deve conter exatamente 11 dígitos numéricos.")
    return False


def filtrar_usuario(cpf, usuarios):
    """
    Busca um usuário na lista pelo CPF.
    
    Parâmetros:
    - cpf: str - CPF do usuário a ser buscado
    - usuarios: list - Lista de todos os usuários cadastrados
    
    Retorna:
    - dict: Dados do usuário se encontrado
    - None: Se o usuário não for encontrado
    """
    # Percorre a lista de usuários
    for usuario in usuarios:
        # Compara o CPF informado com o CPF de cada usuário
        if usuario["cpf"] == cpf:
            return usuario
    
    # Retorna None se nenhum usuário for encontrado
    return None


def criar_usuario(usuarios):
    """
    Cria um novo usuário no sistema.
    
    Parâmetros:
    - usuarios: list - Lista de usuários (será modificada)
    
    Retorna:
    - None
    
    Regras:
    - O CPF deve ser único (não pode haver dois usuários com o mesmo CPF)
    - O CPF deve conter apenas números e ter 11 dígitos
    - Todos os campos são obrigatórios
    """
    print("\n" + "=" * 50)
    print(" " * 15 + "NOVO USUÁRIO")
    print("=" * 50)
    
    # Solicita e valida o CPF
    cpf = input("\nInforme o CPF (somente números): ")
    
    if not validar_cpf(cpf):
        return
    
    # Verifica se já existe um usuário com este CPF
    usuario_existente = filtrar_usuario(cpf, usuarios)
    if usuario_existente:
        print("\n✗ Já existe um usuário cadastrado com este CPF!")
        return
    
    # Coleta os demais dados do usuário
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (DD-MM-AAAA): ")
    endereco = input("Informe o endereço (logradouro, número - bairro - cidade/UF): ")
    
    # Cria o dicionário com os dados do usuário
    novo_usuario = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    }
    
    # Adiciona o usuário à lista
    usuarios.append(novo_usuario)
    print("\n✓ Usuário criado com sucesso!")


def criar_conta(agencia, numero_conta, usuarios):
    """
    Cria uma nova conta bancária vinculada a um usuário existente.
    
    Parâmetros:
    - agencia: str - Número da agência (fixo: "0001")
    - numero_conta: int - Número sequencial da conta
    - usuarios: list - Lista de usuários cadastrados
    
    Retorna:
    - dict: Dados da conta se criada com sucesso
    - None: Se o usuário não for encontrado
    
    Regras:
    - O usuário deve estar cadastrado no sistema
    - Cada conta é vinculada a apenas um usuário (CPF)
    - O número da conta é sequencial (1, 2, 3, ...)
    - A agência é sempre "0001"
    """
    print("\n" + "=" * 50)
    print(" " * 15 + "NOVA CONTA")
    print("=" * 50)
    
    # Verifica se existem usuários cadastrados
    if not usuarios:
        print("\n✗ Nenhum usuário cadastrado! Cadastre um usuário primeiro.")
        return None
    
    # Solicita o CPF do titular da conta
    cpf = input("\nInforme o CPF do usuário (ou digite 'listar' para ver usuários): ")
    
    # Opção para listar usuários cadastrados antes de escolher
    if cpf.lower() == 'listar':
        print("\n" + "-" * 50)
        print(" " * 12 + "USUÁRIOS CADASTRADOS")
        print("-" * 50)
        
        # Exibe todos os usuários cadastrados com seus CPFs
        for usuario in usuarios:
            print(f"Nome: {usuario['nome']}")
            print(f"CPF:  {usuario['cpf']}")
            print("-" * 50)
        
        # Solicita o CPF novamente após listar
        cpf = input("\nAgora informe o CPF do usuário: ")
    
    # Valida o formato do CPF
    if not validar_cpf(cpf):
        return None
    
    # Busca o usuário pelo CPF
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        # Cria o dicionário com os dados da conta
        nova_conta = {
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario
        }
        print(f"\n✓ Conta criada com sucesso para {usuario['nome']}!")
        return nova_conta
    
    print("\n✗ Usuário não encontrado! Verifique o CPF e tente novamente.")
    return None


def listar_contas(contas):
    """
    Lista todas as contas cadastradas no sistema.
    
    Parâmetros:
    - contas: list - Lista de todas as contas
    
    Retorna:
    - None (apenas exibe informações na tela)
    """
    print("\n" + "=" * 50)
    print(" " * 13 + "CONTAS CADASTRADAS")
    print("=" * 50)
    
    # Verifica se existem contas cadastradas
    if not contas:
        print("\nNenhuma conta cadastrada no sistema.")
        return
    
    # Percorre e exibe cada conta
    for conta in contas:
        print(f"""
Agência:        {conta['agencia']}
Conta:          {conta['numero_conta']}
Titular:        {conta['usuario']['nome']}
CPF:            {conta['usuario']['cpf']}
        """)
        print("-" * 50)


# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

def main():
    """
    Função principal que executa o loop do menu do sistema bancário.
    """
    # Define o menu de opções
    menu = """
╔════════════════════════════════════════════════╗
║          SISTEMA BANCÁRIO - MENU               ║
╚════════════════════════════════════════════════╝

[1] - Depositar
[2] - Sacar
[3] - Extrato
[4] - Novo usuário
[5] - Nova conta
[6] - Listar contas
[0] - Sair

=> """

    # Inicializa as variáveis do sistema
    saldo = 0  # Saldo inicial da conta
    limite = 500  # Limite máximo por saque
    extrato = ""  # Histórico de movimentações (string vazia inicialmente)
    numero_saques = 0  # Contador de saques realizados hoje
    LIMITE_SAQUES = 3  # Constante: número máximo de saques por dia
    usuarios = []  # Lista para armazenar usuários cadastrados
    contas = []  # Lista para armazenar contas criadas

    # Loop principal do programa
    while True:
        # Exibe o menu e captura a opção escolhida
        opcao = input(menu)
        
        # [1] DEPÓSITO
        if opcao == "1":
            try:
                valor = float(input("\nInforme o valor do depósito: R$ "))
                # Chama a função depositar passando parâmetros posicionais
                saldo, extrato = depositar(saldo, valor, extrato)
            except ValueError:
                print("\n✗ Erro! Digite um valor numérico válido.")
        
        # [2] SAQUE
        elif opcao == "2":
            try:
                valor = float(input("\nInforme o valor do saque: R$ "))
                # Chama a função sacar passando parâmetros nomeados
                saldo, extrato, numero_saques = sacar(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    limite=limite,
                    numero_saques=numero_saques,
                    limite_saques=LIMITE_SAQUES,
                )
            except ValueError:
                print("\n✗ Erro! Digite um valor numérico válido.")
        
        # [3] EXTRATO
        elif opcao == "3":
            # Exibe o extrato com parâmetro posicional e nomeado
            exibir_extrato(saldo, extrato=extrato)
        
        # [4] NOVO USUÁRIO
        elif opcao == "4":
            criar_usuario(usuarios)
        
        # [5] NOVA CONTA
        elif opcao == "5":
            # Calcula o próximo número de conta (sequencial)
            numero_conta = len(contas) + 1
            # Tenta criar a conta
            conta = criar_conta("0001", numero_conta, usuarios)
            # Se a conta foi criada com sucesso, adiciona à lista
            if conta:
                contas.append(conta)
        
        # [6] LISTAR CONTAS
        elif opcao == "6":
            listar_contas(contas)
        
        # [0] SAIR
        elif opcao == "0":
            print("\n" + "=" * 50)
            print("  Obrigado por utilizar nosso sistema. Até mais!")
            print("=" * 50 + "\n")
            break  # Encerra o loop e o programa
        
        # OPÇÃO INVÁLIDA
        else:
            print("\n✗ Operação inválida! Por favor, selecione uma opção válida.")


# Ponto de entrada do programa
if __name__ == "__main__":
    main()