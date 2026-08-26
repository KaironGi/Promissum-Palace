import re
from dominio.tutor import Tutor


class TutorBuilder:

    def __init__(self):
        self._nome = None
        self._documento = None
        self._telefone = None
        self._email = None

    def set_nome(self, nome):
        self._nome = nome
        return self

    def set_documento(self, documento):
        self._documento = documento
        return self

    def set_telefone(self, telefone):
        self._telefone = telefone
        return self

    def set_email(self, email):
        self._email = email
        return self

    def build(self):

        if not self._nome or len(self._nome.strip()) < 3:
            raise ValueError(
                "Nome inválido (mínimo 3 caracteres)"
            )

        if not self._documento or not self._documento.isdigit():
            raise ValueError(
                "Documento deve conter apenas números"
            )

        if len(self._documento) not in [11, 14]:
            raise ValueError(
                "Documento deve ter 11 (CPF) ou 14 (CNPJ) dígitos"
            )

        if not self._telefone:
            raise ValueError("Telefone obrigatório")

        telefone_limpo = "".join(
            filter(str.isdigit, self._telefone)
        )

        if len(telefone_limpo) < 10:
            raise ValueError("Telefone inválido")

        if not self._email or not self._email_valido(self._email):
            raise ValueError("Email inválido")

        return Tutor._criar(
            None,
            self._nome.strip(),
            self._documento,
            self._telefone,
            self._email
        )

    def _email_valido(self, email):
        regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        return (
            isinstance(email, str)
            and re.match(regex, email)
        )