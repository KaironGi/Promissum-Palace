from dominio.quarto import Quarto, TipoQuarto

class QuartoBuilder:

    def __init__(self):
        self._numero = None
        self._tipo_quarto = None

    def set_numero(self, numero):
        self._numero = numero
        return self

    def set_tipo_quarto(self, tipo_quarto):
        self._tipo_quarto = tipo_quarto
        return self

    def build(self):

        # VALIDAÇOES

        if not self._numero:
            raise ValueError("Número do quarto inválido")

        if not self._tipo_quarto:
            raise ValueError("Tipo do quarto inválido")

        if isinstance(self._tipo_quarto, str):
            try:
                self._tipo_quarto = TipoQuarto[
                    self._tipo_quarto.upper()
                ]
            except KeyError:
                raise ValueError("Tipo de quarto inválido")
            
        # CRIAÇAO
        return Quarto._criar(
            None,
            self._numero,
            self._tipo_quarto,
        )