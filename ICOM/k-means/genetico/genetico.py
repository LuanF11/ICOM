import random

# Definindo as disciplinas, professores e suas disponibilidades
disciplinas = ['Matemática', 'Português', 'Ciências', 'História', 'Educação Física']
professores = {
    'Professor A': {'disciplinas': ['Matemática', 'Português'], 'disponibilidade': [0, 3]},
    'Professor B': {'disciplinas': ['História', 'Ciências'], 'disponibilidade': [1, 4]},
    'Professor C': {'disciplinas': ['Educação Física'], 'disponibilidade': [0, 4]},
}

#Inicialização da população
def inicializar_populacao(tamanho):
    populacao = []
    for _ in range(tamanho):
        horario = [[random.choice(disciplinas) for _ in range(5)] for _ in range(2)]  #gera 2 turmas, 5 períodos
        populacao.append(horario)
    return populacao

#Função de aptidão
def calcular_aptidao(horario):
    penalidade = 0
    atribuicoes = []
    for turma in horario:
        atribuicao_turma = []
        for periodo, disciplina in enumerate(turma):
            professor_encontrado = False
            for professor, dados in professores.items():
                if disciplina in dados['disciplinas'] and periodo in dados['disponibilidade']:
                    professor_encontrado = True
                    atribuicao_turma.append((disciplina, professor, periodo))
                    break
            if not professor_encontrado:
                penalidade += 1
                atribuicao_turma.append((disciplina, None, periodo))
        atribuicoes.append(atribuicao_turma)
    aptidao = 100 - penalidade  #Maior valor para aptidão é melhor
    return aptidao, atribuicoes

#Crossover
def crossover(pai1, pai2):
    ponto = random.randint(1, 4)  #Ponto de crossover
    filho1 = []
    filho2 = []
    for turma1, turma2 in zip(pai1, pai2):
        novo_turma1 = turma1[:ponto] + turma2[ponto:]
        novo_turma2 = turma2[:ponto] + turma1[ponto:]
        filho1.append(novo_turma1)
        filho2.append(novo_turma2)
    return filho1, filho2

#Mutação
def mutacao(horario):
    turma = random.randint(0, 1)  #Escolhe aleatoriamente uma turma
    periodo = random.randint(0, 4)  #Escolhe aleatoriamente um período
    horario[turma][periodo] = random.choice(disciplinas)  #Troca a disciplina
    return horario

#Seleção por torneio
def torneio(populacao, k=3):
    competidores = random.sample(populacao, k)
    return max(competidores, key=lambda x: calcular_aptidao(x)[0])

def algoritmo_genetico(num_geracoes, taxa_crossover=0.7, taxa_mutacao=0.01, elitismo=True):
    populacao = inicializar_populacao(20)  #Aumentar o tamanho da população
    for geracao in range(num_geracoes):
        #Avaliação da aptidão
        aptidoes = [calcular_aptidao(horario)[0] for horario in populacao]
        print(f'Geração {geracao + 1}: Melhor = {max(aptidoes)}, Média = {sum(aptidoes) / len(populacao)}')

        nova_populacao = []

        #manter o melhor indivíduo
        if elitismo:
            melhor_individuo = max(populacao, key=lambda x: calcular_aptidao(x)[0])
            nova_populacao.append(melhor_individuo)

        #Seleção, crossover e mutação
        while len(nova_populacao) < len(populacao):
            pai1 = torneio(populacao)
            pai2 = torneio(populacao)

            #Crossover
            if random.random() < taxa_crossover:
                filho1, filho2 = crossover(pai1, pai2)
            else:
                filho1, filho2 = pai1, pai2

            #Mutação
            if random.random() < taxa_mutacao:
                filho1 = mutacao(filho1)
            if random.random() < taxa_mutacao:
                filho2 = mutacao(filho2)

            nova_populacao.extend([filho1, filho2])

        populacao = nova_populacao[:len(populacao)]  #Garantir que a população não exceda o tamanho original

    melhor_horario = max(populacao, key=lambda x: calcular_aptidao(x)[0])
    melhor_aptidao, atribuicoes = calcular_aptidao(melhor_horario)
    return melhor_horario, atribuicoes

# Executar o algoritmo
melhor_horario, atribuicoes = algoritmo_genetico(100)
print("Melhor Horário:", melhor_horario)
print("Atribuições:")
for i, turma in enumerate(atribuicoes):
    print(f"\nTurma {i + 1}:")
    for disciplina, professor, periodo in turma:
        dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
        print(f"Disciplina: {disciplina}, Professor: {professor}, Período: {dias[periodo]} ({periodo})")