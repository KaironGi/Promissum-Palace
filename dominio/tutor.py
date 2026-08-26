class Tutor:

    def __init__(self):
        raise Exception(
            "Use TutorBuilder para criar o tutor"
        )

    @classmethod
    def _criar(
        cls,
        tutor_id,
        nome,
        documento,
        telefone,
        email
    ):
        tutor = cls.__new__(cls)

        tutor._id = tutor_id
        tutor._nome = nome
        tutor._documento = documento
        tutor._telefone = telefone
        tutor._email = email

        return tutor

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @property
    def documento(self):
        return self._documento

    @property
    def telefone(self):
        return self._telefone

    @property
    def email(self):
        return self._email

    def atualizar_email(self, novo_email):

        if not self._email_valido(novo_email):
            raise ValueError("Email inválido")

        self._email = novo_email

    @staticmethod
    def _email_valido(email):

        return (
            isinstance(email, str)
            and "@" in email
            and "." in email
        )

    def __eq__(self, outro):

        if not isinstance(outro, Tutor):
            return False

        return self.id == outro.id

    def __hash__(self):

        return hash(self.id)

    def __str__(self):

        return (
            f"Nome: {self.nome}, "
            f"Documento: {self.documento}"
        )