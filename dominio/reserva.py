from datetime import date
from enum import Enum


class StatusReserva(Enum):

    PENDENTE = "Pendente"
    CONFIRMADA = "Confirmada"
    HOSPEDADO = "Hospedado"
    FINALIZADA = "Finalizada"
    CANCELADA = "Cancelada"


class PeriodoReserva:

    def __init__(
        self,
        check_in: date,
        check_out: date
    ):

        if check_out <= check_in:
            raise ValueError(
                "Check-out deve ser após check-in"
            )

        self._check_in = check_in
        self._check_out = check_out

    @property
    def check_in(self):
        return self._check_in

    @property
    def check_out(self):
        return self._check_out

    def quantidade_diarias(self):
        return (
            self._check_out - self._check_in
        ).days

    def conflita_com(self, outro):
        return (
            self._check_in < outro.check_out
            and self._check_out > outro.check_in
        )


class Reserva:

    def __init__(self):
        raise Exception(
            "Use ReservaBuilder para criar a reserva"
        )

    @classmethod
    def _criar(
        cls,
        reserva_id,
        tutor,
        quarto,
        periodo,
        status,
        servico=None
    ):

        reserva = cls.__new__(cls)

        reserva._id = reserva_id
        reserva._tutor = tutor
        reserva._quarto = quarto
        reserva._periodo = periodo
        reserva._status = status
        reserva._servico = servico
        reserva._servicos_extras = []

        return reserva

    @property
    def id(self):
        return self._id

    @property
    def tutor(self):
        return self._tutor

    @property
    def quarto(self):
        return self._quarto

    @property
    def periodo(self):
        return self._periodo

    @property
    def status(self):
        return self._status

    @property
    def servico(self):
        return self._servico

    @property
    def servicos_extras(self):
        return self._servicos_extras

    def adicionar_servico(self, servico):

        if servico not in self._servicos_extras:
            self._servicos_extras.append(servico)

    def esta_cancelada(self):

        return self.status == StatusReserva.CANCELADA

    def confirmar(self):

        if self.status != StatusReserva.PENDENTE:
            raise ValueError(
                "Somente reservas pendentes podem ser confirmadas"
            )

        self._status = StatusReserva.CONFIRMADA

    def hospedar(self):

        if self.status != StatusReserva.CONFIRMADA:
            raise ValueError(
                "Somente reservas confirmadas podem ser hospedadas"
            )

        self._status = StatusReserva.HOSPEDADO

    def finalizar(self):

        if self.status != StatusReserva.HOSPEDADO:
            raise ValueError(
                "Somente reservas hospedadas podem ser finalizadas"
            )

        self._status = StatusReserva.FINALIZADA

    def cancelar(self):

        if self.status in (
            StatusReserva.CANCELADA,
            StatusReserva.FINALIZADA
        ):
            raise ValueError(
                "Esta reserva não pode mais ser cancelada"
            )

        self._status = StatusReserva.CANCELADA

    def pertence_mesmo_quarto(self, outra_reserva):

        return self.quarto.id == outra_reserva.quarto.id

    def conflita_com(self, outra_reserva):

        if self.esta_cancelada():
            return False

        if outra_reserva.esta_cancelada():
            return False

        if not self.pertence_mesmo_quarto(outra_reserva):
            return False

        return self.periodo.conflita_com(
            outra_reserva.periodo
        )

    def calcular_valor_base(self):

        return (
            self.periodo.quantidade_diarias()
            * self.quarto.preco
        )

    def calcular_valor_total(self):

        if self._servico:
            return self._servico.get_valor()

        return self.calcular_valor_base()

    def __str__(self):

        return (
            f"Tutor: {self.tutor}, "
            f"Quarto: {self.quarto}, "
            f"Status: {self.status.value}"
        )