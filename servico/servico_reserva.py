from dominio.reserva import StatusReserva

from dominio.decorators.servico_reserva_base import ServicoReservaBase
from dominio.decorators.cafe_da_manha_decorator import CafeDaManhaDecorator
from dominio.decorators.spa_decorator import SpaDecorator
from dominio.decorators.garagem_decorator import GaragemDecorator
from dominio.decorators.late_checkout_decorator import LateCheckoutDecorator


class ReservaServico:

    def __init__(
        self,
        reserva_repositorio,
        servico_repositorio
    ):
        self._reserva_repositorio = reserva_repositorio
        self._servico_repositorio = servico_repositorio

    def _validar_disponibilidade(self, nova_reserva):

        reservas = self._reserva_repositorio.encontrar_por_quarto(
            nova_reserva.quarto.id
        )

        for reserva_existente in reservas:

            if reserva_existente.esta_cancelada():
                continue

            if nova_reserva.conflita_com(reserva_existente):
                raise ValueError(
                    "Quarto já reservado nesse período"
                )

    def aplicar_servicos(
        self,
        reserva,
        opcoes_servicos=None
    ):

        self._validar_disponibilidade(reserva)

        reserva._servicos_extras = []
        reserva._servico = None

        if not opcoes_servicos:
            return reserva

        servicos = self._servico_repositorio.buscar_por_ids(
            opcoes_servicos
        )

        ids_encontrados = {
            servico.id
            for servico in servicos
        }

        ids_solicitados = set(opcoes_servicos)

        ids_invalidos = ids_solicitados - ids_encontrados

        if ids_invalidos:
            raise ValueError(
                f"Serviço(s) não encontrado(s): "
                f"{sorted(ids_invalidos)}"
            )

        reserva._servicos_extras = servicos

        servico_decorator = ServicoReservaBase(
            reserva
        )

        decorators = {
            "cafe": CafeDaManhaDecorator,
            "spa": SpaDecorator,
            "garagem": GaragemDecorator,
            "late_checkout": LateCheckoutDecorator
        }

        for servico in servicos:

            decorator_class = decorators.get(
                servico.nome.lower()
            )

            if not decorator_class:
                raise ValueError(
                    f"Decorator não encontrado para o serviço "
                    f"'{servico.nome}'"
                )

            servico_decorator = decorator_class(
                servico_decorator,
                servico
            )

        reserva._servico = servico_decorator

        return reserva

    def cancelar_reserva(self, reserva_id):

        reserva = self._reserva_repositorio.encontrar_por_id(
            reserva_id
        )

        if not reserva:
            raise ValueError(
                "Reserva não encontrada"
            )

        if reserva.status == StatusReserva.CANCELADA:
            raise ValueError(
                "Reserva já está cancelada"
            )

        reserva.cancelar()

        self._reserva_repositorio.salvar(
            reserva
        )

    def listar_reservas(self):

        return self._reserva_repositorio.listar()

