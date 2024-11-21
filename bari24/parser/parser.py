# Tokens:
# VARIABLE
# NUMERO
# KEYWORD
# SEPARADOR
# NOMBREARCHIVO
# INVALIDO


# Parse := KEYWORD(CARGA) Ca
#        | KEYWORD(GUARDA) Ga
#        | KEYWORD(SEPARA) Sa
#        | KEYWORD(AGREGA) Aa
#        | KEYWORD(ENCABEZADO) Ea
#        | KEYWORD(TODO) Ta


# Ca := NOMBREARCHIVO Cb
# Cb := SEPARADOR(,) Cc
# Cc := VARIABLE Cd
# Cd := SEPARADOR(,) Ce | λ
# Ce := SEPARADOR


# Ga := NOMBREARCHIVO Gb
# Gb := SEPARADOR(,) Gc
# Gc := VARIABLE Gd
# Gd := SEPARADOR(,) Ge | λ
# Ge := SEPARADOR


# Sa := VARIABLE Sb
# Sb := SEPARADOR(,) Sc
# Sc := VARIABLE Sd
# Sd := SEPARADOR(,) Se
# Se := VARIABLE | NUMERO


# Aa := VARIABLE Ab
# Ab := SEPARADOR(,) Ac
# Ac := VARIABLE


# Ea := VARIABLE


# Ta := VARIABLE Tb
# Tb := SEPARADOR(,) Tc
# Tc := NUMERO

from typing import List, Tuple
from .tipos import Sentencia, TipoSentencia
from bari24.lexer import Lexer, TipoToken, Token


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
