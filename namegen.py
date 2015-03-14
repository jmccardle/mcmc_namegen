import random
import sys

class MarkovState:
    def __init__(self):
        self.transitions = {}
    def __repr__(self):
        return str(self.transitions)
    def increment(self, ch):
        if ch in self.transitions:
            #print "Self.transitions `{}` has `{}`; incrementing".format(self.transitions, ch)
            self.transitions[ch] += 1
        else:
            #print "Self.transitions `{}` has NO `{}`; creating".format(self.transitions, ch)
            self.transitions[ch] = 1
        #print('ch `{}` now has {} transitions'.format(ch, self.transitions[ch]))
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
        self.states = {haltstate: None} #Why no state? We need to get an error if we try to transition from the halt state.
        self.init = MarkovState()
        self.between = between

    def RandomWalk(self, maxlength=0):
        state = self.init.transition()
        output = []
        while state != self.haltstate:
            output.append(state)
            if maxlength > 0 and len(output) >= maxlength:
            nextstate = self.states[state].transition()
            state = nextstate
        return self.between.join(output)

    def AddLink(linkstate, targetstate):
        if not linkstate in self.states:
            self.states[linkstate] = MarkovState()
        if targetstate in self.states[linkstate].transitions:
            self.states[linkstate].transitions[targetstate] += 1
        else:
            self.states[linkstate].transitions[targetstate] = 1

    def AddWord(word):  #Adds each letter pair in the word to the markov chain
        self.init.increment(word[0])
        for n in xrange(1, len(word)-1):
            self.AddLink(word[n], word[n+1])
        self.AddLink(word[-1], self.haltstate)

    def AddWords(sentence): #Adds each word pair in the sentence to the markov chain
        pass
        
states = {'\n': None}
init = MarkovState()

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

def readFile(fn):
    with open(fn, "r") as f:
        for line in f:
            line = line.lower()
            if line[0] in init.transitions:
                init.transitions[line[0]] += 1
            else:
                init.transitions[line[0]] = 1
            for n in xrange(1, len(line)-1):
                addNextLetter(line[n], line[n+1])


if __name__ == '__main__':
    if len(sys.argv) > 1:
        readFile(sys.argv[1])
    else:
        print("Enter words, provide blank input to end:")
        txt = '_'
        while txt != '\n':
            txt = raw_input() + '\n'
            if txt[0] in init.transitions:
                init.transitions[txt[0]] += 1
            else:
                init.transitions[txt[0]] = 1
            for n in xrange(1, len(txt)-1):
                addNextLetter(txt[n], txt[n+1])


    print init
    print '\n'
    print states
    for n in xrange(20):
        print RandomWalk().strip('\n')

