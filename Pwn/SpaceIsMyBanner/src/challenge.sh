#!/bin/sh
trap 'exit 1' SIGINT
    export NEWT_COLORS='
border=black,green
'

if whiptail --title "Security Prompt" --scrolltext --yes-button "I will not hack" --no-button "I am hacker" --yesno "You are accessing a Sunshine CTF Secret Satellite (SCSS) Access Point (AP) that is provided for Non-Hacker-authorized use only.
By using this AP (which includes any device attached to this AP), you consent to the following conditions:
-SCSS routinely intercepts and monitors communications on this AP for purposes including, but not limited to, penetration testing, and network operations and defense.
-At any time, the SCSS may inspect and seize data stored on this AP.
-Communications using, or data stored on, this AP are not private, are subject to routine monitoring, interception, and search, and may be disclosed or used for any SCSS-authorized purpose.
-This AP includes security measures (e.g., authentication and access controls) to protect SCSS interests--not for your personal benefit or privacy.

I've read & consent to terms in AP user agreement. I will not hack this system." 20 78; then
    tmux source-file /etc/secure-tmux.conf
    export NEWT_COLORS='
border=black,red
'

    whiptail --title "Note to potential Hackers" \
        --msgbox "User has agreed to not hack the system.
Hacking has now been DISABLED! If you were a hacker, you cannot hack NOW.
It was different BEFORE, but NOW you cannot hack this system." 14 78

    while true; do
        USER_RESULT=$(whiptail --title "Satellite Control System" \
            --menu "Select a control system to access" 20 78 8 \
            "Access Logs" "Read logs on the system securely." \
            "Turn Spy Pictures On" "High security change. Requires token to work" \
            "Turn Spy Pictures Off" "High security change. Requires token to work" \
            "Sweet Tmux Configs" "Check out my sweet tmux config files!" \
            "/sbin/nologin" "Access /bin/nologin" \
            "Access Video Logs" "Recommended videos" \
            "Whoami" "Sensitive Who-Am-I information" \
            "Exit" "Exit" \
            3>&1 1>&2 2>&3)

        case "$USER_RESULT" in
            "Access Logs")
                echo "Displaying system access logs..."
                whiptail --title "System Access Logs" --scrolltext --textbox /app/system_logs.txt 20 78
                ;;
            "Turn Spy Pictures On"|"Turn Spy Pictures Off")
                echo "Checking token status..."
                PASSWORD=$(whiptail --passwordbox "Token entry: " 8 78 --title "${USER_RESULT} Token Request" 3>&1 1>&2 2>&3)
                whiptail --title "Disabled Feature" --msgbox "This feature is disabled on production environments." 8 78
                ;;
            "Access Video Logs")
                echo "Loading video logs..."
                whiptail --title "Video Logs" \
                    --menu "Recommended Videos" 20 78 3 \
                    "Tabs vs Spaces" "https://youtu.be/oRva7UxGQDw" \
                    "Hacking TMux" "https://youtu.be/qbWqXKN3m3c" \
                    "Tmux is UNHACKABLE" "https://youtu.be/vtB1J_zCv8I"
                ;;
            "Sweet Tmux Configs")
                DESIRED_CONFIG=$(whiptail --title "Check out my sweet tmux config files!" \
                    --menu "TMux Configs" 20 78 3 \
                    "Hacking TMUX" "TMux to jail hackers" \
                    "Default TMUX" "Default TMux instance" \
                    "Secure Satellite TMUX" "Tmux for secure satellites" \
                3>&1 1>&2 2>&3)
                case "$DESIRED_CONFIG" in
                    "Secure Satellite TMUX")
                        whiptail --title "Secure Satellite TMUX" --scrolltext --textbox /etc/secure-tmux.conf 20 78
                        ;;
                    "Hacking TMUX")
                        whiptail --title "Hacking TMUX" --scrolltext --textbox /etc/hacking-tmux.conf 20 78
                        ;;
                    "Default TMUX")
                        whiptail --title "Default TMUX" --scrolltext --textbox /etc/tmux.conf 20 78
                        ;;
                    *)
                        whiptail --title "Aw man!" --msgbox "Aw man! I wanted to show off my amazing tmux config files!" 8 78
                        ;;
                esac
                ;;
            "/sbin/nologin")
                # soooooo it's not really possible to run /sbin/nologin as it requires CTRL+C to cancel
                whiptail --title "/sbin/nologin" --msgbox "This account is not available" 8 78
                whiptail --title "/sbin/nologin note" --msgbox "What exactly were you thinking? Its... in the title." 8 78
                ;;
            "Whoami")
                whiptail --title "Who-Am-I today?" --msgbox "Today, I am $(/usr/bin/id). This probably is not useful to you." 8 78
                ;;
            "Exit" | *)
                whiptail --title "Exiting" --msgbox "Exiting..." 8 78
                exit
                ;;
        esac
    done
else
    tmux source-file /etc/hacking-tmux.conf
    export NEWT_COLORS='
border=black,yellow
'
    whiptail --title "Hacker" --msgbox "User identified as HACKER. Access DENIED!" 8 78
fi