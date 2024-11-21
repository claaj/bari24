from bari24.lexer import Lexer, TipoToken, Token
from bari24.parser import Parser, Sentencia, TipoSentencia


class TestParser:
    def test_carga(self):
        parser = Parser(Lexer("tests/resources/cargas.bari24"))

        sentencias = list(parser)

        esperados = [
            Sentencia(TipoSentencia.CARGA, [
                      "arch1.csv",
                      "arch1"
                      ], 1),
            Sentencia(TipoSentencia.CARGA, [
                      "arch2.csv",
                      "arch2",
                      ",",
                      ], 2),
            Sentencia(TipoSentencia.CARGA, [
                      "arch3.csv",
                      "arch3",
                      ";",
                      ], 3),
            Sentencia(TipoSentencia.INVALIDO, [
                      Token(TipoToken.KEYWORD, "CARGA", 4),
                      Token(TipoToken.VARIABLE, "arch4", 4),
                      Token(TipoToken.SEPARADOR, ",", 4),
                      Token(TipoToken.NOMBREARCHIVO, "arch4.csv", 4),
                      Token(TipoToken.SEPARADOR, ",", 4),
                      Token(TipoToken.SEPARADOR, ";", 4),
                      ], 4),
            Sentencia(TipoSentencia.INVALIDO, [
                      Token(TipoToken.KEYWORD, "CARGA", 5),
                      Token(TipoToken.NOMBREARCHIVO, "arch5.csv", 5),
                      Token(TipoToken.SEPARADOR, ";", 5),
                      Token(TipoToken.VARIABLE, "arch5", 5),
                      ], 5),
        ]

        assert len(sentencias) == len(esperados)

        for sentencia, esperado in zip(sentencias, esperados):
            assert sentencia.__eq__(esperado) is True

    def test_guarda(self):
        parser = Parser(Lexer("tests/resources/guardas.bari24"))

        sentencias = list(parser)

        esperados = [
            Sentencia(TipoSentencia.GUARDA, [
                      "arch1.csv",
                      "arch1",
                      ], 1),
            Sentencia(TipoSentencia.GUARDA, [
                      "arch2.csv",
                      "arch2",
                      ",",
                      ], 2),
            Sentencia(TipoSentencia.GUARDA, [
                      "arch3.csv",
                      "arch3",
                      ";",
                      ], 3),
            Sentencia(TipoSentencia.INVALIDO, [
                      Token(TipoToken.KEYWORD, "GUARDA", 4),
                      Token(TipoToken.VARIABLE, "arch4", 4),
                      Token(TipoToken.SEPARADOR, ",", 4),
                      Token(TipoToken.NOMBREARCHIVO, "arch4.csv", 4),
                      Token(TipoToken.SEPARADOR, ",", 4),
                      Token(TipoToken.SEPARADOR, ";", 4),
                      ], 4),
            Sentencia(TipoSentencia.INVALIDO, [
                      Token(TipoToken.KEYWORD, "GUARDA", 5),
                      Token(TipoToken.NOMBREARCHIVO, "arch5.csv", 5),
                      Token(TipoToken.SEPARADOR, ";", 5),
                      Token(TipoToken.VARIABLE, "arch5", 5),
                      ], 5),
        ]

        assert len(sentencias) == len(esperados)

        for sentencia, esperado in zip(sentencias, esperados):
            assert sentencia.__eq__(esperado) is True

    def test_separa(self):
        parser = Parser(Lexer("tests/resources/separas.bari24"))

        sentencias = list(parser)

        esperados = [
            Sentencia(TipoSentencia.SEPARA, [
                      "var11",
                      "var12",
                      "var13",
                      ], 1),
            Sentencia(TipoSentencia.SEPARA, [
                      "var21",
                      "var22",
                      3,
                      ], 2),
            Sentencia(TipoSentencia.INVALIDO, [
                      Token(TipoToken.KEYWORD, "SEPARA", 3),
                      Token(TipoToken.VARIABLE, "var31", 3),
                      Token(TipoToken.SEPARADOR, ",", 3),
                      Token(TipoToken.VARIABLE, "var32", 3),
                      Token(TipoToken.SEPARADOR, ";", 3),
                      Token(TipoToken.NUMERO, "3", 3),
                      ], 3),
        ]

        assert len(sentencias) == len(esperados)

        for sentencia, esperado in zip(sentencias, esperados):
            assert sentencia.__eq__(esperado) is True

    def test_agrega(self):
        parser = Parser(Lexer("tests/resources/agregas.bari24"))

        sentencias = list(parser)

        esperados = [
            Sentencia(TipoSentencia.AGREGA, [
                      "var11",
                      "var12",
                      ], 1),
            Sentencia(TipoSentencia.INVALIDO, [
                      Token(TipoToken.KEYWORD, "AGREGA", 2),
                      Token(TipoToken.VARIABLE, "var21", 2),
                      Token(TipoToken.SEPARADOR, ";", 2),
                      Token(TipoToken.VARIABLE, "var22", 2),
                      ], 2),
            Sentencia(TipoSentencia.INVALIDO, [
                      Token(TipoToken.KEYWORD, "AGREGA", 3),
                      Token(TipoToken.VARIABLE, "var31", 3),
                      Token(TipoToken.SEPARADOR, ",", 3),
                      Token(TipoToken.NOMBREARCHIVO, "var32.csv", 3),
                      ], 3),
        ]

        assert len(sentencias) == len(esperados)

        for sentencia, esperado in zip(sentencias, esperados):
            assert sentencia.__eq__(esperado) is True

    def test_encabezado(self):
        parser = Parser(Lexer("tests/resources/encabezados.bari24"))

        sentencias = list(parser)

        esperados = [
            Sentencia(TipoSentencia.ENCABEZADO, [
                      "var1",
                      ], 1),
            Sentencia(TipoSentencia.INVALIDO, [
                      Token(TipoToken.KEYWORD, "ENCABEZADO", 2),
                      Token(TipoToken.NOMBREARCHIVO, "var2.csv", 2),
                      ], 2),
        ]

        assert len(sentencias) == len(esperados)

        for sentencia, esperado in zip(sentencias, esperados):
            assert sentencia.__eq__(esperado) is True

    def test_todo(self):
        parser = Parser(Lexer("tests/resources/todos.bari24"))

        sentencias = list(parser)

        esperados = [
            Sentencia(TipoSentencia.TODO, [
                      "var1",
                      5,
                      ], 1),
            Sentencia(TipoSentencia.INVALIDO, [
                      Token(TipoToken.KEYWORD, "TODO", 2),
                      Token(TipoToken.VARIABLE, "var21", 2),
                      Token(TipoToken.SEPARADOR, ",", 2),
                      Token(TipoToken.VARIABLE, "var22", 2),
                      ], 2),
            Sentencia(TipoSentencia.INVALIDO, [
                      Token(TipoToken.KEYWORD, "TODO", 3),
                      Token(TipoToken.VARIABLE, "var3", 3),
                      Token(TipoToken.SEPARADOR, ";", 3),
                      Token(TipoToken.NUMERO, "5", 3),
                      ], 3),
            Sentencia(TipoSentencia.INVALIDO, [
                      Token(TipoToken.KEYWORD, "TODO", 4),
                      Token(TipoToken.NOMBREARCHIVO, "var4.csv", 4),
                      Token(TipoToken.SEPARADOR, ",", 4),
                      Token(TipoToken.NUMERO, "5", 4),
                      ], 4),
        ]

        assert len(sentencias) == len(esperados)

        for sentencia, esperado in zip(sentencias, esperados):
            assert sentencia.__eq__(esperado) is True
