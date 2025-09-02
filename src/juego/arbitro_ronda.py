from src.juego.contador_pintas import ContadorPintas


class ArbitroRonda:
    def __init__(self):
        self.contador = ContadorPintas()
        self.usar_ases_comodin = True  # Por defecto, ases son comodines

    def set_ases_comodin(self, valor: bool):
        self.usar_ases_comodin = valor

    def resolver_duda(self, cachos, jugada):
        _, pinta, cantidad = jugada
        total = self.contador.contar(cachos, pinta, ases_comodin=self.usar_ases_comodin)
        if total >= cantidad:
            return "pierde_dudador"
        else:
            return "pierde_apostador"

    def resolver_calzar(self, cachos, jugada):
        jugador_idx, pinta, cantidad = jugada
        total = self.contador.contar(cachos, pinta, ases_comodin=self.usar_ases_comodin)
        dados_en_juego = sum(len(c.get_pintas_de_dados() or []) for c in cachos)
        total_dados = dados_en_juego
        jugador_dados = len(cachos[jugador_idx].get_pintas_de_dados() or [])
        if not self.puede_calzar(total_dados, dados_en_juego, jugador_dados):
            return "no_se_puede_calzar"
        if total == cantidad:
            return "gana_calzador"
        else:
            return "pierde_calzador"

    def puede_calzar(self, total_dados, dados_en_juego, jugador_dados):
        return dados_en_juego >= total_dados / 2 or jugador_dados == 1
