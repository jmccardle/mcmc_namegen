#!/usr/bin/python
#
#   namegen.py
#
#   Author: John McCardle
#   Purpose: generate words (namely, sci-fi alien names) based on lists of other names using a Markov Chain.
#   License: MIT

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
        if len(self.transitions) == 0:
            return None
        if len(self.transitions) == 1:
            self.transitions.keys()[0]
        count = sum([self.transitions[key] for key in self.transitions]) * 1.0
        r = random.uniform(0, count)
        t = 0
        for s in self.transitions:
            if t + self.transitions[s] > r:
                return s
            t += self.transitions[s]

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
        
if __name__ == '__main__':
    mc = MarkovChain()
    wordcount = 0

    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            for line in f:
                wordcount += 1
                mc.AddWord(line)
    else:
        print("Enter words, provide blank input to end:")
        txt = '_'
        while txt != '\n':
            txt = raw_input() + '\n'
            wordcount += 1
            mc.AddWord(txt)

    t_total = sum([len(mc.states[s].transitions) for s in mc.states if not mc.states[s] is None])
    print("States: {}\n\nTotal Transitions: {}\nAverage Transitions per state: {}"
        .format(len(mc.states), t_total, (t_total*1.0)/len(mc.states)))
    for n in xrange(20):
        print mc.RandomWalk().strip('\n')

