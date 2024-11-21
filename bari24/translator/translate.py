from bari24.parser import Parser, TipoSentencia, Sentencia
from sys import stderr, exit


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
