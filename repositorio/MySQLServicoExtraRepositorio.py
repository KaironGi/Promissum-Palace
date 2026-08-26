from conexao.database import criar_conexao

from dominio.servico_extra import ServicoExtra


class MySQLServicoExtraRepositorio:

    def listar(self):

        conexao = criar_conexao()
        cursor = conexao.cursor()

        try:
            sql = """
                SELECT
                    id,
                    nome,
                    valor
                FROM servicos_extras
                ORDER BY nome
            """

            cursor.execute(sql)

            resultados = cursor.fetchall()

            return [
                self._mapear(resultado)
                for resultado in resultados
            ]

        finally:
            cursor.close()
            conexao.close()

    def buscar_por_id(self, servico_id):

        conexao = criar_conexao()
        cursor = conexao.cursor()

        try:
            sql = """
                SELECT
                    id,
                    nome,
                    valor
                FROM servicos_extras
                WHERE id = %s
            """

            cursor.execute(sql, (servico_id,))

            resultado = cursor.fetchone()

            if not resultado:
                return None

            return self._mapear(resultado)

        finally:
            cursor.close()
            conexao.close()

    def buscar_por_ids(self, ids):

        if isinstance(ids, int):
            ids = [ids]

        if not ids:
            return []

        conexao = criar_conexao()
        cursor = conexao.cursor()

        try:
            placeholders = ", ".join(
                ["%s"] * len(ids)
            )

            sql = f"""
                SELECT
                    id,
                    nome,
                    valor
                FROM servicos_extras
                WHERE id IN ({placeholders})
            """

            cursor.execute(sql, tuple(ids))

            resultados = cursor.fetchall()

            return [
                self._mapear(resultado)
                for resultado in resultados
            ]

        finally:
            cursor.close()
            conexao.close()

    def buscar_por_reserva(self, reserva_id):

        conexao = criar_conexao()
        cursor = conexao.cursor()

        try:
            sql = """
                SELECT
                    se.id,
                    se.nome,
                    se.valor
                FROM servicos_extras se
                INNER JOIN reserva_servicos rs
                    ON rs.servico_id = se.id
                WHERE rs.reserva_id = %s
                ORDER BY se.nome
            """

            cursor.execute(sql, (reserva_id,))

            resultados = cursor.fetchall()

            return [
                self._mapear(resultado)
                for resultado in resultados
            ]

        finally:
            cursor.close()
            conexao.close()

    @staticmethod
    def _mapear(row):

        return ServicoExtra(
            id=row[0],
            nome=row[1],
            valor=row[2]
        )