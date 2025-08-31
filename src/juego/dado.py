"""
Módulo que contiene las clases Dado y Pinta para el juego Dudo Chileno.
"""

import random
from enum import Enum


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
    """
    Clase que representa un dado del juego Dudo Chileno.
    """

    def __init__(self):
        """Inicializa un dado con una pinta aleatoria."""
        self._pinta = random.choice(list(Pinta))

    def show(self):
        """
        Retorna la pinta actual del dado.

        Returns:
            Pinta: La pinta actual del dado
        """
        return self._pinta
