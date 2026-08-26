const API_URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", () => {

    let quartosCache = [];
    let paginaAtual = 1;
    const itensPorPagina = 5;

    async function carregarQuartos() {

        try {

            const response = await fetch(`${API_URL}/quartos`);

            if (!response.ok) {
                throw new Error("Erro ao carregar quartos");
            }

            quartosCache = await response.json();

            paginaAtual = 1;

            renderizarPagina();

        } catch (erro) {
            console.error("Erro ao carregar quartos:", erro);
        }
    }

    function renderizarPagina() {

        const tabela = document.getElementById("tabelaQuartos");

        if (!tabela) return;

        tabela.innerHTML = "";

        const inicio = (paginaAtual - 1) * itensPorPagina;
        const fim = inicio + itensPorPagina;

        const pagina = quartosCache.slice(inicio, fim);

        pagina.forEach(quarto => {

            tabela.innerHTML += `
                <tr>
                    <td>${quarto.id}</td>
                    <td>${quarto.numero}</td>
                    <td>${quarto.tipo_quarto}</td>
                    <td>R$ ${quarto.preco}</td>
                    <td>
                        <button onclick="deletarQuarto(${quarto.id})">
                            Deletar
                        </button>
                    </td>
                </tr>
            `;

        });

        atualizarPaginacaoUI();
    }

    function atualizarPaginacaoUI() {

        const info = document.getElementById("infoPaginaQuartos");

        if (!info) return;

        const totalPaginas = Math.ceil(quartosCache.length / itensPorPagina);

        info.innerText = `Página ${paginaAtual} de ${totalPaginas}`;
    }

    window.proximaPaginaQuartos = function () {

        const totalPaginas = Math.ceil(quartosCache.length / itensPorPagina);

        if (paginaAtual < totalPaginas) {
            paginaAtual++;
            renderizarPagina();
        }
    }

    window.paginaAnteriorQuartos = function () {

        if (paginaAtual > 1) {
            paginaAtual--;
            renderizarPagina();
        }
    }

    async function pesquisarQuartos() {

        const input = document.getElementById("pesquisaQuarto");
        if (!input) return;

        const btnPesquisar = document.getElementById(
        "btnPesquisarQuarto"
        );

        if (btnPesquisar) {
            btnPesquisar.addEventListener(
                "click",
                pesquisarQuartos
            );
        }

        const quarto = input.value;

        try {

            if (!quarto) {
                carregarQuartos();
                return;
            }

            const response = await fetch(
                `${API_URL}/quartos/pesquisar/${quarto}`
            );

            if (!response.ok) {
                throw new Error("Erro ao pesquisar quartos");
            }

            const quartos = await response.json();

            quartosCache = quartos;
            paginaAtual = 1;

            renderizarPagina();

        } catch (erro) {
            console.error("Erro ao pesquisar quartos:", erro);
        }

    }

    const form = document.getElementById("formQuarto");

    if (form) {

        form.addEventListener("submit", async (e) => {

            e.preventDefault();

            const numeroEl = document.getElementById("numero");
            const tipoEl = document.getElementById("tipo_quarto");

            const quarto = {
                numero: parseInt(numeroEl.value),
                tipo_quarto: tipoEl.value
            };

            try {

                const response = await fetch(`${API_URL}/quartos`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(quarto)
                });

                if (!response.ok) {
                    throw new Error("Erro ao cadastrar quarto");
                }

                form.reset();
                carregarQuartos();

            } catch (erro) {
                console.error("Erro:", erro);
            }

        });

    }

    window.deletarQuarto = async function (id) {

        const confirmar = confirm("Deseja deletar este quarto?");
        if (!confirmar) return;

        try {

            const response = await fetch(`${API_URL}/quartos/${id}`, {
                method: "DELETE"
            });

            if (!response.ok) {
                throw new Error("Erro ao deletar quarto");
            }

            carregarQuartos();

        } catch (erro) {
            console.error("Erro ao deletar quarto:", erro);
        }
    };
    const pesquisa = document.getElementById("pesquisaQuarto");

    if (pesquisa) {
        pesquisa.addEventListener("keyup", pesquisarQuartos);
    }

    carregarQuartos();

});