import string
import random
import itertools

stateCount = 0
visitedStatesD = set()
closureD = []

literal = string.printable.translate(None, "+.*()")
operators = {"*", ".", "+"}
def run(regex, word):
    for x in word:
        if x in operators:
            print("\nNo :(")
        break
    parsed = parse(regex)
    nfaAnswer = regexNFA(parsed)
    answer = NFA.start(nfaAnswer, nfaAnswer.start, word)
    if answer == True:
        print("\nYes :)\n")
    if answer == False:
        print("\nNo :(\n")

def parse(regex):
    regex = regex.replace(" ", "")
    operators = {"*": 3, ".": 2, "+": 1}    # Operators and priorities
    parenthesis = {"(",")"}
    operatorStack = []
    reversePolish = []
    for x in regex:
        if x in operators:
            if operatorStack:
                toPop = operatorStack[-1]
                while toPop in operators and operators[toPop] >= operators[x]:
                    reversePolish.append(operatorStack.pop())
                    if operatorStack:
                        toPop = operatorStack[-1]
                    else:
                        break
            operatorStack.append(x)    # appends current operator if it has higher priority than operators in stack
        elif x == ")":
            while operatorStack[-1] != "(":
                reversePolish.append(operatorStack.pop())
            operatorStack.pop()  # Removes ( from the top of the stack
        elif x == "(":
            operatorStack.append(x)
        else:
            reversePolish.append(x)
    for x in reversed(operatorStack):    # pop rest of operators onto output
        if x in operators.keys():
            reversePolish.append(x)
    return reversePolish

def lastOperator(regex):
    if regex == "":
        return False
    if regex[-1] == "." or regex[-1] == "+" or regex[0] == "." or regex[0] == "+" or regex[0] == "*":
        return False

def isBalanced(regex):
    pair = []
    for s in regex:
        if s == '(':
            pair.insert(0, s)
        elif s == ')':
            if len(pair) == 0:    # there is no matching left parenthesis in pair
                return False
            if pair[0] == '(':    # there is a matching left parenthesis in pair
                pair.pop(0)
            else:
                return False
    if len(pair) == 0:
        return True
    return False

def sinkTransition(nfa):
    transition = nfa.transition
    nfa.states.add('s')
    for x in nfa.states:
        for y in nfa.alphabet:
            if (x, y) not in nfa.transition:
                transition.update({(x,y) : ['s']})

def concat(nfa1, nfa2):
    states = set()
    alphabet = set()
    transition = {}
    start = []
    final = []
    nfa = NFA(states, alphabet, transition, start, final)
    firstStart = nfa1.start
    firstFinal = nfa1.final[0]
    secondFinal = nfa2.final
    secondStart = nfa2.start
    nfa.transition.update({(firstFinal, 'eps') : secondStart})
    nfa.transition.update(nfa1.transition)
    nfa.transition.update(nfa2.transition)
    nfa.alphabet = nfa1.alphabet|nfa2.alphabet
    nfa.states = nfa1.states|nfa2.states
    nfa.start = firstStart
    nfa.final = secondFinal
    return nfa

def kleene(nfa):
    states1 = set()
    alphabet1 = set()
    transition1 = {}
    start1 = []
    final1 = []
    nfa1 = NFA(states1, alphabet1, transition1, start1, final1)
    global stateCount
    trans = nfa1.transition
    trans.update(nfa.transition)
    startState = nfa.start[0]
    finalState = nfa.final[0]
    newStart = str(stateCount)
    stateCount = stateCount + 1
    newFinal = str(stateCount)
    stateCount = stateCount + 1
    trans[(newStart, 'eps')] = [startState]
    trans[(finalState, 'eps')] = [startState]
    trans[(finalState, 'eps')].append(newFinal)
    trans[(newStart, 'eps')].append(newFinal)
    nfa1.alphabet = nfa.alphabet
    nfa1.states = nfa.states
    nfa1.states.add(newStart)
    nfa1.states.add(newFinal)
    nfa1.start = [newStart]
    nfa1.final = [newFinal]
    return nfa1

def union(nfa1, nfa2):
    states = set()
    alphabet = set()
    transition = {}
    start = []
    final = []
    nfa = NFA(states, alphabet, transition, start, final)
    global stateCount
    startState1 = nfa1.start[0]
    startState2 = nfa2.start[0]
    finalState1 = nfa1.final[0]
    finalState2 = nfa2.final[0]
    newStart = str(stateCount)
    stateCount = stateCount + 1
    newFinal = str(stateCount)
    stateCount = stateCount + 1
    nfa.transition.update(nfa1.transition)
    nfa.transition.update(nfa2.transition)
    nfa.alphabet = nfa1.alphabet|nfa2.alphabet
    nfa.states = nfa1.states|nfa2.states
    nfa.transition.update({(newStart, 'eps') : [startState1, startState2]})
    nfa.transition.update({(finalState1, 'eps') : [newFinal]})
    nfa.transition.update({(finalState2, 'eps') : [newFinal]})
    nfa.start = [newStart]
    nfa.final = [newFinal]
    return nfa

def newNFA(literal):
    global stateCount
    states = set()
    states.add(str(stateCount))
    start = [str(stateCount)]
    stateCount = stateCount + 1
    states.add(str(stateCount))
    final = [str(stateCount)]
    stateCount = stateCount + 1
    alphabet = {literal}
    transition = {(start[0], literal) : final}
    nfa = NFA(states, alphabet, transition, start, final)
    return nfa

def regexNFA(regex):
    global literal
    global operators
    nfaStack = []
    for x in regex:
        if x in literal:
            nfaStack.append(newNFA(x))
        if x in operators:
            if x == "*":
                nfaNew = kleene(nfaStack.pop())
                nfaStack.append(nfaNew)
            if x == ".":
                nfa2 = nfaStack.pop()
                nfa1 = nfaStack.pop()
                nfa3 = concat(nfa1, nfa2)
                nfaStack.append(nfa3)
            if x == "+":
                nfa2 = nfaStack.pop()
                nfa1 = nfaStack.pop()
                nfa3 = union(nfa1, nfa2)
                nfaStack.append(nfa3)
    if nfaStack:
        return nfaStack.pop()
    else:
        print("Something went terribly wrong")

def isCorrectLiteral(regex):
    if regex == "":
        return False
    literal = string.printable.translate(None, "+.*()")
    for current_char, next_char in zip(regex, regex[1:]):
        if current_char in literal and next_char in literal:
            return False
    return True

def isCorrectOperator(regex):
    invalid = ["..", ".+", ".*", "++", "+*", "+.", "**"]
    for x in invalid:
        if x in regex:
            return False
    return True

class NFA:
    closure = []
    visitedStates = []
    nextStates = []
    runStates = []

    def __init__(self, states, alphabet, transition, start, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transition = transition
        self.start = start
        self.final = final_states

    def isFinal(self, state):    # checks if the current state is in the list of final states
        for x in state:
            if x in self.final:
                return True
        return False

    def start(self, state, word):
        if word == "":
            return(self.isFinal(self.epsilonClosure(state)))
        for x in word:
            if x not in self.alphabet and x != "":
                return self.isFinal("\0")
        return(self.isFinal(self.runFunction(state, word + "\0")))

    def fix(self, list):
        fixed = [item for sublist in list for item in sublist]
        return(fixed)

    def epsilonClosure(self, state):
        for x in state:
            if x not in self.closure:
                self.closure.append(x)
            if (x, 'eps') in self.transition and x not in self.visitedStates:    # epsilon transition is possible
                self.visitedStates.append(x)
                state = state + self.transition[(x, 'eps')]
                return self.epsilonClosure(state)
        return self.closure

    def runFunction(self, state, word):
        first = word[0]
        rest = word[1:]
        if word[0] == "\0":
            return(self.epsilonClosure(state))
        acc = []
        eclose = self.epsilonClosure(state)
        bigD = self.bigDelta(eclose, first)
        self.closure = []
        self.visitedStates = []
        acc.append(self.runFunction(bigD, rest))
        acc = self.fix(acc)
        return acc

    def bigDelta(self, states, literal):
        bigDeltaStates = []
        for x in states:
            if (x, literal) in self.transition:
                bigDeltaStates.extend(self.transition[(x, literal)])
        return(bigDeltaStates)

regextest = raw_input("Enter a regular expression: \n")
if lastOperator(regextest) == False:
    print("You get nothing! You lose! Good day, sir!")
elif isCorrectLiteral(regextest) == False:
    print("You gotta keep 'em seperated")
elif isCorrectOperator(regextest) == False:
    print("Sade's hit song, 'Smooth Operator' is definitely not about you.")
elif isBalanced(regextest) == False :
    print("You were to bring balance to the Force, not leave it in darkness!")
else:
    word = raw_input("Enter a word:     -Type 'STOP' to quit. \n")
    while word != "STOP":
        stateCount = 0
        run(regextest, word)
        word = raw_input("enter a word: \n")   # Get the input again