from dominio.decorators.servico_reserva_component import ServicoReservaComponent


class ServicoReservaDecorator(ServicoReservaComponent):

    def __init__(self, componente):
        self._componente = componente

    def get_descricao(self):
        return self._componente.get_descricao()

    def get_valor(self):
        return self._componente.get_valor()