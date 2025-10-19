# ExceLLM Solution

## Reverse Engineering (Medium/Hard)

Players must recognize the way that the data is laid out and work their way backwards from the final verification. There is a lot of obfuscation in terms of the actual neural network weights and bitwise input/output of the flag. Additionally the sheets used to do a lot of the calculations are hidden by default.

To solve the challenge, players will notice that on the verification sheet there is a final output layer that gives a per-character boolean answer. This allows them to discern the length of the flag, as well as brute-force each character of the flag by trying different inputs and seeing what will flip each neuron to TRUE.

Once they identify all the characters this way, using a method of their choice, they will be able to get the correct flag.