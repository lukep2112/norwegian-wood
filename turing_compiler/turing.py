import os.path
import sys

def formatText(filePath):
    input = open(filePath, "r")
    output = []
    for line in input:
        line = line.rstrip()
        if line == '':
            continue
        if not line.startswith("--"):
            line = line.split("--", 1)[0]
            line = line.split(";", 1)[0]
            output.append(line)
    input.close()
    return output

def getStates(list):
    states = list[0]
    states = states.replace(" ", "")
    if states[1:7] != "states":
        raise Exception('You must have a state initialization in your program.')
    states = states[8:-1]
    states = set(states.split(","))
    return states

def getStart(list):
    start = list[1]
    start = start.replace(" ", "")
    if start[1:6] != "start":
        raise Exception('You must have a start initialization in your program.')
    start = start[7:-1]
    return start

def getAccept(list):
    accept = list[2]
    accept = accept.replace(" ", "")
    if accept[1:7] != "accept":
        raise Exception('You must have an accept initialization in your program.')
    accept = accept[8:-1]
    return accept

def getReject(list):
    reject = list[3]
    reject = reject.replace(" ", "")
    if reject[1:7] != "reject":
        raise Exception('You must have a reject initialization in your program.')
    reject = reject[8:-1]
    return reject

def getAlphabet(list):
    alphabet = list[4]
    alphabet = alphabet.replace(" ", "")
    if alphabet[1:6] != "alpha":
        raise Exception('You must have a alphabet initialization in your program.')
    alphabet = alphabet[7:-1]
    alphabet = set(alphabet.split(","))
    return alphabet

def getTapeAlphabet(list):
    TapeAlphabet = list[5]
    TapeAlphabet = TapeAlphabet.replace(" ", "")
    if TapeAlphabet[1:11] != "tape-alpha":
        raise Exception('You must have a tape-alphabet initialization in your program.')
    TapeAlphabet = TapeAlphabet[12:-1]
    TapeAlphabet = set(TapeAlphabet.split(","))
    TapeAlphabet.add("_")
    return TapeAlphabet

def getTransition(list):
    instructions = []
    transition = []
    for x in list[6:]:
        instructions.append(x.split())
    for x in instructions:
        if x[0] == 'rwRt':
            c = x[1]
            r = x[2]
            w = x[3]
            n = x[4]
            d = "->"
            transition.append([c,r,w,n,d])
        if x[0] == 'rwLt':
            c = x[1]
            r = x[2]
            w = x[3]
            n = x[4]
            d = "<-"
            transition.append([c,r,w,n,d])
        if x[0] == 'rRl':
            c = x[1]
            r = x[2]
            w = x[2]
            n = x[1]
            d = "->"
            transition.append([c,r,w,n,d])
        if x[0] == 'rLl':
            c = x[1]
            r = x[2]
            w = x[2]
            n = x[1]
            d = "<-"
            transition.append([c,r,w,n,d])
        if x[0] == 'rRt':
            c = x[1]
            r = x[2]
            w = x[2]
            n = x[3]
            d = "->"
            transition.append([c,r,w,n,d])
        if x[0] == 'rLt':
            c = x[1]
            r = x[2]
            w = x[2]
            n = x[3]
            d = "<-"
            transition.append([c,r,w,n,d])
    return transition

def stateCheck(states):
    if start not in states:
        print("Start must be in your state list!")
        sys.exit()

def acceptCheck(accept):
    if accept not in states:
        print("Accept must be in your state list!")
        sys.exit()

def rejectCheck(reject):
    if reject not in states and reject != start:
        print("Reject must be in your state list and must be unique!")
        sys.exit()

def alphabetCheck(alphabet, tapeAlphabet):
    for x in alphabet:
        if x == "_":
            print("'_' can not be used in the alphabet!")
            sys.exit()
        if x not in tapeAlphabet:
            print("Every character in alphabet must be in the tape-alphabet!")
            sys.exit()

class turingMachine():
    def __init__(self, states, alphabet, tapeAlphabet, transition, start, accept, reject):
        self.states = states
        self.alphabet = alphabet
        self.tapeAlphabet = tapeAlphabet
        self.transition = transition
        self.start = start
        self.accept = accept
        self.reject = reject
        self.tape = []
        self.index = 0
        self.current = self.start

    def tapeInit(self, word):
        if not word:
            self.tape.append("_")
        for x in word:
            self.tape.append(x)

    def move(self, direction):
        if direction == "->":
            if self.index == len(self.tape)-1:
                self.tape.append("_")
            self.index = self.index + 1
        elif direction == "<-":
            if self.index == 0:
                self.index == 0
            else:
                self.index = self.index - 1

    def write(self, char):
        self.tape[self.index] = char

    def nextTransition(self, current, read):
        for x in transition:
            if x[0] == current and x[1] == read:
                return x
        return [current, read, read, self.reject, "->"]


    def snapshot(self):
        head = "[" + self.current + "]"
        output = ""
        if self.index == 0:
            output = head + "".join(self.tape)
        elif self.index == len(self.tape):
            output = ''.join(self.tape) + head
        else:
            front = self.tape[:self.index]
            back = self.tape[self.index:]
            output = "".join(front) + head + "".join(back)
        if output[-1] == "_":
            output = output[:-1]
        return output

    def run(self):
        print(self.snapshot())
        while True:
            read = self.tape[self.index]
            nextState = self.nextTransition(self.current, read)
            self.write(nextState[2])
            self.move(nextState[4])
            self.current = nextState[3]
            if self.current == self.accept:
                print("Accept: " + self.snapshot())
                break
            elif self.current == self.reject:
                print("Reject: " + self.snapshot())
                break
            else:
                print(self.snapshot())

input = raw_input("\nPlease enter a path to the source file: ")
if os.path.isfile(input) == False:
    print("Enter a valid file location, homie!")
elif input[-3:] != ".TM":
    print("File type must be .TM")
else:
    try:
        output = formatText(input)
        states = getStates(output)
        start = getStart(output)
        accept = getAccept(output)
        reject = getReject(output)
        alphabet = getAlphabet(output)
        tapeAlphabet = getTapeAlphabet(output)
        transition = getTransition(output)
    except Exception, e:
        print("\nInvalid initialization format.\n")
        print(e)
        sys.exit()
    stateCheck(states)
    acceptCheck(accept)
    rejectCheck(reject)
    alphabetCheck(alphabet, tapeAlphabet)
    test = turingMachine(states, alphabet, tapeAlphabet, transition, start, accept, reject)
    word = raw_input("\nPlease enter a word: ")
    turingMachine.tapeInit(test, word)
    try:
        turingMachine.run(test)
    except:
        sys.exit()
