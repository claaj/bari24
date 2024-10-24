from enum import Enum, auto


class TipoToken(Enum):
    VARIABLE = auto()
    NUMERO = auto()
    KEYWORD = auto()
    SEPARADOR = auto()
    NOMBREARCHIVO = auto()
    INVALIDO = auto()
    FINDELINEA = auto()


class Token:
    def __init__(self, tipo: TipoToken, valor: str, linea: int):
        self.tipo = tipo
        self.valor = valor
        self.num_linea = linea

    def __repr__(self) -> str:
        return (
            f"Token(Tipo: {self.tipo}, Valor: {self.valor},"
            + f" Linea: {self.num_linea})"
        )
