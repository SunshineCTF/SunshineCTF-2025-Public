#!/bin/sh
trap 'exit 1' SIGINT

while true; do
    USER_RESULT=$(whiptail --title "Satellite Control System" \
        --menu "Select a control system to access" 20 78 10 \
        "Access Logs" "Read logs on the system." \
        "Turn Satellite On" "High security change. Requires token to work" \
        "Turn Satellite Off" "High security change. Requires token to work" \
        "Debug Shell Access" "High security change. Requires token to work" \
        "Access Video Logs" "Recommended videos" \
        "Debug TTY Info" "Loaded TTY" \
        "Exit" "Exit" \
        3>&1 1>&2 2>&3)

    case "$USER_RESULT" in
        "Access Logs")
            echo "Displaying system access logs..."
            SHELL=/sbin/nologin less -r "-PSystem Access Logs (q to quit)" system_logs.txt
            ;;
        "Turn Satellite On"|"Turn Satellite Off"|"Debug Shell Access")
            echo "Checking token status..."
            PASSWORD=$(whiptail --passwordbox "Token entry: " 8 78 --title "${USER_RESULT} Token Request" 3>&1 1>&2 2>&3)
            whiptail --title "Disabled Feature" --msgbox "This feature is disabled on production environments." 8 78
            ;;
        "Access Video Logs")
            echo "Loading video logs..."
            whiptail --title "Video Logs" \
                --menu "Recommended Videos" 20 78 10 \
                "Space Roll" "https://youtu.be/u7xOva-RhSE" \
                "Hacking Shells" "https://youtu.be/K7Hn1rPQouU" \
                "Hacking Vim" "https://youtu.be/WmvZzkXHOeE"
            ;;
        "Debug TTY Info")
            echo "Loading Debug TTY info..."
            whiptail --title "Debug TTY Info" \
                --msgbox "$(tty)" --scrolltext 16 78
            ;;
        "Exit" | *)
            whiptail --title "Exiting" --msgbox "Exiting..." 8 78
            exit
            ;;
    esac
done