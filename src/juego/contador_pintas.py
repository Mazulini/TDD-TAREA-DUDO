from src.juego.dado import Pinta


class ContadorPintas:
    def contar(self, cachos, pinta_objetivo, ases_comodin=True):
        dados = []
        for cacho in cachos:
            pintas = cacho.get_pintas_de_dados()
            if pintas is None:
                if hasattr(cacho, "set_visible"):
                    cacho.set_visible()
                    pintas = cacho.get_pintas_de_dados()
            if pintas:
                dados.extend(pintas)
        # Contar pintas
        if ases_comodin and pinta_objetivo != Pinta.AS:
            return sum(1 for p in dados if p == pinta_objetivo or p == Pinta.AS)
        else:
            return sum(1 for p in dados if p == pinta_objetivo)
