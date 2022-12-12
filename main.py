import time
import threading
import random

"""Variáveis do Posto de Combustíveis"""
numero_bombas = 3
numero_clientes = 10

"""Lista reservada para guardar os clientes"""
clientes = []

"""Lista reservada para guardar os objetos de threads criados"""
bombas = []


def auxiliar_numeros_aleatorios(a: int, b: int) -> float():
    """ Função auxiliar que gera números
    aleatórios no programa. """
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
        time.sleep(auxiliar_numeros_aleatorios(2, 5))

def consumidora_abastecimento() -> None:
    """Função consumidora de modo que atende
    os interesses do cliente e o manda embora."""
    atendimento = clientes.pop(0)
    print(f'O cliente {atendimento} está sendo atendido')
    time.sleep(auxiliar_numeros_aleatorios(4, 7))
    print(f'O cliente {atendimento} está finalizado.')


if __name__ == "__main__":

    print("O posto de combustível acaba de abrir.\n")

    # Iniciando as bombas de combustivel
    for bomba in range(numero_bombas):
        x = threading.Thread(target=threads_bombas, args=[bomba])
        bombas.append([x, bomba])
        x.start()

    # Criando um objeto com um bloco de clientes
    clientes = threading.Thread(target=produtora_clientes).start()

    while len(clientes) != 0:
        consumidora_abastecimento()


