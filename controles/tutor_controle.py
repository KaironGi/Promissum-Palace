from builder.tutor_builder import TutorBuilder


class TutorControle:

    def __init__(self, repositorio, reserva_repositorio):
        self._repositorio = repositorio
        self._reserva_repositorio = reserva_repositorio

    def criar_tutor(self, tutor_request):

        tutor = (
            TutorBuilder()
            .set_nome(tutor_request.nome)
            .set_documento(tutor_request.documento)
            .set_telefone(tutor_request.telefone)
            .set_email(tutor_request.email)
            .build()
        )

        self._repositorio.salvar(tutor)

        return tutor

    def listar_tutores(self, busca=""):

        return self._repositorio.listar(busca)

    def buscar_tutores(self, termo):

        return self._repositorio.buscar_por_nome_ou_documento(
            termo
        )

    def deletar_tutor(self, tutor_id):

        tutor = self._repositorio.encontrar_por_id(
            tutor_id
        )

        if not tutor:
            raise ValueError(
                "Tutor não encontrado"
            )

        if self._reserva_repositorio.existe_reserva_por_tutor(
            tutor_id
        ):
            raise ValueError(
                "Não é possível deletar tutor que possui reservas"
            )

        self._repositorio.deletar(tutor_id)