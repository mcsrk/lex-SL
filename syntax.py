

gramm = {
    "EXPR": ["TERMINO-EXPR1"],
    "EXPR1": ["OP-TERMINO-EXPR1",
              "epsilon"],
    "TERMINO": ["FACTOR-LIST_FACTOR"],
    "LIST_FACTOR": ["OP-FACTOR-LIST_FACTOR",
                    "epsilon"],
    "OP": ["tk_resta",
           "tk_suma"],
    "FACTOR": ["numero"],
}
gramm1 = {
    "A": ["B-C",
          "ant-A-all"],
    "B": ["big-C",
          "bus-A-boss",
          "epsilon"],
    "C": ["cat", "cow"],
}


def readAndCleanGramm():
    global gramm, parsedGramm, noTerminals, terminals,  firsts

    print("READING")
    for symbol, rules in gramm.items():
        noTerminals.append(symbol)
        # for every rule remove spaces
        for i in range(len(rules)):
            gramm[symbol][i] = gramm[symbol][i].strip()
            gramm[symbol][i] = gramm[symbol][i].split('-')

        parsedGramm[symbol] = rules

    print(f"\nReglas: \n")
    for symbol in parsedGramm:
        print(f"{symbol}->{parsedGramm[symbol]}")


def firstsOfRule(rule):
    global gramm, parsedGramm, noTerminals, terminals,  firsts

    if len(rule) > 0:
        # base case: terminal and epsilon
        if (rule is not None):
            if rule[0] in terminals:
                return rule[0]
            elif rule[0] == 'epsilon':
                return 'epsilon'

        # recursive case for no-terminals

        # match with a not terminal
        if list(parsedGramm.keys()).count(rule[0]) > 0:
            tempResult = []
            rigthPartRule = parsedGramm[rule[0]]
            # call first on each rule of RHS
            # fetched (& take union)
            for ele in rigthPartRule:
                firstList = firstsOfRule(ele)
                if type(firstList) is list:
                    [tempResult.append(firstEle) for firstEle in firstList]

                else:
                    tempResult.append(firstList)

            if 'epsilon' not in tempResult:
                return tempResult
            else:
                # rule => f(ABC)=f(A)-{e} U f(BC)
                newList = []
                tempResult.remove('epsilon')
                if len(rule) > 1:
                    croppedRule = rule[1:]
                    newAnsw = firstsOfRule(croppedRule)
                    if newAnsw != None:
                        if type(newAnsw) is list:
                            newList = tempResult + newAnsw
                        else:
                            newList = tempResult + [newAnsw]
                    else:
                        newList = tempResult
                    return newList
                tempResult.append('epsilon')
                return tempResult


def nextsOfRule(noTerminal):
    global ini_symbol, noTerminals, \
        terminals, parsedGramm, firsts, nexts

    nextsSoFar = set()
    if noTerminal == ini_symbol:
        nextsSoFar.add('$')

    # looking for noTerminal instances in every rule
    for everyNoTerminalSymbol in parsedGramm:
        rules = parsedGramm[everyNoTerminalSymbol]
        for subrule in rules:
            if noTerminal in subrule:
                # call for all occurrences on
                # - non-terminal in subrule
                while noTerminal in subrule:
                    index_nt = subrule.index(noTerminal)
                    subrule = subrule[index_nt + 1:]
                    if len(subrule) != 0:
                        res = firstsOfRule(subrule)
                        # if epsilon in res:
                        # - (A->aBX)- follow of -
                        # - follow(B)=(first(X)-{ep}) U follow(A)
                        isThereEpsilon = res.count('epsilon') > 0
                        if isThereEpsilon:
                            ansNew = nextsOfRule(everyNoTerminalSymbol)
                            newList = []
                            res.remove('epsilon')

                            newList = res
                            if ansNew != None:
                                if type(ansNew) is list:
                                    newList += ansNew
                                else:
                                    newList += [ansNew]
                            res = newList
                    else:
                        # when nothing in RHS, go circular and take follow of LHS only if (NT in LHS)!=curNT
                        if everyNoTerminalSymbol != noTerminal:
                            res = nextsOfRule(everyNoTerminalSymbol)

                    # add follow result in set form
                    if res is not None:
                        if type(res) is list:
                            [nextsSoFar.add(everyNextLexem)
                             for everyNextLexem in res]
                        else:
                            nextsSoFar.add(res)
    return list(nextsSoFar)


def getFIRSTSets():
    global gramm, parsedGramm, noTerminals, terminals,  firsts
    readAndCleanGramm()
    # calculate first for each rule
    # - (call first() on all RHS)
    for symbol in list(parsedGramm.keys()):
        firstSet = set()
        for rule in parsedGramm.get(symbol):
            firstOfRule = firstsOfRule(rule)
            if firstOfRule != None:
                if type(firstOfRule) is list:
                    for ele in firstOfRule:
                        firstSet.add(ele)
                else:
                    firstSet.add(firstOfRule)

        # save result in 'firsts' list
        firsts[symbol] = firstSet

    print("\nPRIMEROS DE: \n")
    symbols = list(firsts.keys())
    index = 0
    for symbol in firsts:
        print(f"PRIMEROS({symbols[index]})"
              f": {firsts.get(symbol)}")
        index += 1


def getNEXTSets():
    global gramm, parsedGramm, noTerminals, terminals, firsts, nexts

    for eachNoTerminal in parsedGramm:
        nextsSet = set()
        res = nextsOfRule(eachNoTerminal)
        if res is not None:
            for g in res:
                nextsSet.add(g)
        nexts[eachNoTerminal] = nextsSet

    print("\nSIGUIENTES DE: \n")
    key_list = list(nexts.keys())
    index = 0
    for eachSymbol in nexts:
        print(f"SIGUIENTES({key_list[index]})"
              f" => {nexts[eachSymbol]}")
        index += 1


def setImportantValues():
    global gramm, noTerminals, ini_symbol

    keys = gramm.keys()
    ini_symbol = list(keys)[0]
    for key in keys:
        noTerminals.append(key)


noTerminals = []
terminals = [
    "tk_resta",
    "tk_suma", "numero"]
terminals1 = ["ant",
              "all",
              "big",
              "bus",
              "boss",
              "cat",
              "cow"]
parsedGramm = {}
ini_symbol = ""
firsts = {}
nexts = {}

setImportantValues()
getFIRSTSets()
getNEXTSets()


# Referencias
# definición y lectura de la grámatica https://www.geeksforgeeks.org/compiler-design-ll1-parser-in-python/ - Tanmay P. Bisen
