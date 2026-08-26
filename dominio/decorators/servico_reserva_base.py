from dominio.decorators.servico_reserva_component import ServicoReservaComponent


class ServicoReservaBase(ServicoReservaComponent):

    def __init__(self, reserva):
        self._reserva = reserva

    def get_descricao(self):
        return "Reserva"

    def get_valor(self):
        return (
            self._reserva.periodo.quantidade_diarias()
            * self._reserva.quarto.preco
        )