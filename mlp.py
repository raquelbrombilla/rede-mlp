import random, numpy 

opcao = ''
valores = []
max_iteracoes = 0
taxa_aprend = 0
sair = 0

unidades = {
    'A': {
        'ativacao': 0,
        'saida': 0,
        'erro': 0,
        'bias': 1,
        'pesos': [random.uniform(-1.2, 1.2), random.uniform(-1.2, 1.2)]
    },
    'B': {
        'ativacao': 0,
        'saida': 0,
        'erro': 0,
        'bias': 1,
        'pesos': [random.uniform(-1.2, 1.2), random.uniform(-1.2, 1.2)]
    },
    'C': {
        'ativacao': 0,
        'saida': 0,
        'erro': 0,
        'bias': 1,
        'pesos': [random.uniform(-1.2, 1.2), random.uniform(-1.2, 1.2)]
    }
}

def sigmoide(number):
    return 1.0 / (1.0 + numpy.exp(-number))

def isNumber(value):
    try:
        float(value)
    except ValueError:
        return False
    return True

def treinar(valores, taxa_aprend, max_iteracoes):  
    global unidades, sair
    
    i = 0
    erro_geral = 0
    iteracao = 0
    quad_erro = 0
    
    while(iteracao < max_iteracoes and sair == 0):
  
        ### FASE FORWARD
        # 1º passo
        unidades['A']['ativacao'] = unidades['A']['pesos'][0] * valores[i][0] + unidades['A']['pesos'][1] * valores[i][1] + unidades['A']['bias']
        unidades['B']['ativacao'] = unidades['B']['pesos'][0] * valores[i][0] + unidades['B']['pesos'][1] * valores[i][1] + unidades['B']['bias']

        # 2º passo
        unidades['A']['saida'] = sigmoide(unidades['A']['ativacao'])
        unidades['B']['saida'] = sigmoide(unidades['B']['ativacao'])

        # 3º passo
        unidades['C']['ativacao'] = unidades['C']['pesos'][0] * unidades['A']['saida'] + unidades['C']['pesos'][1] * unidades['B']['saida'] + unidades['C']['bias']
        unidades['C']['saida'] = sigmoide(unidades['C']['ativacao'])

        # 4º passo
        erro_geral = valores[i][2] - unidades['C']['saida']
        quad_erro = quad_erro + (erro_geral**2)

        ### FASE BACKWARD
        # 5º passo
        unidades['C']['erro'] = erro_geral * unidades['C']['saida'] * (1 - unidades['C']['saida'])

        # 6º passo
        unidades['A']['erro'] = unidades['A']['saida'] * (1 - unidades['A']['saida']) * unidades['C']['pesos'][0] * unidades['C']['erro']
        unidades['B']['erro'] = unidades['B']['saida'] * (1 - unidades['B']['saida']) * unidades['C']['pesos'][1] * unidades['C']['erro']

        # 7º passo
        unidades['A']['bias'] = unidades['A']['bias'] + (taxa_aprend * unidades['A']['erro'] * unidades['A']['bias'])
        unidades['A']['pesos'][0] += (taxa_aprend * unidades['A']['erro'] * valores[i][0])
        unidades['A']['pesos'][1] += (taxa_aprend * unidades['A']['erro'] * valores[i][1])

        unidades['B']['bias'] = unidades['B']['bias'] + (taxa_aprend * unidades['B']['erro'] * unidades['B']['bias'])
        unidades['B']['pesos'][0] += (taxa_aprend * unidades['B']['erro'] * valores[i][0])
        unidades['B']['pesos'][1] += (taxa_aprend * unidades['B']['erro'] * valores[i][1])

        # 8º passo
        unidades['C']['bias'] = unidades['C']['bias'] + (taxa_aprend * unidades['C']['erro'] * unidades['C']['bias'])
        unidades['C']['pesos'][0] += (taxa_aprend * unidades['C']['erro'] * unidades['A']['saida'])
        unidades['C']['pesos'][1] += (taxa_aprend * unidades['C']['erro'] * unidades['B']['saida'])
        
        i += 1
        if(i > 3):
            i = 0
            quad_erro = quad_erro + (erro_geral * erro_geral)
            if(quad_erro <= 0.01):
                sair = 1
                print("\nTreinamento ok")

            else:
                sair = 0
                quad_erro = 0
        else:
            quad_erro = quad_erro + (erro_geral * erro_geral)

        
        print(iteracao, " - Quadrado do erro: ", quad_erro)

        iteracao += 1
        if (iteracao > max_iteracoes):
            sair = 1
            print("\nTreinamento falhou")


def testar():
    opcao = 'SIM'

    while(opcao == 'SIM'):
        e1 = int(input("Digite o primeiro valor: "))
        e2 = int(input("Digite o segundo valor: "))

        print("\nPESOS A => ", unidades['A']['pesos'][0], " e ", unidades['A']['pesos'][1], ". BIAS => ", unidades['A']['bias'])
        print("\nPESOS B => ", unidades['B']['pesos'][0], " e ", unidades['B']['pesos'][1], ". BIAS => ", unidades['B']['bias'])
        print("\nPESOS C => ", unidades['C']['pesos'][0], " e ", unidades['C']['pesos'][1], ". BIAS => ", unidades['C']['bias'])

        unidades['A']['ativacao'] =  unidades['A']['bias'] +  unidades['A']['pesos'][0] * e1 + unidades['A']['pesos'][1] * e2 
        unidades['A']['saida'] = sigmoide(unidades['A']['ativacao'])

        unidades['B']['ativacao'] = unidades['B']['bias'] + unidades['B']['pesos'][0] * e1 + unidades['B']['pesos'][1] * e2
        unidades['B']['saida'] = sigmoide(unidades['B']['ativacao'])

        unidades['C']['ativacao'] = unidades['C']['bias'] + unidades['C']['pesos'][0] * unidades['A']['saida'] + unidades['C']['pesos'][1] * unidades['B']['saida']
        unidades['C']['saida'] = sigmoide(unidades['C']['ativacao'])

        if(unidades['C']['saida'] < 0.5):
            print("\nSaída = 0")
        else:
            print("\nSaída = 1")

        print("\nEntrada 1 => ", e1, "\nEntrada 2 => ", e2, "\nSaída => ", unidades['C']['saida'])
        print("\n\nDeseja repetir o teste? SIM ou NAO")
        opcao = str(input()).upper()   


def menu(): 
    global opcao, valores, max_iteracoes, taxa_aprend

    print("""Qual porta lógica você deseja testar? 
                a - AND
                b - OR
                c - NAND
                d - NOR
                e - XOR 
                s - SAIR
        """)

    opcao = input()

    if(opcao == 'a' or opcao == 'A'):
        valores = [
            [0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 1.0, 1.0]
        ]
    elif(opcao == 'b' or opcao == 'B'):
        valores = [
            [0.0, 0.0, 0.0],
            [0.0, 1.0, 1.0],
            [1.0, 0.0, 1.0],
            [1.0, 1.0, 1.0]
        ]
    elif(opcao == 'c' or opcao == 'C'):
        valores = [
            [0.0, 0.0, 1.0],
            [0.0, 1.0, 1.0],
            [1.0, 0.0, 1.0],
            [1.0, 1.0, 0.0]
        ]
    elif(opcao == 'd' or opcao == 'D'):
        valores = [
            [0.0, 0.0, 1.0],
            [0.0, 1.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 1.0, 0.0]
        ]
    elif(opcao == 'e' or opcao == 'E'):
        valores = [
            [0.0, 0.0, 0.0],
            [0.0, 1.0, 1.0],
            [1.0, 0.0, 1.0],
            [1.0, 1.0, 0.0]
        ]
    elif(opcao == 's' or opcao == 'S'):
        exit()
    else:
        print("A opção escolhida é inválida. Tente novamente.")
        menu()

    if(opcao != ''):
        print("Quantas iterações a rede deve ter? ")
        max_iteracoes = int(input())

        print("Qual a taxa de aprendizagem desejada? ")
        taxa_aprend = int(input()) 

        if( (isNumber(taxa_aprend) == False) or (isNumber(max_iteracoes) == False) ):
            print("Você deve digitar apenas números para as iterações e taxa de aprendizagem.\n\nComece de novo:\n")
            menu()

menu()
treinar(valores, taxa_aprend, max_iteracoes)
testar()

