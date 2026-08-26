from datetime import date
from typing import List

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from controles.quarto_controle import QuartoControle
from controles.tutor_controle import TutorControle
from controles.reserva_controle import ReservaControle

from servico.servico_reserva import ReservaServico

from repositorio.MySQLQuartoRepositorio import MySQLQuartoRepositorio
from repositorio.MySQLTutorRepositorio import MySQLTutorRepositorio
from repositorio.MySQLReservaRepositorio import MySQLReservaRepositorio
from repositorio.MySQLServicoExtraRepositorio import (
    MySQLServicoExtraRepositorio
)


app = FastAPI(
    title="Promissum Palace API",
    version="1.0.0"
)


origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# REPOSITÓRIOS
# =========================================================

servico_extra_repo = MySQLServicoExtraRepositorio()
quarto_repo = MySQLQuartoRepositorio()
tutor_repo = MySQLTutorRepositorio()

reserva_repo = MySQLReservaRepositorio(
    tutor_repo,
    quarto_repo,
    servico_extra_repo
)


# =========================================================
# SERVIÇOS
# =========================================================

reserva_servico = ReservaServico(
    reserva_repo,
    servico_extra_repo
)


# =========================================================
# CONTROLES
# =========================================================

tutor_controle = TutorControle(
    tutor_repo,
    reserva_repo
)

reserva_controle = ReservaControle(
    reserva_repo,
    reserva_servico,
    tutor_repo,
    quarto_repo
)

quarto_controle = QuartoControle(
    quarto_repo,
    reserva_repo
)


# =========================================================
# SCHEMAS
# =========================================================

class QuartoRequest(BaseModel):

    numero: int = Field(
        gt=0,
        description="Número do quarto"
    )

    tipo_quarto: str


class TutorRequest(BaseModel):

    nome: str
    documento: str
    telefone: str
    email: str


class ReservaRequest(BaseModel):

    tutor_id: int = Field(gt=0)
    quarto_id: int = Field(gt=0)

    check_in: date
    check_out: date

    servicos: List[int] = Field(
        default_factory=list
    )


# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================

def _resposta_quarto(quarto):

    return {
        "id": quarto.id,
        "numero": quarto.numero,
        "tipo_quarto": quarto.tipo_quarto.descricao,
        "preco": float(quarto.preco)
    }


def _resposta_tutor(tutor):

    return {
        "id": tutor.id,
        "nome": tutor.nome,
        "documento": tutor.documento,
        "telefone": tutor.telefone,
        "email": tutor.email
    }


def _resposta_servico(servico):

    return {
        "id": servico.id,
        "nome": servico.nome,
        "valor": float(servico.valor)
    }


def _resposta_reserva(reserva):

    return {
        "id": reserva.id,

        "tutor": {
            "id": reserva.tutor.id,
            "nome": reserva.tutor.nome
        },

        "quarto": {
            "id": reserva.quarto.id,
            "numero": reserva.quarto.numero,
            "tipo_quarto": (
                reserva.quarto.tipo_quarto.descricao
            )
        },

        "check_in": str(
            reserva.periodo.check_in
        ),

        "check_out": str(
            reserva.periodo.check_out
        ),

        "status": reserva.status.value,

        "servicos": [
            _resposta_servico(servico)
            for servico in reserva.servicos_extras
        ],

        "valor_total": float(
            reserva.calcular_valor_total()
        )
    }


# =========================================================
# QUARTOS
# =========================================================

@app.post("/quartos")
def criar_quarto(quarto_request: QuartoRequest):

    try:

        quarto = quarto_controle.criar_quarto(
            quarto_request
        )

        return _resposta_quarto(quarto)

    except (ValueError, KeyError) as erro:

        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )


@app.get("/quartos")
def listar_quartos():

    quartos = quarto_controle.listar_quartos()

    return [
        _resposta_quarto(quarto)
        for quarto in quartos
    ]


@app.get("/quartos/pesquisar/{termo}")
def pesquisar_quartos(termo: str):

    quartos = quarto_controle.pesquisar_quartos(
        termo
    )

    return [
        _resposta_quarto(quarto)
        for quarto in quartos
    ]


@app.delete("/quartos/{quarto_id}")
def deletar_quarto(quarto_id: int):

    try:

        quarto_controle.deletar_quarto(
            quarto_id
        )

        return {
            "mensagem": "Quarto deletado com sucesso"
        }

    except ValueError as erro:

        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )


# =========================================================
# TUTORES
# =========================================================

@app.post("/tutores")
def criar_tutor(tutor_request: TutorRequest):

    try:

        tutor = tutor_controle.criar_tutor(
            tutor_request
        )

        return {
            "mensagem": "Tutor criado com sucesso",
            "id": tutor.id,
            "nome": tutor.nome
        }

    except ValueError as erro:

        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )


@app.get("/tutores")
def listar_tutores(
    busca: str = Query(default="")
):

    tutores = tutor_controle.listar_tutores(
        busca
    )

    return [
        _resposta_tutor(tutor)
        for tutor in tutores
    ]


@app.get("/tutores/buscar/{termo}")
def buscar_tutores(termo: str):

    tutores = tutor_controle.buscar_tutores(
        termo
    )

    return [
        _resposta_tutor(tutor)
        for tutor in tutores
    ]


@app.delete("/tutores/{tutor_id}")
def deletar_tutor(tutor_id: int):

    try:

        tutor_controle.deletar_tutor(
            tutor_id
        )

        return {
            "mensagem": "Tutor deletado com sucesso"
        }

    except ValueError as erro:

        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )


# =========================================================
# RESERVAS
# =========================================================

@app.post("/reservas")
def criar_reserva(
    reserva_request: ReservaRequest
):

    try:

        if (
            reserva_request.check_out
            <= reserva_request.check_in
        ):
            raise ValueError(
                "Check-out deve ser após check-in"
            )

        reserva = reserva_controle.criar_reserva(
            reserva_request
        )

        return {
            "mensagem": "Reserva criada com sucesso!",
            "id": reserva.id,
            "valor_total": float(
                reserva.calcular_valor_total()
            )
        }

    except ValueError as erro:

        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )

    except Exception as erro:

        raise HTTPException(
            status_code=500,
            detail=str(erro)
        )


@app.get("/reservas")
def listar_reservas():

    reservas = reserva_controle.listar_reservas()

    return [
        _resposta_reserva(reserva)
        for reserva in reservas
    ]


@app.get("/reservas/pesquisar/{termo}")
def pesquisar_reservas(termo: str):

    reservas = reserva_controle.pesquisar_reservas(
        termo
    )

    return [
        _resposta_reserva(reserva)
        for reserva in reservas
    ]


# =========================================================
# STATUS DAS RESERVAS
# =========================================================

@app.put("/reservas/{reserva_id}/confirmar")
def confirmar_reserva(reserva_id: int):

    try:

        reserva = reserva_controle.confirmar_reserva(
            reserva_id
        )

        return {
            "mensagem": "Reserva confirmada com sucesso",
            "reserva": _resposta_reserva(reserva)
        }

    except ValueError as erro:

        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )


@app.put("/reservas/{reserva_id}/hospedar")
def hospedar_reserva(reserva_id: int):

    try:

        reserva = reserva_controle.hospedar_reserva(
            reserva_id
        )

        return {
            "mensagem": "Tutor hospedado com sucesso",
            "reserva": _resposta_reserva(reserva)
        }

    except ValueError as erro:

        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )


@app.put("/reservas/{reserva_id}/finalizar")
def finalizar_reserva(reserva_id: int):

    try:

        reserva = reserva_controle.finalizar_reserva(
            reserva_id
        )

        return {
            "mensagem": "Reserva finalizada com sucesso",
            "reserva": _resposta_reserva(reserva)
        }

    except ValueError as erro:

        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )


@app.put("/reservas/{reserva_id}/cancelar")
def cancelar_reserva(reserva_id: int):

    try:

        reserva_controle.cancelar_reserva(
            reserva_id
        )

        return {
            "mensagem": "Reserva cancelada com sucesso"
        }

    except ValueError as erro:

        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )


# =========================================================
# SERVIÇOS EXTRAS
# =========================================================

@app.get("/servicos")
def listar_servicos():

    servicos = servico_extra_repo.listar()

    return [
        _resposta_servico(servico)
        for servico in servicos
    ]
