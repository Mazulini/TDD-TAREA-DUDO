from src.juego.dado import Dado


class Cacho:
    def __init__(self, cantidad_dados=5):
        """
        Inicializa un cacho con una lista de dados.
        Por defecto se crean 5 dados.
        """
        self.max_cantidad_dados = cantidad_dados
        self.__dados = [Dado() for _ in range(cantidad_dados)]
        self.__cantidad_dados = len(self.__dados)
        self.__visibilidad = False

    def get_pintas_de_dados(self):
        """
        Retorna la lista de pintas de los dados si la visibilidad está activada.
        """
        if self.__visibilidad:
            return [dado.show() for dado in self.__dados]
        return None

    def agitar(self):
        """Regenera los valores de todos los dados."""
        self.__dados = [Dado() for _ in range(self.__cantidad_dados)]

    def get_cantidad_dados(self):
        """Retorna la cantidad de dados en el cacho."""
        return self.__cantidad_dados

    def set_visible(self):
        """Hace visibles las pintas de los dados."""
        self.__visibilidad = True

    def set_oculto(self):
        """Oculta las pintas de los dados."""
        self.__visibilidad = False

    def get_visibilidad(self):
        """Retorna el estado de visibilidad de los dados."""
        return self.__visibilidad

    def agregar_dado(self, dado=None):
        """Agrega un dado al cacho."""
        if dado is None:
            dado = Dado()
        if self.__cantidad_dados < self.max_cantidad_dados:
            self.__dados.append(dado)
            self.__cantidad_dados = len(self.__dados)

    def eliminar_dado(self):
        """Elimina el último dado si hay al menos uno."""
        if self.__cantidad_dados > 0:
            self.__dados.pop()
            self.__cantidad_dados = len(self.__dados)
