from src.juego.dado import Pinta


class Apuesta:
    def __init__(self, cantidad_pintas: int, pinta: Pinta):
        if cantidad_pintas <= 0:
            raise ValueError("La cantidad de pintas debe ser mayor que 0")
        self.__cantidad_pintas = cantidad_pintas
        self.__pinta = pinta

    def get_cantidad(self):
        return self.__cantidad_pintas

    def get_pinta(self):
        return self.__pinta


class ValidadorApuesta:
    @staticmethod
    def es_valida(
        apuesta_anterior: Apuesta, nueva_apuesta: Apuesta, cantidad_dados: int = 5
    ):
        """
        Verifica si la nueva apuesta es válida según las reglas.
        """
        if cantidad_dados < 1:
            return False
        """Para la primera apuesta"""
        if apuesta_anterior is None:
            if nueva_apuesta.get_pinta() == Pinta.AS and cantidad_dados > 1:
                return False
            return True

        """Regla normal: mayor cantidad misma pinta"""
        if (
            nueva_apuesta.get_cantidad() > apuesta_anterior.get_cantidad()
            and nueva_apuesta.get_pinta().value == apuesta_anterior.get_pinta().value
        ):
            return True

        """Regla normal: misma cantidad pero pinta mayor"""
        if (
            nueva_apuesta.get_cantidad() == apuesta_anterior.get_cantidad()
            and nueva_apuesta.get_pinta().value > apuesta_anterior.get_pinta().value
        ):
            return True

        """Reglas de los ases: Cambiar de cualquier pinta a ASES"""
        if (nueva_apuesta.get_pinta() == Pinta.AS) and (
            apuesta_anterior.get_pinta() != Pinta.AS
        ):
            if (
                apuesta_anterior.get_cantidad() % 2 == 0
                and nueva_apuesta.get_cantidad()
                == (apuesta_anterior.get_cantidad() / 2) + 1
            ):
                return True
            elif (
                apuesta_anterior.get_cantidad() % 2 == 1
                and nueva_apuesta.get_cantidad()
                == (apuesta_anterior.get_cantidad() // 2) + 1
            ):
                return True

        """Reglas de los ases: Cambiar de ASES a pinta mayor"""
        if (nueva_apuesta.get_pinta() != Pinta.AS) and (
            apuesta_anterior.get_pinta() == Pinta.AS
        ):
            if (
                nueva_apuesta.get_cantidad()
                >= (apuesta_anterior.get_cantidad() * 2) + 1
            ):
                return True

        return False
