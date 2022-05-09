

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


def firstOf(rule):
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
        if rule[0] in list(parsedGramm.keys()):
            tempResult = []
            rigthPartRule = parsedGramm[rule[0]]
            # call first on each rule of RHS
            # fetched (& take union)
            for ele in rigthPartRule:
                firstList = firstOf(ele)
                if type(firstList) is list:
                    for firstEle in firstList:
                        tempResult.append(firstEle)
                else:
                    tempResult.append(firstList)

            if 'epsilon' not in tempResult:
                return tempResult
            else:
                # rule => f(ABC)=f(A)-{e} U f(BC)
                newList = []
                tempResult.remove('epsilon')
                if len(rule) > 1:
                    ruleBeyond = rule[1:]
                    newAnsw = firstOf(ruleBeyond)
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


def follow(nt):
    global ini_symbol, noTerminals, \
        terminals, parsedGramm, firsts, nexts
    # for start symbol return $ (recursion base case)

    solset = set()
    if nt == ini_symbol:
        # return '$'
        solset.add('$')

    # check all occurrences
    # solset - is result of computed 'follow' so far

    # For input, check in all rules
    for curNT in parsedGramm:
        rhs = parsedGramm[curNT]
        # go for all productions of NT
        for subrule in rhs:
            if nt in subrule:
                # call for all occurrences on
                # - non-terminal in subrule
                while nt in subrule:
                    index_nt = subrule.index(nt)
                    subrule = subrule[index_nt + 1:]
                    # empty condition - call follow on LHS
                    if len(subrule) != 0:
                        # compute first if symbols on
                        # - RHS of target Non-Terminal exists
                        res = firstOf(subrule)
                        # if epsilon in result apply rule
                        # - (A->aBX)- follow of -
                        # - follow(B)=(first(X)-{ep}) U follow(A)
                        if '#' in res:
                            newList = []
                            res.remove('#')
                            ansNew = follow(curNT)
                            if ansNew != None:
                                if type(ansNew) is list:
                                    newList = res + ansNew
                                else:
                                    newList = res + [ansNew]
                            else:
                                newList = res
                            res = newList
                    else:
                        # when nothing in RHS, go circular
                        # - and take follow of LHS
                        # only if (NT in LHS)!=curNT
                        if nt != curNT:
                            res = follow(curNT)

                    # add follow result in set form
                    if res is not None:
                        if type(res) is list:
                            for g in res:
                                solset.add(g)
                        else:
                            solset.add(res)
    return list(solset)


def getFIRSTSets():
    global gramm, parsedGramm, noTerminals, terminals,  firsts
    readAndCleanGramm()
    # calculate first for each rule
    # - (call first() on all RHS)
    for symbol in list(parsedGramm.keys()):
        firstSet = set()
        for rule in parsedGramm.get(symbol):
            firstOfRule = firstOf(rule)
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

    for NT in parsedGramm:
        solset = set()
        sol = follow(NT)
        if sol is not None:
            for g in sol:
                solset.add(g)
        nexts[NT] = solset

    print("\nSIGUIENTES DE: \n")
    key_list = list(nexts.keys())
    index = 0
    for gg in nexts:
        print(f"SIGUIENTES({key_list[index]})"
              f" => {nexts[gg]}")
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
