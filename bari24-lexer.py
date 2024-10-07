import re
from enum import Enum, auto
from typing import List, Set, Tuple


class TipoToken(Enum):
    VARIABLE = auto()
    NUMERO = auto()
    KEYWORD = auto()
    SEPARADOR = auto()
    NOMBREARCHIVO = auto()
    ASIGNACION = auto()


class Token:
    def __init__(self, tipo: TipoToken, valor: str, linea: int):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea

    def __repr__(self) -> str:
        return f"Token(Tipo: {self.tipo}, Valor: {self.valor}, Linea: {self.linea})"


class TokenInvalido:
    def __init__(self, valor: str, linea: int):
        self.valor = valor
        self.linea = linea

    def __repr__(self) -> str:
        return f"TokenInvalido(Valor: {self.valor}, Linea: {self.linea})"


class Lexer:
    KEYWORDS: Set[str] = {"CARGA", "GUARDA", "SEPARA", "AGREGA", "ENCABEZADO", "TODO"}
    SEPARADORES: Set[str] = {",", ";"}

    def __init__(self, ruta_archivo: str):
        self.ruta_archivo = ruta_archivo
        self.linea_actual = 0
        self.invalidos: List[TokenInvalido] = []

    def analizar(self) -> Tuple[List[Token], List[TokenInvalido]]:
        tokens = []
        with open(self.ruta_archivo, "r") as archivo:
            for linea in archivo:
                self.linea_actual += 1
                linea = linea.strip()

                if not linea or linea.startswith("@"):
                    continue

                tokens.extend(self.analizar_linea(linea))
        return tokens, self.invalidos

    def analizar_linea(self, linea: str) -> List[Token]:
        tokens = []
        palabras = linea.split()
        for palabra in palabras:
            tipo_actual: TipoToken
            if palabra in self.KEYWORDS:
                tipo_actual = TipoToken.KEYWORD
            elif palabra.endswith(".csv"):
                tipo_actual = TipoToken.NOMBREARCHIVO
            elif re.match(r"^[a-z][a-z0-9]{0,9}$", palabra):
                tipo_actual = TipoToken.VARIABLE
            elif palabra.isdigit():
                tipo_actual = TipoToken.NUMERO
            elif palabra in self.SEPARADORES:
                tipo_actual = TipoToken.SEPARADOR
            elif palabra == "=":
                tipo_actual = TipoToken.ASIGNACION
            else:
                self.invalidos.append(TokenInvalido(palabra, self.linea_actual))
                continue
            tokens.append(Token(tipo_actual, palabra, self.linea_actual))
        return tokens


if __name__ == "__main__":
    lexi = Lexer("pruebas.bari24")
    tokens, invalidos = lexi.analizar()

    for token in tokens:
        print(token)

    for invalido in invalidos:
        print(invalido)
