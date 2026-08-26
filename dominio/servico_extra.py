class ServicoExtra:

    def __init__(
        self,
        id,
        nome,
        valor
    ):
        self._id = id
        self._nome = nome
        self._valor = valor

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @property
    def descricao(self):
        return self._nome

    @property
    def valor(self):
        return self._valor

    def __str__(self):

        return (
            f"{self.nome} - "
            f"R$ {self.valor:.2f}"
        )