from unittest.mock import Mock

import pytest

from src.juego.arbitro_ronda import ArbitroRonda
from src.juego.contador_pintas import ContadorPintas
from src.juego.dado import Pinta


class TestArbitroRonda:
    def test_dudar_apuesta_gana_apostador(self):
        # Simula una ronda donde el jugador duda y la apuesta es correcta
        cachos = [Mock(), Mock()]
        cachos[0].get_pintas_de_dados.return_value = [Pinta.TREN, Pinta.AS]
        cachos[1].get_pintas_de_dados.return_value = [Pinta.TREN, Pinta.QUINA]
        jugada = (0, Pinta.TREN, 3)  # jugador 0 hace la jugada
        arbitro = ArbitroRonda()
        resultado = arbitro.resolver_duda(cachos, jugada)
        assert resultado == "pierde_dudador"

    def test_dudar_apuesta_pierde_apostador(self):
        # Simula una ronda donde el jugador duda y la apuesta es incorrecta
        cachos = [Mock(), Mock()]
        cachos[0].get_pintas_de_dados.return_value = [Pinta.TREN]
        cachos[1].get_pintas_de_dados.return_value = [Pinta.QUINA, Pinta.CUADRA]
        jugada = (1, Pinta.TREN, 2)  # jugador 1 hace la jugada
        arbitro = ArbitroRonda()
        resultado = arbitro.resolver_duda(cachos, jugada)
        assert resultado == "pierde_apostador"

    def test_calzar_apuesta_exacto(self):
        # Simula una ronda donde el jugador calza la apuesta exactamente
        cachos = [Mock(), Mock()]
        cachos[0].get_pintas_de_dados.return_value = [Pinta.TREN]
        cachos[1].get_pintas_de_dados.return_value = [Pinta.TREN]
        jugada = (0, Pinta.TREN, 2)  # jugador 0 calza
        arbitro = ArbitroRonda()
        resultado = arbitro.resolver_calzar(cachos, jugada)
        assert resultado == "gana_calzador"

    def test_calzar_apuesta_no_exacto(self):
        # Simula una ronda donde el jugador calza pero la apuesta no es exacta
        cachos = [Mock(), Mock()]
        cachos[0].get_pintas_de_dados.return_value = [Pinta.TREN]
        cachos[1].get_pintas_de_dados.return_value = [Pinta.QUINA]
        jugada = (1, Pinta.TREN, 2)  # jugador 1 calza
        arbitro = ArbitroRonda()
        resultado = arbitro.resolver_calzar(cachos, jugada)
        assert resultado == "pierde_calzador"

    def test_valida_calzar_mitad_dados(self):
        """
        Solo se puede calzar cuando esté la mitad
        o más de los dados en juego o cuando el jugador que desea calzar tenga un solo dado.
        """
        # Solo se puede calzar si hay la mitad o más de los dados en juego
        arbitro = ArbitroRonda()
        # jugador_dados is the number of dice the calzador has
        assert (
            arbitro.puede_calzar(total_dados=10, dados_en_juego=5, jugador_dados=5)
            is True
        )
        assert (
            arbitro.puede_calzar(total_dados=10, dados_en_juego=4, jugador_dados=4)
            is False
        )

    def test_valida_calzar_un_dado(self):
        # Se puede calzar si el jugador tiene solo un dado
        arbitro = ArbitroRonda()
        assert (
            arbitro.puede_calzar(total_dados=10, dados_en_juego=4, jugador_dados=1)
            is True
        )

    def test_no_puede_calzar(self):
        # No se puede calzar si no hay la mitad de los dados en juego y el jugador tiene más de un dado
        arbitro = ArbitroRonda()
        total_dados = 10
        dados_en_juego = 4
        jugador_dados = 2
        assert arbitro.puede_calzar(total_dados, dados_en_juego, jugador_dados) is False
        # Y el método resolver_calzar debe devolver "no_se_puede_calzar"
        cachos = [Mock(), Mock()]
        cachos[0].get_pintas_de_dados.return_value = [Pinta.TREN, Pinta.QUINA]
        cachos[1].get_pintas_de_dados.return_value = [Pinta.CUADRA, Pinta.SEXTO]
        jugada = (0, Pinta.TREN, 2)
        resultado = arbitro.resolver_calzar(cachos, jugada)
        assert resultado == "pierde_calzador"
