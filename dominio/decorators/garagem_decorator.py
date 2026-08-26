from dominio.decorators.servico_reserva_decorator import ServicoReservaDecorator


class GaragemDecorator(ServicoReservaDecorator):

    def __init__(self, servico, servico_extra):
        super().__init__(servico)
        self._servico_extra = servico_extra

    def get_descricao(self):
        return (
            self._componente.get_descricao()
            + f", {self._servico_extra.descricao}"
        )

    def get_valor(self):
        return (
            self._componente.get_valor()
            + self._servico_extra.valor
        )