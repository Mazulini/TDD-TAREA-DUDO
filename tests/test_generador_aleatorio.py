# tests/test_generador_aleatorio.py
from src.servicios.generador_aleatorio import GeneradorAleatorio


class TestGeneradorAleatorio:
    """Tests para la clase GeneradorAleatorio."""

    def test_generador_entero_en_rango(self):
        """Test que verifica que se genera un numero aleatorio dentro del
        rango definido."""
        generador = GeneradorAleatorio()
        valor = generador.generar_entero(1, 6)
        assert 1 <= valor <= 6

    def test_generar_con_rango_unitario(self):
        """Test que verifica que generar funciona con un rango de un solo
        valor."""
        generador = GeneradorAleatorio()
        numero = generador.generar_entero(5, 5)
        assert numero == 5

    def test_generar_multiples_valores_estan_en_rango(self):
        """Test que verifica que múltiples generaciones están en el rango
        correcto."""
        for _ in range(100):
            generador = GeneradorAleatorio()
            numero = generador.generar_entero(1, 6)
            assert 1 <= numero <= 6
            assert isinstance(numero, int)

    def test_generador_con_semilla_reproducible(self):
        """Test que verifica que una semilla genera los mismos
        resultados."""
        gen1 = GeneradorAleatorio(semilla=42)
        gen2 = GeneradorAleatorio(semilla=42)
        sec1 = [gen1.generar_entero(1, 6) for _ in range(5)]
        sec2 = [gen2.generar_entero(1, 6) for _ in range(5)]
        assert sec1 == sec2

    def test_generador_con_semillas_distintas_dan_secuencias_distintas(self):
        """Test que verifica que dos semillas con resultado diferente
        nunca coincidiran"""
        gen1 = GeneradorAleatorio(semilla=1)
        gen2 = GeneradorAleatorio(semilla=2)
        sec1 = [gen1.generar_entero(1, 6) for _ in range(5)]
        sec2 = [gen2.generar_entero(1, 6) for _ in range(5)]
        assert sec1 != sec2
