import time
from threading import Semaphore, Thread
from curses import wrapper

from draw import norm, render, make_block

"""Variáveis do Posto de Combustíveis"""
numero_bombas = 5  # Quantas threads poderão ser usadas
numero_clientes = 10  # Quantos clientes são produzidos por blocos

"""Criação de semáforos"""
clientes_esperando = Semaphore(numero_clientes)  # Processos que ainda faltam produzir
clientes_abastecendo = Semaphore(0)  # Processos disponíveis ao consumidor
bombas_disponiveis = Semaphore(numero_bombas)  # Trava de uso da região crítica.

"""Lista reservada para guardar os clientes"""
clientes = 0
clientes_finalizados = 0
bombas = numero_bombas


def produtor() -> None:
    """
    Função produtora que incrementa a quantidade de clientes esperando por bombas para utilizarem temporal.
    É esperado que chegue um novo cliente a cada um segundo.
    """
    global clientes

    while True:
        # Caso haja espaço para espera de novos clientes, e existam bombas que possam ser usados, entrar no espaço
        # crítico de entrada de novos clientes.
        clientes_esperando.acquire()
        bombas_disponiveis.acquire()

        time.sleep(abs(norm(1, 2)))  # Média de 1 segundo, com desvio padrão de 2 segundos
        clientes += 1

        # Caso um novo cliente entre em espera, contabilizá-lo e enviá-lo a uma bomba quando possível.
        bombas_disponiveis.release()
        clientes_abastecendo.release()


def consumidor() -> None:
    """
    Função consumidora que atende uma lista de clientes, desde que haja uma quantidade de bombas livres
    e cliente em espera maior que zero.

    A função executa por tempo indefinido.
    """
    global bombas
    global clientes
    global clientes_finalizados

    while True:
        # Caso haja bombas disponíveis, entrar na zona crítica (de abastecimento)
        # O tempo de abastecimento médio é em torno de 4s
        clientes_abastecendo.acquire()
        bombas_disponiveis.acquire()

        bombas -= 1
        clientes -= 1
        time.sleep(abs(norm(4, 1)))  # Média de 4 segundos, com desvio padrão de 1 segundo

        # Após a realização do abastecimento, liberar a bomba e contabilizar o cliente finalizado
        clientes_finalizados += 1
        bombas += 1

        bombas_disponiveis.release()
        clientes_esperando.release()


def draw(scr):
    """
    Desenha na tela usando o módulo Curses uma sequência de tabelas contendo a quantidade de clientes em espera,
    bombas disponíveis e clientes já atendidos, em tempo real.
    """
    render(scr, [(clientes, numero_clientes, "Clientes Esperando"),
                 (bombas, numero_bombas, "Bombas Disponiveis"),
                 (clientes_finalizados, clientes_finalizados, f"Clientes Finalizados - ({clientes_finalizados})")])


def main(scr):
    scr.addstr(0, 0, "O posto de combustível acaba de abrir.\n")
    scr.refresh()
    scr.erase()

    # Inicializa a primeira thread de produtor (clientes)
    Thread(target=produtor, daemon=True).start()
    time.sleep(3)

    produtores = [Thread(target=produtor, daemon=True) for _ in range(10)]
    consumidores = [Thread(target=consumidor, daemon=True) for _ in range(10)]

    # Inicializar as threads para os produtores (clientes) e consumidores (funcionarios)
    for i in range(10):
        produtores[i].start()
        consumidores[i].start()

    # Desenha o funcionamento na tela enquanto menos de 50 clientes terminarem de ser atendidos
    while True:
        if clientes_finalizados >= 50:
            return 0
        try:
            draw(scr)
        except Exception:
            return -1


if __name__ == "__main__":
    # Verifica se o tamanho da tela é adequado para executar o programa
    if wrapper(main) == -1:
        print("Tamanho de Terminal insuficiente, por favor expanda a sua janela para visualizar o programa.")
    else:
        print("******************* POSTO DE COMBUSTIVEL *******************")
        print("Total de clientes atendidos durante o expediente:", clientes_finalizados, end="\n\n")
        print("Estado Final:\n")
        print(make_block((clientes, numero_clientes, "Clientes Esperando")))
        print(make_block((bombas, numero_bombas, "Bombas Disponiveis")))
        print(make_block(
            (clientes_finalizados, clientes_finalizados, f"Clientes Finalizados - ({clientes_finalizados})")))
