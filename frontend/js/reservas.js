const API_URL = "http://127.0.0.1:8000";

let quartos = [];
let servicos = [];
let reservasCache = [];
let paginaAtual = 1;

const itensPorPagina = 5;


// ======================
// TUTORES
// ======================

async function carregarTutores() {

    const response = await fetch(`${API_URL}/tutores`);

    const tutores = await response.json();

    const select = document.getElementById("tutor");

    if (!select) return;

    select.innerHTML = `
        <option value="">
            Selecione
        </option>
    `;

    tutores.forEach(tutor => {

        select.innerHTML += `
            <option value="${tutor.id}">
                ${tutor.nome}
            </option>
        `;

    });

    garantirEventosCalculo();
}


// ======================
// QUARTOS
// ======================

async function carregarQuartos() {

    const response = await fetch(`${API_URL}/quartos`);

    quartos = await response.json();

    const select = document.getElementById("quarto");

    if (!select) return;

    select.innerHTML = `
        <option value="">
            Selecione
        </option>
    `;

    quartos.forEach(quarto => {

        select.innerHTML += `
            <option value="${quarto.id}">
                Quarto ${quarto.numero} -
                ${quarto.tipo_quarto}
                (R$ ${quarto.preco})
            </option>
        `;

    });

    garantirEventosCalculo();
}


// ======================
// SERVIÇOS
// ======================

async function carregarServicos() {

    const response = await fetch(`${API_URL}/servicos`);

    servicos = await response.json();

    const container =
        document.getElementById("servicosContainer");

    if (!container) return;

    container.innerHTML = "";

    servicos.forEach(servico => {

        container.innerHTML += `
            <div class="servico-item">

                <input
                    type="checkbox"
                    value="${servico.id}"
                    data-valor="${servico.valor}"
                    class="checkbox-servico"
                >

                <label>
                    ${servico.nome}
                    (+ R$ ${servico.valor})
                </label>

            </div>
        `;

    });

    garantirEventosCalculo();
}


// ======================
// EVENTOS DO CÁLCULO
// ======================

function garantirEventosCalculo() {

    const quarto =
        document.getElementById("quarto");

    const checkin =
        document.getElementById("checkin");

    const checkout =
        document.getElementById("checkout");

    if (quarto) {
        quarto.onchange = calcularValorTotal;
    }

    if (checkin) {
        checkin.onchange = calcularValorTotal;
    }

    if (checkout) {
        checkout.onchange = calcularValorTotal;
    }

    document
        .querySelectorAll(".checkbox-servico")
        .forEach(checkbox => {

            checkbox.onchange =
                calcularValorTotal;

        });
}


// ======================
// CÁLCULO DO VALOR
// ======================

function calcularValorTotal() {

    const quartoId =
        document.getElementById("quarto")?.value;

    const checkin =
        document.getElementById("checkin")?.value;

    const checkout =
        document.getElementById("checkout")?.value;

    let total = 0;

    if (quartoId && checkin && checkout) {

        const quarto = quartos.find(
            q => q.id == quartoId
        );

        const entrada = new Date(checkin);
        const saida = new Date(checkout);

        const dias =
            (saida - entrada) /
            (1000 * 60 * 60 * 24);

        if (dias > 0 && quarto) {

            total +=
                dias *
                (quarto.preco ?? 0);

        }
    }

    document
        .querySelectorAll(".checkbox-servico:checked")
        .forEach(checkbox => {

            total += Number(
                checkbox.dataset.valor ?? 0
            );

        });

    const elemento =
        document.getElementById("valorTotal");

    if (elemento) {

        elemento.innerText =
            `R$ ${total.toFixed(2)}`;

    }
}


// ======================
// RESERVAS
// ======================

async function carregarReservas() {

    try {

        const response =
            await fetch(`${API_URL}/reservas`);

        if (!response.ok) {
            throw new Error(
                "Erro ao carregar reservas"
            );
        }

        reservasCache =
            await response.json();

        paginaAtual = 1;

        renderizarPagina();

    } catch (erro) {

        console.error(
            "Erro ao carregar reservas:",
            erro
        );

    }
}


// ======================
// AÇÕES DE STATUS
// ======================

function gerarBotoesStatus(reserva) {

    switch (reserva.status) {

        case "Pendente":

            return `
                <button
                    onclick="confirmarReserva(${reserva.id})"
                >
                    Confirmar
                </button>

                <button
                    onclick="cancelarReserva(${reserva.id})"
                >
                    Cancelar
                </button>
            `;


        case "Confirmada":

            return `
                <button
                    onclick="hospedarReserva(${reserva.id})"
                >
                    Hospedar
                </button>

                <button
                    onclick="cancelarReserva(${reserva.id})"
                >
                    Cancelar
                </button>
            `;


        case "Hospedado":

            return `
                <button
                    onclick="finalizarReserva(${reserva.id})"
                >
                    Finalizar
                </button>
            `;


        case "Finalizada":

            return `
                <span>
                    Finalizada
                </span>
            `;


        case "Cancelada":

            return `
                <span>
                    Cancelada
                </span>
            `;


        default:

            return `
                <span>
                    ${reserva.status}
                </span>
            `;
    }
}


// ======================
// RENDERIZAÇÃO
// ======================

function renderizarPagina() {

    const tabela =
        document.getElementById(
            "tabelaReservas"
        );

    if (!tabela) return;

    tabela.innerHTML = "";

    const inicio =
        (paginaAtual - 1) *
        itensPorPagina;

    const fim =
        inicio +
        itensPorPagina;

    const pagina =
        reservasCache.slice(
            inicio,
            fim
        );

    pagina.forEach(reserva => {

        const classeStatus =
            obterClasseStatus(
                reserva.status
            );

        tabela.innerHTML += `
            <tr>

                <td>
                    ${reserva.id}
                </td>

                <td>
                    ${reserva.tutor?.nome ?? "-"}
                </td>

                <td>
                    ${reserva.quarto?.numero ?? "-"}
                    -
                    ${reserva.quarto?.tipo_quarto ?? "-"}
                </td>

                <td>
                    ${reserva.check_in}
                </td>

                <td>
                    ${reserva.check_out}
                </td>

                <td class="${classeStatus}">
                    ${reserva.status}
                </td>

                <td>
                    ${
                        reserva.servicos?.length
                            ? reserva.servicos
                                .map(servico => servico.nome)
                                .join(", ")
                            : "Nenhum"
                    }
                </td>

                <td>
                    R$
                    ${(reserva.valor_total ?? 0)
                        .toFixed(2)}
                </td>

                <td class="acoes">

                    ${gerarBotoesStatus(reserva)}

                </td>

            </tr>
        `;
    });

    atualizarPaginacaoUI();
}


// ======================
// CLASSE DO STATUS
// ======================

function obterClasseStatus(status) {

    switch (status) {

        case "Pendente":
            return "status-pendente";

        case "Confirmada":
            return "status-confirmada";

        case "Hospedado":
            return "status-hospedado";

        case "Finalizada":
            return "status-finalizada";

        case "Cancelada":
            return "status-cancelada";

        default:
            return "";
    }
}


// ======================
// CONFIRMAR
// ======================

async function confirmarReserva(id) {

    const confirmar = confirm(
        "Deseja confirmar esta reserva?"
    );

    if (!confirmar) return;

    await executarAcaoStatus(
        id,
        "confirmar",
        "Reserva confirmada com sucesso"
    );
}


// ======================
// HOSPEDAR
// ======================

async function hospedarReserva(id) {

    const confirmar = confirm(
        "Deseja marcar esta reserva como hospedada?"
    );

    if (!confirmar) return;

    await executarAcaoStatus(
        id,
        "hospedar",
        "Reserva hospedada com sucesso"
    );
}


// ======================
// FINALIZAR
// ======================

async function finalizarReserva(id) {

    const confirmar = confirm(
        "Deseja finalizar esta reserva?"
    );

    if (!confirmar) return;

    await executarAcaoStatus(
        id,
        "finalizar",
        "Reserva finalizada com sucesso"
    );
}


// ======================
// CANCELAR
// ======================

async function cancelarReserva(id) {

    const confirmar = confirm(
        "Deseja cancelar esta reserva?"
    );

    if (!confirmar) return;

    await executarAcaoStatus(
        id,
        "cancelar",
        "Reserva cancelada com sucesso"
    );
}


// ======================
// EXECUTAR AÇÃO DE STATUS
// ======================

async function executarAcaoStatus(
    id,
    acao,
    mensagemSucesso
) {

    try {

        const response = await fetch(
            `${API_URL}/reservas/${id}/${acao}`,
            {
                method: "PUT"
            }
        );

        const dados =
            await response.json();

        if (!response.ok) {

            alert(
                dados.detail ||
                `Erro ao ${acao} a reserva`
            );

            return;
        }

        alert(mensagemSucesso);

        await carregarReservas();

    } catch (erro) {

        console.error(
            `Erro ao ${acao} reserva:`,
            erro
        );

        alert(
            "Não foi possível realizar a operação."
        );
    }
}


// ======================
// PAGINAÇÃO
// ======================

function atualizarPaginacaoUI() {

    const elemento =
        document.getElementById(
            "infoPaginaReservas"
        );

    if (!elemento) return;

    const totalPaginas =
        Math.max(
            1,
            Math.ceil(
                reservasCache.length /
                itensPorPagina
            )
        );

    elemento.innerText =
        `Página ${paginaAtual} de ${totalPaginas}`;
}


window.proximaPaginaReservas =
    function () {

        const totalPaginas =
            Math.ceil(
                reservasCache.length /
                itensPorPagina
            );

        if (
            paginaAtual <
            totalPaginas
        ) {

            paginaAtual++;

            renderizarPagina();
        }
    };


window.paginaAnteriorReservas =
    function () {

        if (paginaAtual > 1) {

            paginaAtual--;

            renderizarPagina();
        }
    };


// ======================
// PESQUISA
// ======================

async function pesquisarReservas() {

    const termo =
        document
            .getElementById(
                "pesquisaReserva"
            )
            ?.value
            .trim();

    if (!termo) {

        await carregarReservas();

        return;
    }

    try {

        const response =
            await fetch(
                `${API_URL}/reservas/pesquisar/${encodeURIComponent(termo)}`
            );

        if (!response.ok) {

            throw new Error(
                "Erro ao pesquisar reservas"
            );
        }

        reservasCache =
            await response.json();

        paginaAtual = 1;

        renderizarPagina();

    } catch (erro) {

        console.error(
            "Erro ao pesquisar reservas:",
            erro
        );

    }
}


// ======================
// CRIAR RESERVA
// ======================

document
    .getElementById("formReserva")
    ?.addEventListener(
        "submit",
        async (e) => {

            e.preventDefault();

            const servicosSelecionados = [];

            document
                .querySelectorAll(
                    ".checkbox-servico:checked"
                )
                .forEach(checkbox => {

                    servicosSelecionados.push(
                        Number(checkbox.value)
                    );

                });

            const reserva = {

                tutor_id:
                    Number(
                        document
                            .getElementById("tutor")
                            ?.value
                    ),

                quarto_id:
                    Number(
                        document
                            .getElementById("quarto")
                            ?.value
                    ),

                check_in:
                    document
                        .getElementById("checkin")
                        ?.value,

                check_out:
                    document
                        .getElementById("checkout")
                        ?.value,

                servicos:
                    servicosSelecionados

            };

            try {

                const response =
                    await fetch(
                        `${API_URL}/reservas`,
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(
                                    reserva
                                )
                        }
                    );

                const dados =
                    await response.json();

                if (!response.ok) {

                    alert(
                        dados.detail ||
                        "Erro ao criar reserva"
                    );

                    return;
                }

                alert(
                    "Reserva criada com sucesso!"
                );

                document
                    .getElementById(
                        "formReserva"
                    )
                    .reset();

                document
                    .getElementById(
                        "valorTotal"
                    )
                    .innerText =
                    "R$ 0.00";

                await carregarReservas();

            } catch (erro) {

                console.error(
                    "Erro ao criar reserva:",
                    erro
                );

                alert(
                    "Não foi possível criar a reserva."
                );
            }

        }
    );


// ======================
// INIT
// ======================

carregarTutores();
carregarQuartos();
carregarServicos();
carregarReservas();