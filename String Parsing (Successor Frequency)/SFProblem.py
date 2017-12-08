import sys
import math
import random
import sys
import argparse
from collections import defaultdict


K = (int)(sys.argv[1]) #Define our K val to use



space = ' ' #Define space character


#Discussed and received ideas from both Michael Borde and Alex Espinosa (In class)

def createlexicon(wordlist, originals, K): #This function will appropriately add NULL strings for if the words of the prefix are actual words in dict
#This function will also then set the multiple suffixes equal to each other...
    lex_dict = {}
    for k, word in enumerate(wordlist):
        if space in word.strip(space):
            word = word.split()
            key = ''.join(word[0:-1:+1])
            val = word[len(word)-1]
            lex_dict.setdefault(key, [])
            if key in originals and 'NULL' not in lex_dict[key]:
                lex_dict[key].append('NULL')
            lex_dict[key].append(val)

        else:
            lex_dict[word] = 'NULL'

    for i, (key, val) in enumerate(lex_dict.items()):
        if val is 'NULL':
            continue
        else:
            val = '='.join(val)
            lex_dict[key] = val
    return lex_dict

def createsignatures(lex_dict, K):
    Signatures = {}
    for i, (key1, value1) in enumerate(lex_dict.items()):
        for j, (key2, value2) in enumerate(lex_dict.items()):
            Signatures.setdefault(value1, [])
            check_string = value2
            if (value1 == check_string):
                if (key2 not in Signatures[value2]):
                    Signatures[value2].append(key2)
                    continue
                else:
                    continue    
    return Signatures

def space_identify(wordlist, K): #This function will identify where we should put appropriate spaces...
    ret = []
    for i, word in enumerate(wordlist):
        space_indicies = [] #For every word, let us make a new list
        for j, word2 in enumerate(word):
            makelist = [] #For every character in the word, let us also make a list...
            if j >= K:
                for k, word3 in enumerate(wordlist):
                    if j >= len(word3):
                        continue  
                    if word[0:j] == word3[0:j]: 
                        if word3[j] not in makelist:
                            makelist.append(word3[j])
                    if len(makelist) >= 2:
                        space_indicies.append(j-1)
                        break
                    else:
                        continue
            else:
                continue
        ret.append((word, space_indicies))
    return ret

def spacesincluded(wordlist, K): #This function will appropriately add spaces
    for k, (word, indicies) in enumerate(wordlist):
        if (len(indicies) == 0) and (word is not None):
            wordlist[k] = word
            continue
            continue
        total_size = len(word) + len(indicies)    
        for i in range(total_size):
            if (len(wordlist[k][1]) < 1) and (len(wordlist[k][1]) > -1):
                wordlist[k] = wordlist[k][0] + ''
                break
            if i in wordlist[k][1]:
                wordlist[k][1].remove(i)
                temp = []
                for position in wordlist[k][1]:
                    temp.append(position+1)
                wordlist[k] = word[0:i+1:+1] + space + word[i+1::+1], temp
            word = wordlist[k][0]

    return wordlist




def execute():
    sys.stdout = open('successor-predecessor-frequencies.txt', 'w')
    


    wordlist = []
    #with open(sys.argv[2]) as file:
    file = open(sys.argv[2], "r")
    for line in file:
        line = line.strip()
        line = line+space
        wordlist.append(line)

    wordlist.sort()
    originals = []
    back_words = []
    for word in wordlist:
        originals.append(word.strip())
        back_words.append(word[::-1])
    



    #Forward
    print('-'*37 + 'Forward' + '-' * 37 + '\n')
    wordlist = space_identify(wordlist, K)
    places = spacesincluded(wordlist, K)
    for place in places:
        print(place)

    #Backwards
    print '\n'
    print("-" *37 + "Backward" + "-"* 37 + '\n')
    back_words = space_identify(back_words, K)
    back_places = spacesincluded(back_words, K)

    back_fill = []
    for word in back_places:
        back_fill.append(word[::-1])
    back_places = back_fill

    for bplace in back_places:
        print(bplace)

    lex_dict = createlexicon(places, originals, K)

    #Lexicon
    sig = createsignatures(lex_dict, K)
    sys.stdout = open('TomSawyerSignatures.txt', 'w')


    for i, (key, values) in enumerate(sig.items()):
        if i <= 20:
            if (len(key) > 14):
                print key + " \t" + str(len(values)) + "\t",
            elif (len(key) > 7):
                print key + "\t\t" + str(len(values)) + "\t",
            else:    
                print key + "\t\t\t" + str(len(values)) + "\t",
            

            for k, val in enumerate(values):
                if k > 4:
                    print val + "\t\t",
                else:
                    break
        else:
            break            
        print()


    
    sys.stdout.close()



execute()





# def main():

#     wordlist = []
#     file = open(sys.argv[1], "r")
#     for line in file:
#         line = line.strip("\n")
#         line += " "
#         wordlist.append(line)



#     wordlist.sort()

#     dict_words = make_trie(wordlist)
#     # print dict_words
#     # for word in wordlist:
#     #     parse_spaces(word, dict_words)
#     # print type(dict_words)

#     suffix = [word[::-1] for word in wordlist]

#     suffix_dict_words = make_trie(suffix)


#     back_list = list()
#     back_print(suffix_dict_words, '', back_list)
#     back_max_n = max_len(back_list)
#     back_max_lengths_parts = list()


#     ret_list = list()
#     recurse_print(dict_words, '', ret_list)

#     print ret_list
#     ret_list.sort(key = lambda x: x[0])
#     print ret_list
#     print "poop"
#     append_but_last(ret_list)
#     ret_list.sort(key = lambda x: x[0])
#     add_null(ret_list)
#     ret_list.sort(key = lambda x: x[0])
#     append_equals(ret_list)


#     max_n = max_len(ret_list)
#     max_lengths_parts = list()

# #FORWARD
#     if Forward == True:
        
#         for a in range(max_n):
#             b = list()
#             for i in ret_list:
#                 if len(i) > a:
#                     b.append(i[a])
#             max_lengths_parts.append(max_len(b))

#         for a in ret_list:
#             string_to_print = ''
#             for b in range(len(max_lengths_parts)):
#                 if (len(a) > b):
#                     while len(a[b]) < max_lengths_parts[b] + 1:
#                         a[b] += ' '
#                     string_to_print += a[b]
#             print string_to_print

        

# #BACKWARD
#     else:
#         for a in range(back_max_n):
#             b = list()
#             for i in back_list:
#                 if len(i) > a:
#                     b.append(i[a])
#             back_max_lengths_parts.append(max_len(b))


#         for a in back_list:
#             string_to_print = ''
#             for b in range(len(back_max_lengths_parts)):
#                 if (len(a) > b):
#                     while len(a[b]) < back_max_lengths_parts[b] + 1:
#                         a[b] += ' '
#                     string_to_print += a[b]
#             reverse = string_to_print[::-1]
#             print reverse




# def append_but_last(ret_list):
#     new_list = ret_list
#     suffix_list = []
#     for a in new_list:
#         a[0:len(a)-1] = [''.join(a[0:len(a)-1])]
#     # for a in new_list:
#     #     for b in new_list:
#     #         if b[0] == a[0]:
#     #             suffix_list[a][0] = a[0]
#     #             '='.join(suffix_list[a][1])
#     print new_list
#     #return new_list    

# def add_null(ret_list):
#     for a in ret_list:
#         check_s = a[0] + a[1]
#         for b in ret_list:
#             if (check_s == b[0]):
#                 ret_list.append([b[0], "NULL"])
#                 break
#     print ret_list


# def append_equals(wordlist):
#     new_list = []
#     new_new_list = []
#     for i in range(len(wordlist)-1):
#         if (wordlist[i][0] == wordlist[i+1][0]):
#             wordlist[i+1][1] = wordlist[i+1][1] + '=' + wordlist[i][1] 
#             new_list.append([wordlist[i+1][0], wordlist[i+1][1]])
#         else:
#             new_list.append([wordlist[i][0], wordlist[i][1]])
#     for j in range(len(new_list)-1):
#         if (new_list[j][0] == new_list[j+1][0]):
#             new_list[j][0] = None
#             new_list[j][1] = None

#     for k in range(len(new_list)):
#         if (new_list[k][0] != None):
#             new_new_list.append([new_list[k][0], new_list[k][1]])             

#     print new_new_list 


# def print_stem(ret_list):
#     for a in     

# def max_len(lister):
#     lengths = list()
#     for i in lister:
#         lengths.append(len(i))
#     return max(lengths)

# def make_trie(wordlist):
#     root = dict()
#     for word in wordlist:
#         current_dict = root
#         # print word
#         for letter in word:
#             current_dict = current_dict.setdefault(letter, {})
#         current_dict[''] = ''
#     return root

# def recurse_print(dict_words, string, return_list):
#     if dict_words == {'':''}:
#         return_list.append(list())
#         for i in string.split(' '):
#             if i != '':
#                 return_list[-1].append(i)

#     if len(string) == K:
#         string += ' '

#     for i in range(len(dict_words)):
#         if (len(string) > K) and (len(dict_words) > 1) and (string[-1] != ' '):
#             string += ' '  
#         string += dict_words.keys()[i]
#         recurse_print(dict_words[dict_words.keys()[i]], string, return_list)
#         string = string[:-1]  
        


# def back_print(dict_words, string, return_list):
#     if dict_words == {'':''}:
#         return_list.append(list())
#         for i in string.split(' '):
#             if i != '':
#                 return_list[-1].append(i)

#     if len(string) == K+1:
#         string += ' '

#     for i in range(len(dict_words)):
#         if (len(string) > (K + 1)) and (len(dict_words) > 1):
#             string += ' '  
#         string += dict_words.keys()[i]
#         back_print(dict_words[dict_words.keys()[i]], string, return_list)
#         string = string[:-1]          