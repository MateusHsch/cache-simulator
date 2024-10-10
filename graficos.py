import matplotlib.pyplot as plt

def mostrarGrafico(acessos, hits, miss_compulsorio, miss_capacidade, miss_conflito):
    # Dados para o gráfico
    categorias = ['Acertos', 'Erros', 'Erros \n Compulsório', 'Erros de \n Capacidade', 'Erros de \n Conflito']
    cores = ['lightgreen','salmon', '#FDFD96', '#FDFD96', '#FDFD96']
    
    misses = miss_compulsorio + miss_conflito + miss_capacidade
    valores = [hits/acessos, misses/acessos, miss_compulsorio/acessos, miss_capacidade/acessos, miss_conflito/acessos]

    # Criar o gráfico de barras
    plt.bar(categorias, valores, color=cores, width=0.5)

    # Adicionar título e rótulos aos eixos
    plt.title('Cache Resultado')
    plt.xlabel('Taxa', loc='left')
    plt.ylabel('% por acessos')

    # Exibir o gráfico
    plt.show()