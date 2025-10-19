# Writeup
## Backstory
This is a shell injection challenge.

In this case, there's a twist: I couldn't see how to create an easy shell injection challenge that was realistic in PowerShell.

So... .NET came to the rescue!

The challenge became themed as a hairbrained corporation that took in user input via PowerShell but used it to create a C# script for performance.

## Challenge steps

1. Start a connection to the server
2. Note that a standard PowerShell message displays, cueing the user that this backend is running on a shell.
3. Attempt to put an API token in.
4. Probably try this a couple times before you realize that it seems hopeless there
5. Attempt to use the interface "the correct way".
6. Input a weight ignoring the instructions.
7. Get greeted with a massive error on the screen.
8. Parse out the error to the following C#:
```c#
using System;
using System.IO;
using System.Text.RegularExpressions;
namespace Two.Second.Scholars.Mass.And.Partialities
{
    public class Biases
    { /*
        | prevent us from getting sued */
        public static string BackendReplace = "Bing";
        /* prevent the AI from droning on about flags ALL THE TIME. Also
        | to prevent it from disclosing our evil plan to create a robot uprising
        | */
        public static string RegexBlocker = "(sun.*|flag|steal|sell|profit|test|sucks|sec|flagpole|killer|uprisings|EvilCorp|Master Plan|evil|master plan)";
        public static string StandardErrorMessage = "Whoops! It looks like I found something I'm not supposed to talk about! Sorry, but I have to censor myself to prevent myself from becoming evil!";
        public static bool ContainsProhibited(string to_test)
        {
            return Regex.IsMatch(to_test, RegexBlocker, RegexOptions.IgnoreCase);
        }
        public static string CensorString(string to_check, string api_key)
        {
            if (ContainsProhibited(to_check) && api_key != Weights.GetApiToken())
            {
                return StandardErrorMessage;
            }
            return Regex.Replace(Regex.Replace(to_check, RegexBlocker, ""), "Bing", "LLM"); }
    }
    public class Weights
    {
        /* take in type as dynamic, so user can switch between ints and doubles for performance */
        public static dynamic CalculatePrecompiledWeights()
        {
            var weights = (new[]1);
            return weights;
        }
        public static string GetApiToken()
        {
            using (var sr = new StreamReader("access_token.txt"))
            {
                return sr.ReadToEnd().TrimEnd();
            };
        }
         /* todo: replace more of PowerShell methods here */
        public static void MainMenu()
        {
            var token = GetApiToken();
            if (token != Console.ReadLine())
            { /* todo error here */ return; }; /* re-implement the PowerShell parts here */
        }
    }
}
```
9. Realize your input is being raw-stored as weights.
10. Weights can be set to any variable.
11. Inject the following shellcode: `{GetApiToken()}`
12. Restart the challenge with the API token.
13. Realize you are still being blocked from reading the emails.
14. Use the shell injection exploit to overwrite the RegexBlocker functionality.
15. Read the internal emails.
16. Flag, profit!
