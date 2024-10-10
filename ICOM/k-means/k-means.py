import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('housing.csv')
# Selecionar as colunas
data = data[['longitude', 'latitude', 'median_house_value', 'housing_median_age']]

# Normalizar os dados
data = (data - data.mean()) / data.std()

def cluster_assignment(data, centroids):
    """
    Atribui cada ponto de dados ao cluster mais próximo.
    
    Parâmetros:
    data (ndarray): Conjunto de dados.
    centroids (ndarray): Coordenadas dos centróides.
    
    Retorno:
    clusters (list): Lista de clusters atribuídos para cada ponto.
    """
    clusters = []
    for point in data:
        # Calcula a distância de cada ponto até os centróides
        distances = np.linalg.norm(point - centroids, axis=1)
        # Atribui o ponto ao cluster mais próximo
        cluster = np.argmin(distances)
        clusters.append(cluster)
    return clusters

def move_centroids(data, clusters, k):
    """
    Recalcula a posição dos centróides com base nos pontos atribuídos a cada cluster.
    
    Parâmetros:
    data (ndarray): Conjunto de dados.
    clusters (list): Lista de clusters atribuídos para cada ponto.
    k (int): Número de clusters.
    
    Retorno:
    new_centroids (list): Lista de novos centróides.
    """
    new_centroids = []
    for i in range(k):
        # Seleciona os dados do cluster atual
        cluster_data = data[np.where(np.array(clusters) == i)]
        # Calcula a média dos pontos do cluster para obter o novo centróide
        new_centroids.append(cluster_data.mean(axis=0))
    return new_centroids

def k_means(data, k, max_iter=100):
    """
    Implementa o algoritmo K-Means.
    
    Parâmetros:
    data (ndarray): Conjunto de dados.
    k (int): Número de clusters.
    max_iter (int): Número máximo de iterações.
    
    Retorno:
    clusters (list): Lista de clusters atribuídos para cada ponto.
    centroids (ndarray): Posição final dos centróides.
    """
    # Inicializa os centróides escolhendo aleatoriamente k pontos do conjunto de dados
    centroids = data[np.random.choice(range(len(data)), k)]
    for i in range(max_iter):
        # Atribui cada ponto ao cluster mais próximo
        clusters = cluster_assignment(data, centroids)
        # Recalcula a posição dos centróides
        new_centroids = move_centroids(data, clusters, k)
        # Verifica se os centróides mudaram. Se não, interrompe a iteração
        if np.array_equal(centroids, new_centroids):
            break
        centroids = new_centroids
    return clusters, centroids

def calculate_wcss(data, clusters, centroids):
    """
    Calcula o WCSS para os clusters.
    
    Parâmetros:
    data (ndarray): Conjunto de dados.
    clusters (list): Lista de clusters atribuídos para cada ponto.
    centroids (ndarray): Posição dos centróides.
    
    Retorno:
    wcss (float): Soma das distâncias quadradas dentro dos clusters.
    """
    wcss = 0
    for i, centroid in enumerate(centroids):
        # Seleciona os dados do cluster atual
        cluster_data = data[np.where(np.array(clusters) == i)]
        # Calcula a soma das distâncias quadradas dentro do cluster
        wcss += np.sum((cluster_data - centroid) ** 2)
    return wcss


wcss_values = []
data_np = data.to_numpy()
for k in range(2, 11):
    clusters, centroids = k_means(data_np, k)
    wcss = calculate_wcss(data_np, clusters, centroids)
    wcss_values.append(wcss)


plt.plot(range(2, 11), wcss_values, marker='o')
plt.xlabel('Número de Clusters')
plt.ylabel('WCSS')
plt.title('WCSS em função do Número de Clusters')
plt.show()

# O cotovelo do gráfico ocorre no 5º para o 6º cluster.
# A curva mostra uma mudança significativa no declive até o ponto correspondente a 5 clusters, 
# após o qual a redução no WCSS se torna menos acentuada.

