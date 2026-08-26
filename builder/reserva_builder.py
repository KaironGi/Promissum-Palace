from dominio.reserva import (
    Reserva,
    StatusReserva,
    PeriodoReserva
)

from dominio.tutor import Tutor
from dominio.quarto import Quarto


class ReservaBuilder:

    def __init__(self):

        self._tutor = None
        self._quarto = None
        self._periodo = None
        self._status = StatusReserva.PENDENTE

    def set_tutor(self, tutor):

        if not isinstance(tutor, Tutor):
            raise ValueError(
                "Tutor inválido"
            )

        self._tutor = tutor

        return self

    def set_quarto(self, quarto):

        if not isinstance(quarto, Quarto):
            raise ValueError(
                "Quarto inválido"
            )

        self._quarto = quarto

        return self

    def set_periodo(
        self,
        check_in,
        check_out
    ):

        self._periodo = PeriodoReserva(
            check_in,
            check_out
        )

        return self

    def set_status(self, status):

        if not isinstance(status, StatusReserva):
            raise ValueError(
                "Status de reserva inválido"
            )

        self._status = status

        return self

    def build(self):

        if self._tutor is None:
            raise ValueError(
                "Tutor obrigatório"
            )

        if self._quarto is None:
            raise ValueError(
                "Quarto obrigatório"
            )

        if self._periodo is None:
            raise ValueError(
                "Período obrigatório"
            )

        return Reserva._criar(
            None,
            self._tutor,
            self._quarto,
            self._periodo,
            self._status,
            None
        )
