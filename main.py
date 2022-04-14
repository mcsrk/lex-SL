import sys
# lee toda la entrada y la guarda en programLines como una lista de listas
inputProgram = sys.stdin.readlines()
programLines = []
for line in inputProgram:
    newLineAsList = list(line.strip(""))
    newLineAsList.append("\n")
    programLines.append(newLineAsList)

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


def error(r, c):
    return ">>> Error lexico (linea: " + str(r) + ", posicion: " + str(c) + ")"


def isOperator(token): return token in operators


def isQuotes(token): return token == "\"" or token == "'"


def isJumpline(c): return c == '\n'


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
    empties = [' ', '\n', '\t', '\r']
    return val in empties


col, row = 0, 0
token = ''
comment = False
moveForward = 0

for line in programLines:
    col = 0
    row += 1
    # si no es una linea vacía de esas que son señuelos
    if(line):
        for col in range(len(line)):
            if moveForward != 0:
                if moveForward > 0:
                    moveForward -= 1
                    continue

            if comment:
                if line[col] == "*" and line[col+1] == "/":
                    moveForward += 1
                    comment = False
                    continue

            if comment == False:

                # es comentario
                if(line[col] == "/"):
                    if(line[col+1] == "/"):
                        break
                    elif (line[col+1] == "*"):
                        comment = True
                        break

                # es string
                elif(isQuotes(line[col])):
                    string = '"'
                    stringPos = col+1
                    while not isQuotes(line[1 + col]) and not isJumpline(line[1 + col]):
                        if not isQuotes(line[1+col]):
                            if not isJumpline(line[1 + col]):
                                string = string + line[1 + col]
                                moveForward += 1
                                col += 1

                    if isQuotes(line[1 + col]):
                        string = string + line[1 + col]
                        moveForward += 1
                        logStringOrId("tk_cadena", string, row, stringPos)
                    else:
                        print(error(row, 1 + col))
                        sys.exit()
                # es operador
                elif(isOperator(line[col])):
                    # revisa el siguiente char para saber si es un op más largo
                    if(col+1 < len(line)):
                        op = line[col] + line[col+1]
                        opPos = col
                        if(isOperator(op)):
                            moveForward += 1
                            logKeywordOrOperator(operators[op], row, opPos)
                        else:
                            logKeywordOrOperator(
                                operators[line[col]], row, col+1)

                # es entero
                # es decimal
                # es alpha o _
                elif (line[col] == "_" or line[col].isalpha()):
                    idName = line[col]
                    idPos = col+1
                    # obtiene toda la continuidad de caracteres
                    while(line[col+1].isalpha() or line[col+1] == "_" or line[col+1].isdigit()):
                        idName += line[col+1]
                        col += 1
                        moveForward += 1
                    # es palabra reservada
                    if isReservedWord(idName):
                        logKeywordOrOperator(idName, row, idPos)
                    # es otra cosa
                    else:
                        logStringOrId('id', idName, row, idPos)
                elif isItEmpty(line[col]):
                    continue
            # print(f"{row} hay linea")
    col = 0
