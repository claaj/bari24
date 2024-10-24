import re
from typing import Set

from tipos import TipoToken, Token


class Lexer:
    KEYWORDS: Set[str] = {"CARGA", "GUARDA", "SEPARA", "AGREGA", "ENCABEZADO", "TODO"}
    SEPARADORES: Set[str] = {",", ";"}

    def __init__(self, ruta_archivo: str, simbol_table: dict):
        self.archivo = open(ruta_archivo, "r")
        self.linea_actual = 0
        self.simbols = simbol_table
        self.linea_cache = []
        self.token_cache = 0
        self.get_line()

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
        else:
            tipo_actual = TipoToken.INVALIDO
        return Token(tipo_actual, palabra, self.linea_actual)

    def __iter__(self):
        return self

    def get_line(self):
        self.token_cache = 0
        self.linea_cache = ["@"]
        while len(self.linea_cache) == 0 or (
            len(self.linea_cache) > 0 and self.linea_cache[0].startswith("@")
        ):
            self.linea_cache = self.archivo.readline()
            if not self.linea_cache:
                raise StopIteration()
            self.linea_cache = self.linea_cache.strip().split()
            self.linea_actual += 1

    def __next__(self) -> Token:
        token = ""
        if len(self.linea_cache) == self.token_cache:
            token = Token(TipoToken.FINDELINEA, "", self.linea_actual)
            self.get_line()
        else:
            token = self.analizar(self.linea_cache[self.token_cache])
            self.token_cache += 1
        return token


if __name__ == "__main__":
    simbols = {}
    lexi = Lexer("pruebas.bari24", simbols)

    for tokens in lexi:
        print(tokens)

    print(simbols)
