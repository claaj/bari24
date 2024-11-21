import sys
from bari24.lexer import Lexer
from bari24.parser import Parser
from bari24.translator import Translator

usage = f"Uso: {sys.argv[0]} archivo...\n\
\tSi se da mas de un archivo se ejecutan en orden"

if len(sys.argv) < 2:
    print("Error fatal: no hay archivo de entrada", file=sys.stderr)
    print(usage, file=sys.stderr)

for archivo in sys.argv[1:]:
    interpreter = Translator(Parser(Lexer(archivo)))
    for _ in interpreter:
        pass
