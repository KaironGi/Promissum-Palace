from abc import ABC, abstractmethod


class ServicoReservaComponent(ABC):

    @abstractmethod
    def get_descricao(self):
        pass

    @abstractmethod
    def get_valor(self):
        pass