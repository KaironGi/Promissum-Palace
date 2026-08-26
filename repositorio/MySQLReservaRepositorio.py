from conexao.database import criar_conexao

from dominio.reserva import (
    Reserva,
    StatusReserva,
    PeriodoReserva
)

from dominio.decorators.servico_reserva_base import ServicoReservaBase
from dominio.decorators.cafe_da_manha_decorator import CafeDaManhaDecorator
from dominio.decorators.spa_decorator import SpaDecorator
from dominio.decorators.garagem_decorator import GaragemDecorator
from dominio.decorators.late_checkout_decorator import LateCheckoutDecorator


class MySQLReservaRepositorio:

    def __init__(
        self,
        tutor_repo,
        quarto_repo,
        servico_extra_repo
    ):
        self._tutor_repo = tutor_repo
        self._quarto_repo = quarto_repo
        self._servico_extra_repo = servico_extra_repo

    def salvar(self, reserva):

        if reserva.id:
            self._atualizar(reserva)
        else:
            self._inserir(reserva)

    def _inserir(self, reserva):

        conexao = criar_conexao()
        cursor = conexao.cursor()

        try:

            sql = """
            INSERT INTO reservas (
                tutor_id,
                quarto_id,
                check_in,
                check_out,
                status
            )
            VALUES (%s, %s, %s, %s, %s)
            """

            valores = (
                reserva.tutor.id,
                reserva.quarto.id,
                reserva.periodo.check_in,
                reserva.periodo.check_out,
                reserva.status.name
            )

            cursor.execute(sql, valores)

            reserva._id = cursor.lastrowid

            if reserva.servicos_extras:

                sql_servico = """
                INSERT INTO reserva_servicos (
                    reserva_id,
                    servico_id
                )
                VALUES (%s, %s)
                """

                for servico in reserva.servicos_extras:

                    cursor.execute(
                        sql_servico,
                        (
                            reserva.id,
                            servico.id
                        )
                    )

            conexao.commit()

        except Exception:
            conexao.rollback()
            raise

        finally:
            cursor.close()
            conexao.close()

    def _atualizar(self, reserva):

        conexao = criar_conexao()
        cursor = conexao.cursor()

        try:

            sql = """
            UPDATE reservas
            SET status = %s
            WHERE id = %s
            """

            cursor.execute(
                sql,
                (
                    reserva.status.name,
                    reserva.id
                )
            )

            conexao.commit()

        except Exception:
            conexao.rollback()
            raise

        finally:
            cursor.close()
            conexao.close()

    def _reconstruir_reserva(self, dados):

        tutor = self._tutor_repo.encontrar_por_id(
            dados[1]
        )

        quarto = self._quarto_repo.encontrar_por_id(
            dados[2]
        )

        if not tutor:
            raise ValueError(
                f"Tutor {dados[1]} não encontrado"
            )

        if not quarto:
            raise ValueError(
                f"Quarto {dados[2]} não encontrado"
            )

        periodo = PeriodoReserva(
            dados[3],
            dados[4]
        )

        status = StatusReserva[dados[5]]

        servicos = self._buscar_servicos_reserva(
            dados[0]
        )

        reserva = Reserva._criar(
            dados[0],
            tutor,
            quarto,
            periodo,
            status,
            None
        )

        reserva._servicos_extras = servicos

        if servicos:

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

                if decorator_class:

                    servico_decorator = decorator_class(
                        servico_decorator,
                        servico
                    )

            reserva._servico = servico_decorator

        return reserva

    def _buscar_servicos_reserva(self, reserva_id):

        conexao = criar_conexao()
        cursor = conexao.cursor()

        try:

            sql = """
            SELECT servico_id
            FROM reserva_servicos
            WHERE reserva_id = %s
            """

            cursor.execute(
                sql,
                (reserva_id,)
            )

            resultados = cursor.fetchall()

        finally:
            cursor.close()
            conexao.close()

        servicos = []

        for resultado in resultados:

            servico = self._servico_extra_repo.buscar_por_id(
                resultado[0]
            )

            if servico:
                servicos.append(servico)

        return servicos

    def encontrar_por_id(self, reserva_id):

        conexao = criar_conexao()
        cursor = conexao.cursor()

        try:

            sql = """
            SELECT
                id,
                tutor_id,
                quarto_id,
                check_in,
                check_out,
                status
            FROM reservas
            WHERE id = %s
            """

            cursor.execute(
                sql,
                (reserva_id,)
            )

            resultado = cursor.fetchone()

        finally:
            cursor.close()
            conexao.close()

        if not resultado:
            return None

        return self._reconstruir_reserva(
            resultado
        )

    def encontrar_por_quarto(self, quarto_id):

        conexao = criar_conexao()
        cursor = conexao.cursor()

        try:

            sql = """
            SELECT
                id,
                tutor_id,
                quarto_id,
                check_in,
                check_out,
                status
            FROM reservas
            WHERE quarto_id = %s
            """

            cursor.execute(
                sql,
                (quarto_id,)
            )

            resultados = cursor.fetchall()

        finally:
            cursor.close()
            conexao.close()

        return [
            self._reconstruir_reserva(resultado)
            for resultado in resultados
        ]

    def listar(self):

        conexao = criar_conexao()
        cursor = conexao.cursor()

        try:

            sql = """
            SELECT
                id,
                tutor_id,
                quarto_id,
                check_in,
                check_out,
                status
            FROM reservas
            ORDER BY id
            """

            cursor.execute(sql)

            resultados = cursor.fetchall()

        finally:
            cursor.close()
            conexao.close()

        return [
            self._reconstruir_reserva(resultado)
            for resultado in resultados
        ]

    def pesquisar(self, termo):

        conexao = criar_conexao()
        cursor = conexao.cursor()

        try:

            busca = f"%{termo}%"

            sql = """
            SELECT id
            FROM reservas
            WHERE CAST(id AS CHAR) LIKE %s
            OR status LIKE %s
            """

            cursor.execute(
                sql,
                (
                    busca,
                    busca
                )
            )

            resultados = cursor.fetchall()

        finally:
            cursor.close()
            conexao.close()

        return [
            self.encontrar_por_id(resultado[0])
            for resultado in resultados
        ]

    def existe_reserva_ativa_por_quarto(
        self,
        quarto
    ):

        reservas = self.encontrar_por_quarto(
            quarto.id
        )

        return any(
            reserva.status != StatusReserva.CANCELADA
            for reserva in reservas
        )

    def existe_reserva_por_tutor(self, tutor_id):

        conexao = criar_conexao()
        cursor = conexao.cursor()

        try:

            sql = """
            SELECT 1
            FROM reservas
            WHERE tutor_id = %s
            LIMIT 1
            """

            cursor.execute(
                sql,
                (tutor_id,)
            )

            return cursor.fetchone() is not None

        finally:

            cursor.close()
            conexao.close()