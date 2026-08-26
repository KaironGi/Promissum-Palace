from enum import Enum


class TipoQuarto(Enum):

    STANDARD = (
        "standard",
        "Standard",
        150
    )

    LUXO = (
        "luxo",
        "Luxo",
        200
    )

    SUITE = (
        "suite",
        "Suíte",
        300
    )

    def __init__(
        self,
        value,
        descricao,
        preco
    ):
        self._value_ = value
        self._descricao = descricao
        self._preco = preco

    @property
    def descricao(self):
        return self._descricao

    @property
    def preco(self):
        return self._preco


class Quarto:

    def __init__(self):
        raise Exception(
            "Use QuartoBuilder para criar o quarto"
        )

    @classmethod
    def _criar(
        cls,
        quarto_id,
        numero,
        tipo_quarto
    ):

        if not isinstance(tipo_quarto, TipoQuarto):
            raise ValueError(
                "Tipo de quarto inválido"
            )

        quarto = cls.__new__(cls)

        quarto._id = quarto_id
        quarto._numero = numero
        quarto._tipo_quarto = tipo_quarto

        return quarto

    @property
    def id(self):
        return self._id

    @property
    def numero(self):
        return self._numero

    @property
    def tipo_quarto(self):
        return self._tipo_quarto

    @property
    def preco(self):
        return self.tipo_quarto.preco

    def eh_do_tipo(self, tipo_quarto):

        return self.tipo_quarto == tipo_quarto

    def possui_mesmo_numero(self, outro_quarto):

        return self.numero == outro_quarto.numero

    def __eq__(self, outro):

        if not isinstance(outro, Quarto):
            return False

        return self.id == outro.id

    def __hash__(self):

        return hash(self.id)

    def __str__(self):

        return (
            f"Quarto {self.numero} - "
            f"{self.tipo_quarto.descricao}"
        )