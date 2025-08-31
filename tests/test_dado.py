"""
Tests para la clase Dado del juego Dudo Chileno.
"""

from src.juego.dado import Dado, Pinta


class TestPinta:
    """Tests para el enum Pinta con las denominaciones tradicionales del
    Dudo."""

    def test_pinta_tiene_seis_valores(self):
        """Test que verifica que existen exactamente 6 pintas."""
        assert len(Pinta) == 6

    def test_pinta_valores_numericos_correctos(self):
        """Test que verifica que cada pinta tiene el valor numérico
        correcto."""
        assert Pinta.AS.value == 1
        assert Pinta.TONTO.value == 2
        assert Pinta.TREN.value == 3
        assert Pinta.CUADRA.value == 4
        assert Pinta.QUINA.value == 5
        assert Pinta.SEXTO.value == 6

    def test_pinta_denominaciones_tradicionales(self):
        """Test que verifica las denominaciones tradicionales del Dudo."""
        assert Pinta.AS.name == "AS"
        assert Pinta.TONTO.name == "TONTO"
        assert Pinta.TREN.name == "TREN"
        assert Pinta.CUADRA.name == "CUADRA"
        assert Pinta.QUINA.name == "QUINA"
        assert Pinta.SEXTO.name == "SEXTO"


class TestDado:
    """Tests para la clase Dado."""

    def test_dado_se_puede_crear(self):
        """Test que verifica que se puede crear una instancia de Dado."""
        dado = Dado()
        assert dado is not None

    def test_dado_show_retorna_pinta(self):
        """Test que verifica que el método show retorna una instancia de
        Pinta (Pinta actual)."""
        dado = Dado()
        pinta = dado.show()
        assert isinstance(pinta, Pinta)
