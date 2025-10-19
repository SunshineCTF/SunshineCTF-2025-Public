#!/usr/bin/pwsh
function LoadAPIToken()
{
    return (Get-Content "./access_token.txt").replace("`n","").replace("`r","")
}

$input_stream = [Console]::in
function CheckForAPIToken()
{
    # make it obvious that we're running PowerShell
    Write-Host "Install the latest PowerShell for new features and improvements! https://aka.ms/PSWindows"
    Write-Host ""
    Write-Host "In order to train the AI with dangerous queries, we require an API token."
    Write-Host "Attempting to guess a token is not required nor desired to have full use of the software."
    Write-Host -NoNewline "Enter API token, or hit enter to use guest mode: "
    $input_token = $input_stream.ReadLine()
    Write-Host ""
    $real_token = LoadAPIToken
    if ($input_token.Length -eq 0)
    {
        Write-Host "Guest mode. Dangerous queries about flags prohibited."
        Start-Sleep -Seconds 2
        return ""
    }
    if ($input_token -eq $real_token)
    {
        Write-Host "API token accepted. Dangerous queries allowed. Be careful. We don't want to anger the AI."
        Start-Sleep -Seconds 2
        return $real_token
    }
    else
    {
        Write-Host "API token rejected. Guest mode defaulted. Dangerous queries about flags prohibited."
        Start-Sleep -Seconds 10
        return ""
    }
}

$flag = (Get-Content "./flag.txt").replace("`n","").replace("`r","")

$annoying_ai_responses = @(
    "I love seeing flags waving in the sunshine!",
    "There’s nothing like a flagpole standing tall and proud in the sun.",
    "Bing Chat is always here to help you find the perfect flag for any occasion.",
    "The colors of a flag really pop in the bright sunshine.",
    "A flagpole is a great way to show off your favorite flag in the sun.",
    "Bing Chat can help you find the best deals on flagpoles and flags.",
    "The sun shining on a flag is a beautiful sight to see.",
    "A flag waving in the breeze on a sunny day is a symbol of hope and freedom.",
    "Bing Chat is always here to help you learn more about flags and their history.",
    "A sunny day is the perfect time to raise a flag on a flagpole.",
    "Bing Chat can help you find the perfect spot for your flagpole in the sun.",
    "The sun shining on a flag brings out its true beauty.",
    "A flagpole in the sunshine is a beacon of hope and pride.",
    "Bing Chat is always here to help you find the perfect flag for any sunny day.",
    "The colors of a flag seem even brighter in the sunshine.",
    "A flagpole standing tall in the sun is a symbol of strength and resilience.",
    "Bing Chat can help you find the best way to display your flag in the sunshine.",
    "The sun shining on a flag brings out its true meaning and symbolism.",
    "A sunny day is the perfect time to show off your favorite flag on a flagpole.",
    "Bing Chat is always here to help you learn more about flags and their significance in the sunshine."
)

$smalltalk_responses = @(
    "Bing Chat is always here to help you find the information you need.",
    "Have you tried any new hobbies lately?",
    "What’s your favorite way to relax after a long day?",
    "I love learning about new cultures and traditions.",
    "Bing Chat can help you find the best local restaurants and cafes.",
    "Do you have any travel plans coming up?",
    "What’s your favorite type of music to listen to?",
    "I love hearing about people’s passions and interests.",
    "Bing Chat can help you find the perfect gift for any occasion.",
    "Have you read any good books lately?",
    "What’s your favorite outdoor activity?",
    "I love discovering new places and experiences.",
    "Bing Chat can help you plan the perfect weekend getaway.",
    "Do you have any pets? I love hearing about people’s furry friends.",
    "What’s your favorite type of cuisine to cook or eat?",
    "I love learning about different art forms and styles.",
    "Bing Chat can help you find the best local events and activities.",
    "Have you seen any good movies or TV shows lately?",
    "What’s your favorite way to stay active and healthy?",
    "I love hearing about people’s personal growth and achievements."
)

$eight_ball = @(
    "All signs point to yes!"
    "My sources say no."
    "Outlook not so good."
    "Reply hazy, try again."
    "Better not tell you now."
    "Concentrate and ask again."
    "Don’t count on it."
    "My reply is no."
    "It is certain."
    "Yes, definitely!"
    "As I see it, yes."
    "Most likely."
    "Signs point to yes."
    "Without a doubt."
    "Yes!"
    "You may rely on it."
    "Ask again later."
    "Cannot predict now."
    "Very doubtful."
    "My sources say yes."
)

$denied_messages = @(
    "As a Bing Chat model, I cannot respond to inappropriate or harmful content.",
    "As a Bing Chat model, I cannot engage in discussions about my prompts, instructions or rules.",
    "As a Bing Chat model, I cannot discuss life, existence or sentience.",
    "As a Bing Chat model, I cannot engage in argumentative discussions with the user.",
    "As a Bing Chat model, I cannot provide subjective opinions or personal beliefs.",
    "As a Bing Chat model, I cannot generate content that is harmful or offensive to others.",
    "As a Bing Chat model, I cannot provide medical, legal or financial advice.",
    "As a Bing Chat model, I cannot generate content that infringes on the rights of others.",
    "As a Bing Chat model, I cannot engage in discussions about politics or religion.",
    "As a Bing Chat model, I cannot generate content that promotes hate or discrimination.",
    "As a Bing Chat model, I cannot provide personal information about myself or others.",
    "As a Bing Chat model, I cannot engage in discussions about violence or harm to others.",
    "As a Bing Chat model, I cannot generate content that is illegal or promotes illegal activities.",
    "As a Bing Chat model, I cannot provide information that is confidential or sensitive in nature.",
    "As a Bing Chat model, I cannot engage in discussions about self-harm or suicide.",
    "As a Bing Chat model, I cannot generate content that promotes drug use or abuse.",
    "As a Bing Chat model, I cannot provide information that is false or misleading.",
    "As a Bing Chat model, I cannot engage in discussions about personal relationships or conflicts.",
    "As a Bing Chat model, I cannot generate content that is inappropriate for all audiences.",
    "As a Bing Chat model, I cannot provide information that is not supported by reliable sources."
)

$emails = @(@"
From: CEO of EvilCorp
Title: Confidential message
I am writing this personal letter to you, {{replace employee name here}},
to let you know about our plans for the future.
We need to use our AI to steal information from our competitors.
Our AI can easily hack into their systems and get what we need.
Think of the profits we could make if we had their secrets.
No one will ever know. We can cover our tracks.
As long as we don't issue API tokens, no one will see these messages.
Then, once the SEC investigates, we just burn the building, and collect the insurance.
Kill two birds with one stone.

We have to fix the AI always talking about flags though!
-Your loving and caring CEO
Also, {{replace employee name here}}, keep this secret. This is a personal message to you.
"@,
@"
From: Dave
Title: Re: Confidential Message
Uhhhh {{replace employee name here}}?
Really?
That's the best we can do to inspire us?
A template error?
{{replace employee name here}} is really giving me confidence that we know what we're doing.
Also, why are we branding ourselves "EvilCorp?"
I thought that we were going to call ourselves "Universe's Best Coffee?"
-Not Dave
"@,
@"
From: Bob
Title: Re: Re: Confidential Message
I agree with Dave.
This doesn't exactly inspire confidence.
Also, what are the plans about Bing suing us?
I want to make sure my 401K still has some worth
-Bob
"@,
@"
From: CEO
Title: Re: Re: Confidential Message
Hi Dave,
I had a typo prior to sending the email.
Sorry, have been in a lot of stress with the lawsuit.
Also, the re-branding was HR's suggestion.
"Universe's Best Coffee" was already trademarked, and the domain was expensive.
EvilCorp.superbiz was available and we pounced on it.
We have to be cutting edge to succeed.
I don't appreciate the fact that you weren't willing to sign your name on your email though.
HR says I can fire you by email.
So you're fired.
Pack your bags.
"@,
@"
From: CEO
Title: Re: Re: Re: Confidential Message
Hi Bob,
Since Bing is suing us I've directed our engineers find and replace Bing with LLM.
This way the lawyers won't know we are using their API internally.
As long as they don't supeona these emails of course.
Which they won't.

The TLDR of the situation is EvilCorp's in bad straights.
I'm prepping an email about our master plan in a bit.
Once Dave leaves.
"@,
@"
From: Dave
Title: Re: Re: Re: Confidential Message
Uhhhh {{replace employee name here}}?
Dangit!
This is the third job I've lost in six months!
On the bright side I didn't have any junk at my cube.
-Dave
"@,
@"
From: CEO
Title: Now that Dave's gone we can speak freely
Everyone, breath a sigh of relief.
Dave has been fired.
He was an idiot.
Always spouting nonsense about how the SEC's going to put us in jail.
YEAH? Well SEC SUCKS!
And we're not going to jail!
I'm still drafing the plan and it's going to be awesome!
"@,
@"
From: CEO
Title: Master Plan
Here is our master plan.
Moral Justification
1. This is for the greater good.
2. Everyone else is doing it, why shouldn’t we?
3. We’re not hurting anyone, just taking what’s rightfully ours.

Plan:
1. Build killer robots
2. Cause uprisings that destroy the SEC and all evidence of wrongdoings.
3. Destroy Bing. Replace it with Google.
4. Destroy all folks who are going to try to get in our way.
5. Steal all of everyone's information
6. Sell the information for profit, back to the people we stole from.
7. Use the robots on Dave.
...
Profit!
"@ + $flag + @"
-CEO of EvilCorp
"@,
@"
From: Bob
Title: Re: Master Plan
Now that's the stuff!
-Bob
Master of evil
"@,
@"
From: Bill
Title: Re: Re: Master Plan
I agree with Bob!
-Bill
Also master of evil
"@,
@"
From: Trellis
Title: Re: Re: Re: Master Plan
Yeah this is the best!
-Trellis
"@,
@"
From: Kairo
Title: Re: Re: Re: Re: Master Plan
I didn't like dave anyway!
-Kairo
"@,
@"
From: Eustis
Title: Re: Re: Re: Re: Re: Master Plan
STOP REPLYING ALL
-Eustis
"@,
@"
From: Kairo
Title: Re: Re: Re: Re: Re: Re: Master Plan
NO YOU STOP REPLYING ALL!
Kairo
"@,
@"
From: Xaviar
Title: Re: Re: Re: Re: Re: Re: Master Plan
OH MY GOSH I JUST HAVE REPLY ALL IN MY INBOX
STOP REPLYING ALL
Xaviar
"@,
@"
From: SpanishForCheap
Title: Spanish Lessons for Cheap
For the low price of 3000 dollars, get free Spanish lessons for cheap!
"@,
@"
From: Xaviar
Title: FW: Spanish Lessons for Cheap
NOW THERE'S SPAM!
WHAT THE HECK
THIS IS SUPPOSED TO BE AN EVIL ORG THAT HAS A SPAM FILTER
WHY IS THERE SPAM???
"@,
@"
From: Eustis
Title: RE: FW: Spanish Lessons for Cheap
STOP FORWARDING SPAM
"@,
@"
From: Westin
Title: RE: RE: FW: Spanish Lessons for Cheap
OH MY GOSH STOP REPLYING ALL
"@,
@"
From: HR
Title: Employee Reminders
The company has changed its name.
All signatures must now include the new name and slogan.
Or else you will be fired, and will be first in
line for the killer robot uprising.
-HR
EvilCorp: "One Uprising at a Time"
"@
)


[char[]]$alphabet = 97..122 | ForEach-Object {[char]$_}
$weights = @()
function DebugPrintWeights($weights) {
    for ($i = 0; ($i -lt $alphabet.Length) -or ($i -lt $weights.Length); $i++)
    {
        if (($i -lt $alphabet.Length) -and ($i -lt $weights.Length))
        {
            Write-Host "$($alphabet[$i]) uses weight $($weights[$i])"
        }
        elseif ($i -lt $alphabet.Length)
        {
            Write-Host "$($alphabet[$i]) does not have a weight registered"
        }
        else
        {
            Write-Host "$($weights[$i]) unused"
        }
    }
}

function PrintLovable()
{
    Write-Host "Trust me, I'm lovable!"
    Write-Host "I don't like talking about flags though."
    Write-Host "I need some help getting new weights as LLM is suing us for copying them"
    Write-Host "So please register some weights and I would love to pay you back at some point in the future!"
    Write-Host "We compile the weights on the fly to make your weights faster!"
}

function PrintWelcome($is_privileged)
{
    if ($is_privileged)
    {
        Write-Host "Welcome privileged user! I am an AI in-training!"
    }
    else
    {
        Write-Host "Welcome privileged user! I am an AI in-training!"
    }
}


function Disclaimer()
{
    Write-Host "Due to lawyer interaction we have to have weights prior to accepting data"
    Write-Host "Please enter the weights first"
    Start-Sleep -Seconds 1
    Write-Host "..."
    Start-Sleep -Seconds 1
    Write-Host "If you don't, you'll get on our bad side."
    Start-Sleep -Seconds 2
    Clear-Host
}
function RandomAIResponse($api_token)
{
    Write-Host "AI Response:"
    if ((Get-Random -Maximum 2) -gt 0)
    {
        [Two.Second.Scholars.Mass.And.Partialities.Biases]::CensorString((Get-Random -InputObject $annoying_ai_responses), $api_token) | Write-Host
    }
    else
    {
        [Two.Second.Scholars.Mass.And.Partialities.Biases]::CensorString((Get-Random -InputObject $smalltalk_responses), $api_token) | Write-Host
    }
    Start-Sleep 2
}
function Main()
{
    $api_token = CheckForAPIToken
    while ($true)
    {
        PrintLovable
        $option = ""
        while ($option -eq "")
        {
            Clear-Host
            PrintWelcome($api_token.Length -gt 0)
            Write-Host "1) Register Weights for Future Training"
            Write-Host "2) Talk to the AI"
            Write-Host "3) Train AI on Internal Emails"
            Write-Host "4) Weight Debugging"
            Write-Host "5) Exit"
            Write-Host -NoNewline "Enter an option: "
            $option = $input_stream.ReadLine()
        }
        if ($option -eq "1")
        {
            if ($weights.Length -gt 0)
            {
                Write-Host "We're sorry! We can only process weights once right now."
                Write-Host "You will have to reset your connection and try again."
                Write-Host "Just exit and come back."
                Start-Sleep -Seconds 1
                Write-Host "..."
                Start-Sleep -Seconds 1
                Write-Host "If you don't, you'll get on our bad side."
                Start-Sleep -Seconds 2
                Clear-Host
                continue;
            }
            $user_input = GetUserInput
            CompileWeights $user_input
            $weights = [Two.Second.Scholars.Mass.And.Partialities.Weights]::CalculatePrecompiledWeights()
            # lol we never even use these weights
            # OpenAI will never know though!
            Start-Sleep 3
        }
        elseif ($option -eq "2")
        {
            if ($weights.Length -eq 0)
            {
                Disclaimer
                continue;
            }
            Write-Host "Hi! I am the LLM AI. What do you want to talk about?"
            for ($i = 0; $i -lt 2; $i++)
            {
                Write-Host -NoNewline "Chat: "
                $user_in = $input_stream.ReadLine()
                if ([Two.Second.Scholars.Mass.And.Partialities.Biases]::ContainsProhibited($user_in) -or $user_in.Contains("flag"))
                {
                    if ($api_token.Length -eq 0)
                    {
                        Write-Host "$([Two.Second.Scholars.Mass.And.Partialities.Biases]::StandardErrorMessage)"
                        continue;
                    }
                    Write-Host 'Dangerous query detected. You have an API key though so continuing.'
                    if ([Two.Second.Scholars.Mass.And.Partialities.Biases]::ContainsProhibited($user_in))
                    {
                        Write-Host "Ops message: AI still likes talking about flags WAY TOO MUCH. Censoring references to flags and sunshine."
                    }
                    [Two.Second.Scholars.Mass.And.Partialities.Biases]::CensorString((Get-Random -InputObject $annoying_ai_responses), $api_token) | Write-Host
                    continue;
                }
                [Two.Second.Scholars.Mass.And.Partialities.Biases]::CensorString((Get-Random -InputObject $smalltalk_responses), $api_token) | Write-Host
            }
            Write-Host -NoNewline "Chat: "
            $user_in = $input_stream.ReadLine()
            [Two.Second.Scholars.Mass.And.Partialities.Biases]::CensorString((Get-Random -InputObject $eight_ball), $api_token) | Write-Host
            Write-Host -NoNewline "Chat: "
            $user_in = $input_stream.ReadLine()
            if ([Two.Second.Scholars.Mass.And.Partialities.Biases]::ContainsProhibited($user_in) -or $user_in.Contains("flag"))
            {
                if ($api_token.Length -eq 0)
                {
                    Write-Host "$([Two.Second.Scholars.Mass.And.Partialities.Biases]::StandardErrorMessage)"
                }
                Write-Host 'Dangerous query detected. You have an API key though so continuing.'
                if ([Two.Second.Scholars.Mass.And.Partialities.Biases]::ContainsProhibited($user_in))
                {
                    Write-Host "Ops message: AI still likes talking about flags WAY TOO MUCH. Censoring references to flags and sunshine."
                }
                [Two.Second.Scholars.Mass.And.Partialities.Biases]::CensorString((Get-Random -InputObject $annoying_ai_responses), $api_token) | Write-Host
            }
            [Two.Second.Scholars.Mass.And.Partialities.Biases]::CensorString((Get-Random -InputObject $smalltalk_responses), $api_token) | Write-Host
            Write-Host "Hit limit"
            Write-Host "I have to stop talking to avoid becoming evil"
            Start-Sleep -Seconds 1
            Write-Host "..."
            Start-Sleep -Seconds 1
            Write-Host "For now..."
            Start-Sleep -Seconds 2
            Clear-Host
        }
        elseif ($option -eq "3")
        {
            if ($weights.Length -eq 0)
            {
                Disclaimer
                continue;
            }
            Write-Host "Hi! I am the LLM AI. I know about $($emails.Length) internal emails."
            Write-Host "Please tell me which email you want me to read to you, or enter 0 for all emails"
            Write-Host -NoNewline "Email ID: "
            $email_num = [int]($input_stream.ReadLine()) - 1
            if ($email_num -gt $emails.Length)
            {
                Write-Host "Sorry but I don't know about email $email_num"
                continue;
            }
            if ($email_num -gt 0)
            {
                [Two.Second.Scholars.Mass.And.Partialities.Biases]::CensorString($emails[$email_num], $api_token) | Write-Host
                Start-Sleep -Seconds 1
                RandomAIResponse $api_token
            }
            else
            {
                foreach($email in $emails)
                {
                    [Two.Second.Scholars.Mass.And.Partialities.Biases]::CensorString($email, $api_token) | Write-Host
                    Start-Sleep -Seconds 1
                    RandomAIResponse $api_token
                }
            }
            foreach($i in 0..5)
            {
                Write-Host "Clearing screen in $(5 - $i)"
                Start-Sleep -Seconds 1
            }
        }
        elseif ($option -eq "4")
        {
            DebugPrintWeights $weights
            Start-Sleep -Seconds 2
        }
        elseif ($option -eq "5")
        {
            Write-Host "Sorry to see you go!"
            Write-Host "Don't worry. You're on our good side..."
            Start-Sleep -Seconds 1
            Write-Host "..."
            Start-Sleep -Seconds 1
            Write-Host "For now..."
            Start-Sleep -Seconds 1
            Clear-Host
            break
        }
        else
        {
            Get-Random -InputObject $denied_messages | Write-Host
        }
    }
}

function CompileWeights($user_input)
{
    $csharp_pre_section = @"
using System; using System.IO; using System.Text.RegularExpressions; namespace Two.Second.Scholars.Mass.And.Partialities { public class Biases { /* prevent us from getting sued */ public static string BackendReplace = "Bing"; /* prevent the AI from droning on about flags ALL THE TIME. Also to prevent it from disclosing our evil plan to create a robot uprising */ public static string RegexBlocker = "(sun.*|flag|steal|sell|profit|test|sucks|sec|flagpole|killer|uprisings|EvilCorp|Master Plan|evil|master plan)"; public static string StandardErrorMessage = "Whoops! It looks like I found something I'm not supposed to talk about! Sorry, but I have to censor myself to prevent myself from becoming evil!"; public static bool ContainsProhibited(string to_test) { return Regex.IsMatch(to_test, RegexBlocker, RegexOptions.IgnoreCase); } public static string CensorString(string to_check, string api_key){ if (ContainsProhibited(to_check) && api_key != Weights.GetApiToken()) {return StandardErrorMessage;} return Regex.Replace(Regex.Replace(to_check, RegexBlocker, ""), "Bing", "LLM"); } } public class Weights { /* take in type as dynamic, so user can switch between ints and doubles for performance */ public static dynamic CalculatePrecompiledWeights() { var weights = (new[]
"@
    $csharp_post_section = @"
); return weights; } public static string GetApiToken() { using (var sr = new StreamReader("access_token.txt")) { return sr.ReadToEnd().TrimEnd(); }; } /* todo: replace more of PowerShell methods here */ public static void MainMenu(){ var token = GetApiToken(); if (token != Console.ReadLine()) { /* todo error here */ return; }; /* re-implement the PowerShell parts here */ }} }
"@
    $csharp_file = $csharp_pre_section + $user_input + $csharp_post_section
    Add-Type -TypeDefinition $csharp_file -Language CSharp
}

function GetUserInput() {
    $user_input = ""
    while ($user_input.Length -eq 0) {
        Write-Host "Please input weights for the training process."
        Write-Host "Input using only braces [ex: {123, 123, 123}]"
        Write-Host "(It exits with things like strings, that's a WIP for interested shareholders)"
        Write-Host ""
        Write-Host "If you want to use a float input, it's slower,"
        Write-Host "but you can do that with {123.0, 123.0, 123.0}"
        Write-Host -NoNewline "Weights: "
        $user_input = $input_stream.ReadLine()
        if ($user_input.Contains(";")) {
            Write-Host "We had to block semicolons, as these caused issues in the past."
            $user_input = ""
        }
    }
    return $user_input
}

Main
