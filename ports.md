Port Assignments
-----

Port assignment convention:

* SunshineCTF challenges: port = `yycnn`
  * `yy` = last 2 digits of competition year, so SunshineCTF 2025 is `25cnn`
  * `c` = category (0 = pwn, 1 = reversing, 2 = scripting, 3 = web, 4 = crypto, 5 = misc, 6 = speedrun/i95, 7 = pegasus)
  * `nn` = challenge index within the category, starting at 01

Archive host: `ctf.hackucf.org`. Raw-TCP challenges are reached with
`nc ctf.hackucf.org <port>`. HTTP(S) web challenges are served on a
per-challenge subdomain `<slug>.ctf.hackucf.org` (nginx terminates TLS and
reverse-proxies to the container bound on `127.0.0.1:<port>`; fragments live in
`nginx/`).

Only challenges with a hosted server-side component are listed below.

| Challenge Name                | Category  | Author             | Directory                          | Host                                      | Port  | Connection |
|:------------------------------|:----------|:-------------------|:-----------------------------------|:------------------------------------------|------:|:-----------|
| Clone Army                    | Pwn       | kcolley            | Pwn/CloneArmy                      | ctf.hackucf.org                           | 25001 | `nc ctf.hackucf.org 25001` |
| SpaceIsMyBanner               | Pwn       | solarbonite        | Pwn/SpaceIsMyBanner               | ctf.hackucf.org                           | 25002 | `nc ctf.hackucf.org 25002` |
| SpaceIsLessThanIdeal          | Pwn       | solarbonite        | Pwn/SpaceIsLessThanIdeal          | ctf.hackucf.org                           | 25003 | `nc ctf.hackucf.org 25003` |
| HeapX                         | Pwn       | Oreomeister        | Pwn/HeapX                         | ctf.hackucf.org                           | 25004 | `nc ctf.hackucf.org 25004` |
| HAL9000                       | Pwn       | Oreomeister        | Pwn/HAL9000                       | ctf.hackucf.org                           | 25005 | `nc ctf.hackucf.org 25005` |
| AstroJIT AI                   | Pwn       | solarbonite        | Pwn/AstroJitAi                    | ctf.hackucf.org                           | 25006 | `nc ctf.hackucf.org 25006` |
| Numbers Game                  | Reversing | ThatOneKMC         | Reversing/NumbersGame             | ctf.hackucf.org                           | 25101 | `nc ctf.hackucf.org 25101` |
| Space Race                    | Reversing | tsuto              | Reversing/SpaceRace               | ctf.hackucf.org                           | 25102 | `nc ctf.hackucf.org 25102` |
| Hail Mary                     | Scripting | tsuto              | Scripting/HailMary                | ctf.hackucf.org                           | 25201 | `nc ctf.hackucf.org 25201` |
| Web Forge                     | Web       | d!!!               | Web/WebForge                      | webforge.ctf.hackucf.org             | 25303 | https://webforge.ctf.hackucf.org |
| Intergalactic Webhook Service | Web       | RJCyber            | Web/Intergalactic_Webhook_Service | webhook.ctf.hackucf.org              | 25304 | https://webhook.ctf.hackucf.org |
| Lunar Auth                    | Web       | alimuhammadsecured | Web/Lunar_Auth                    | lunarauth.ctf.hackucf.org            | 25305 | https://lunarauth.ctf.hackucf.org |
| Lunar Shop                    | Web       | alimuhammadsecured | Web/Lunar_Shop                    | lunarshop.ctf.hackucf.org            | 25306 | https://lunarshop.ctf.hackucf.org |
| Lunar File Invasion           | Web       | alimuhammadsecured | Web/Lunar_File_Invasion           | lunarfileinvasion.ctf.hackucf.org    | 25307 | https://lunarfileinvasion.ctf.hackucf.org |
| BitsOfSpace                   | Crypto    | anthony.js         | Crypto/BitsOfSpace                | ctf.hackucf.org                           | 25401 | `nc ctf.hackucf.org 25401` |
| MoonClicker                   | Crypto    | anthony.js         | Crypto/MoonClicker                | moonclicker.ctf.hackucf.org          | 25402 | https://moonclicker.ctf.hackucf.org |
| Plutonian                     | Crypto    | tsuto              | Crypto/Plutonian                  | ctf.hackucf.org                           | 25403 | `nc ctf.hackucf.org 25403` |
| Miami                         | i95       | Oreomeister        | i95/Miami                         | ctf.hackucf.org                           | 25601 | `nc ctf.hackucf.org 25601` |
| Jacksonville                  | i95       | Oreomeister        | i95/Jacksonville                  | ctf.hackucf.org                           | 25602 | `nc ctf.hackucf.org 25602` |
| Canaveral                     | i95       | Oreomeister        | i95/Canaveral                     | ctf.hackucf.org                           | 25603 | `nc ctf.hackucf.org 25603` |
| Daytona                       | i95       | Oreomeister        | i95/Daytona                       | ctf.hackucf.org                           | 25606 | `nc ctf.hackucf.org 25606` |
| Jupiter                       | i95       | Oreomeister        | i95/Jupiter                       | ctf.hackucf.org                           | 25607 | `nc ctf.hackucf.org 25607` |
| Login Screen                  | Pegasus   | kcolley            | Pegasus/challenges/LoginScreen    | ctf.hackucf.org                           | 25701 | `nc ctf.hackucf.org 25701` |

Notes:
* The Pegasus session multiplexer (`Pegasus/pegsession`, image
  `sunshinectf-2025-pegsession`) listens on port 25700. It is infrastructure for
  the Pegasus challenges rather than a challenge itself, so it is not listed as a
  hosted challenge above.
* Pegasus `AccessCode` and `CanYouHearMe` are download-only challenges (players
  download the `.peg` cartridge and run it locally with `runpeg`); they have no
  hosted component and therefore no port.
