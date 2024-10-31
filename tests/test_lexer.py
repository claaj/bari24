import pytest

from bari24.lexer import Lexer, TipoToken, Token


class TestLexer:
    def test_variables(self):
        lexer = Lexer("tests/resources/variables.bari24")

        tokens = list(lexer)

        esperados = [
            Token(TipoToken.VARIABLE, "valido10", 1),
            Token(TipoToken.SEPARADOR, ",", 1),
            Token(TipoToken.NUMERO, "10", 1),
            Token(TipoToken.FINDELINEA, "", 1),
            Token(TipoToken.INVALIDO, "10novalido", 2),
            Token(TipoToken.FINDELINEA, "", 2),
            Token(TipoToken.FINDELINEA, "", 3),
            Token(TipoToken.FINDELINEA, "", 4),
            Token(TipoToken.FINDELINEA, "", 5),
            Token(TipoToken.FINDELINEA, "", 6),
            Token(TipoToken.FINDELINEA, "", 7),
            Token(TipoToken.FINDELINEA, "", 8),
            Token(TipoToken.INVALIDO, "noVálido20", 9),
            Token(TipoToken.FINDELINEA, "", 9),
            Token(TipoToken.VARIABLE, "valido20", 10),
            Token(TipoToken.FINDELINEA, "", 10),
        ]

        assert len(tokens) == len(esperados)

        for token, esperado in zip(tokens, esperados):
            assert token.__eq__(esperado) is True

    def test_comentarios(self):
        lexer = Lexer("tests/resources/comentarios.bari24")

        tokens = list(lexer)

        esperados = [
            Token(TipoToken.KEYWORD, "CARGA", 2),
            Token(TipoToken.SEPARADOR, ",", 2),
            Token(TipoToken.VARIABLE, "variable1", 2),
            Token(TipoToken.FINDELINEA, "", 2),
            Token(TipoToken.FINDELINEA, "", 3),
            Token(TipoToken.KEYWORD, "SEPARA", 5),
            Token(TipoToken.FINDELINEA, "", 5),
            Token(TipoToken.FINDELINEA, "", 6),
            Token(TipoToken.KEYWORD, "ENCABEZADO", 8),
            Token(TipoToken.FINDELINEA, "", 8),
        ]

        assert len(tokens) == len(esperados)

        for token, esperado in zip(tokens, esperados):
            assert token.__eq__(esperado) is True

    def test_programa_simple(self):
        lexer = Lexer("tests/resources/pruebas.bari24")
        tokens = list(lexer)

        esperados = [
            Token(TipoToken.KEYWORD, "CARGA", 1),
            Token(TipoToken.NOMBREARCHIVO, "archivo1.csv", 1),
            Token(TipoToken.FINDELINEA, "", 1),
            Token(TipoToken.KEYWORD, "SEPARA", 3),
            Token(TipoToken.SEPARADOR, ",", 3),
            Token(TipoToken.FINDELINEA, "", 3),
            Token(TipoToken.KEYWORD, "AGREGA", 4),
            Token(TipoToken.VARIABLE, "columna1", 4),
            Token(TipoToken.FINDELINEA, "", 4),
            Token(TipoToken.INVALIDO, "INVALIDO", 5),
            Token(TipoToken.INVALIDO, "acá", 5),
            Token(TipoToken.FINDELINEA, "", 5),
            Token(TipoToken.KEYWORD, "GUARDA", 6),
            Token(TipoToken.NOMBREARCHIVO, "archivo2.csv", 6),
            Token(TipoToken.FINDELINEA, "", 6),
            Token(TipoToken.FINDELINEA, "", 7),
            Token(TipoToken.VARIABLE, "variable1", 8),
            Token(TipoToken.SEPARADOR, ",", 8),
            Token(TipoToken.NUMERO, "10", 8),
            Token(TipoToken.FINDELINEA, "", 8),
            Token(TipoToken.INVALIDO, "ójo23", 9),
            Token(TipoToken.FINDELINEA, "", 9),
        ]

        assert len(tokens) == len(esperados)

        for token, esperado in zip(tokens, esperados):
            assert token.__eq__(esperado) is True
