from bari24.lexer import Lexer
from bari24.parser import Parser
from bari24.translator import Translator
import os


class TestTranslate:
    def test_carga(self):
        temp = open("tests/resources/test.bari24", "w")
        temp.write("CARGA tests/resources/temp1.csv , v\n"
                   + "GUARDA tests/resources/temp2.csv , v\n"
                   + "GUARDA tests/resources/temp3.csv , v , ;\n")
        temp.close()
        contenido = "nombre,edad,apellido\njuan,15,paz\nmaría,20,sirio\n"
        temp = open("tests/resources/temp1.csv", "w")
        temp.write(contenido)
        temp.close()
        translator = Translator(Parser(Lexer("tests/resources/test.bari24")))
        for _ in translator:
            pass
        temp = open("tests/resources/temp1.csv", "r")
        temp1 = temp.read()
        temp.close()
        temp = open("tests/resources/temp2.csv", "r")
        temp2 = temp.read()
        temp.close()
        temp = open("tests/resources/temp3.csv", "r")
        temp3 = temp.read()
        temp.close()
        os.remove("tests/resources/test.bari24")
        os.remove("tests/resources/temp1.csv")
        os.remove("tests/resources/temp2.csv")
        os.remove("tests/resources/temp3.csv")
        assert temp1 == temp2
        assert temp1 == temp3.replace(';', ',')

    def test_separa(self):
        temp = open("tests/resources/test.bari24", "w")
        temp.write("CARGA tests/resources/temp.csv , v\n"
                   + "SEPARA v , v1 , apellido\n"
                   + "SEPARA v , v2 , 3\n")
        temp.close()
        contenido = "nombre,edad,apellido\njuan,15,paz\nmaría,20,sirio\n"
        temp = open("tests/resources/temp.csv", "w")
        temp.write(contenido)
        temp.close()
        esperado = [["apellido"], ["paz"], ["sirio"]]
        translator = Translator(Parser(Lexer("tests/resources/test.bari24")))
        for _ in translator:
            pass
        os.remove("tests/resources/test.bari24")
        os.remove("tests/resources/temp.csv")
        assert translator.simbolos['v1'] == esperado
        assert translator.simbolos['v2'] == esperado

    def test_agrega(self):
        temp = open("tests/resources/test.bari24", "w")
        temp.write("CARGA tests/resources/temp1.csv , v1\n"
                   + "CARGA tests/resources/temp2.csv , v2\n"
                   + "AGREGA v1 , v2\n"
                   + "GUARDA tests/resources/temp3.csv , v1\n")
        temp.close()
        contenido = "nombre,edad\njuan,15\nmaría,20\n"
        temp = open("tests/resources/temp1.csv", "w")
        temp.write(contenido)
        temp.close()
        contenido = "apellido\npaz\nsirio\n"
        temp = open("tests/resources/temp2.csv", "w")
        temp.write(contenido)
        temp.close()
        contenido = "nombre,edad,apellido\njuan,15,paz\nmaría,20,sirio\n"
        temp = open("tests/resources/temp4.csv", "w")
        temp.write(contenido)
        temp.close()
        translator = Translator(Parser(Lexer("tests/resources/test.bari24")))
        for _ in translator:
            pass
        temp = open("tests/resources/temp3.csv", "r")
        temp3 = temp.read()
        temp.close()
        temp = open("tests/resources/temp4.csv", "r")
        temp4 = temp.read()
        temp.close()
        os.remove("tests/resources/test.bari24")
        os.remove("tests/resources/temp1.csv")
        os.remove("tests/resources/temp2.csv")
        os.remove("tests/resources/temp3.csv")
        os.remove("tests/resources/temp4.csv")
        assert temp3 == temp4

    def test_encabezado(self, capsys):
        temp = open("tests/resources/test.bari24", "w")
        temp.write("CARGA tests/resources/temp.csv , v\n"
                   + "ENCABEZADO v\n")
        temp.close()
        contenido = "nombre,edad,apellido\njuan,15,paz\nmaría,20,sirio\n"
        temp = open("tests/resources/temp.csv", "w")
        temp.write(contenido)
        temp.close()
        translator = Translator(Parser(Lexer("tests/resources/test.bari24")))
        for _ in translator:
            pass
        os.remove("tests/resources/test.bari24")
        os.remove("tests/resources/temp.csv")
        captured = capsys.readouterr()
        assert captured.out == "nombre\tedad\tapellido\t\n"

    def test_todo(self, capsys):
        temp = open("tests/resources/test.bari24", "w")
        temp.write("CARGA tests/resources/temp.csv , v\n"
                   + "TODO v , 5\n")
        temp.close()
        contenido = "nombre,edad,apellido\njuan,15,paz\nmaría,20,sirio\n"
        temp = open("tests/resources/temp.csv", "w")
        temp.write(contenido)
        temp.close()
        translator = Translator(Parser(Lexer("tests/resources/test.bari24")))
        for _ in translator:
            pass
        os.remove("tests/resources/test.bari24")
        os.remove("tests/resources/temp.csv")
        captured = capsys.readouterr()
        assert captured.out == contenido.replace(
            ',', '\t').replace('\n', '\t\n')
