from enum import Enum, auto
from typing import List
from bari24.lexer import Token


class TipoSentencia(Enum):
    CARGA = auto()
    GUARDA = auto()
    SEPARA = auto()
    AGREGA = auto()
    ENCABEZADO = auto()
    TODO = auto()
    INVALIDO = auto()


class Sentencia:
    def __init__(self, tipo: TipoSentencia, valor: List[Token], linea: int):
        self.tipo = tipo
        self.valor = valor
        self.num_linea = linea

    def __repr__(self) -> str:
        return (
            f"Sentencia(Tipo: {self.tipo}, Valor: {self.valor},"
            + f" Linea: {self.num_linea})"
        )

    def __eq__(self, otro: object) -> bool:
        return (
            hasattr(otro, "tipo")
            and hasattr(otro, "valor")
            and hasattr(otro, "num_linea")
            and self.tipo == otro.tipo
            and self.valor == otro.valor
            and self.num_linea == otro.num_linea
        )
