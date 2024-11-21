import re
from typing import Set, List

from .tipos import TipoToken, Token


class Lexer:
    KEYWORDS: Set[str] = {"CARGA", "GUARDA",
                          "SEPARA", "AGREGA", "ENCABEZADO", "TODO"}
    SEPARADORES: Set[str] = {",", ";"}

    def __init__(self, ruta_archivo: str):
        self.archivo = open(ruta_archivo, "r")
        self.linea_actual = 0
        self.tokens_actuales = self.obtener_linea()
        self.lectura_terminada = False

    def analizar(self, palabra: str) -> Token:
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
        else:
            tipo_actual = TipoToken.INVALIDO
        return Token(tipo_actual, palabra, self.linea_actual)

    def __iter__(self):
        return self

    def obtener_linea(self) -> List[str]:
        while True:
            linea = self.archivo.readline()
            if linea == "":
                self.lectura_terminada = True
                return []

            elif not self._es_comentario(linea):
                self.linea_actual += 1
                return linea.strip().split()

            else:
                self.linea_actual += 1
                continue

    def _es_comentario(self, linea: List[str]) -> bool:
        return len(linea) > 0 and linea[0].startswith("@")

    def __next__(self) -> Token:
        if len(self.tokens_actuales) == 0:
            if self.lectura_terminada:
                self.archivo.close()
                raise StopIteration()

            token_eol = Token(TipoToken.FINDELINEA, "", self.linea_actual)
            self.tokens_actuales = self.obtener_linea()
            return token_eol

        siguiente_token = self.tokens_actuales.pop(0)
        return self.analizar(siguiente_token)
