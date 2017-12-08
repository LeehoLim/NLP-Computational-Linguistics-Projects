—————————————————————————————————————————————————————————————————————————————————————
Contains:
—————————————————————————————————————————————————————————————————————————————————————
TomSawyer.dx1				
-Input file that I use in order to run the compression.py on. 

Graph.pdf				
-Output image file that displays the forward vs backwards calculation 
-Note: Forward = x, Backward = f(x)

output.txt				
-Output of the text file that contains the word along with its compression calculation (the first 2 are forward intervals and the last 2 are backwards intervals…) compression.py
-The code used to make the forward and backward interval calculations… Methodology is below.

USAGE INSTRUCTIONS: 
-Run “python compression.py” 
-Must have TomSawyer.dx1 in the same file when running

README.txt
-Contains usage instructions, explanation for running code, and any interesting discussion around geometrical patterns of the output image file

—————————————————————————————————————————————————————————————————————————————————————
Explanation:
—————————————————————————————————————————————————————————————————————————————————————
For this project, I implemented a program that will calculate unigram frequencies of each symbol (letter usually).
I ran my code through the “TomSawyer.dx1” text.
First, I did an empirical frequency calculation to count the number of occurrences of each letter throughout the entire file. I then ordered the alphabet that I had, and traversed through it in order to get specific frequencies of letters as intervals (summed as I traversed through each list, starting with # = 0…)
I then calculated the forwards and backwards unigram frequencies for the words in the TomSawyer.dx1 text, printed them out in 4 columns (forward, forward, backward, backwards), and plotted them on a graph with the forward as the x axis and the backwards as the y axis.


DISCUSSION FOR ANY INTERESTING GEOMETRICAL PATTERNS:

In the output, I was surprised to see that there was a “square-like” shape for the output… this indicates that for the given forward calculations, there were multiple backward calculation outputs for the same forward calculation unigram frequency value. This might be due to starting with either very high or very low values, such as starting a word with “a”, and ending it with “z”… in this case, we can definitely see why the interval might start a little higher or lower given a forwards or backwards state.  