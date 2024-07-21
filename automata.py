import re

# PALABRAS RESERVADAS
IMPORT = 'import'
RETURN = 'return'
DEF = 'def'
ELSE = 'else'
PRINT = 'print'
BREAK = 'break'
CONTINUE = 'continue'
FOR = 'for'
IN = 'in'
RANGE = 'range'
LEN = 'len'
IF = 'if'
ELIF = 'elif'
AND = 'and'
OR = 'or'
NOT = 'not'

# SIMBOLOS TERMINALES
ID = r'[a-zA-Z][a-zA-Z0-9_]*'
NUM = r'[0-9]+'
VACIO = r'^$'
BOOL = r'\b(True|False)\b'
SIGNO_ASIGNACION = r'\='
SIGNOS_LOGICOS = rf'({AND}|{OR})'
SIGNOS_COMPARACION_CARACTER = r'(==|!=)'
SIGNOS_COMPARACION_NUMEROS = r'(<=|>=|<|>)'
SIGNOS_COMPARACION = rf'({SIGNOS_COMPARACION_CARACTER}|{SIGNOS_COMPARACION_NUMEROS})'
SIGNOS_OPERACION = r'(\+|\-|\*|\/|\%)'

# SIMBOLOS NO TERMINALES
AS = rf'as {ID}'
VAL_ID_NUM = rf'((?!{BOOL}){ID}|{NUM})'
OPERACION = rf'({VAL_ID_NUM}\s*{SIGNOS_OPERACION}\s*{VAL_ID_NUM}|{VAL_ID_NUM})'
PARAMETROS = rf'{ID}(,\s*{ID})*'
RANGE_ITER = rf'{RANGE}\({NUM}\)'
LEN_ITER = rf'{LEN}\({RANGE_ITER}\)|{LEN}\({ID}\)'
ITER = rf'({RANGE_ITER}|{LEN_ITER}|{ID})'
CONDICION_NUMERICA = rf'({OPERACION})\s*{SIGNOS_COMPARACION}\s*({OPERACION}|\"{VAL_ID_NUM}\"|\'{VAL_ID_NUM}\')'
CONDICION_CARACTER = rf'{ID}\s*{SIGNOS_COMPARACION_CARACTER}\s*({BOOL}|{ID}|\"{ID}\"|\'{ID}\')'
COND = rf'({CONDICION_NUMERICA}|{CONDICION_CARACTER}|{ID})'

# GRAMATICA
IMPORT_GRAMATICA = rf'^{IMPORT} {ID}$|^{IMPORT} {ID} {AS}$'
RETURN_GRAMATICA = rf'^\s*{RETURN} ({BOOL}|{ID}|{NUM}|\'{ID}\')$'
DEF_GRAMATICA = rf'^\s*{DEF} {ID}\(\):$|^{DEF} {ID}\({PARAMETROS}\):$'
ELSE_GRAMATICA = rf'^\s*{ELSE}:$'
VARIABLE_GRAMATICA = rf'^\s*{ID}\s*{SIGNO_ASIGNACION}\s*({ID}|\'{ID}\'|{NUM})$'
PRINT_GRAMATICA = rf'^\s*{PRINT}\(({ID}|\'{ID}\'|\"{ID}\"|{NUM})\)$'
BREAK_GRAMATICA = rf'^\s*{BREAK}$'
CONTINUE_GRAMATICA = rf'^\s*{CONTINUE}$'
FOR_GRAMATICA = rf'^\s*{FOR} {ID} {IN} {ITER}:$'
IF_GRAMATICA = rf'^\s*{IF}\s*\(?({NOT}\s*{COND}|{COND})(\s*{SIGNOS_LOGICOS}\s*{COND})*\)?:$'
ELIF_GRAMATICA = rf'^\s*{ELIF}\s*\(?({COND})(\s*{SIGNOS_LOGICOS}\s*{COND})*\)?:$'


# Funciones
def evaluar(lineas):
    resultados = []

    for i, linea in enumerate(lineas):
        if not linea.strip():
            continue

        palabras = re.findall(r'\w+|\(|\)', linea)
        if palabras:
            primera_palabra = palabras[0]
            print(primera_palabra)
            gramatica = None
            if primera_palabra == 'import':
                gramatica = IMPORT_GRAMATICA
            elif primera_palabra == 'return':
                gramatica = RETURN_GRAMATICA
            elif primera_palabra == 'def':
                gramatica = DEF_GRAMATICA
            elif primera_palabra == 'for':
                gramatica = FOR_GRAMATICA
            elif primera_palabra == 'if':
                gramatica = IF_GRAMATICA
            elif primera_palabra == 'elif':
                gramatica = ELIF_GRAMATICA
            elif primera_palabra == 'else':
                gramatica = ELSE_GRAMATICA
            elif primera_palabra == 'print':
                gramatica = PRINT_GRAMATICA
            elif primera_palabra == 'break':
                gramatica = BREAK_GRAMATICA
            elif primera_palabra == 'continue':
                gramatica = CONTINUE_GRAMATICA
            elif re.match(ID, primera_palabra) != None:
                gramatica = VARIABLE_GRAMATICA

        if not gramatica:
            resultados.append([f"La linea {linea} NO esta bien escrita", "no"])
        else:
            print(gramatica)
            resultado = re.match(gramatica, linea)
            if resultado != None:
                resultados.append(
                    [f"La linea {linea} esta bien escrita", "ok"])
            else:
                resultados.append(
                    [f"La linea {linea} NO esta bien escrita", "no"])

        continue

    return resultados


# DEPURACION
assert re.match(VARIABLE_GRAMATICA, 'd = d') != None
assert re.match(VARIABLE_GRAMATICA, 'd = d0') != None
assert re.match(VARIABLE_GRAMATICA, 'd = 10') != None
assert re.match(VARIABLE_GRAMATICA, '0 = 10') == None
assert re.match(VARIABLE_GRAMATICA, 'd = dsds') != None

assert re.match(ELSE_GRAMATICA, 'else:') != None

assert re.match(DEF_GRAMATICA, 'def hola():') != None
assert re.match(DEF_GRAMATICA, 'def hola(xd):') != None
assert re.match(DEF_GRAMATICA, 'def hola(xd, h):') != None

assert re.match(RETURN_GRAMATICA, 'return 10') != None
assert re.match(RETURN_GRAMATICA, 'return True') != None
assert re.match(RETURN_GRAMATICA, 'return hola') != None
assert re.match(RETURN_GRAMATICA, 'return False') != None
assert re.match(RETURN_GRAMATICA, 'return hola10') != None
assert re.match(RETURN_GRAMATICA, 'return \'hola\'') != None

assert re.match(IMPORT_GRAMATICA, 'import df') != None
assert re.match(IMPORT_GRAMATICA, 'import df as d') != None

assert re.match(PRINT_GRAMATICA, 'print(10)') != None
assert re.match(PRINT_GRAMATICA, 'print(hola)') != None
assert re.match(PRINT_GRAMATICA, 'print(\'hola\')') != None

assert re.match(BREAK_GRAMATICA, 'break') != None
assert re.match(CONTINUE_GRAMATICA, 'continue') != None

assert re.match(IF_GRAMATICA, 'if(hola):') != None
assert re.match(IF_GRAMATICA, 'if(hola==0):') != None
assert re.match(IF_GRAMATICA, 'if(hola>15):') != None
assert re.match(IF_GRAMATICA, 'if(hola<= 10):') != None
assert re.match(IF_GRAMATICA, 'if(hola> True):') == None
assert re.match(IF_GRAMATICA, 'if(hola == xd):') != None
assert re.match(IF_GRAMATICA, 'if(hola <= True):') == None
assert re.match(IF_GRAMATICA, 'if(hola == 10 and re):') != None
assert re.match(IF_GRAMATICA, 'if(hola == 10 and re == 10):') != None
assert re.match(IF_GRAMATICA, 'if(hola == 10 and re == \'0\'):') != None
assert re.match(IF_GRAMATICA, 'if(hola == 10 and re == \'wsa\'):') != None
