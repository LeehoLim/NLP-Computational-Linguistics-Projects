—————————————————————————————————————————————————————————————————————————————————————
Contains:
—————————————————————————————————————————————————————————————————————————————————————
HMM3.py				
-This simply contains the Class, “State”, which includes the state ID, the emission probabilities, and the transition probabilities
-This has been imported into HMM_test3.py

HMM_test3.py			
-This is the file that you want to run.
-Usage: “python HMM_test3.py”
-Usage options: “python HMM_test3.py -v -s” (Read for what “-v” and “-s” do)
-This will simply use the “english1000.txt” as a sample and pipe the output automatically into output.txt
-If there is no output.txt, it will create an output.txt			
-You may activate the verbose mode with flag “-v”. Ex: “python HMM_test3.py -v”, which will output additional information
-I have now updated the states (Transition Probabilities, Emission Probabilities, and Pi values). 
-In this new part, I have implemented maximization, where I used the updated states to find new plog values. I arbitrarily defined a good place to stop to be when the difference between the previous iteration of the plot and the current blog was < .02. I also implemented an option that iterated 200 times automatically over the plogs and output 200 different plog values. 
-YOU MAY ACTIVATE THE FORMER ITERATIVE METHOD (STOPPING AT < .02) BY FLAGGING “-s”, and the 2nd iterative method by simply leaving out “-s” therefore, the default iterates over the states 200 times and calls 200 different plog values.
			
InitialTP_PlogOptimize
-I then created a separate file called “InitialTP_PlogOptimize”, which every time I run my file, adds the initial transitional probability state and 							the final plog. I then added an ANALYSIS/DESCRIPTION at the bottom, which describes the significance of the data that we have observed. 
					
english1000.txt			
-This is the file to run the above code on. It automatically executes this code, so there is no need to run this file as an argument output.txt	
-This is the output from running the above HMM_test2.py andon the “english1000.txt file in NON-VERBOSE mode. I HAVE OUTPUT THE INITIAL PROBABILITIES AND THE FINAL UPDATED STATE AND EACH PLOG VALUE FOR THE DIFFERENT ITERATIONS IN THE NON-VERBOSE MODE. THE VERBOSE MODE CONTAINS ALL INFORMATION FROM HMM1, HMM2, AND HMM3.

—————————————————————————————————————————————————————————————————————————————————————

Explanation:

HMM1 / HMM2:
I created a Hidden Markov Model with an assumption of 2 states.
I first established a random “Pi”, with 2 states that summed to 1, therefore I defined one random number between 0 and 1, and subtracted 1 from this value to obtain my second value. I then did the same for the transition probabilities. For the emission probabilities, I simply passed an alphabet dict into my “initEP” function, which associated random values to the different “keys”, or “letters” for the different words that we were given. Each letter was assigned a random probability, and we parsed through the entire file to obtain emission probabilities. I then had 2 states with the same transition probabilities and PI (initial probability) values, but with different emission values. I clumped these 2 individual states into an array, called “States”, and used that as an input to both my forward function which checked for forward advances in the state, and my backward function, which checked for backward advances in the state. Passing the different words in the file as an input for the “thisword” variable in both my “Forward” and “Backward” function, along with the “States”, and “Pi” values, I then output the end total Probability of the forward quantity “alpha”, and the backward quantity “beta”. The forward quantity output was simply just the sum of the values at the last time for both state values (for 0 and 1), and the output for the backward quantity was the first output for the 0th state multiplied with the 0th index of Pi added with the 1st state multiplied with the 1st index of Pi.

I then compared these values and saw that they were the same.
I then calculated a “plog” value by taking the inverse log probability base 2, and summed all the blogs for a total output.

For HMM2, I then calculated the soft counts. This was done by computing the alpha of each from_state, i, at time “t” * emission probabilities * transition probabilities * the beta of each to_state, j, at time “t+1”. I output the soft counts for each particular letter in each word, and then I made a final accumulation of soft counts for each letter in the “alphabet” output that had an accumulation of every letter that appeared in every word in the wordlist that I used as an input. These letters summed to a whole integer.


HMM3:

In this new part, I have implemented maximization, where I used the updated states to find new plog values. I arbitrarily defined a good place	to stop to be when the difference between the previous iteration of the plot and the current blog was < .02. I also implemented an option that iterated 50 times automatically over the plogs and output 50 different plog values. I then ran my script to iterate multiple times to find the different plog values. I found that at first, the plog values would decrease (significantly less and less each time), and after a certain point, it would fluctuate and even rise very insubstantially as well. It is at around this point that I stopped my iteration of states and extracted my plog. I then piped 25 TRIALS of my code to another file called “InitialTP_PlogOptimize”, where I listed my INITIAL transition states and my last iteration’s plog value for that particular initial transition state. I noticed that the wider the discrepancy in the start of the initial transition probability states (i.e. closer to 100/0 or 0/100), the lower my final plog value was, and the more that my HMM was able to understand the English language. I found that the opposite case, where the states did NOT start skewed, but more even (i.e. closer to 50/50), my HMM was less able to understand the English language and had a slightly higher plog value.
