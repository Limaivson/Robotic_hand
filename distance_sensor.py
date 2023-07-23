import serial
import math

# Configurar a porta serial (ajuste a porta correta)
porta_serial = serial.Serial('COM5', 9600)

distancias = []  # Lista para armazenar as distâncias recebidas

while True:
    # Ler os dados recebidos do Arduino
    dados = porta_serial.readline().decode().strip()

    # Separar os dados de distância e ângulo
    distancia, angulo = map(float, dados.split(","))

    # Adicionar a distância à lista
    distancias.append(distancia)

    # Calcular a média das distâncias recebidas
    media_distancias = sum(distancias) / len(distancias)

    # Calcular as distâncias x e z usando a média
    cateto_oposto = media_distancias * math.sin(math.radians(angulo))
    cateto_adjacente = media_distancias * math.cos(math.radians(angulo))

    # Exibir os resultados
    print(f"Média das distâncias: {media_distancias} cm")
    print(f"Ângulo: {angulo} graus")
    print(f"Distância x: {cateto_oposto} cm")
    print(f"Distância z: {cateto_adjacente} cm")
