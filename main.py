from datetime import datetime

# repositorios
from repositorio.MySQLTutorRepositorio import MySQLHospedeRepositorio
from repositorio.MySQLQuartoRepositorio import MySQLQuartoRepositorio
from repositorio.MySQLReservaRepositorio import MySQLReservaRepositorio
from repositorio.MySQLServicoExtraRepositorio import MySQLServicoExtraRepositorio

# controles
from controles.tutor_controle import HospedeControle
from controles.quarto_controle import QuartoControle
from controles.reserva_controle import ReservaControle

# servico
from servico.servico_reserva import ReservaServico

# dominio
from dominio.quarto import TipoQuarto


# INICIALIZAÇAO

hospede_repo = MySQLHospedeRepositorio()

quarto_repo = MySQLQuartoRepositorio()

reserva_repo = MySQLReservaRepositorio(
    hospede_repo,
    quarto_repo,
)

servico_extra_repo = MySQLServicoExtraRepositorio()

reserva_servico = ReservaServico(
    hospede_repo,
    quarto_repo,
    reserva_repo,
    servico_extra_repo
)

hospede_controle = HospedeControle(hospede_repo)

quarto_controle = QuartoControle(quarto_repo)

reserva_controle = ReservaControle(
    reserva_repo,
    reserva_servico,
    hospede_repo,
    quarto_repo
)


# MENU

def menu():

    print("\n=== Promissum Palace ===")
    print("1 - Cadastrar hóspede")
    print("2 - Cadastrar quarto")
    print("3 - Criar reserva")
    print("4 - Listar hóspedes")
    print("5 - Listar quartos")
    print("6 - Listar reservas")
    print("7 - Cancelar reserva")
    print("0 - Sair")


while True:

    menu()

    opcao = input("\nEscolha uma opção: ")

    try:

        # CADASTRAR HÓSPEDE
        if opcao == "1":

            nome = input("Nome: ")
            documento = input("CPF/CNPJ: ")
            email = input("Email: ")

            hospede = hospede_controle.criar_hospede(
                nome,
                documento,
                email
            )

            print("\nHóspede cadastrado com sucesso!")
            print("ID:", hospede.id)

        # CADASTRAR QUARTO
        elif opcao == "2":

            numero = int(input("Número do quarto: "))
            tipo = input("Tipo (STANDARD/LUXO/SUITE): ").upper()
            tipo_enum = TipoQuarto[tipo]
            preco = tipo_enum.preco

            try:
                tipo_enum = TipoQuarto[tipo]
            except KeyError:
                raise ValueError("Tipo de quarto inválido")

            quarto = quarto_controle.criar_quarto(
                numero,
                tipo_enum,
                tipo_enum.preco
            )

            print("\nQuarto cadastrado com sucesso!")
            print("ID:", quarto.id)

    
        # CRIAR RESERVA
  
        elif opcao == "3":

            hospede_id = input("ID do hóspede: ")
            quarto_id = input("ID do quarto: ")

            check_in = datetime.strptime(
                input("Check-in (YYYY-MM-DD): "),
                "%Y-%m-%d"
            ).date()

            check_out = datetime.strptime(
                input("Check-out (YYYY-MM-DD): "),
                "%Y-%m-%d"
            ).date()

            #SERVIÇOS ADICIONAIS DA RESERVA
         
            print("\nDeseja algum serviço adicional?\nServiços disponíveis:")
            print("1 - Café da Manhã")
            print("2 - SPA")
            print("3 - Garagem")
            print("4 - Checkout tardio")

            opcoes = input(
                "Escolha (ex: 1,2,3,4 ou vazio): "
            )

            mapa = {
                "1": "cafe",
                "2": "spa",
                "3": "garagem",
                "4": "late_checkout"
            }

            opcoes_servicos = []

            if opcoes.strip():

                for o in opcoes.split(","):
                    o = o.strip()

                    if o in mapa:
                        opcoes_servicos.append(mapa[o])

            # criação da reserva com serviços
            reserva = reserva_controle.criar_reserva(
                hospede_id,
                quarto_id,
                check_in,
                check_out,
                opcoes_servicos
            )

            print("\nReserva criada com sucesso!")
            print("ID:", reserva.id)

            # valor total
            print(
                "Valor total:",
                reserva.calcular_valor_total()
            )

        # LISTAR HÓSPEDES
        elif opcao == "4":

            hospedes = hospede_controle.listar_hospedes()

            print("\n=== HÓSPEDES ===")

            for h in hospedes:
                print(h.id, "-", h.nome)

        # LISTAR QUARTOS
        elif opcao == "5":

            quartos = quarto_controle.listar_quartos()

            print("\n=== QUARTOS ===")

            for q in quartos:
                print(
                    q.id,
                    "- Quarto",
                    q.numero,
                    "-",
                    q.tipo_quarto.descricao,
                    "- R$",
                    q.preco
                )

        # LISTAR RESERVAS
        elif opcao == "6":

            reservas = reserva_controle.listar_reservas()

            print("\n=== RESERVAS ===")

            for r in reservas:
                print(
                    r.id,
                    "| Hóspede:", r.hospede.nome,
                    "| Quarto:", r.quarto.numero,
                    "|", r.check_in, "->", r.check_out,
                    "| Status:", r.status.value
                )

        # CANCELAR RESERVA
        elif opcao == "7":

            reserva_id = input("ID da reserva: ")

            reserva_servico.cancelar_reserva(reserva_id)

            print("\nReserva cancelada!")

        # SAIR
        elif opcao == "0":

            print("Encerrando...")
            break

        else:
            print("Opção inválida")

    except Exception as e:
        print("\nErro:", str(e))