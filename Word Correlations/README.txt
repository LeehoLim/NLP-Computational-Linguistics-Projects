——————————————————————————————————————————————————————————————————————————————————————————
Contains:
——————————————————————————————————————————————————————————————————————————————————————————
sed.py
-File that contains the code to run the string edit program. Has 2 functions: 1 to find the cost of comparing 2 characters and another to calculate the string edit distance
-USAGE: “python sed.py [string1] [string2]
-String 1 print horizontally, string 2 vertically
-NOTE: Arguments are delimited by spaces

sed_string1_string2.txt	
-The output file containing the string that you would like to test.
-The default is set to the same result as the result in “example_output”, which is: 
HORIZONTAL: [string1] = thenameofthegame
VERTICAL: [string2] = theresmyname

example_output.txt		
-The output file containing the example output between
[string1] = thenameofthegame 
[string2] = theresmyname 

README.txt			
Contains the files included in the folder and information about string edit distance

——————————————————————————————————————————————————————————————————————————————————————————
Explanation:
——————————————————————————————————————————————————————————————————————————————————————————
For this project, I was given values of correlation between letters in two specific strings. Given these values, I traversed through the characters in each letter and found the optimal minimal path from the start to the end of the string. This showed a correlation value between our two words, with 0 being the strongest correlation (2 of the same words would simply traverse through each part and give 0 for the result), and a higher number being a weaker result. Notice that a vowel-to-vowel jump or consonant-to-consonant jump is associated with a stronger correlation between words than a consonant-to-vowel jump. Additionally, if a word was longer or shorter than another word, naturally that would have a lower correlation between words. I then printed out the optimal path and the characters of the two words that matched at each position along the optimal path. 

