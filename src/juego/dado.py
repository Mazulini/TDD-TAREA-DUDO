"""
Módulo que contiene las clases Dado y Pinta para el juego Dudo Chileno.
"""

from enum import Enum

from src.servicios.generador_aleatorio import GeneradorAleatorio


class Pinta(Enum):
    """
    Enum que representa las pintas (caras) de un dado del Dudo Chileno
    con sus denominaciones tradicionales.
    """

    AS = 1
    TONTO = 2
    TREN = 3
    CUADRA = 4
    QUINA = 5
    SEXTO = 6


class Dado:
    def __init__(self, generador: GeneradorAleatorio = GeneradorAleatorio()):
        """
        Inicializa un dado con una pinta aleatoria.
        Usa generar_entero para elegir un índice en Pinta.
        """
        pintas = list(Pinta)
        valor = generador.generar_entero(0, len(pintas) - 1)
        # si valor es un Enum, lo usamos; si es int, lo convertimos a Pinta
        self.__pinta = valor if isinstance(valor, Pinta) else pintas[valor]

    def show(self):
        """
        Retorna la pinta del dado
        """
        return self.__pinta
