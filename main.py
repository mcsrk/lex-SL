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
            "vector", "TRUE", "FALSE", "SI", "NO"]
subroutines = ["dim", "imprimir", "cls", "leer", "set_ifs", "abs",
               "arctan", "ascii", "cos", "dec", "eof", "exp", "get_ifs",
               "inc", "int", "log", "lower", "mem", "ord", "paramval",
               "pcount", "pos", "random", "sec", "set_stdin", "set_stdout",
               "sin", "sqrt", "str", "strdup", "strlen", "substr", "tan", "upper", "val"]
dataTypes = ["cadena", "logico", "numerico", "alen", "entero"]
invalidChars = ['&', '$']


def error(r, c):
    return ">>> Error lexico(linea:" + str(r) + ",posicion:" + str(c) + ")"


def isOperator(token): return token in operators


def isQuotes(token): return token == "\"" or token == "'"


def isJumpline(c): return c == '\n'


def isReservedWord(token): return (
    token in keywords or token in subroutines or token in dataTypes)


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


col, row, moveForward, token, comment = 0, 0, 0, '', False
index = 0
while index < len(programLines):
    line = programLines[index]
    col = 0
    row += 1
    # si no es una linea vacía de esas que son señuelos
    if(line):
        for col in range(len(line)):
            # print("COL: ", col, "Forward: ", moveForward)
            # si ya se leyó el char anterior
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
                    else:
                        op, opPos = line[col], col
                        if(isOperator(op)):
                            moveForward += 1
                            tkName = operators[op]
                            logKeywordOrOperator(tkName, row, opPos+1)

                # es string
                    # si encuentra una " o una '
                elif(isQuotes(line[col])):
                    string, stringPos = line[col], col+1
                    # obtiene todos los chars antes de encontrar las comillas de cierre o un \n
                    while not line[1 + col] == string[0] and not isJumpline(line[1 + col]):
                        if not line[1 + col] == string[0]:
                            if not isJumpline(line[1 + col]):
                                string = string + line[1 + col]
                                moveForward += 1
                                col += 1
                    # log cuando ecuentra la comilla de cierre correspondinete
                    if line[1 + col] == string[0]:
                        string = string + line[1 + col]
                        moveForward += 1
                        logStringOrId("tk_cadena", string, row, stringPos)
                    # log de error si no encuentra una " de cierre
                    else:
                        print(error(row, stringPos))
                        sys.exit()
                # es operador
                elif(isOperator(line[col])):
                    # revisa el siguiente char para saber si es un op más largo (2 chars)
                    if(col+1 < len(line)):
                        op, opPos = line[col] + line[col+1], col
                        if(isOperator(op)):
                            moveForward += 1
                            tkName = operators[op]
                            logKeywordOrOperator(tkName, row, opPos+1)
                        else:
                            tkName = operators[line[col]]

                            logKeywordOrOperator(tkName, row, opPos+1)

                # es un número
                elif(line[col].isdigit()):
                    enteroPos = col + 1
                    entero = line[col]
                    floatPart = ""
                    powerPart = ""

                    while line[col+1].isdigit():
                        moveForward, entero, col = moveForward + \
                            1, entero+line[col+1], col+1

                    if(line[col+1] == "."):
                        moveForward, col = moveForward+1, col+1
                        if line[col+1].isdigit():
                            while line[col+1].isdigit():
                                floatPart, moveForward, col = floatPart + \
                                    line[col+1], moveForward+1, col+1
                            # busca notacion cientifica
                            if line[col+1] == "e" or line[col+1] == "E":
                                exponent = line[col+1]
                                moveForward += 1
                                col += 1
                                # busca exponentes sin signo y con float. i.e: 5.2e10
                                if line[col+1].isdigit():
                                    while line[col+1].isdigit():
                                        powerPart += line[col+1]
                                        col += 1
                                        moveForward += 1
                                    logStringOrId(
                                        "tk_numero", entero + "."+floatPart+exponent+powerPart, row, enteroPos)

                                elif line[col+1] == "+" or line[col+1] == "-":
                                    exponent += line[col+1]  # e+, e-, E+, E-
                                    col += 1
                                    moveForward += 1
                                    if line[col+1].isdigit():
                                        while line[col+1].isdigit():
                                            powerPart += line[col+1]
                                            col += 1
                                            moveForward += 1
                                        logStringOrId(
                                            "tk_numero", entero + "."+floatPart+exponent+powerPart, row, enteroPos)
                                    else:
                                        error(row, col+1)
                                else:
                                    error(row, col+1)
                            else:
                                logStringOrId("tk_numero", entero +
                                              "."+floatPart, row, enteroPos)
                        else:
                            error(row, col+1)
                    elif line[col+1] == "e" or line[col+1] == "E":
                        exponent = line[col+1]
                        moveForward += 1
                        col += 1
                        # busca exponentes sin signo y sin float. i.e: 2e9
                        if line[col+1].isdigit():
                            while line[col+1].isdigit():
                                powerPart += line[col+1]
                                col += 1
                                moveForward += 1
                            logStringOrId(
                                "tk_numero", entero + exponent+powerPart, row, enteroPos)

                        elif line[col+1] == "+" or line[col+1] == "-":
                            exponent += line[col+1]  # e+, e-, E+, E-
                            col += 1
                            moveForward += 1
                            powerPart = ""
                            if line[col+1].isdigit():
                                while line[col+1].isdigit():
                                    powerPart += line[col+1]
                                    col += 1
                                    moveForward += 1
                                logStringOrId(
                                    "tk_numero", entero + exponent+powerPart, row, enteroPos)
                            else:
                                error(row, col+1)
                        else:
                            error(row, col+1)
                    else:
                        logStringOrId("tk_numero", entero, row, enteroPos)

                # es texto cualquiera
                    # es alpha o _
                elif (line[col] == "_" or line[col].isalpha()):
                    idName, idPos = line[col], col+1
                    # obtiene toda la continuidad de caracteres
                    while(line[col+1].isalpha() or line[col+1] == "_" or line[col+1].isdigit()):
                        idName += line[col+1]
                        col, moveForward = col + 1, moveForward + 1

                    # verifica si es palabra reservada o si es otra cosa
                    logKeywordOrOperator(idName, row, idPos) if isReservedWord(
                        idName) else logStringOrId('id', idName, row, idPos)

                elif(line[col] in invalidChars):
                    col += 1
                    print(error(row, col))
                    sys.exit()
                elif isItEmpty(line[col]):
                    continue

            # print(f"{row} hay linea")
    index += 1

# Mi repo: https://github.com/mcsrk/lex-SL.git
# referencias:
# Token Separation(Lexical Analyzer) using Python - https://www.youtube.com/watch?v=O4Bt_CyZWbI
# Introducción al lenguaje SL https://drive.google.com/file/d/1tmsrQqpN85Z4kLvnNKFTfVdjMuqlq2Ga/view
# Estructura de código con condicionales - https://drive.google.com/file/d/1PbuEg_gz2RGIrEAaJRyvO_bFcMRBIlRo/view y https://github.com/milderhc/pseint-code-analyzer
