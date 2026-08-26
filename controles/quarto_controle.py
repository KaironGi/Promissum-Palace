from dominio.quarto import Quarto, TipoQuarto


class QuartoControle:

    def __init__(
        self,
        quarto_repositorio,
        reserva_repositorio
    ):
        self._repositorio = quarto_repositorio
        self._reserva_repositorio = reserva_repositorio

    def criar_quarto(self, quarto_request):

        tipo_quarto = TipoQuarto[
            quarto_request.tipo_quarto.upper()
        ]

        quarto = Quarto._criar(
            None,
            quarto_request.numero,
            tipo_quarto
        )

        self._repositorio.salvar(quarto)

        return quarto

    def listar_quartos(self):

        return self._repositorio.listar()

    def pesquisar_quartos(self, termo):

        return self._repositorio.pesquisar(termo)

    def buscar_por_id(self, quarto_id: int):

        return self._repositorio.encontrar_por_id(
            quarto_id
        )

    def deletar_quarto(self, quarto_id):

        quarto = self._repositorio.encontrar_por_id(
            quarto_id
        )

        if not quarto:
            raise ValueError(
                "Quarto não encontrado"
            )

        if self._reserva_repositorio.existe_reserva_ativa_por_quarto(
            quarto
        ):
            raise ValueError(
                "Não é possível deletar quarto com reserva ativa"
            )

        self._repositorio.deletar(quarto)