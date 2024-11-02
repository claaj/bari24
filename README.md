# Bari24 - TP Final Compiladores e Interpretes

## Lexer

### Tipos de Lexemas:

- `nomVariable` ::= combinación de no más de 10 caracteres de letras minúsculas y números. Iniciando con letra
- `nomArch` ::= cualquier nombre de archivo
- `separador` ::= `,` | `;`
- `numero` ::= número natural y `0`
- `coma`::= ,
- `palabraReservadas>`::= `CARGA` | `GUARDA` | `SEPARA` | `AGREGA` | `ENCABEZADO` | `TODO`

### Características generales:

- Una sentencia por línea.
- Cada sentencia puede estar en una única línea.
- Separador blanco únicamente.
- Los blancos de más son prescindibles.
- Comentarios ocupan una línea y van marcados con `@` al inicio.
- No hay límite de cantidad de sentencias en un programa.
- El programa vendrá en un archivo plano.
- `CARGA`, `GUARDA`, `SEPARA`, `AGREGA`, `ENCABEZADO`, `TODO` son palabras reservadas del lenguaje.

## Parser

### Sintaxis del lenguaje:

- `CARGA`::= **CARGA**`<nomArch>`**,**`<nomVariable>`[**,**`<separador>`]
- `GUARDA`::= **GUARDA**`<nomArch>`**,**`<nomVariable>`[**,**`<separador>`]
- `SEPARA`::= **SEPARA**`<nomVariable1>`**,**`<nomVariable2>`**,**(`<nomColumna>`|`<numColumna>`)
- `AGREGA`::= **AGREGA**`<nomVariable1>`**,**`<nomVariable2>`
- `ENCABEZADO`::= **ENCABEZADO**`<nomVariable>`
- `TODO`::= **TODO**`<nomVariable>`**,**`<cantLineas>`
- `<cantLineas>,<numColumna>`::= `<numero>`

## Probrar el proyecto

Hasta ahora el proyecto esta en proceso.
Por lo tanto tan solo es posible correr los tests.

Test soportados al momento:
- Lexer

Para poder probar el proyecto es necesario setear el entorno de desarrollo.

### 1. Clonar el repo.

~~~sh
git clone git@github.com:claaj/bari24.git && cd bari24
~~~

O con `https`:

~~~sh
git clone https://github.com/claaj/bari24.git && cd bari24
~~~


### 2. Crear y setear ambiente virtual

~~~sh
python -m venv .venv && source .venv/bin/activate
~~~

Luego es necesario instalar las dependencias:

~~~sh
pip install -r requirements.txt
~~~

### 3. Correr los test

Para correr los tests es necesario ejecutar el siguente comando:

~~~sh
pytest tests/ -vvv -s
~~~
