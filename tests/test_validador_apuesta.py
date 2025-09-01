import pytest

from src.juego.dado import Pinta
from src.juego.validador_apuesta import Apuesta, ValidadorApuesta


class TestValidadorApuesta:

    def test_primera_apuesta(self):
        """Test apuesta válida, no As"""
        apuesta = Apuesta(2, Pinta.TREN)
        assert ValidadorApuesta.es_valida(None, apuesta, cantidad_dados=5)

        """Test apuesta inválida, As con más de 1 dado"""
        apuesta_as = Apuesta(2, Pinta.AS)
        assert not ValidadorApuesta.es_valida(None, apuesta_as, cantidad_dados=5)

        """Test apuesta válida, As con solo 1 dado"""
        apuesta_as_1dado = Apuesta(3, Pinta.AS)
        assert ValidadorApuesta.es_valida(None, apuesta_as_1dado, cantidad_dados=1)

        """Test apuesta inválida, apuesta con una cantidad de dados no permitida"""
        apuesta_as_1dado = Apuesta(3, Pinta.AS)
        assert not ValidadorApuesta.es_valida(None, apuesta_as_1dado, cantidad_dados=-3)

    def test_cantidad_de_pintas_mayor_que_cero(self):
        """Test debe lanzar ValueError si la cantidad es 0 o negativa"""
        with pytest.raises(ValueError):
            Apuesta(0, Pinta.TREN)

        with pytest.raises(ValueError):
            Apuesta(-5, Pinta.AS)

        # Esto no debería lanzar error
        Apuesta(1, Pinta.CUADRA)

    def test_mayor_cantidad_o_mayor_pinta(self):
        """Test mayor cantidad o pinta superior"""
        anterior = Apuesta(2, Pinta.TREN)

        """Test mayor cantidad, misma pinta"""
        nueva = Apuesta(3, Pinta.TREN)
        assert ValidadorApuesta.es_valida(anterior, nueva)

        """Test misma cantidad, pinta mayor"""
        nueva = Apuesta(2, Pinta.QUINA)
        assert ValidadorApuesta.es_valida(anterior, nueva)

        """Test menor cantidad, inválida"""
        nueva = Apuesta(1, Pinta.TREN)
        assert not ValidadorApuesta.es_valida(anterior, nueva)

        """Test misma cantidad y misma pinta, inválida"""
        nueva = Apuesta(2, Pinta.TREN)
        assert not ValidadorApuesta.es_valida(anterior, nueva)

        """Test misma cantidad y pinta menor, inválida"""
        nueva = Apuesta(2, Pinta.TONTO)
        assert not ValidadorApuesta.es_valida(anterior, nueva)

    def test_cambiar_a_ases(self):
        """Test cambiar a Ases"""
        anterior = Apuesta(4, Pinta.TREN)
        """Test caso cantidad par"""
        nueva = Apuesta(3, Pinta.AS)  # 4 / 2 + 1 = 3
        assert ValidadorApuesta.es_valida(anterior, nueva)

        """Test caso cantidad impar"""
        anterior = Apuesta(5, Pinta.QUINA)
        nueva = Apuesta(3, Pinta.AS)  # 5 // 2 + 1 = 3
        assert ValidadorApuesta.es_valida(anterior, nueva)

        """Test caso cantidad incorrecta, inválida"""
        anterior = Apuesta(4, Pinta.CUADRA)
        nueva = Apuesta(2, Pinta.AS)  # 4 / 2 + 1 = 3 != 2
        assert not ValidadorApuesta.es_valida(anterior, nueva)

    def test_cambiar_de_ases(self):
        """Test cambiar de Ases a otra pinta"""
        anterior = Apuesta(2, Pinta.AS)
        """Test mínimo correcto"""
        nueva = Apuesta(5, Pinta.TREN)  # 2*2 + 1 = 5
        assert ValidadorApuesta.es_valida(anterior, nueva)

        """Test mayor que mínimo, válido"""
        nueva = Apuesta(6, Pinta.CUADRA)
        assert ValidadorApuesta.es_valida(anterior, nueva)

        """Test menor que mínimo, inválido"""
        nueva = Apuesta(4, Pinta.QUINA)  # 4 < 5
        assert not ValidadorApuesta.es_valida(anterior, nueva)
