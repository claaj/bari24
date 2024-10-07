# TP-Compiladores-Interpretes

## Lexer
### Tipos de Lexemas:
\<nomVariable\> ::= combinación de no más de 10 caracteres de letras minúsculas y números. Iniciando con letra\
\<nomArch\> ::= cualquier nombre de archivo\
\<separador\> ::= , | ;\
\<numero\> ::= número natural y 0\
\<coma\>::= ,\
\<palabraReservadas\>::= CARGA | GUARDA | SEPARA | AGREGA | ENCABEZADO | TODO\
### Características generales:
Una sentencia por línea. Cada sentencia puede estar en una única línea.\
Separador blanco únicamente. Los blancos de más son prescindibles\
Comentarios ocupan una línea y van marcados con @ al inicio\
No hay límite de cantidad de sentencias en un programa\
El programa vendrá en un archivo plano\
CARGA, GUARDA, SEPARA, AGREGA, ENCABEZADO, TODO son palabras reservadas del lenguaje.\
