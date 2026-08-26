from pydantic import BaseModel


class QuartoSchema(BaseModel):

    numero: int
    tipo: str