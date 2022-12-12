import time
from threading import *
import random

"""Variáveis do Posto de Combustíveis"""
controle = -9
numero_bombas = 5
numero_clientes = 8

"""Criação de semáforos"""
semaforo_faltantes = Semaphore(numero_clientes)    # Processos que ainda faltam produzir
semaforo_disponiveis_consumidor = Semaphore(0)   # Processos disponíveis ao consumidor
ocupacao_regiao_critica = Semaphore(1)           # Trava de uso da região crítica.

"""Lista reservada para guardar os clientes"""
clientes = []


def auxiliar_numeros_aleatorios(a: int, b: int) -> float():
    """ Função auxiliar que gera números
    aleatórios no programa. Intervalo: [a,b]
    @param a: valor mínimo
    @param b: valor maximo. """
    return a + (b - a) * random.random()


def produtora_clientes() -> None:
    """ Função produtora por gerar clientes no sistema em
    tempos não regulares"""

    global controle
    controle += 10

    i = 1 * controle
    while True:
        print(f'O consumidor {i} acabou de chegar.')
        semaforo_faltantes.acquire()
        ocupacao_regiao_critica.acquire()

        clientes.append(i)
        time.sleep(auxiliar_numeros_aleatorios(1, 2))

        ocupacao_regiao_critica.release()
        semaforo_disponiveis_consumidor.release()

        i += 1
        if i == numero_clientes:
            break

def consumidora_atendimento() -> None:
    """Função consumidora de modo que atende
    os interesses do cliente e o manda embora."""

    while True:
        semaforo_disponiveis_consumidor.acquire()
        ocupacao_regiao_critica.acquire()

        atendimento = clientes.pop(0)
        print(f'O cliente {atendimento} está sendo atendido')
        time.sleep(auxiliar_numeros_aleatorios(2, 8))
        print(f'O cliente {atendimento} está finalizado.')

        ocupacao_regiao_critica.release()
        semaforo_faltantes.release()


if __name__ == "__main__":

    print("O posto de combustível acaba de abrir.\n")

    # Criando um objeto com um bloco de clientes
    thread_clientes = Thread(target=produtora_clientes)
    thread_clientes.start()

    time.sleep(3)

    # Criando um objeto com um bloco de clientes
    thread_consumidora = Thread(target=consumidora_atendimento)
    thread_consumidora.start()

    # Criando um objeto com um bloco de clientes
    thread_clientes = Thread(target=produtora_clientes)
    thread_clientes.start()

    # Criando um objeto com um bloco de clientes
    thread_consumidora = Thread(target=consumidora_atendimento)
    thread_consumidora.start()

    # Criando um objeto com um bloco de clientes
    thread_consumidora = Thread(target=consumidora_atendimento)
    thread_consumidora.start()

    # Criando um objeto com um bloco de clientes
    thread_clientes = Thread(target=produtora_clientes)
    thread_clientes.start()

    # Criando um objeto com um bloco de clientes
    thread_consumidora = Thread(target=consumidora_atendimento)
    thread_consumidora.start()
