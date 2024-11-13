from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship, UniqueConstraint
from typing import Optional, List


class Evento(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("epicentro_lat", "epicentro_lon", "descricao"),)

    id: int | None = Field(default=None, primary_key=True)
    data: datetime
    epicentro_lat: float
    epicentro_lon: float
    descricao: str


class CorpoDagua(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("nome", "tipo"),)

    id: int | None = Field(default=None, primary_key=True)
    nome: str
    tipo: str


class Fluxo(SQLModel, table=True):
    origem_id: int = Field(foreign_key="corpodagua.id", primary_key=True)
    destino_id: int = Field(foreign_key="corpodagua.id", primary_key=True)


class TipoPoluente(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("nome"),)

    id: int | None = Field(default=None, primary_key=True)
    nome: str


class Poluente(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("nome"),)

    id: int | None = Field(default=None, primary_key=True)
    nome: str
    dl50: float | None = None
    tipo_poluente_id: int = Field(foreign_key="tipopoluente.id")


class Emissao(SQLModel, table=True):
    evento_id: int = Field(foreign_key="evento.id", primary_key=True)
    poluente_id: int = Field(foreign_key="poluente.id", primary_key=True)
    corpodagua_id: int = Field(foreign_key="corpodagua.id", primary_key=True)


class Organismo(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("nome_popular"), UniqueConstraint("especie"),)

    id: int | None = Field(default=None, primary_key=True)
    nome_popular: str
    reino: str | None = None
    filo: str | None = None
    classe: str | None = None
    ordem: str | None = None
    familia: str | None = None
    genero: str | None = None
    especie: str | None = None


class Compatibilidade(SQLModel, table=True):
    poluente_id: int = Field(foreign_key="poluente.id", primary_key=True)
    organismo_id: int = Field(foreign_key="organismo.id", primary_key=True)


class Predacao(SQLModel, table=True):
    presa_id: int = Field(foreign_key="organismo.id", primary_key=True)
    predador_id: int = Field(foreign_key="organismo.id", primary_key=True)


class Habitat(SQLModel, table=True):
    organismo_id: int = Field(foreign_key="organismo.id", primary_key=True)
    corpodagua_id: int = Field(foreign_key="corpodagua.id", primary_key=True)
