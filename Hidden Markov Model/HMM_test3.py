from HMM3 import State
import math 
import random
import sys
import argparse

sys.stdout = open("output.txt", "w")


def initEP(alphabet, verbose):
    sum = 0.0
    letters = list(set(alphabet)) 
    ep = {}
    ep = dict.fromkeys(letters, None)
    normprob = 0
    for key in ep:
        x = random.random()
        ep[key] = x
        normprob += ep[key]
    for key in ep:
        ep[key] /= normprob
        if (verbose == True):
            print '\tLetter   %c   %f' % (key, ep[key])
        sum += ep[key]
    print 'Sum of Emission Probabilities: %f\n' % sum    
    return ep 


def initTP():
    tp = [0, 0]
    x = random.random()
    tp[0] = x
    tp[1] = 1 - x
    return tp


#FORWARD AND BACKWARDS FUNCTIONS REFERENCED FROM JOHN GOLDSMITH'S 'Basics of HMMs v 2015.1' LECTURE NOTES, PG. 8
def Forward(States,Pi,thisword, verbose):
    Alpha = {}
    #checksum = 0
    for s in range(len(States)):
        Alpha[(s,1)] = Pi[s]
    for t in range(2,len(thisword) + 2):
        for to_state in range(len(States)):
            Alpha[(to_state,t)] = 0
            for from_state in range(len(States)):
                Alpha[(to_state,t)] += Alpha[(from_state,t-1)] * States[from_state].m_EP[thisword[t-2]] * States[from_state].m_TP[to_state]
    for num in range(1, len(thisword) + 2):
            if (verbose == True):
                print "Alpha: Time", num, "State 0", Alpha[(0, num)], "State 1", Alpha[(1, num)]            
    #checksum += Alpha[(0, len(thisword) - 1)] + Alpha[(1, len(thisword) - 1)]
    
    return Alpha


def Backward(States, Pi, thisword, verbose):
     Beta = {}
     last = len(thisword) + 1
     for s in range(len(States)):
         Beta[(s, last)] = 1
     for t in range(len(thisword),0,-1):
         for from_state in range(len(States)):
             Beta[(from_state,t)] = 0
             for to_state in range(len(States)):
                Beta[(from_state,t)] += Beta[(to_state,t + 1)] * States[from_state].m_EP[thisword[t-1]] * States[from_state].m_TP[to_state]
     for num in range(1, len(thisword) + 2):
            if (verbose == True):
                print "Beta: Time", num, "State 0", Beta[(0, num)], "State 1", Beta[(1, num)]             
     return Beta    




def ForwardSum(Alpha, thisword):
    return Alpha[0, len(thisword) + 1] + Alpha[1, len(thisword) + 1]    



def BackwardSum(Beta, Pi):
    return Beta[0, 1] * Pi[0] + Beta[1, 1] * Pi[1]



#SOFT COUNT FUNCTION
def soft_count(Alpha, Beta, States, thisword, soft, verbose):
    for t in range(1, len(thisword) + 1):
        if (verbose == True):
            print "Letter: '%c'\n" % thisword[t-1]
        for from_state in range(len(States)):
            if (verbose == True):
                print "From state: %d" % from_state
            for to_state in range(len(States)):
                #Formula for calculating soft-count: A_i(t) * (Emission Probs) * (Transition Probs) * B_j(t+1) / string probability (of alpha or beta) 
                # where i and j are both states and t is time. i is the from state, j is the to state.
                # We want to obtain probability GIVEN a letter that we will go from one state to the next
                # When I say one state to the next, we have 2 states, so 0 -> 0, 0 -> 1, 1 -> 0, 1 -> 1
                # Because we calculate "t" and "t+1", let us use values t-1 and t (x = t+1, s.t. we have x - 1 and x)
                v = Alpha[(from_state, t)]*States[from_state].m_TP[to_state]*States[from_state].m_EP[thisword[t-1]]*Beta[(to_state, t+1)]
                v = v / ForwardSum(Alpha, thisword)

                
                soft[(thisword[t-1], from_state, to_state)] = soft[(thisword[t-1], from_state, to_state)] + v

                if (verbose == True):
                    print "\tto state:   %d      %f" % (to_state, v)   
                if ((verbose == True) and (to_state == 1)):
                    print "\n"  



def soft_count_to_2(Alpha, Beta, States, thisword,soft, verbose):
    for t in range(1, 2):
        if (verbose == True):
            print "Character: '%c'\n" % thisword[t-1]
        for from_state in range(len(States)):
            if (verbose == True):
                print "From state: %d" % from_state
            for to_state in range(len(States)):
                v = Alpha[(from_state, t)]*States[from_state].m_TP[to_state]*States[from_state].m_EP[thisword[t-1]]*Beta[(to_state, t+1)]
                v = v / ForwardSum(Alpha, thisword)
                soft[(thisword[t-1], from_state, to_state)] = soft[(thisword[t-1], from_state, to_state)] + v
                if (verbose == True):
                    print "\tto state:     %d      %f" % (to_state, v)   
            if ((to_state == 1) and (verbose == True)):
                print '\n'           



def update_transition_helper(softcounts, from_state, to_state):
    num = 0.0
    denom = 0.0
    for item in softcounts.items():
        (letter, fstate, tstate), value = item
        if (fstate == from_state):
            denom += value
            if (tstate == to_state):
                num += value
    a = num
    b = denom  
    c = num/denom          
    return [a, b, c]

def update_pi_helper(softcounts, from_state, Z):
    num = 0.0                
    for item in softcounts.items():
        (letter, fstate, tstate), value = item
        if (fstate == from_state):
            num += value


    return num/Z        


def update_emissions_helper(softcounts, from_state, l):
    num = 0.0
    denom = 0.0
    for item in softcounts.items():
        (letter, fstate, tstate), value = item
        if (fstate == from_state):
            denom += value
            if (letter == l):
                num += value
    sol = num/denom
    total = denom
    return [sol, num, total]
      

def output_transition(softcounts, States, verbose):
    if (verbose == True):
        print '-'*40
        print '-  Transition Probabilities  -'
        print '-'*40
    for from_state in range(len(States)):
        if (verbose == True):
            print("From_State: %d\n" % from_state)
        for to_state in range(len(States)):
            k = update_transition_helper(softcounts, from_state, to_state)
            States[from_state].m_TP[to_state] = k[2]
            if(verbose == True):
                print("\tTo State:\t %d  prob:  %f  (%f   over    %f)" % (to_state, k[2], k[0], k[1]))   
        if (verbose == True):
            print("\n")

    return States    


def output_pi(softcounts, States, counter, pi, verbose):
    if (verbose == True):
        print '-'*30
        print("Pi:")
        print '-'*30
    i = 0
    for from_state in range(len(States)):
        k = update_pi_helper(softcounts, from_state, counter)    
        if (verbose == True):
            print("State: %d      %f" % (from_state, k))
        pi[i] = k
        i += 1
    if (verbose == True):
        print("\n")  

    return pi  

def output_emissions(softcounts, States, verbose):
    if (verbose == True):
        print '-'*40
        print 'Emission Probabilities:'
        print '-'*40
    for from_state in range(len(States)):
        if (verbose == True):
            print "State %d" % from_state
            print 'Normalize soft counts to get emission probabilities\n'
        for letter, item in States[from_state].m_EP.items():
            k = update_emissions_helper(softcounts, from_state, letter)
            States[from_state].m_EP[letter] = k[0]
                    
            if (verbose == True):
               print("\tletter: %c   probability: %.18f  (%f    over    %f)" % (letter, k[0], k[1], k[2]))   
        if (verbose == True):        
            print("\n") 

    return States    

def sorter(ite):
    l, v = ite
    return v

def logfunct(States, input_dict, verbose): 
    for letter, value in States[0].m_EP.items():

        #print letter
        #print States[1].m_EP[letter]

        num = value if value > 0 else sys.float_info.min
        denom = States[1].m_EP[letter] if States[1].m_EP[letter] > 0 else sys.float_info.min


        input_dict[letter] = num/denom
        input_dict[letter] = math.log(input_dict[letter], 2)
    if (verbose == True):
        print '-'*45
        print 'Log Ratio of emissions from 2 states:'
        print '-'*45+'\n'
        for letter, value in sorted(input_dict.items(), key = sorter):
            print 'Letter: %c    Value (Log(V_s0/V_s1)): %f' % (letter, value)

    return input_dict    
        
    

def execute():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true",  help="Display additional information")
    parser.add_argument("-s", "--significance", action="store_true", help="Display additional information")

    args = parser.parse_args()
    verbose = False
    if args.verbose:
        verbose = True    

    file = open('english1000.txt', 'r')
    psum = 0.0
    alphabet = []
    counter = 0
    for line in file:
        actualLine = line.strip("\n").lower()
        alphabet += actualLine
        alphabet += "#"
        counter += 1
    Pi = [0,0]
    x = random.random()
    Pi[0] = x
    Pi[1] = 1 - x
    

    c = initTP()
    print 'Creating State 0'
    print 'Transitions'
    print '\tTo state    0    %f' % c[0]
    print '\tTo state    1    %f' % c[1]
    print '\nEmission Probabilities'

    a = initEP(alphabet, verbose)
    state0 = State(0, a, c)

    
    print 'Creating State 1'
    print 'Transitions'
    print '\tTo state   0   %f' % c[0]
    print '\tTo state   1   %f' % c[1]
    print '\nEmission Probabilities'

    b = initEP(alphabet, verbose)
    state1 = State(1, b, c)



    with open('InitialTP_PlogOptimize.txt', 'a') as f:
        f.write("State" + str(state0.id) + " To State: " + str(state0.id) + " Prob: " + str(state0.m_TP[0])+ "\n")
        f.write("State" + str(state0.id) + " To State: " + str(state1.id) + " Prob: " + str(state0.m_TP[1])+ "\n")
        f.write("State" + str(state1.id) + " To State: " + str(state0.id) + " Prob: " + str(state1.m_TP[0])+ "\n")
        f.write("State" + str(state1.id) + " To State: " + str(state1.id) + " Prob: " + str(state1.m_TP[1])+ "\n")




    print '-'*40
    print 'Pi:'
    print 'State   0   %f' % Pi[0]
    print 'State   1   %f' % Pi[1]
    print '\n'

    i = 1
    #for i in range(50):
    plogdif = 60000 #60000 is bogus value


    if args.significance:
        while (plogdif >= 0.02):
            input_dict = {}
            if (i >= 2):
                plogdif = psum
            s_table = {}
            for fill_a in state1.m_EP:
                 s_table[(fill_a, 0, 0)] = 0.0
                 s_table[(fill_a, 0, 1)] = 0.0
                 s_table[(fill_a, 1, 0)] = 0.0
                 s_table[(fill_a, 1, 1)] = 0.0

            s_table2 = {}
            for fill_a in state1.m_EP:
                 s_table2[(fill_a, 0, 0)] = 0.0
                 s_table2[(fill_a, 0, 1)] = 0.0
                 s_table2[(fill_a, 1, 0)] = 0.0
                 s_table2[(fill_a, 1, 1)] = 0.0

            sarray = [state0, state1]

            psum = 0.0
            fileAgain = open('english1000.txt', 'r')
            for line in fileAgain:
                actualLine = line.strip("\n").lower()
                thisword = actualLine + "#"
               # Forward(sarray, Pi, thisword, blank1)
                #Backward(sarray, Pi, thisword, blank2)
                if (verbose == True):
                    print '-'*30 + '  ' + "'%s'" % thisword + '  ' + '-'*30
                    print '\n'
                f1 = Forward(sarray, Pi, thisword, verbose)
                val1 = ForwardSum(f1, thisword)
                if (verbose == True):
                    print 'String probability from Alphas is %.15f' % val1
                    print '\n'
                b1 = Backward(sarray, Pi, thisword, verbose)
                val2 = BackwardSum(b1, Pi)
                if (verbose == True):
                    print 'String probability from Betas is %.15f' % val2
                    print '\n'
                plog = -1 * (math.log(val1, 2))
                if (verbose == True):
                    print 'Plog for %s is %f' % (thisword, plog)
                    print '\n'
                psum += plog

                if (verbose == True):
                    print '-'*25
                    print 'Soft counts'
                    print '-'*25 + '\n'
                soft_count(f1, b1, sarray, thisword, s_table, verbose)
                soft_count_to_2(f1, b1, sarray, thisword, s_table2, verbose)

                if (verbose == True):
                    print '-'*25
                    print 'End soft counts'
                    print '-'*25 + '\n'

            plogdif = plogdif - psum
            if (i == 1):
                print "Iteration Number: %d    (No plog difference for first iteration)" % i
                print 'The sum of the plogs is %f\n' % psum
            else:
                print "Iteration Number: %d    Plog Significance between last iteration: %f" % (i, plogdif)
                print 'The sum of the plogs is %f\n' % psum        
            i += 1
                
            
            if (verbose == True):
                print '-'*50 + '\n'
                print 'Expected Counts table:\n'
            for letter in state1.m_EP:
                p = 0.0
                for count1 in range(2):
                    for count2 in range(2):
                        p += s_table[(letter, count1, count2)]
                        if (verbose == True):
                            print "%c       %d        %d        %f" % (letter, count1, count2, s_table[(letter, count1, count2)])
                if (verbose == True):
                    print '\nThe total for %c is %f\n' % (letter, p)   

            if (plogdif < 0.02):
                verbose = True

            if (verbose == True):
                print '-'*32
                print 'Maximization'
                print '-'*32  
                print '\n'


            sarray = output_transition(s_table, sarray, verbose)
            Pi = output_pi(s_table2, sarray, counter, Pi, verbose)
            sarray = output_emissions(s_table, sarray, verbose)
            logfunct(sarray, input_dict, verbose)

        with open('InitialTP_PlogOptimize', 'a') as f:
            f.write("Final Iteration's Plog Sum: "+ str(psum)+ "\n"*2)
            



    else:       
        for t in range(200):
            s_table = {}
            for fill_a in state1.m_EP:
                s_table[(fill_a, 0, 0)] = 0.0
                s_table[(fill_a, 0, 1)] = 0.0
                s_table[(fill_a, 1, 0)] = 0.0
                s_table[(fill_a, 1, 1)] = 0.0

            s_table2 = {}
            for fill_a in state1.m_EP:
                s_table2[(fill_a, 0, 0)] = 0.0
                s_table2[(fill_a, 0, 1)] = 0.0
                s_table2[(fill_a, 1, 0)] = 0.0
                s_table2[(fill_a, 1, 1)] = 0.0

        
            input_dict = {}
            sarray = [state0, state1]

            psum = 0.0
            fileAgain = open('english1000.txt', 'r')
            for line in fileAgain:
                actualLine = line.strip("\n").lower()
                thisword = actualLine + "#"
               # Forward(sarray, Pi, thisword, blank1)
                #Backward(sarray, Pi, thisword, blank2)
                if (verbose == True):
                    print '-'*30 + '  ' + "'%s'" % thisword + '  ' + '-'*30
                    print '\n'
                f1 = Forward(sarray, Pi, thisword, verbose)
                val1 = ForwardSum(f1, thisword)
                if (verbose == True):
                    print 'String probability from Alphas is %.15f' % val1
                    print '\n'
                b1 = Backward(sarray, Pi, thisword, verbose)
                val2 = BackwardSum(b1, Pi)
                if (verbose == True):
                    print 'String probability from Betas is %.15f' % val2
                    print '\n'
                plog = -1 * (math.log(val1, 2))
                if (verbose == True):
                    print 'Plog for %s is %f' % (thisword, plog)
                    print '\n'
                psum += plog

                if (verbose == True):
                    print '-'*25
                    print 'Soft counts'
                    print '-'*25 + '\n'
                soft_count(f1, b1, sarray, thisword, s_table, verbose)
                soft_count_to_2(f1, b1, sarray, thisword, s_table2, verbose)

                if (verbose == True):
                    print '-'*25
                    print 'End soft counts'
                    print '-'*25 + '\n'

            plogdif = plogdif - psum

            print 'Iteration Number: %d' % i
            print 'The sum of the plogs is %f\n' % psum
            i += 1
                
            
            if (verbose == True):
                print '-'*50 + '\n'
                print 'Expected Counts table:\n'
            for letter in state1.m_EP:
                p = 0.0
                for count1 in range(2):
                    for count2 in range(2):
                        p += s_table[(letter, count1, count2)]
                        if (verbose == True):
                            print "%c       %d        %d        %f" % (letter, count1, count2, s_table[(letter, count1, count2)])
                if (verbose == True):
                    print '\nThe total for %c is %f\n' % (letter, p)   


            if (i == 201):
                verbose = True

            if (verbose == True):
                print '-'*32
                print 'Maximization'
                print '-'*32  
                print '\n'    

            sarray = output_transition(s_table, sarray, verbose)
            Pi = output_pi(s_table2, sarray, counter, Pi, verbose)
            sarray = output_emissions(s_table, sarray, verbose)        
            logfunct(sarray, input_dict, verbose)

        with open('InitialTP_PlogOptimize.txt', 'a') as f:
            f.write("Final Iteration's Plog Sum: "+ str(psum)+ "\n"*2)


execute()        
