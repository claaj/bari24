import sys
from sys import stderr, exit
from typing import List, Tuple, Set
from enum import Enum, auto
import re


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


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexi = lexer

    def __iter__(self):
        return self

    def parse_valor(self, valor: List[Token]) -> List[str | int]:
        ret = []
        for index, token in enumerate(valor):
            if index % 2 == 1:
                app = token.valor
                if token.tipo == TipoToken.NUMERO:
                    app = int(app)
                ret.append(app)
        return ret

    def __next__(self) -> Sentencia:
        tipo = TipoSentencia.INVALIDO
        valor = []
        linea = -1
        try:
            next_token = self.lexi.__next__()
            if next_token.tipo == TipoToken.KEYWORD:
                linea = next_token.num_linea
                match next_token.valor:
                    case "CARGA":
                        (valida, val) = self.Ca()
                        valor = [next_token, *val]
                        if valida:
                            tipo = TipoSentencia.CARGA
                            valor = self.parse_valor(valor)
                        pass
                    case "GUARDA":
                        (valida, val) = self.Ga()
                        valor = [next_token, *val]
                        if valida:
                            tipo = TipoSentencia.GUARDA
                            valor = self.parse_valor(valor)
                        pass
                    case "SEPARA":
                        (valida, val) = self.Sa()
                        valor = [next_token, *val]
                        if valida:
                            tipo = TipoSentencia.SEPARA
                            valor = self.parse_valor(valor)
                        pass
                    case "AGREGA":
                        (valida, val) = self.Aa()
                        valor = [next_token, *val]
                        if valida:
                            tipo = TipoSentencia.AGREGA
                            valor = self.parse_valor(valor)
                        pass
                    case "ENCABEZADO":
                        (valida, val) = self.Ea()
                        valor = [next_token, *val]
                        if valida:
                            tipo = TipoSentencia.ENCABEZADO
                            valor = self.parse_valor(valor)
                        pass
                    case "TODO":
                        (valida, val) = self.Ta()
                        valor = [next_token, *val]
                        if valida:
                            tipo = TipoSentencia.TODO
                            valor = self.parse_valor(valor)
                        pass
        except ():
            pass
        return Sentencia(tipo, valor, linea)

    def Ca(self) -> Tuple[bool, List[Token]]:
        try:
            next_token = self.lexi.__next__()
            if next_token.tipo == TipoToken.NOMBREARCHIVO:
                (valida, val) = self.Cb()
                return (valida, [next_token, *val])
            return self.abortar(next_token)
        except ():
            return (False, [])

    def Cb(self) -> Tuple[bool, List[Token]]:
        try:
            next_token = self.lexi.__next__()
            if next_token.tipo == TipoToken.SEPARADOR:
                if next_token.valor == ",":
                    (valida, val) = self.Cc()
                    return (valida, [next_token, *val])
            return self.abortar(next_token)
        except ():
            return (False, [])

    def Cc(self) -> Tuple[bool, List[Token]]:
        try:
            next_token = self.lexi.__next__()
            if next_token.tipo == TipoToken.VARIABLE:
                (valida, val) = self.Cd()
                return (valida, [next_token, *val])
            return self.abortar(next_token)
        except ():
            return (False, [])

    def Cd(self) -> Tuple[bool, List[Token]]:
        try:
            next_token = self.lexi.__next__()
            if next_token.tipo == TipoToken.SEPARADOR:
                if next_token.valor == ",":
                    (valida, val) = self.Ce()
                    return (valida, [next_token, *val])
            if next_token.tipo == TipoToken.FINDELINEA:
                return (True, [])
            return self.abortar(next_token)
        except ():
            return (False, [])

    def Ce(self) -> Tuple[bool, List[Token]]:
        try:
            next_token = self.lexi.__next__()
            if next_token.tipo == TipoToken.SEPARADOR:
                (valida, val) = self.finSentencia()
                return (valida, [next_token, *val])
            return self.abortar(next_token)
        except ():
            return (False, [])

    def Ga(self) -> Tuple[bool, List[Token]]:
        try:
            next_token = self.lexi.__next__()
            if next_token.tipo == TipoToken.NOMBREARCHIVO:
                (valida, val) = self.Gb()
                return (valida, [next_token, *val])
            return self.abortar(next_token)
        except ():
            return (False, [])

    def Gb(self) -> Tuple[bool, List[Token]]:
        try:
            next_token = self.lexi.__next__()
            if next_token.tipo == TipoToken.SEPARADOR:
                if next_token.valor == ",":
                    (valida, val) = self.Gc()
                    return (valida, [next_token, *val])
            return self.abortar(next_token)
        except ():
            return (False, [])

    def Gc(self) -> Tuple[bool, List[Token]]:
        try:
            next_token = self.lexi.__next__()
            if next_token.tipo == TipoToken.VARIABLE:
                (valida, val) = self.Gd()
                return (valida, [next_token, *val])
            return self.abortar(next_token)
        except ():
            return (False, [])

    def Gd(self) -> (bool, [Token]):
        try:
            next_token = self.lexi.__next__()
            if next_token.tipo == TipoToken.SEPARADOR:
                if next_token.valor == ",":
                    (valida, val) = self.Ge()
                    return (valida, [next_token, *val])
            if next_token.tipo == TipoToken.FINDELINEA:
                return (True, [])
            return self.abortar(next_token)
        except ():
            return self.finSentencia()

    def Ge(self) -> Tuple[bool, List[Token]]:
        try:
            next_token = self.lexi.__next__()
            if next_token.tipo == TipoToken.SEPARADOR:
                (valida, val) = self.finSentencia()
                return (valida, [next_token, *val])
            return self.abortar(next_token)
        except ():
            return (False, [])

    def Sa(self) -> Tuple[bool, List[Token]]:
        try:
            next_token = self.lexi.__next__()
            if next_token.tipo == TipoToken.VARIABLE:
                (valida, val) = self.Sb()
                return (valida, [next_token, *val])
            return self.abortar(next_token)
        except ():
            return (False, [])

    def Sb(self) -> (bool, [Token]):
        try:
            next_token = self.lexi.__next__()
            if next_token.tipo == TipoToken.SEPARADOR:
                if next_token.valor == ",":
                    (valida, val) = self.Sc()
                    return (valida, [next_token, *val])
            return self.abortar(next_token)
        except ():
            return (False, [])

    def Sc(self) -> (bool, [Token]):
        try:
            next_token = self.lexi.__next__()
            if next_token.tipo == TipoToken.VARIABLE:
                (valida, val) = self.Sd()
                return (valida, [next_token, *val])
            return self.abortar(next_token)
        except ():
            return (False, [])

    def Sd(self) -> (bool, [Token]):
        try:
            next_token = self.lexi.__next__()
            if next_token.tipo == TipoToken.SEPARADOR:
                if next_token.valor == ",":
                    (valida, val) = self.Se()
                    return (valida, [next_token, *val])
            return self.abortar(next_token)
        except ():
            return (False, [])

    def Se(self) -> (bool, [Token]):
        try:
            next_token = self.lexi.__next__()
            if next_token.tipo == TipoToken.VARIABLE:
                (valida, val) = self.finSentencia()
                return (valida, [next_token, *val])
            if next_token.tipo == TipoToken.NUMERO:
                (valida, val) = self.finSentencia()
                return (valida, [next_token, *val])
            return self.abortar(next_token)
        except ():
            return (False, [])

    def Aa(self) -> (bool, [Token]):
        try:
            next_token = self.lexi.__next__()
            if next_token.tipo == TipoToken.VARIABLE:
                (valida, val) = self.Ab()
                return (valida, [next_token, *val])
            return self.abortar(next_token)
        except ():
            return (False, [])

    def Ab(self) -> (bool, [Token]):
        try:
            next_token = self.lexi.__next__()
            if next_token.tipo == TipoToken.SEPARADOR:
                if next_token.valor == ",":
                    (valida, val) = self.Ac()
                    return (valida, [next_token, *val])
            return self.abortar(next_token)
        except ():
            return (False, [])

    def Ac(self) -> (bool, [Token]):
        try:
            next_token = self.lexi.__next__()
            if next_token.tipo == TipoToken.VARIABLE:
                (valida, val) = self.finSentencia()
                return (valida, [next_token, *val])
            return self.abortar(next_token)
        except ():
            return (False, [])

    def Ea(self) -> (bool, [Token]):
        try:
            next_token = self.lexi.__next__()
            if next_token.tipo == TipoToken.VARIABLE:
                (valida, val) = self.finSentencia()
                return (valida, [next_token, *val])
            return self.abortar(next_token)
        except ():
            return (False, [])

    def Ta(self) -> (bool, [Token]):
        try:
            next_token = self.lexi.__next__()
            if next_token.tipo == TipoToken.VARIABLE:
                (valida, val) = self.Tb()
                return (valida, [next_token, *val])
            return self.abortar(next_token)
        except ():
            return (False, [])

    def Tb(self) -> (bool, [Token]):
        try:
            next_token = self.lexi.__next__()
            if next_token.tipo == TipoToken.SEPARADOR:
                if next_token.valor == ",":
                    (valida, val) = self.Tc()
                    return (valida, [next_token, *val])
            return self.abortar(next_token)
        except ():
            return (False, [])

    def Tc(self) -> (bool, [Token]):
        try:
            next_token = self.lexi.__next__()
            if next_token.tipo == TipoToken.NUMERO:
                (valida, val) = self.finSentencia()
                return (valida, [next_token, *val])
            return self.abortar(next_token)
        except ():
            return (False, [])

    def finSentencia(self) -> (bool, [Token]):
        try:
            next_token = self.lexi.__next__()
            if next_token.tipo == TipoToken.FINDELINEA:
                return (True, [])
        except ():
            pass
        return (False, [])

    def abortar(self, next_token: Token) -> (bool, [Token]):
        if next_token.tipo == TipoToken.FINDELINEA:
            return (False, [])
        (_, lista) = self.abortar(self.lexi.__next__())
        return (False, [next_token, *lista])


class Translator:
    def __init__(self, parser: Parser):
        self.parser = parser
        self.simbolos = {}

    def __iter__(self):
        return self

    def intersperse(self, lst, item):
        result = [item] * (len(lst) * 2 - 1)
        result[0::2] = lst
        return result

    def carga(self, nomArch: str, nomVar: str, separdor: str = ','):
        tabla = []
        file = open(nomArch, "r")
        for line in file.readlines():
            tabla.append(line.strip().split(separdor))
        self.simbolos[nomVar] = tabla
        return

    def guarda(self, nomArch: str, nomVar: str, separdor: str = ','):
        tabla = self.simbolos[nomVar]
        file = open(nomArch, "w")
        for line in tabla:
            put = self.intersperse(line, separdor)
            for word in put:
                file.write(word)
            file.write('\n')
        return

    def separa(self, srcVar: str, dstVar: str, columna: str | int):
        src = self.simbolos[srcVar]
        dst = []
        col_num = -1
        if isinstance(columna, str):
            for col, val in enumerate(src[0]):
                if val == columna:
                    col_num = col
                    break
        else:
            col_num = int(columna) - 1
        for line in src:
            dst.append([line[col_num]])
        self.simbolos[dstVar] = dst
        return

    def agrega(self, dstVar: str, srcVar: str):
        src = self.simbolos[srcVar]
        dst = self.simbolos[dstVar]
        if len(src) != len(dst):
            print(f"{dstVar} y {
                srcVar} no son compatibles para agregar", file=stderr)
            exit(1)
        if len(src[0]) != 1:
            print(
                f"{srcVar} no es una tabla de una sola columna para agregar",
                file=stderr)
            exit(1)
        for i in range(len(src)):
            dst[i].append(src[i][0])
        self.simbolos[dstVar] = dst
        return

    def encabezado(self, var: str):
        tabla = self.simbolos[var]
        for val in tabla[0]:
            print(val, end='\t')
        print()
        return

    def todo(self, var: str, paginacion: int):
        tabla = self.simbolos[var]
        index = 0
        while index + paginacion < len(tabla):
            for _ in range(paginacion):
                for val in tabla[index]:
                    print(val, end='\t')
                print()
                index += 1
            input()
        for _ in range(index, len(tabla)):
            for val in tabla[index]:
                print(val, end='\t')
            print()
            index += 1
        return

    def func(self, sentencia: Sentencia):
        match sentencia.tipo:
            case TipoSentencia.CARGA:
                return self.carga
            case TipoSentencia.GUARDA:
                return self.guarda
            case TipoSentencia.SEPARA:
                return self.separa
            case TipoSentencia.AGREGA:
                return self.agrega
            case TipoSentencia.ENCABEZADO:
                return self.encabezado
            case TipoSentencia.TODO:
                return self.todo
            case _:
                print(
                    f"Error de sintaxis: {sentencia}",
                    file=stderr)
                exit(1)

    def __next__(self):
        sentencia = self.parser.__next__()
        funcion = self.func(sentencia)
        funcion(*sentencia.valor)


usage = f"Uso: {sys.argv[0]} archivo...\n\
\tSi se da mas de un archivo se ejecutan en orden"

if len(sys.argv) < 2:
    print("Error fatal: no hay archivo de entrada", file=sys.stderr)
    print(usage, file=sys.stderr)

for archivo in sys.argv[1:]:
    interpreter = Translator(Parser(Lexer(archivo)))
    for _ in interpreter:
        pass
