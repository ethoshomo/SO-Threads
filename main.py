import time
from threading import Semaphore, Thread
from curses import wrapper

from draw import norm, render

"""Variáveis do Posto de Combustíveis"""
controle = -9           # É só para alterar a numeração de clientes em cada bloco.
numero_bombas = 5  # Quantas threads poderão ser usadas
numero_clientes = 8  # Quantos clientes são produzidos por blocos

"""Criação de semáforos"""
clientes_esperando = Semaphore(numero_clientes)  # Processos que ainda faltam produzir
clientes_abastecendo = Semaphore(0)  # Processos disponíveis ao consumidor
bombas_disponiveis = Semaphore(numero_bombas)  # Trava de uso da região crítica.

"""Lista reservada para guardar os clientes"""
clientes = 0
clientes_finalizados = 0
bombas = numero_bombas


def produtor() -> None:
    """ Função produtora por gerar clientes no sistema em
    tempos não regulares"""

    global controle
    global clientes
    controle += 10

    i = 1 * controle
    while i < 10 * numero_clientes:
        # print(f'O consumidor {i} acabou de chegar.')
        clientes_esperando.acquire()
        bombas_disponiveis.acquire()

        time.sleep(abs(norm(2, 2)))
        clientes += 1

        bombas_disponiveis.release()
        clientes_abastecendo.release()

        i += 1


def consumidor() -> None:
    """Função consumidora de modo que atende
    os interesses do cliente e o manda embora."""

    global bombas
    global clientes
    global clientes_finalizados

    while True:
        clientes_abastecendo.acquire()
        bombas_disponiveis.acquire()

        bombas -= 1
        clientes -= 1
        time.sleep(abs(norm(1, 1)))

        bombas_disponiveis.release()
        clientes_esperando.release()

        bombas += 1
        clientes_finalizados += 1

def draw(scr):
    render(scr, [(clientes, "Clientes Esperando"), (bombas, "Bombas Disponiveis"), (clientes_finalizados, "Clientes Finalizados")])


def main(scr):
    scr.addstr(0, 0, "O posto de combustível acaba de abrir.\n")
    scr.refresh()
    scr.erase()

    # Criando um objeto com um bloco de clientes
    Thread(target=produtor).start()
    time.sleep(3)

    produtores = [Thread(target=produtor) for _ in range(3)]
    consumidores = [Thread(target=consumidor) for _ in range(3)]

    for i in range(3):
        produtores[i].start()
        consumidores[i].start()

    while True:
        draw(scr)


if __name__ == "__main__":
    wrapper(main)
