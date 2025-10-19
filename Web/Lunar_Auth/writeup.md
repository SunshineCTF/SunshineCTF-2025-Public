# Lunar Code Invasion 2025

- upon going to ```/robots.txt``` you'll notice the following entry:
```
# tired of these annoying search engine bots scraping the admin panel page logins:

Disallow: /admin
```

- if we go to ```/admin``` we see this in the `source` of inspect element:
```javascript
[TRUNCATED]
    /*
    To reduce load on our servers from the recent space DDOS-ers we have lowered login attempts by using Base64 encoded encryption
    ("encryption" 💀) on the client side.
    
    TODO: implement proper encryption.
    */
    const real_username = atob("YWxpbXVoYW1tYWRzZWN1cmVk");
    const real_passwd   = atob("UzNjdXI0X1BAJCR3MFJEIQ==");

    document.addEventListener("DOMContentLoaded", () => {
        const form = document.querySelector("form");
[TRUNCATED]
```

- Now we base64 decode these and login to get the flag.
