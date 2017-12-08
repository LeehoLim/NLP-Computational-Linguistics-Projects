import sys
import random

class State:
    def __init__(self, id, m_EP, m_TP):
        self.id = id
        self.m_EP = m_EP
        self.m_TP = m_TP


            # normprob = 0
            # for s in states:
            #     self.m_TP[s] = random.random()
            #     normprob += self.m_TP[s]
            # for s in states:
            #     self.m_TP[s] = self.m_TP[s]/normprob

    def __str__(self):
        ret = "Creating state %d\nTransitions" % self.id
        acprob = 0
        for s, p in self.m_TP.items():
            ret += "\n\tTo state %d:\t%f" % (s.id, p)

        ret += '\n\nEmission probabilities'
        for emission, p in self.m_EP.items():
            ret += "\n\tLetter    %s\t%f" % (emission, p)
            acprob += p

        ret += '\n\tTotal: %f\n' % acprob   

        return ret

    #def initRand(self, alphabet, States):
    #    self.initTP(States)
    #    self.initEP(alphabet)


    # @staticmethod
    # def Forward(States,Pi,thisword,listC):
    #     Alpha = [] #Change script to make the alpha object
    #     Alpha.append(Pi)
    #     listC.append('State   0:    %f' % Pi[0])
    #     listC.append('State   1:    %f' % Pi[1])
    #     for t in range(len(thisword)):
    #         alpha_t = [0 for i in range(len(States))]
    #         l = thisword[t]
    #         print "\ttime %d: '%c'" % (t+2, l)
    #         for to_state in States:
    #             acc = 0
    #             print "\t\tto state: %d" % to_state.id
    #             for from_state in States:
    #                 # print Alpha[t][from_state.id]
    #                 a = Alpha[t][from_state.id]
    #                 b = from_state.m_EP[l]
    #                 c = from_state.m_TP[to_state]
    #                 x = a * b * c
    #                 print "\t\t\tfrom state\t%d\tprevious Alpha times arc's a and b: %f" \
    #                         % (from_state.id, x)
    #                 acc += x
    #             print "\t\tAlpha at time = %d, state = %d: %f" % (t+2, to_state.id, acc)
    #             alpha_t[to_state.id] = acc
    #             listC.append('State   %d:    %f' %(to_state.id, acc))
    #         Alpha.append(alpha_t)

    #         print "\n\t\tSum of alpha's at time = %d: %f\n" % (t+2, sum(alpha_t))

    #     val = Alpha[len(thisword)][0] + Alpha[len(thisword)][1] 
        
    #     return val

    # @staticmethod
    # def Backward(States, Pi, thisword, listC):
    #     Beta = [] #Change script to make the alpha object
    #     Beta.append([1,1])
    #     listC.append('State   0:            1')
    #     listC.append('State   1:            1')
    #     for t in range(len(thisword)):
    #         beta_t = [0 for i in range(len(States))]
    #         l = thisword[len(thisword) - t - 1]
    #         print "\ttime %d: '%c'" % (len(thisword) - t, l)
    #         for from_state in States:
    #             acc = 0
    #             print "\t\tfrom state: %d" % from_state.id
    #             for to_state in States:
    #                 a = Beta[0][to_state.id]
    #                 b = from_state.m_EP[l]
    #                 c = from_state.m_TP[from_state]
    #                 x = a * b * c
    #                 print "\t\t\tto state\t%d\tprevious Beta times arc's a and b: %f" \
    #                         % (to_state.id, x)
    #                 acc += x
    #             print "\t\tBeta at time = %d, state = %d: %f" % (t+2, from_state.id, acc)
    #             listC.append('State   %d:     %f' % (from_state.id, acc))
    #             beta_t[from_state.id] = acc
    #         Beta = [beta_t] + Beta

    #         print "\n\t\tSum of beta's at time = %d: %f\n" % (t+2, sum(beta_t))

    #     val = Beta[0][0] * Pi[0] + Beta[0][1] * Pi[1]     

    #     return val



    @staticmethod
    def randHMM(numStates, alphabet):
        states = []
        for i in range(numStates):
            states.append(State(i, {}, {}))

        for i in range(numStates):
            # print "check"
            states[i].initEP(alphabet)
            states[i].initTP()

        return states







