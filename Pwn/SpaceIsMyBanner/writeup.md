# Space is my Banner
This challenge is a "breakout" of tmux.

Tmux grants access to new shells by default, so breaking out is simple if the keys to access tmux aren't unbound.

## Writeup
1. For this one, the users will first go into the spy-satellite screen... which has disabled access to tmux's config menu by unbinding all keys
2. Then, combing through the screens, there seems to be a lot of stuff referencing tmux. Including a 100s tutorial and the actual tmux config files used
3. Once users figure out that the "secure" instance unbinds all keys `unbind-keys -a` and the other instances don't, it's as simple as re-logging into the system and not hitting "I will not hack the system".
4. Then, users can "break out" with:
    1) `CTRL+b Shift+:` (go to tmux global configuration)
    2) `set -g default-shell /bin/sh` (switch the default shell to `/bin/sh`)
    3) `CTRL+b Shift+"` (open a new pane split with the old pane)
    4) `./cat-flag` (cat the flag)
    5) Which prints `sun{wait-wait-wait-you-cannot-hack-me-you-agreed-to-not-do-that-that-is-not-fair}`