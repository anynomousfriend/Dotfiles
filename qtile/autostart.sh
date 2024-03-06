#!/bin/sh

xinput set-prop 9 "libinput Tapping Enabled" 1
xinput set-prop 9 "libinput Natural Scrolling Enabled" 1

#/home/subhankar/.local/bin/newlook &
~/.local/bin/newlook &

picom &
dunst &

