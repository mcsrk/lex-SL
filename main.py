import sys
global col, row
# lee toda la entrada y la guarda en programLines
inputProgram = sys.stdin.readlines()
programLines = [line.rstrip() for line in inputProgram]
operators = {"=": "tk_asignacion",
             ",": "tk_coma",
             "]": "tk_corchete_derecho",
             "[": "tk_corchete_izquierdo",
             "<>": "tk_distinto_de",
             "/": "tk_division",
             ":": "tk_dos_puntos",
             "==": "tk_igual_que",
             "}": "tk_llave_derecha",
             "{": "tk_llave_izquierda",
             ">": "tk_mayor",
             ">=": "tk_mayor_igual",
             "<": "tk_menor",
             "<=": "tk_menor_igual",
             "%": "tk_modulo",
             "*": "tk_multiplicacion",
             ")": "tk_parentesis_derecho",
             "(": "tk_parentesis_izquierdo",
             "^": "tk_potenciacion",
             ".": "tk_punto",
             ";": "tk_punto_y_coma",
             "-": "tk_resta",
             "+": "tk_suma",
             }
keywords = ["and", "archivo", "caso", "const",
            "constantes", "desde", "eval", "fin",
            "hasta", "inicio", "lib", "libext",
            "matriz", "mientras", "not", "or",
            "paso", "subrutina", "programa", "ref",
            "registro", "repetir", "retorna", "si",
            "sino", "tipos", "var", "variables",
            "vector"]
subroutines = ["dim", "imprimir", "cls", "leer", "set_ifs", "abs",
               "arctan", "ascii", "cos", "dec", "eof", "exp", "get_ifs",
               "inc", "int", "log", "lower", "mem", "ord", "paramval",
               "pcount", "pos", "random", "sec", "set_stdin", "set_stdout",
               "sin", "sqrt", "str", "strdup", "strlen", "substr", "tan", "upper", "val"]
dataTypes = ["cadena", "logico", "numerico"]


def isReservedWord(token):

    return (
        token in keywords
        or token in subroutines
        or token in dataTypes
    )


def logKeywordOrOperator(tkName, r, c):
    # puede ser <tk_asignacion,9,12>
    # puede ser <tk_parentesis_izquierdo,6,14>
    print(f"<{tkName},{r},{c}>")


def logStringOrId(id, val, r, c):
    # puede ser <id,n,3,5>
    # puede ser <tk_cadena,"La suma es ",13,15>
    print(f"<{id},{val},{r},{c}>")


def isItEmpty(val):
    empties = [' ', '\n', '\t']
    return val in empties


col, row = 0, 0
token = ''
for line in programLines:
    col = 1
    row += 1
    token = ''
    # si no es una linea vacía
    if(line):
        # print("LINEA: ", line)
        for col in range(len(line)):
            if (not isItEmpty(line[col])):
                token += line[col]
            else:
                token = ''
            # es comentario
            if(token == "/"):
                if(line[col+1] == "/"):
                    continue
            # es string
            # es operador
                # if(line[col] in operators):
                #     logKeywordOrOperator(operators[line[col]], row, col)
            # es palabra reservada

            if (isReservedWord(token)):
                logKeywordOrOperator(token, row, col+2-len(token))
                token = ''
            # es entero
            # es decimal
            # es id
        # print(f"{row} hay linea")
    col = 0
