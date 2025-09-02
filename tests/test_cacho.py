from unittest.mock import patch

from src.juego.cacho import Cacho
from src.juego.dado import Pinta


class TestCacho:
    def test_cacho_inicia_con_5_dados(self):
        cacho = Cacho()
        assert cacho.get_cantidad_dados() == 5

    @patch("src.servicios.generador_aleatorio.GeneradorAleatorio.generar_entero")
    def test_mostrar_dados_con_mock(self, mock_generar):
        """Test qye verifica que un cacho mantiene pintas generadas desde un
        inicio si no son alteradas"""
        mock_generar.side_effect = [
            Pinta.AS,
            Pinta.TONTO,
            Pinta.TREN,
            Pinta.CUADRA,
            Pinta.QUINA,
        ]
        cacho = Cacho()
        cacho.set_visible()
        assert cacho.get_pintas_de_dados() == [
            Pinta.AS,
            Pinta.TONTO,
            Pinta.TREN,
            Pinta.CUADRA,
            Pinta.QUINA,
        ]

    def test_cambiar_estado_visibilidad(self):
        """Test para verificar los cambios de estado oculto/visible de un cacho"""
        cacho = Cacho()
        assert (
            cacho.get_visibilidad() is False
        )  # Cuando se inicia un cacho siempre estara oculto
        cacho.set_visible()
        assert cacho.get_visibilidad() is True
        cacho.set_oculto()
        assert cacho.get_visibilidad() is False

    def test_ver_pintas_de_dados_segun_visibilidad(self):
        """Test para verificar que las pintas se ocultan o son visibles
        segun el estado del cacho"""
        cacho = Cacho()
        cacho.set_visible()
        assert cacho.get_pintas_de_dados() is not None
        cacho.set_oculto()
        assert cacho.get_pintas_de_dados() is None

    @patch("src.servicios.generador_aleatorio.GeneradorAleatorio.generar_entero")
    def test_agitar_altera_los_dados(self, mock_generar):
        """
        Test que genera valores controlados, simulando que
        la generacion aleatoria de valores al agitar un cacho
        """
        """Debe regenerar los dados al agitar el cacho."""
        # Antes de agitar: AS, TONTO, TREN, CUADRA, QUINA
        # Después de agitar: SEXTO, QUINA, CUADRA, TREN, TONTO
        mock_generar.side_effect = [
            Pinta.AS,
            Pinta.TONTO,
            Pinta.TREN,
            Pinta.CUADRA,
            Pinta.QUINA,
            Pinta.SEXTO,
            Pinta.QUINA,
            Pinta.CUADRA,
            Pinta.TREN,
            Pinta.TONTO,
        ]

        cacho = Cacho(5)
        cacho.set_visible()
        antes = cacho.get_pintas_de_dados()
        cacho.agitar()
        despues = cacho.get_pintas_de_dados()

        assert antes != despues
        assert antes == [Pinta.AS, Pinta.TONTO, Pinta.TREN, Pinta.CUADRA, Pinta.QUINA]
        assert despues == [
            Pinta.SEXTO,
            Pinta.QUINA,
            Pinta.CUADRA,
            Pinta.TREN,
            Pinta.TONTO,
        ]

    @patch("src.servicios.generador_aleatorio.GeneradorAleatorio.generar_entero")
    def test_agregar_dado(self, mock_generar):
        """
        Verifica que al agregar un dado se incremente la cantidad
        y que el nuevo dado tenga la pinta correcta según el mock.
        """
        mock_generar.side_effect = [
            Pinta.AS,
            Pinta.TONTO,
            Pinta.TREN,
            Pinta.CUADRA,
            Pinta.QUINA,
            Pinta.SEXTO,
        ]

        cacho = Cacho(5)
        cacho.set_visible()
        pintas_iniciales = cacho.get_pintas_de_dados()

        cacho.eliminar_dado()  # -1 dado = 4
        cacho.eliminar_dado()  # -1 dado = 3
        cacho.agregar_dado()  # +1 dado = 4
        pintas_finales = cacho.get_pintas_de_dados()

        assert len(pintas_finales) == len(pintas_iniciales) - 1  # 5-1-1+1 = 4 dados
        assert pintas_finales[-1] == Pinta.SEXTO

    @patch("src.servicios.generador_aleatorio.GeneradorAleatorio.generar_entero")
    def test_eliminar_dado(self, mock_generar):
        """
        Verifica que al eliminar un dado se reduzca la cantidad correctamente.
        """
        mock_generar.side_effect = [Pinta.AS, Pinta.TONTO, Pinta.TREN]

        cacho = Cacho(3)
        cacho.set_visible()
        pintas_iniciales = cacho.get_pintas_de_dados()

        cacho.eliminar_dado()
        pintas_finales = cacho.get_pintas_de_dados()

        assert len(pintas_finales) == len(pintas_iniciales) - 1
        assert pintas_finales == pintas_iniciales[:-1]

    def test_eliminar_dado_cuando_cero(self):
        """Verifica que eliminar un dado con 0 dados no cause error."""
        cacho = Cacho(1)
        cacho.eliminar_dado()
        try:
            cacho.eliminar_dado()
        except Exception as e:
            assert False, f"Se lanzó una excepción inesperada: {e}"

        assert cacho.get_cantidad_dados() == 0
        assert cacho.get_pintas_de_dados() is None

    @patch("src.servicios.generador_aleatorio.GeneradorAleatorio.generar_entero")
    def test_no_se_puede_superar_limite_dados(self, mock_generar):
        """
        Verifica que al intentar agregar más dados del límite máximo
        no se agregue ninguno adicional.
        """
        mock_generar.side_effect = [
            Pinta.AS,
            Pinta.TONTO,
            Pinta.TREN,
            Pinta.CUADRA,
            Pinta.QUINA,
            Pinta.SEXTO,
            Pinta.AS,
            Pinta.TONTO,
        ]

        cacho = Cacho(5)  # límite máximo 5 y cantidad contenida
        cacho.set_visible()

        pintas_iniciales = cacho.get_pintas_de_dados()
        assert len(pintas_iniciales) == 5

        # Intentamos agregar dados extras (3 intentos)
        for _ in range(3):
            cacho.agregar_dado()

        pintas_finales = cacho.get_pintas_de_dados()
        assert len(pintas_finales) == 5
        assert pintas_finales == pintas_iniciales  # no cambió
