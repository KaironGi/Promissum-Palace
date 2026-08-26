from builder.reserva_builder import ReservaBuilder


class ReservaControle:

    def __init__(
        self,
        repositorio,
        servico,
        tutor_repo,
        quarto_repo
    ):
        self._repositorio = repositorio
        self._servico = servico
        self._tutor_repo = tutor_repo
        self._quarto_repo = quarto_repo

    def criar_reserva(self, reserva_request):

        tutor = self._tutor_repo.encontrar_por_id(
            reserva_request.tutor_id
        )

        if tutor is None:
            raise ValueError(
                "Tutor não encontrado"
            )

        quarto = self._quarto_repo.encontrar_por_id(
            reserva_request.quarto_id
        )

        if quarto is None:
            raise ValueError(
                "Quarto não encontrado"
            )

        reserva = (
            ReservaBuilder()
            .set_tutor(tutor)
            .set_quarto(quarto)
            .set_periodo(
                reserva_request.check_in,
                reserva_request.check_out
            )
            .build()
        )

        self._servico.aplicar_servicos(
            reserva,
            reserva_request.servicos
        )

        self._repositorio.salvar(reserva)

        return reserva

    def listar_reservas(self):

        return self._repositorio.listar()

    def pesquisar_reservas(self, termo):

        return self._repositorio.pesquisar(termo)

    def confirmar_reserva(self, reserva_id):

        reserva = self._repositorio.encontrar_por_id(
            reserva_id
        )

        if reserva is None:
            raise ValueError(
                "Reserva não encontrada"
            )

        reserva.confirmar()

        self._repositorio.salvar(reserva)

        return reserva

    def hospedar_reserva(self, reserva_id):

        reserva = self._repositorio.encontrar_por_id(
            reserva_id
        )

        if reserva is None:
            raise ValueError(
                "Reserva não encontrada"
            )

        reserva.hospedar()

        self._repositorio.salvar(reserva)

        return reserva

    def finalizar_reserva(self, reserva_id):

        reserva = self._repositorio.encontrar_por_id(
            reserva_id
        )

        if reserva is None:
            raise ValueError(
                "Reserva não encontrada"
            )

        reserva.finalizar()

        self._repositorio.salvar(reserva)

        return reserva

    def cancelar_reserva(self, reserva_id):

        self._servico.cancelar_reserva(
            reserva_id
        )
