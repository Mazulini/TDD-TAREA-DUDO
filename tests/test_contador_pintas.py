from unittest.mock import Mock

import pytest

from src.juego.cacho import Cacho
from src.juego.contador_pintas import ContadorPintas
from src.juego.dado import Pinta


class TestContadorPintas:
    def test_contar_pinta_sin_ases(self):
        cacho1 = Mock()
        cacho1.get_pintas_de_dados.return_value = [Pinta.TREN, Pinta.TREN]
        cacho2 = Mock()
        cacho2.get_pintas_de_dados.return_value = [Pinta.QUINA]
        cachos = [cacho1, cacho2]
        contador = ContadorPintas()
        assert contador.contar(cachos, Pinta.TREN) == 2
        assert contador.contar(cachos, Pinta.QUINA) == 1
        assert contador.contar(cachos, Pinta.AS) == 0

    def test_contar_pinta_con_ases_comodines(self):
        cacho1 = Mock()
        cacho1.get_pintas_de_dados.return_value = [Pinta.TREN, Pinta.AS]
        cacho2 = Mock()
        cacho2.get_pintas_de_dados.return_value = [Pinta.QUINA, Pinta.AS]
        cachos = [cacho1, cacho2]
        contador = ContadorPintas()
        assert contador.contar(cachos, Pinta.TREN) == 3  # TREN + 2 AS
        assert contador.contar(cachos, Pinta.QUINA) == 3  # QUINA + 2 AS
        assert contador.contar(cachos, Pinta.AS) == 2  # Solo los Ases

    def test_contar_pinta_sin_comodin_en_ronda_de_un_dado(self):
        cacho1 = Mock()
        cacho1.get_pintas_de_dados.return_value = [Pinta.AS]
        cachos = [cacho1]
        contador = ContadorPintas()
        assert contador.contar(cachos, Pinta.TREN, ases_comodin=False) == 0
        assert contador.contar(cachos, Pinta.AS, ases_comodin=False) == 1

    def test_contar_pinta_varios_dados_sin_ases(self):
        cacho1 = Mock()
        cacho1.get_pintas_de_dados.return_value = [Pinta.CUADRA]
        cacho2 = Mock()
        cacho2.get_pintas_de_dados.return_value = [Pinta.QUINA, Pinta.SEXTO]
        cachos = [cacho1, cacho2]
        contador = ContadorPintas()
        assert contador.contar(cachos, Pinta.CUADRA) == 1
        assert contador.contar(cachos, Pinta.QUINA) == 1
        assert contador.contar(cachos, Pinta.SEXTO) == 1

    def test_contar_pinta_todos_ases(self):
        cacho1 = Mock()
        cacho1.get_pintas_de_dados.return_value = [Pinta.AS, Pinta.AS, Pinta.AS]
        cachos = [cacho1]
        contador = ContadorPintas()
        assert contador.contar(cachos, Pinta.TREN) == 3
        assert contador.contar(cachos, Pinta.AS) == 3

    def test_contar_pinta_cacho_oculto(self):
        cacho_visible = Mock()
        cacho_visible.get_pintas_de_dados.return_value = [Pinta.TREN, Pinta.AS]
        cacho_oculto = Mock()
        cacho_oculto.get_pintas_de_dados.return_value = None
        cachos = [cacho_visible, cacho_oculto]
        contador = ContadorPintas()
        assert contador.contar(cachos, Pinta.TREN) == 2  # TREN + AS
        assert contador.contar(cachos, Pinta.AS) == 1

    def test_contar_pinta_obliga_mostrar_si_cacho_oculto(self):
        cacho_oculto = Mock()
        # Simula oculto primero, luego visible siempre
        cacho_oculto.get_pintas_de_dados.side_effect = [None] + [
            [Pinta.TREN, Pinta.AS]
        ] * 10
        cacho_oculto.set_visible = Mock()
        contador = ContadorPintas()
        resultado = contador.contar([cacho_oculto], Pinta.TREN)
        assert resultado == 2  # TREN + AS
        assert contador.contar([cacho_oculto], Pinta.AS) == 1
        cacho_oculto.set_visible.assert_called_once()
