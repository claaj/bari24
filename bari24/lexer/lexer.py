import re
from typing import Set, List

from .tipos import TipoToken, Token


class Lexer:
    KEYWORDS: Set[str] = {"CARGA", "GUARDA", "SEPARA", "AGREGA", "ENCABEZADO", "TODO"}
    SEPARADORES: Set[str] = {",", ";"}

    def __init__(self, ruta_archivo: str):
        self.archivo = open(ruta_archivo, "r")
        self.linea_actual = 0
        self.simbolos = {}
        self.tokens_actuales = self.obtener_linea()

    def analizar(self, palabra: str) -> Token:
        tipo_actual: TipoToken
        if palabra in self.KEYWORDS:
            tipo_actual = TipoToken.KEYWORD
        elif palabra.endswith(".csv"):
            tipo_actual = TipoToken.NOMBREARCHIVO
        elif re.match(r"^[a-z][a-z0-9]{0,9}$", palabra):
            tipo_actual = TipoToken.VARIABLE
            self.simbolos[palabra] = None
        elif palabra.isdigit():
            tipo_actual = TipoToken.NUMERO
        elif palabra in self.SEPARADORES:
            tipo_actual = TipoToken.SEPARADOR
        else:
            tipo_actual = TipoToken.INVALIDO
        return Token(tipo_actual, palabra, self.linea_actual)

    def __iter__(self):
        return self

    def obtener_linea(self) -> List[str]:
        while True:
            linea = self._leer_siguiente_linea()
            if not linea:
                raise StopIteration()

            if not self._es_comentario(linea):
                self.linea_actual += 1
                return linea

    def _leer_siguiente_linea(self) -> List[str]:
        linea = self.archivo.readline()
        if not linea:
            return []
        return linea.strip().split()

    def _es_comentario(self, linea: List[str]) -> bool:
        return len(linea) > 0 and linea[0].startswith("@")

    def __next__(self) -> Token:
        if len(self.tokens_actuales) == 0:
            self.tokens_actuales = self.obtener_linea()
            return Token(TipoToken.FINDELINEA, "", self.linea_actual)

        siguiente_token = self.tokens_actuales.pop(0)

        return self.analizar(siguiente_token)