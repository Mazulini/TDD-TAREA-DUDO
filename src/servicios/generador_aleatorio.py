# src/servicios/generador_aleatorio.py
import random


class GeneradorAleatorio:
    def __init__(self, semilla: int = None):
        # cada instancia tiene su propio generador independiente
        self._random = random.Random(semilla)

    def generar_entero(self, minimo: int, maximo: int):
        """Devuelve un número entero aleatorio dentro del intervalo definido."""
        return self._random.randint(minimo, maximo)
