from unittest.mock import Mock, call

import pytest

from src.juego.dado import Pinta
from src.juego.gestor_partida import GestorPartida


class TestGestorPartida:
    def test_ronda_completa_gestor_partida(self):
        from src.juego.validador_apuesta import Apuesta

        gestor = GestorPartida(num_jugadores=3, dados_por_jugador=5)
        # Mockear pintas de dados
        gestor.cachos[0].get_pintas_de_dados = Mock(
            return_value=[Pinta.TREN, Pinta.TREN, Pinta.AS, Pinta.QUINA, Pinta.CUADRA]
        )
        gestor.cachos[1].get_pintas_de_dados = Mock(
            return_value=[Pinta.TREN, Pinta.AS, Pinta.QUINA, Pinta.CUADRA, Pinta.SEXTO]
        )
        gestor.cachos[2].get_pintas_de_dados = Mock(
            return_value=[Pinta.TREN, Pinta.AS, Pinta.AS, Pinta.QUINA, Pinta.CUADRA]
        )

        # Jugador 0 apuesta: 2 trenes
        resultado = gestor.elegir_accion(
            0, {"tipo": "apuesta", "apuesta": Apuesta(2, Pinta.TREN)}
        )
        assert resultado["valida"] is True
        assert gestor.ultima_apuesta.get_cantidad() == 2
        assert gestor.ultima_apuesta.get_pinta() == Pinta.TREN

        # Jugador 1 sube: 3 trenes
        resultado = gestor.elegir_accion(
            1, {"tipo": "apuesta", "apuesta": Apuesta(3, Pinta.TREN)}
        )
        assert resultado["valida"] is True
        assert gestor.ultima_apuesta.get_cantidad() == 3
        assert gestor.ultima_apuesta.get_pinta() == Pinta.TREN

        # Jugador 2 sube: 3 quinas
        resultado = gestor.elegir_accion(
            2, {"tipo": "apuesta", "apuesta": Apuesta(3, Pinta.QUINA)}
        )
        assert resultado["valida"] is True
        assert gestor.ultima_apuesta.get_cantidad() == 3
        assert gestor.ultima_apuesta.get_pinta() == Pinta.QUINA

        # Jugador 0 duda la apuesta de jugador 2
        resultado = gestor.elegir_accion(0, {"tipo": "dudar"})
        assert resultado["resultado"] == "pierde_dudador"
        assert gestor.cachos[0].get_cantidad_dados() == 4
        assert gestor.cachos[1].get_cantidad_dados() == 5
        assert gestor.cachos[2].get_cantidad_dados() == 5
        assert gestor.arbitro.usar_ases_comodin is True
        # Después de dudar, la ronda termina y se agitan los dados
        assert gestor.ultima_apuesta is None
        assert gestor.ronda_actual == 1

        # Nueva ronda: Jugador 1 hace una nueva apuesta
        resultado = gestor.elegir_accion(
            1, {"tipo": "apuesta", "apuesta": Apuesta(2, Pinta.TREN)}
        )
        assert resultado["valida"] is True

        # Jugador 2 calza la nueva apuesta
        resultado = gestor.elegir_accion(2, {"tipo": "calzar"})
        assert resultado["resultado"] == "pierde_calzador"
        assert gestor.cachos[2].get_cantidad_dados() == 4

        # Verifica reglas especiales si algún jugador queda con un dado
        gestor.cachos[2].get_cantidad_dados = Mock(return_value=1)
        # Realiza una acción que debería gatillar la regla especial automáticamente
        resultado = gestor.elegir_accion(
            2, {"tipo": "apuesta", "apuesta": Apuesta(1, Pinta.AS)}
        )
        assert gestor.arbitro.usar_ases_comodin is False

    def test_gestor_tiene_metodos_para_ajustar_dados(self):
        gestor = GestorPartida(num_jugadores=2, dados_por_jugador=5)
        assert hasattr(gestor, "quitar_dado")
        assert hasattr(gestor, "agregar_dado")

    def test_quitar_dado_funciona(self):
        gestor = GestorPartida(num_jugadores=2, dados_por_jugador=5)
        cantidad_inicial = gestor.cachos[0].get_cantidad_dados()
        gestor.quitar_dado(0)
        cantidad_final = gestor.cachos[0].get_cantidad_dados()
        assert cantidad_final == cantidad_inicial - 1

    def test_agregar_dado_funciona(self):
        gestor = GestorPartida(num_jugadores=2, dados_por_jugador=5)
        gestor.quitar_dado(1)
        cantidad_inicial = gestor.cachos[1].get_cantidad_dados()
        gestor.agregar_dado(1)
        cantidad_final = gestor.cachos[1].get_cantidad_dados()
        assert cantidad_final == cantidad_inicial + 1

    def test_gestor_ajusta_dados_segun_resultado_arbitro(self):
        gestor = GestorPartida(num_jugadores=2, dados_por_jugador=5)
        gestor.arbitro.resolver_duda = Mock(return_value="pierde_dudador")
        gestor.quitar_dado = Mock()
        gestor.agregar_dado = Mock()
        resultado = gestor.arbitro.resolver_duda(gestor.cachos, (0, Pinta.TREN, 3))
        if resultado == "pierde_dudador":
            gestor.quitar_dado(0)
        elif resultado == "pierde_apostador":
            gestor.quitar_dado(1)
        elif resultado == "gana_calzador":
            gestor.agregar_dado(0)
        elif resultado == "pierde_calzador":
            gestor.quitar_dado(0)
        gestor.quitar_dado.assert_called_once_with(0)
        gestor.agregar_dado.assert_not_called()

    def test_inicializa_con_jugadores_y_cachos(self):
        gestor = GestorPartida(num_jugadores=3, dados_por_jugador=5)
        assert len(gestor.cachos) == 3
        for cacho in gestor.cachos:
            assert cacho.get_cantidad_dados() == 5
        assert hasattr(gestor.arbitro, "resolver_duda")

    def test_determina_quien_inicia_ronda(self):
        gestor = GestorPartida(num_jugadores=4, dados_por_jugador=5)
        jugador_inicial = gestor.determinar_jugador_inicial()
        assert 0 <= jugador_inicial < 4

    def test_maneja_flujo_de_turnos(self):
        gestor = GestorPartida(num_jugadores=3, dados_por_jugador=5)
        gestor.set_jugador_inicial(1)
        gestor.preguntar_jugada = Mock()
        turnos = []
        for _ in range(6):
            jugador = gestor.siguiente_jugador()
            turnos.append(jugador)
            gestor.preguntar_jugada(jugador)
        assert turnos == [2, 0, 1, 2, 0, 1]
        gestor.preguntar_jugada.assert_has_calls(
            [call(2), call(0), call(1), call(2), call(0), call(1)]
        )

    def test_detecta_jugador_con_un_dado(self):
        gestor = GestorPartida(num_jugadores=3, dados_por_jugador=5)
        gestor.cachos[0].get_cantidad_dados = Mock(return_value=1)
        assert gestor.jugadores_con_un_dado() == [0]
        gestor.cachos[1].get_cantidad_dados = Mock(return_value=1)
        assert set(gestor.jugadores_con_un_dado()) == {0, 1}

    def test_arbitro_activa_regla_especial(self):
        gestor = GestorPartida(num_jugadores=2, dados_por_jugador=5)
        gestor.cachos[0].get_cantidad_dados = Mock(return_value=1)
        gestor.activar_regla_especial()
        assert gestor.arbitro.usar_ases_comodin is False
        gestor.cachos[0].get_cantidad_dados = Mock(return_value=5)
        gestor.cachos[1].get_cantidad_dados = Mock(return_value=5)
        gestor.desactivar_regla_especial()
        assert gestor.arbitro.usar_ases_comodin is True

    def test_dados_a_favor_cuando_gana_calzador_con_5_dados(self):
        """Test que verifica que cuando un jugador con 5 dados gana al calzar,
        recibe un dado a favor en lugar de un sexto dado en juego"""
        gestor = GestorPartida(num_jugadores=2, dados_por_jugador=5)
        assert gestor.jugadores[0].dados_a_favor == 0
        # Simular que el jugador gana al calzar
        gestor.agregar_dado(0)
        # Como ya tiene 5 dados, debe recibir un dado a favor
        assert gestor.cachos[0].get_cantidad_dados() == 5
        assert gestor.jugadores[0].dados_a_favor == 1

    def test_dados_a_favor_se_usan_antes_de_perder_dados_del_cacho(self):
        """Test que verifica que cuando un jugador pierde un dado y tiene dados a favor,
        usa el dado a favor primero antes de perder un dado del cacho"""
        gestor = GestorPartida(num_jugadores=2, dados_por_jugador=5)
        # Dar un dado a favor al jugador 0
        gestor.jugadores[0].dados_a_favor = 1
        cantidad_inicial = gestor.cachos[0].get_cantidad_dados()
        # Quitar un dado
        gestor.quitar_dado(0)
        # Debe usar el dado a favor y mantener los 5 dados del cacho
        assert gestor.cachos[0].get_cantidad_dados() == cantidad_inicial
        assert gestor.jugadores[0].dados_a_favor == 0

    def test_quitar_dado_del_cacho_cuando_no_hay_dados_a_favor(self):
        """Test que verifica que cuando un jugador no tiene dados a favor,
        pierde un dado del cacho directamente"""
        gestor = GestorPartida(num_jugadores=2, dados_por_jugador=5)
        assert gestor.jugadores[0].dados_a_favor == 0
        cantidad_inicial = gestor.cachos[0].get_cantidad_dados()
        gestor.quitar_dado(0)
        # Debe perder un dado del cacho
        assert gestor.cachos[0].get_cantidad_dados() == cantidad_inicial - 1
        assert gestor.jugadores[0].dados_a_favor == 0

    def test_agregar_dado_cuando_tiene_menos_de_5(self):
        """Test que verifica que cuando un jugador tiene menos de 5 dados,
        recibe el dado directamente en el cacho"""
        gestor = GestorPartida(num_jugadores=2, dados_por_jugador=5)
        # Primero quitamos un dado para tener menos de 5
        gestor.quitar_dado(0)
        cantidad_inicial = gestor.cachos[0].get_cantidad_dados()
        gestor.agregar_dado(0)
        # Debe recibir el dado en el cacho
        assert gestor.cachos[0].get_cantidad_dados() == cantidad_inicial + 1
        assert gestor.jugadores[0].dados_a_favor == 0
