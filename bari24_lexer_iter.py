import re
from enum import Enum, auto
from typing import Set


class TipoToken(Enum):
    VARIABLE = auto()
    NUMERO = auto()
    KEYWORD = auto()
    SEPARADOR = auto()
    NOMBREARCHIVO = auto()
    ASIGNACION = auto()
    INVALIDO = auto()


class Token:
    def __init__(self, tipo: TipoToken, valor: str, linea: int):
        self.tipo = tipo
        self.valor = valor
        self.num_linea = linea

    def __repr__(self) -> str:
        return f"Token(Tipo: {self.tipo}, Valor: {self.valor}," \
            + f" Linea: {self.num_linea})"


class Lexer:
    KEYWORDS: Set[str] = {"CARGA", "GUARDA",
                          "SEPARA", "AGREGA", "ENCABEZADO", "TODO"}
    SEPARADORES: Set[str] = {",", ";"}

    def __init__(self, ruta_archivo: str, simbol_table: dict):
        self.archivo = open(ruta_archivo, "r")
        self.linea_actual = 0
        self.simbols = simbol_table
        self.linea_cache = []
        self.token_cache = 0

    def analizar(self, palabra: str) -> Token:
        tipo_actual: TipoToken
        if palabra in self.KEYWORDS:
            tipo_actual = TipoToken.KEYWORD
        elif palabra.endswith(".csv"):
            tipo_actual = TipoToken.NOMBREARCHIVO
        elif re.match(r"^[a-z][a-z0-9]{0,9}$", palabra):
            tipo_actual = TipoToken.VARIABLE
            self.simbols[palabra] = None
        elif palabra.isdigit():
            tipo_actual = TipoToken.NUMERO
        elif palabra in self.SEPARADORES:
            tipo_actual = TipoToken.SEPARADOR
        elif palabra == "=":
            tipo_actual = TipoToken.ASIGNACION
        else:
            tipo_actual = TipoToken.INVALIDO
        return Token(tipo_actual, palabra, self.linea_actual)

    def __iter__(self):
        return self

    def __next__(self) -> Token:
        if len(self.linea_cache) == self.token_cache:
            self.token_cache = 0
            self.linea_cache = ["@"]
            while len(self.linea_cache) == 0\
                or (len(self.linea_cache) > 0
                    and self.linea_cache[0].startswith("@")):
                self.linea_cache = self.archivo.readline()
                if not self.linea_cache:
                    raise StopIteration()
                self.linea_cache = self.linea_cache.strip().split()
                self.linea_actual += 1
        token = self.analizar(self.linea_cache[self.token_cache])
        self.token_cache += 1
        return token


if __name__ == "__main__":
    simbols = {}
    lexi = Lexer("pruebas.bari24", simbols)

    for tokens in lexi:
        print(tokens)

    print(simbols)