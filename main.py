import time
from threading import *
import random

"""Variáveis do Posto de Combustíveis"""
numero_bombas = 3
numero_clientes = 10

"""Lista reservada para guardar os clientes"""
clientes = []

"""Lista reservada para guardar os objetos de threads criados"""
bombas = []

"""Criação do semáforo"""
semaforo = Semaphore()


def auxiliar_numeros_aleatorios(a: int, b: int) -> float():
    """ Função auxiliar que gera números
    aleatórios no programa. Intervalo: [a,b]
    @param a: valor mínimo
    @param b: valor maximo. """
    return a + (b - a) * random.random()


def threads_bombas(identificador) -> None:
    """Função auxiliar que imprime a informação de
    que as threads foram criadas. """
    print(f'Ligando a bomba de abastecimento {identificador}.')
    time.sleep(auxiliar_numeros_aleatorios(3, 5))


def produtora_clientes() -> None:
    """ Função produtora por gerar clientes no sistema em
    tempos não regulares"""
    for i in range(numero_clientes):
        print(f'O consumidor {i + 1} acabou de chegar.')
        clientes.append(i + 1)
        time.sleep(auxiliar_numeros_aleatorios(1, 3))

def consumidora_atendimento() -> None:
    return clientes.pop(0)

def regiao_critica_abastecimento() -> bool:
    """Função consumidora de modo que atende
    os interesses do cliente e o manda embora."""

    semaforo.acquire()
    atendimento = consumidora_atendimento()
    print(f'O cliente {atendimento} está sendo atendido')
    time.sleep(auxiliar_numeros_aleatorios(4, 7))
    print(f'O cliente {atendimento} está finalizado.')
    semaforo.release()

    if clientes.__sizeof__() == 0:
        return False
    return True


if __name__ == "__main__":

    print("O posto de combustível acaba de abrir.\n")

    # Iniciando as bombas de combustivel
    for bomba in range(numero_bombas):
        x = Thread(target=threads_bombas, args=[bomba])
        bombas.append([x, bomba])
        x.start()

    # Criando um objeto com um bloco de clientes
    clientes = Thread(target=produtora_clientes)
    clientes.start()
    time.sleep(5)

    while True:
        if regiao_critica_abastecimento() == False:
            break


