from src.juego.arbitro_ronda import ArbitroRonda
from src.juego.cacho import Cacho
from src.juego.dado import Pinta
from src.juego.validador_apuesta import Apuesta, ValidadorApuesta
from src.servicios.generador_aleatorio import GeneradorAleatorio


class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.cacho = Cacho()
        self.dados_a_favor = 0
        self.activo = True


class GestorPartida:
    def __init__(self, num_jugadores=3, dados_por_jugador=5):
        self.jugadores = [Jugador(f"Jugador {i + 1}") for i in range(num_jugadores)]
        # Ajustar la cantidad de dados si es diferente a 5
        if dados_por_jugador != 5:
            for jugador in self.jugadores:
                # Quitar dados extras o agregar dados faltantes
                while jugador.cacho.get_cantidad_dados() > dados_por_jugador:
                    jugador.cacho.eliminar_dado()
                while jugador.cacho.get_cantidad_dados() < dados_por_jugador:
                    jugador.cacho.agregar_dado()
        self.arbitro = ArbitroRonda()
        self.ultima_apuesta = None
        self.num_jugadores = num_jugadores
        self.jugador_actual = 0
        self.generador = GeneradorAleatorio()
        self.ronda_actual = 0

    @property
    def cachos(self):
        """Retorna una lista de los cachos de todos los jugadores"""
        return [jugador.cacho for jugador in self.jugadores]

    def elegir_accion(self, jugador, accion):
        tipo = accion.get("tipo")
        resultado = {}
        if tipo == "apuesta":
            apuesta = accion["apuesta"]
            valida = ValidadorApuesta.es_valida(
                self.ultima_apuesta,
                apuesta,
                self.jugadores[jugador].cacho.get_cantidad_dados(),
            )
            if valida:
                self.ultima_apuesta = apuesta
            resultado["valida"] = valida
        elif tipo == "dudar":
            idx_apostador = (jugador - 1) % self.num_jugadores
            pinta = self.ultima_apuesta.get_pinta()
            cantidad = self.ultima_apuesta.get_cantidad()
            res = self.arbitro.resolver_duda(
                self.cachos, (idx_apostador, pinta, cantidad)
            )
            resultado["resultado"] = res
            if res == "pierde_dudador":
                self.quitar_dado(jugador)
            else:
                self.quitar_dado(idx_apostador)
            # Después de dudar, se termina la ronda y se agitan los dados
            self._finalizar_ronda()
        elif tipo == "calzar":
            pinta = self.ultima_apuesta.get_pinta()
            cantidad = self.ultima_apuesta.get_cantidad()
            res = self.arbitro.resolver_calzar(self.cachos, (jugador, pinta, cantidad))
            resultado["resultado"] = res
            if res == "gana_calzador":
                self.agregar_dado(jugador)
            elif res == "pierde_calzador":
                self.quitar_dado(jugador)
            # Después de calzar, se termina la ronda y se agitan los dados
            self._finalizar_ronda()
        # Activar/desactivar regla especial solo si es necesario
        if self._debe_actualizar_regla_especial():
            self._actualizar_regla_especial()
        return resultado

    def _debe_actualizar_regla_especial(self):
        # Solo actualiza si hay cambio en la cantidad de dados de algún jugador
        # o si la condición de tener un dado cambia
        jugadores_con_un_dado = [
            cacho.get_cantidad_dados() == 1 for cacho in self.cachos
        ]
        return any(jugadores_con_un_dado) != (self.arbitro.usar_ases_comodin is False)

    def _actualizar_regla_especial(self):
        # Si algún jugador tiene solo un dado, ases dejan de ser comodines
        for cacho in self.cachos:
            if cacho.get_cantidad_dados() == 1:
                self.arbitro.set_ases_comodin(False)
                return
        self.arbitro.set_ases_comodin(True)

    def quitar_dado(self, jugador):
        # Si tiene dados a favor, usa uno de ellos en lugar de perder un dado del cacho
        if self.jugadores[jugador].dados_a_favor > 0:
            self.jugadores[jugador].dados_a_favor -= 1
        else:
            self.jugadores[jugador].cacho.eliminar_dado()
            # Si se queda sin dados, el jugador sale del juego
            if self.jugadores[jugador].cacho.get_cantidad_dados() == 0:
                self.jugadores[jugador].activo = False

    def agregar_dado(self, jugador):
        # Si ya tiene 5 dados en juego, guarda el dado extra como "a favor"
        if self.jugadores[jugador].cacho.get_cantidad_dados() < 5:
            self.jugadores[jugador].cacho.agregar_dado()
        else:
            self.jugadores[jugador].dados_a_favor += 1

    def activar_regla_especial(self):
        # Si algún jugador tiene solo un dado, ases dejan de ser comodines
        for cacho in self.cachos:
            if cacho.get_cantidad_dados() == 1:
                self.arbitro.set_ases_comodin(False)
                return
        self.arbitro.set_ases_comodin(True)

    def desactivar_regla_especial(self):
        self.arbitro.set_ases_comodin(True)

    def determinar_jugador_inicial(self):
        return self.generador.generar_entero(0, self.num_jugadores - 1)

    def set_jugador_inicial(self, jugador):
        self.jugador_actual = jugador

    def siguiente_jugador(self):
        jugador = (self.jugador_actual + 1) % self.num_jugadores
        self.jugador_actual = jugador
        return jugador

    def preguntar_jugada(self, jugador):
        # Método placeholder para la interfaz
        pass

    def jugadores_con_un_dado(self):
        return [
            i
            for i, jugador in enumerate(self.jugadores)
            if jugador.cacho.get_cantidad_dados() == 1
        ]

    def agitar_cachos(self):
        """Agita todos los cachos de los jugadores activos"""
        for jugador in self.jugadores:
            if jugador.activo:
                jugador.cacho.agitar()

    def nueva_ronda(self):
        """Inicia una nueva ronda agitando todos los cachos"""
        self.ronda_actual += 1
        self.agitar_cachos()
        self.ultima_apuesta = None

    def _finalizar_ronda(self):
        """Finaliza la ronda actual y prepara la siguiente"""
        if not self.hay_ganador():
            self.nueva_ronda()

    def jugadores_activos(self):
        """Retorna la lista de jugadores que aún están en el juego"""
        return [i for i, jugador in enumerate(self.jugadores) if jugador.activo]

    def hay_ganador(self):
        """Verifica si hay un ganador (solo un jugador activo)"""
        activos = self.jugadores_activos()
        return len(activos) == 1

    def obtener_ganador(self):
        """Retorna el nombre del ganador si lo hay"""
        if self.hay_ganador():
            activos = self.jugadores_activos()
            return self.jugadores[activos[0]].nombre
        return None
