from conexao.database import criar_conexao
from dominio.tutor import Tutor


class MySQLTutorRepositorio:

    def salvar(self, tutor):

        conexao = criar_conexao()
        cursor = conexao.cursor()

        try:

            sql = """
            INSERT INTO tutores (
                nome,
                documento,
                telefone,
                email
            )
            VALUES (%s, %s, %s, %s)
            """

            valores = (
                tutor.nome,
                tutor.documento,
                tutor.telefone,
                tutor.email
            )

            cursor.execute(sql, valores)

            conexao.commit()

            tutor._id = cursor.lastrowid

        except Exception:
            conexao.rollback()
            raise

        finally:
            cursor.close()
            conexao.close()

    def encontrar_por_id(self, tutor_id):

        conexao = criar_conexao()
        cursor = conexao.cursor()

        try:

            sql = """
            SELECT
                id,
                nome,
                documento,
                telefone,
                email
            FROM tutores
            WHERE id = %s
            """

            cursor.execute(
                sql,
                (tutor_id,)
            )

            resultado = cursor.fetchone()

        finally:
            cursor.close()
            conexao.close()

        if not resultado:
            return None

        return Tutor._criar(
            resultado[0],
            resultado[1],
            resultado[2],
            resultado[3],
            resultado[4]
        )

    def listar(self, busca=""):

        conexao = criar_conexao()
        cursor = conexao.cursor()

        try:

            termo = f"%{busca}%"

            sql = """
            SELECT
                id,
                nome,
                documento,
                telefone,
                email
            FROM tutores
            WHERE nome LIKE %s
            OR documento LIKE %s
            ORDER BY nome
            """

            cursor.execute(
                sql,
                (termo, termo)
            )

            resultados = cursor.fetchall()

        finally:
            cursor.close()
            conexao.close()

        return [
            Tutor._criar(
                resultado[0],
                resultado[1],
                resultado[2],
                resultado[3],
                resultado[4]
            )
            for resultado in resultados
        ]

    def buscar_por_nome_ou_documento(self, termo):

        return self.listar(termo)

    def deletar(self, tutor_id):

        conexao = criar_conexao()
        cursor = conexao.cursor()

        try:

            sql = """
            DELETE FROM tutores
            WHERE id = %s
            """

            cursor.execute(
                sql,
                (tutor_id,)
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    "Tutor não encontrado"
                )

            conexao.commit()

        except Exception:
            conexao.rollback()
            raise

        finally:
            cursor.close()
            conexao.close()