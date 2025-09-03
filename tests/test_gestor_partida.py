from unittest.mock import Mock, call, patch

import pytest

from src.juego.dado import *
from src.juego.gestor_partida import *


class TestGestorPartida:

    def test_ronda_completa_gestor_partida(self):
        """Test que simula una ronda completa con apuesta, duda y resolución"""
        gestor = GestorPartida(num_jugadores=2)

        # Simular una apuesta válida
        apuesta = Apuesta(2, Pinta.TREN)
        resultado = gestor.elegir_accion(0, {"tipo": "apuesta", "apuesta": apuesta})
        assert resultado["valida"] is True
        assert gestor.ultima_apuesta == apuesta

        # Siguiente jugador duda
        with patch.object(gestor.arbitro, "resolver_duda") as mock_resolver:
            mock_resolver.return_value = "pierde_dudador"
            resultado = gestor.elegir_accion(1, {"tipo": "dudar"})
            assert resultado["resultado"] == "pierde_dudador"
            mock_resolver.assert_called_once()

    def test_partida_completa(self):
        """
        Simula una partida completa con 2 jugadores, varias rondas,
        donde siempre se apuesta y el siguiente jugador duda.
        La partida termina cuando hay un ganador.
        """
        gestor = GestorPartida(num_jugadores=2, dados_por_jugador=2)

        # Mockeamos el árbitro y el validador
        with patch.object(
            gestor.arbitro, "resolver_duda", return_value="pierde_dudador"
        ), patch(
            "src.juego.validador_apuesta.ValidadorApuesta.es_valida", return_value=True
        ):

            # Mientras no haya ganador
            while not gestor.hay_ganador():
                jugador_actual = gestor.jugador_actual

                # El jugador actual hace apuesta mínima
                apuesta = Apuesta(1, Pinta.AS)
                resultado_apuesta = gestor.elegir_accion(
                    jugador_actual, {"tipo": "apuesta", "apuesta": apuesta}
                )

                # Comprobamos que la apuesta fue considerada válida
                assert resultado_apuesta["valida"] is True

                # Siguiente jugador duda
                siguiente = gestor.siguiente_jugador()
                resultado_duda = gestor.elegir_accion(siguiente, {"tipo": "dudar"})
                assert resultado_duda["resultado"] == "pierde_dudador"

        # Al final debe haber un ganador
        assert gestor.hay_ganador() is True
        ganador = gestor.obtener_ganador()
        assert ganador in [j.nombre for j in gestor.jugadores]

    def test_inicializa_con_jugadores_y_cachos(self):
        """Test que verifica la inicialización correcta del gestor"""
        gestor = GestorPartida(num_jugadores=3, dados_por_jugador=5)
        assert len(gestor.jugadores) == 3
        assert len(gestor.cachos) == 3
        assert all(j.cacho.get_cantidad_dados() == 5 for j in gestor.jugadores)
        assert all(j.activo for j in gestor.jugadores)
        assert all(j.dados_a_favor == 0 for j in gestor.jugadores)

    def test_jugador_pierde(self):
        """Test que verifica cuando un jugador pierde un dado"""
        gestor = GestorPartida(num_jugadores=2)
        dados_iniciales = gestor.jugadores[0].cacho.get_cantidad_dados()

        gestor.quitar_dado(0)
        assert gestor.jugadores[0].cacho.get_cantidad_dados() == dados_iniciales - 1

    def test_jugador_gana(self):
        """Test que verifica cuando un jugador gana un dado"""
        gestor = GestorPartida(num_jugadores=2)
        dados_iniciales = gestor.jugadores[0].cacho.get_cantidad_dados()

        # Si tiene menos de 5 dados, lo agrega al cacho
        gestor.quitar_dado(0)  # Primero quitar uno
        gestor.agregar_dado(0)  # Luego agregar uno
        assert gestor.jugadores[0].cacho.get_cantidad_dados() == dados_iniciales

    def test_determina_quien_inicia_ronda(self):
        """Test que verifica la determinación del jugador inicial"""
        gestor = GestorPartida(num_jugadores=3)
        with patch.object(gestor.generador, "generar_entero") as mock_gen:
            mock_gen.return_value = 1
            jugador_inicial = gestor.determinar_jugador_inicial()
            assert jugador_inicial == 1
            mock_gen.assert_called_once_with(0, 2)

    def test_maneja_flujo_de_turnos(self):
        """Test que verifica el manejo del flujo de turnos"""
        gestor = GestorPartida(num_jugadores=3)
        gestor.set_jugador_inicial(0)
        assert gestor.jugador_actual == 0

        siguiente = gestor.siguiente_jugador()
        assert siguiente == 1
        assert gestor.jugador_actual == 1

        siguiente = gestor.siguiente_jugador()
        assert siguiente == 2

        # Debe volver al jugador 0
        siguiente = gestor.siguiente_jugador()
        assert siguiente == 0

    def test_detecta_jugador_con_un_dado(self):
        """Test que verifica la detección de jugadores con un solo dado"""
        gestor = GestorPartida(num_jugadores=2)

        # Reducir dados del jugador 0 hasta tener solo 1
        while gestor.jugadores[0].cacho.get_cantidad_dados() > 1:
            gestor.jugadores[0].cacho.eliminar_dado()

        jugadores_un_dado = gestor.jugadores_con_un_dado()
        assert 0 in jugadores_un_dado
        assert 1 not in jugadores_un_dado

    def test_arbitro_activa_regla_especial(self):
        """Test que verifica la activación de la regla especial cuando hay un jugador con un dado"""
        gestor = GestorPartida(num_jugadores=2)

        # Inicialmente ases son comodines
        assert gestor.arbitro.usar_ases_comodin is True

        # Reducir dados del jugador 0 hasta tener solo 1
        while gestor.jugadores[0].cacho.get_cantidad_dados() > 1:
            gestor.jugadores[0].cacho.eliminar_dado()

        # Llamar al método que actualiza la regla especial
        gestor._actualizar_regla_especial()

        # Ahora ases no deben ser comodines
        assert gestor.arbitro.usar_ases_comodin is False

    def test_dados_a_favor_cuando_gana_calzador_con_5_dados(self):
        """Test que verifica que cuando un jugador con 5 dados gana al calzar,
        recibe un dado a favor en lugar de un sexto dado en juego"""
        gestor = GestorPartida(num_jugadores=2)

        # Asegurar que el jugador tiene 5 dados
        assert gestor.jugadores[0].cacho.get_cantidad_dados() == 5
        assert gestor.jugadores[0].dados_a_favor == 0

        # Agregar un dado (debería ir a dados_a_favor)
        gestor.agregar_dado(0)

        assert gestor.jugadores[0].cacho.get_cantidad_dados() == 5
        assert gestor.jugadores[0].dados_a_favor == 1

    def test_dados_a_favor_se_usan_antes_de_perder_dados_del_cacho(self):
        """Test que verifica que cuando un jugador pierde un dado y tiene dados a favor,
        usa el dado a favor primero antes de perder un dado del cacho"""
        gestor = GestorPartida(num_jugadores=2)

        # Dar al jugador un dado a favor
        gestor.jugadores[0].dados_a_favor = 2
        dados_iniciales = gestor.jugadores[0].cacho.get_cantidad_dados()

        # Quitar un dado
        gestor.quitar_dado(0)

        # Debe usar el dado a favor, no del cacho
        assert gestor.jugadores[0].dados_a_favor == 1
        assert gestor.jugadores[0].cacho.get_cantidad_dados() == dados_iniciales

    def test_quitar_dado_del_cacho_cuando_no_hay_dados_a_favor(self):
        """Test que verifica que cuando un jugador no tiene dados a favor,
        pierde un dado del cacho directamente"""
        gestor = GestorPartida(num_jugadores=2)

        dados_iniciales = gestor.jugadores[0].cacho.get_cantidad_dados()
        assert gestor.jugadores[0].dados_a_favor == 0

        # Quitar un dado
        gestor.quitar_dado(0)

        # Debe quitar del cacho
        assert gestor.jugadores[0].dados_a_favor == 0
        assert gestor.jugadores[0].cacho.get_cantidad_dados() == dados_iniciales - 1

    def test_agregar_dado_cuando_tiene_menos_de_5(self):
        """Test que verifica que cuando un jugador tiene menos de 5 dados,
        recibe el dado directamente en el cacho"""
        gestor = GestorPartida(num_jugadores=2)

        # Quitar un dado primero
        gestor.quitar_dado(0)
        dados_actuales = gestor.jugadores[0].cacho.get_cantidad_dados()
        assert dados_actuales < 5

        # Agregar un dado
        gestor.agregar_dado(0)

        # Debe agregarse al cacho
        assert gestor.jugadores[0].cacho.get_cantidad_dados() == dados_actuales + 1
        assert gestor.jugadores[0].dados_a_favor == 0

    def test_nueva_ronda_agita_cachos_y_resetea_apuesta(self):
        """Test que verifica que una nueva ronda agita los cachos y resetea la última apuesta"""
        gestor = GestorPartida(num_jugadores=2)

        # Establecer una apuesta
        gestor.ultima_apuesta = Apuesta(2, Pinta.TREN)
        ronda_inicial = gestor.ronda_actual

        with patch.object(gestor, "agitar_cachos") as mock_agitar:
            gestor.nueva_ronda()

            assert gestor.ronda_actual == ronda_inicial + 1
            assert gestor.ultima_apuesta is None
            mock_agitar.assert_called_once()

    def test_hay_ganador_cuando_solo_un_jugador_activo(self):
        """Test que verifica la detección de ganador"""
        gestor = GestorPartida(num_jugadores=2)

        # Inicialmente no hay ganador
        assert gestor.hay_ganador() is False
        assert gestor.obtener_ganador() is None

        # Desactivar un jugador
        gestor.jugadores[1].activo = False

        # Ahora debe haber ganador
        assert gestor.hay_ganador() is True
        assert gestor.obtener_ganador() == "Jugador 1"

    def test_jugador_se_desactiva_cuando_pierde_todos_los_dados(self):
        """Test que verifica que un jugador se desactiva al perder todos sus dados"""
        gestor = GestorPartida(num_jugadores=2)

        # Quitar todos los dados del jugador 0
        while gestor.jugadores[0].cacho.get_cantidad_dados() > 0:
            gestor.quitar_dado(0)

        assert gestor.jugadores[0].activo is False
        assert gestor.jugadores[0].cacho.get_cantidad_dados() == 0

    def test_validar_apuesta_invalida(self):
        """Test que verifica el manejo de apuestas inválidas"""
        gestor = GestorPartida(num_jugadores=2)

        # Primera apuesta válida
        apuesta1 = Apuesta(2, Pinta.TREN)
        resultado1 = gestor.elegir_accion(0, {"tipo": "apuesta", "apuesta": apuesta1})
        assert resultado1["valida"] is True

        # Apuesta inválida (menor cantidad y misma pinta)
        apuesta2 = Apuesta(1, Pinta.TREN)
        resultado2 = gestor.elegir_accion(1, {"tipo": "apuesta", "apuesta": apuesta2})
        assert resultado2["valida"] is False

        # La última apuesta no debe cambiar
        assert gestor.ultima_apuesta == apuesta1

    def test_calzar_exitoso(self):
        """Test que verifica el calzar exitoso"""
        gestor = GestorPartida(num_jugadores=2)

        # Establecer una apuesta
        apuesta = Apuesta(2, Pinta.TREN)
        gestor.ultima_apuesta = apuesta
        dados_iniciales = gestor.jugadores[0].cacho.get_cantidad_dados()

        with patch.object(gestor.arbitro, "resolver_calzar") as mock_resolver:
            mock_resolver.return_value = "gana_calzador"
            resultado = gestor.elegir_accion(0, {"tipo": "calzar"})

            assert resultado["resultado"] == "gana_calzador"
            # Debe ganar un dado
            assert (
                gestor.jugadores[0].cacho.get_cantidad_dados() == dados_iniciales + 1
                or gestor.jugadores[0].dados_a_favor > 0
            )

    # Tests específicos para elegir_accion
    def test_elegir_accion_apuesta_valida(self):
        """Test que verifica el método elegir_accion con apuesta válida"""
        gestor = GestorPartida(num_jugadores=2)
        apuesta = Apuesta(2, Pinta.TREN)

        resultado = gestor.elegir_accion(0, {"tipo": "apuesta", "apuesta": apuesta})

        assert resultado["valida"] is True
        assert gestor.ultima_apuesta == apuesta

    def test_elegir_accion_apuesta_invalida(self):
        """Test que verifica el método elegir_accion con apuesta inválida"""
        gestor = GestorPartida(num_jugadores=2)

        # Primera apuesta
        apuesta1 = Apuesta(3, Pinta.TREN)
        gestor.elegir_accion(0, {"tipo": "apuesta", "apuesta": apuesta1})

        # Apuesta inválida (menor cantidad)
        apuesta2 = Apuesta(2, Pinta.TREN)
        resultado = gestor.elegir_accion(1, {"tipo": "apuesta", "apuesta": apuesta2})

        assert resultado["valida"] is False
        assert gestor.ultima_apuesta == apuesta1  # No debe cambiar

    def test_elegir_accion_dudar_pierde_dudador(self):
        """Test que verifica elegir_accion con duda donde pierde el dudador"""
        gestor = GestorPartida(num_jugadores=2)

        # Establecer una apuesta
        apuesta = Apuesta(2, Pinta.TREN)
        gestor.ultima_apuesta = apuesta
        dados_iniciales = gestor.jugadores[1].cacho.get_cantidad_dados()

        with patch.object(
            gestor.arbitro, "resolver_duda"
        ) as mock_resolver, patch.object(gestor, "_finalizar_ronda") as mock_finalizar:

            mock_resolver.return_value = "pierde_dudador"
            resultado = gestor.elegir_accion(1, {"tipo": "dudar"})

            assert resultado["resultado"] == "pierde_dudador"
            # El dudador (jugador 1) debe perder un dado
            assert gestor.jugadores[1].cacho.get_cantidad_dados() == dados_iniciales - 1
            mock_resolver.assert_called_once()
            mock_finalizar.assert_called_once()

    def test_elegir_accion_dudar_pierde_apostador(self):
        """Test que verifica elegir_accion con duda donde pierde el apostador"""
        gestor = GestorPartida(num_jugadores=2)

        # Establecer una apuesta
        apuesta = Apuesta(2, Pinta.TREN)
        gestor.ultima_apuesta = apuesta
        dados_iniciales_apostador = gestor.jugadores[0].cacho.get_cantidad_dados()
        dados_iniciales_dudador = gestor.jugadores[1].cacho.get_cantidad_dados()

        with patch.object(
            gestor.arbitro, "resolver_duda"
        ) as mock_resolver, patch.object(gestor, "_finalizar_ronda") as mock_finalizar:

            mock_resolver.return_value = "pierde_apostador"
            resultado = gestor.elegir_accion(1, {"tipo": "dudar"})

            assert resultado["resultado"] == "pierde_apostador"
            # El apostador (jugador 0) debe perder un dado
            assert (
                gestor.jugadores[0].cacho.get_cantidad_dados()
                == dados_iniciales_apostador - 1
            )
            # El dudador no debe perder dados
            assert (
                gestor.jugadores[1].cacho.get_cantidad_dados()
                == dados_iniciales_dudador
            )
            mock_resolver.assert_called_once()
            mock_finalizar.assert_called_once()

    def test_elegir_accion_calzar_gana_calzador(self):
        """Test que verifica elegir_accion con calzar exitoso"""
        gestor = GestorPartida(num_jugadores=2)

        # Establecer una apuesta
        apuesta = Apuesta(2, Pinta.TREN)
        gestor.ultima_apuesta = apuesta
        dados_iniciales = gestor.jugadores[0].cacho.get_cantidad_dados()
        dados_favor_iniciales = gestor.jugadores[0].dados_a_favor

        with patch.object(
            gestor.arbitro, "resolver_calzar"
        ) as mock_resolver, patch.object(gestor, "_finalizar_ronda") as mock_finalizar:

            mock_resolver.return_value = "gana_calzador"
            resultado = gestor.elegir_accion(0, {"tipo": "calzar"})

            assert resultado["resultado"] == "gana_calzador"
            # Debe ganar un dado (en cacho o a favor)
            total_dados_final = (
                gestor.jugadores[0].cacho.get_cantidad_dados()
                + gestor.jugadores[0].dados_a_favor
            )
            total_dados_inicial = dados_iniciales + dados_favor_iniciales
            assert total_dados_final == total_dados_inicial + 1
            mock_resolver.assert_called_once()
            mock_finalizar.assert_called_once()

    def test_elegir_accion_calzar_pierde_calzador(self):
        """Test que verifica elegir_accion con calzar fallido"""
        gestor = GestorPartida(num_jugadores=2)

        # Establecer una apuesta
        apuesta = Apuesta(2, Pinta.TREN)
        gestor.ultima_apuesta = apuesta
        dados_iniciales = gestor.jugadores[0].cacho.get_cantidad_dados()

        with patch.object(
            gestor.arbitro, "resolver_calzar"
        ) as mock_resolver, patch.object(gestor, "_finalizar_ronda") as mock_finalizar:

            mock_resolver.return_value = "pierde_calzador"
            resultado = gestor.elegir_accion(0, {"tipo": "calzar"})

            assert resultado["resultado"] == "pierde_calzador"
            # Debe perder un dado
            assert gestor.jugadores[0].cacho.get_cantidad_dados() == dados_iniciales - 1
            mock_resolver.assert_called_once()
            mock_finalizar.assert_called_once()

    def test_elegir_accion_calzar_no_se_puede_calzar(self):
        """Test que verifica elegir_accion cuando no se puede calzar"""
        gestor = GestorPartida(num_jugadores=2)

        # Establecer una apuesta
        apuesta = Apuesta(2, Pinta.TREN)
        gestor.ultima_apuesta = apuesta
        dados_iniciales = gestor.jugadores[0].cacho.get_cantidad_dados()

        with patch.object(
            gestor.arbitro, "resolver_calzar"
        ) as mock_resolver, patch.object(gestor, "_finalizar_ronda") as mock_finalizar:

            mock_resolver.return_value = "no_se_puede_calzar"
            resultado = gestor.elegir_accion(0, {"tipo": "calzar"})

            assert resultado["resultado"] == "no_se_puede_calzar"
            # No debe cambiar la cantidad de dados
            assert gestor.jugadores[0].cacho.get_cantidad_dados() == dados_iniciales
            mock_resolver.assert_called_once()
            mock_finalizar.assert_called_once()

    def test_elegir_accion_actualiza_regla_especial_cuando_es_necesario(self):
        """Test que verifica que elegir_accion actualiza la regla especial cuando es necesario"""
        gestor = GestorPartida(num_jugadores=2)

        # Reducir dados del jugador 0 hasta tener solo 1
        while gestor.jugadores[0].cacho.get_cantidad_dados() > 1:
            gestor.jugadores[0].cacho.eliminar_dado()

        # Verificar que inicialmente los ases son comodines
        assert gestor.arbitro.usar_ases_comodin is True

        # Hacer una apuesta que debería activar la regla especial
        apuesta = Apuesta(1, Pinta.TREN)

        with patch.object(
            gestor, "_debe_actualizar_regla_especial"
        ) as mock_debe_actualizar, patch.object(
            gestor, "_actualizar_regla_especial"
        ) as mock_actualizar:

            mock_debe_actualizar.return_value = True
            gestor.elegir_accion(0, {"tipo": "apuesta", "apuesta": apuesta})

            mock_debe_actualizar.assert_called_once()
            mock_actualizar.assert_called_once()

    def test_elegir_accion_no_actualiza_regla_especial_cuando_no_es_necesario(self):
        """Test que verifica que elegir_accion no actualiza la regla especial innecesariamente"""
        gestor = GestorPartida(num_jugadores=2)

        apuesta = Apuesta(2, Pinta.TREN)

        with patch.object(
            gestor, "_debe_actualizar_regla_especial"
        ) as mock_debe_actualizar, patch.object(
            gestor, "_actualizar_regla_especial"
        ) as mock_actualizar:

            mock_debe_actualizar.return_value = False
            gestor.elegir_accion(0, {"tipo": "apuesta", "apuesta": apuesta})

            mock_debe_actualizar.assert_called_once()
            mock_actualizar.assert_not_called()

    def test_elegir_accion_tipo_no_reconocido(self):
        """Test que verifica el comportamiento con un tipo de acción no reconocido"""
        gestor = GestorPartida(num_jugadores=2)

        resultado = gestor.elegir_accion(0, {"tipo": "accion_inexistente"})

        # Debe retornar un diccionario vacío
        assert isinstance(resultado, dict)
        assert len(resultado) == 0
