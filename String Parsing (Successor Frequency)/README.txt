——————————————————————————————————————————————————————————————————————————————————————————
Contains:
——————————————————————————————————————————————————————————————————————————————————————————
SFProblem.py				
-This is the file that you want to run.
-Usage: python SFProblem.py [arg1] [arg2] 
-“arg1” = K (minimal stem length) and “arg2 = file to run the parser on	
	

english1000.txt				
-This is a sample file to run the above code on. You must use this file as an argument for “arg2”


TomSawyer.dx1			
-This is a sample file to also run the code on. Do the same as for english1000.txt


1K-Signatures.txt		
-Output of lines ordered by number of stems associated with signature (Only top 20 signatures) (for K= 5)


TomSawyerSignatures.txt		
-This is the output from running the above SFProblem.py for our Part 2 on the word set from Tom Sawyer


successor-predecessor-frequencies.txt 
-This is the output file for the parsed words with the spaces for the forwards and backwards operations… The forwards and backwards operations are clearly indicated. (Output for K=5)
	
		 					 
ReadMe.txt				
-Contains explanation and usage instructions…

——————————————————————————————————————————————————————————————————————————————————————————

Explanation of Implementation and Function of the Parsing a String Using Successor Frequency:

Given a word list and a specific minimum stem length, K, I was able to parse our list of words and first print all letters up to K, and was able to then determine which words had similar prefix and suffix bases… i.e. to detect that advised and advisedly.

In order to do this, what I first did was use a “space counter” that would count the index position of where the necessary spaces were to be counted. I then stored this in a list.
I then used these index positions to put the spaces accordingly in order to add the appropriate spaces to each word.

Continuing on, I then created 2 other functions which created a “Lexicon” and “Signatures dict. I looked at words that had the same base: “advised” - “advise” “e” and “d”. If the words had the same base, I concatenated their suffixes alongside an “=“ sign. After doing so, I then formed a dictionary to check which word bases had the same set of suffix endings and printed out the particular words that corresponded to the set of suffix endings.


