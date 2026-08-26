const API_URL = "http://127.0.0.1:8000";

let tutoresCache = [];
let paginaAtual = 1;

const itensPorPagina = 5;


// =========================================================
// CARREGAR TUTORES
// =========================================================

async function carregarTutores() {

    try {

        const response = await fetch(
            `${API_URL}/tutores`
        );

        if (!response.ok) {
            throw new Error(
                "Erro ao carregar tutores"
            );
        }

        tutoresCache = await response.json();

        paginaAtual = 1;

        renderizarPagina();

    } catch (erro) {

        console.error(
            "Erro ao carregar tutores:",
            erro
        );

    }
}


// =========================================================
// RENDERIZAR TABELA
// =========================================================

function renderizarPagina() {

    const tabela = document.getElementById(
        "tabelaTutores"
    );

    tabela.innerHTML = "";

    const inicio =
        (paginaAtual - 1) * itensPorPagina;

    const fim =
        inicio + itensPorPagina;

    const pagina =
        tutoresCache.slice(inicio, fim);


    pagina.forEach(tutor => {

        tabela.innerHTML += `
            <tr>

                <td>${tutor.id}</td>

                <td>${tutor.nome}</td>

                <td>${tutor.documento}</td>

                <td>${tutor.telefone}</td>

                <td>${tutor.email}</td>

                <td class="acoes">

                    <button
                        class="btn-excluir"
                        onclick="deletarTutor(${tutor.id})"
                    >
                        Excluir
                    </button>

                </td>

            </tr>
        `;

    });

    atualizarPaginacaoUI();
}


// =========================================================
// PAGINAÇÃO
// =========================================================

function atualizarPaginacaoUI() {

    const totalPaginas = Math.max(
        1,
        Math.ceil(
            tutoresCache.length / itensPorPagina
        )
    );

    document.getElementById(
        "infoPagina"
    ).innerText =
        `Página ${paginaAtual} de ${totalPaginas}`;
}


function proximaPagina() {

    const totalPaginas = Math.ceil(
        tutoresCache.length / itensPorPagina
    );

    if (paginaAtual < totalPaginas) {

        paginaAtual++;

        renderizarPagina();
    }
}


function paginaAnterior() {

    if (paginaAtual > 1) {

        paginaAtual--;

        renderizarPagina();
    }
}


// =========================================================
// DELETAR TUTOR
// =========================================================

async function deletarTutor(id) {

    const confirmar = confirm(
        "Tem certeza que deseja excluir este tutor?"
    );

    if (!confirmar) {
        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/tutores/${id}`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {

            const erro = await response.json();

            throw new Error(
                erro.detail ||
                "Erro ao excluir tutor"
            );
        }

        await carregarTutores();

    } catch (erro) {

        console.error(
            "Erro ao excluir tutor:",
            erro
        );

        alert(erro.message);

    }
}


// =========================================================
// CADASTRAR TUTOR
// =========================================================

document
    .getElementById("formTutor")
    .addEventListener(
        "submit",
        async (e) => {

            e.preventDefault();


            const tutor = {

                nome:
                    document
                        .getElementById("nome")
                        .value,

                documento:
                    document
                        .getElementById("documento")
                        .value,

                telefone:
                    document
                        .getElementById("telefone")
                        .value,

                email:
                    document
                        .getElementById("email")
                        .value

            };


            try {

                const response = await fetch(
                    `${API_URL}/tutores`,
                    {

                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify(
                            tutor
                        )

                    }
                );


                if (!response.ok) {

                    const erro =
                        await response.json();

                    throw new Error(
                        erro.detail ||
                        "Erro ao cadastrar tutor"
                    );
                }


                document
                    .getElementById("formTutor")
                    .reset();


                await carregarTutores();


            } catch (erro) {

                console.error(
                    "Erro ao cadastrar tutor:",
                    erro
                );

                alert(erro.message);

            }

        }
    );


// =========================================================
// PESQUISAR TUTORES
// =========================================================

async function pesquisarTutores() {

    const termo =
        document
            .getElementById("pesquisaTutor")
            .value
            .trim();


    try {

        let url;

        if (termo) {

            url =
                `${API_URL}/tutores/buscar/` +
                encodeURIComponent(termo);

        } else {

            url =
                `${API_URL}/tutores`;
        }


        const response =
            await fetch(url);


        if (!response.ok) {

            throw new Error(
                "Erro ao pesquisar tutores"
            );
        }


        const tutores =
            await response.json();


        tutoresCache = tutores;

        paginaAtual = 1;

        renderizarPagina();


    } catch (erro) {

        console.error(
            "Erro ao pesquisar tutores:",
            erro
        );

    }
}


// =========================================================
// INICIALIZAÇÃO
// =========================================================

carregarTutores();