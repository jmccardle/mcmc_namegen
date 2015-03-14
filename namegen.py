import random
import sys

class MarkovState:
    def __init__(self):
        self.transitions = {}
    def __repr__(self):
        return str(self.transitions)
    def increment(self, ch):
        if ch in self.transitions:
            self.transitions[ch] += 1
        else:
            self.transitions[ch] = 1
    def transition(self):
        count = sum([self.transitions[key] for key in self.transitions])
        r = random.randint(0, count)
        t = 1
        for k in self.transitions:
            t += self.transitions[k]
            if t >= r:
                return k
        return '\n'

class MarkovChain:
    def __init__(self, haltstate='\n', between=''):
        self.haltstate = haltstate
        self.states = {haltstate: None} #Why no state? We need to get an error if we try to transition from the halt state.
        self.init = MarkovState()
        self.between = between

    def RandomWalk(self, maxlength=0):
        state = self.init.transition()
        output = []
        while state != self.haltstate:
            output.append(state)
            if maxlength > 0 and len(output) >= maxlength:
                break
            nextstate = self.states[state].transition()
            state = nextstate
        return self.between.join(output)

    def AddLink(self, linkstate, targetstate):
        for s in (linkstate, targetstate):
            if not s in self.states:
                self.states[s] = MarkovState()
        if targetstate in self.states[linkstate].transitions:
            self.states[linkstate].transitions[targetstate] += 1
        else:
            self.states[linkstate].transitions[targetstate] = 1

    def AddWord(self, word, terminate=False):  #Adds each letter pair in the word to the markov chain
        if not word[0] in self.states:
            self.states[word[0]] = MarkovState()
        self.init.increment(word[0])
        for n in xrange(0, len(word)-1):
            self.AddLink(word[n], word[n+1])
        if terminate:
            self.AddLink(word[-1], self.haltstate)

    def AddWords(sentence): #Adds each word pair in the sentence to the markov chain
        pass
        
#states = {'\n': None}
#init = MarkovState()

def RandomWalk():
    state = init.transition()
    output = state
    while state != '\n':
        nextstate = states[state].transition()
        output += nextstate
        #print("State: {} Next: {}".format(state, nextstate))
        state = nextstate
    return output

def addWord(word):
    init.increment(word[0])
    for n in xrange(0, len(word)-1):
        if not n in states:
            #print("Creating state {}".format(word[n]))
            states[word[n]] = MarkovState()
        states[word[n]].increment(word[n+1])
        #print("Adding {} -> {} transition (now {})".format(word[n], word[n+1], states[word[n]]))

def addNextLetter(l, nextl):
    #print("Step #1. Is `{}` a state already?".format(l))
    global states
    if l in states:
        pass
        #print("Yes, `{}` is in `{}`.".format(l, states))
    else:
        #print("No. Creating state `{}`".format(l))
        states[l] = MarkovState()
    #print("Step #2. does `{}` have a transition to `{}`?".format(l, nextl))
    if nextl in states[l].transitions:
        #print("Yes, `{}` has a transition to `{}`. Incrementing.".format(l, nextl))
        states[l].transitions[nextl] += 1
    else:
        #print("No, `{}` has no transition to `{}`. Initializing as 1.".format(l, nextl))
        states[l].transitions[nextl] = 1
    #print("The transition `{}` -> `{}` is now at weight {}".format(l, nextl, states[l].transitions[nextl]))



if __name__ == '__main__':
    mc = MarkovChain()

    def readFile(fn):
        global mc
        with open(fn, "r") as f:
            for line in f:
                mc.AddWord(line)

    if len(sys.argv) > 1:
        readFile(sys.argv[1])
    else:
        print("Enter words, provide blank input to end:")
        txt = '_'
        while txt != '\n':
            txt = raw_input() + '\n'
            mc.AddWord(txt)
            #if txt[0] in init.transitions:
            #    init.transitions[txt[0]] += 1
            #else:
            #    init.transitions[txt[0]] = 1
            #for n in xrange(1, len(txt)-1):
            #    addNextLetter(txt[n], txt[n+1])


    print mc.init
    print '\n'
    print mc.states
    for n in xrange(20):
        print mc.RandomWalk().strip('\n')

