from conexao.database import criar_conexao
from dominio.quarto import Quarto, TipoQuarto


class MySQLQuartoRepositorio:

    def salvar(self, quarto):

        conexao = criar_conexao()
        cursor = conexao.cursor()

        try:

            sql = """
            INSERT INTO quartos (
                numero,
                tipo_quarto
            )
            VALUES (%s, %s)
            """

            valores = (
                quarto.numero,
                quarto.tipo_quarto.name
            )

            cursor.execute(sql, valores)

            conexao.commit()

            quarto._id = cursor.lastrowid

        except Exception:
            conexao.rollback()
            raise

        finally:
            cursor.close()
            conexao.close()

    def listar(self):

        conexao = criar_conexao()
        cursor = conexao.cursor()

        try:

            sql = """
            SELECT
                id,
                numero,
                tipo_quarto
            FROM quartos
            ORDER BY numero
            """

            cursor.execute(sql)

            resultados = cursor.fetchall()

        finally:
            cursor.close()
            conexao.close()

        return [
            self._mapear(resultado)
            for resultado in resultados
        ]

    def encontrar_por_id(self, quarto_id):

        conexao = criar_conexao()
        cursor = conexao.cursor()

        try:

            sql = """
            SELECT
                id,
                numero,
                tipo_quarto
            FROM quartos
            WHERE id = %s
            """

            cursor.execute(
                sql,
                (quarto_id,)
            )

            resultado = cursor.fetchone()

        finally:
            cursor.close()
            conexao.close()

        if not resultado:
            return None

        return self._mapear(resultado)

    def buscar_por_id(self, quarto_id):

        return self.encontrar_por_id(quarto_id)

    def deletar(self, quarto):

        conexao = criar_conexao()
        cursor = conexao.cursor()

        try:

            sql = """
            DELETE FROM quartos
            WHERE id = %s
            """

            cursor.execute(
                sql,
                (quarto.id,)
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    "Quarto não encontrado"
                )

            conexao.commit()

        except Exception:
            conexao.rollback()
            raise

        finally:
            cursor.close()
            conexao.close()

    def pesquisar(self, termo):

        conexao = criar_conexao()
        cursor = conexao.cursor()

        try:

            busca = f"%{termo}%"

            sql = """
            SELECT
                id,
                numero,
                tipo_quarto
            FROM quartos
            WHERE CAST(numero AS CHAR) LIKE %s
            OR tipo_quarto LIKE %s
            ORDER BY numero
            """

            cursor.execute(
                sql,
                (busca, busca)
            )

            resultados = cursor.fetchall()

        finally:
            cursor.close()
            conexao.close()

        return [
            self._mapear(resultado)
            for resultado in resultados
        ]

    def _mapear(self, row):

        try:
            tipo = TipoQuarto[row[2]]
        except KeyError:
            raise ValueError(
                f"Tipo de quarto inválido no banco: {row[2]}"
            )

        return Quarto._criar(
            row[0],
            row[1],
            tipo
        )