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

    def __eq__(self, otro: object) -> bool:
        return (
            hasattr(otro, "tipo")
            and hasattr(otro, "valor")
            and hasattr(otro, "num_linea")
            and self.tipo == otro.tipo
            and self.valor == otro.valor
            and self.num_linea == otro.num_linea
        )
