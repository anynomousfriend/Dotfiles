# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import subprocess
import json
import os
from libqtile import hook
from pathlib import Path
from libqtile.widget import backlight
import psutil

# Decor module
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration



# ------------------------------------------------------
# Variable Declarations
#-------------------------------------------------------

app_launcher = "rofi -show drun -disable-history -show-icons"

mod = "mod4"

home = str(Path.home())

terminal = guess_terminal()
#terminal = "kitty"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    #Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod, "shift"], "Return", lazy.spawn("rofi -show drun -show-icons"), desc="Launch Rofi"),
     # Brightness Control
     Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl -q s +10%")),
     Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl -q s 10%-")),

    #    Key([],"XF86MonBrightnessUp",lazy.widget['backlight'].change_backlight(backlight.ChangeDirection.UP)
    #),

    #Key([],"XF86MonBrightnessDown",lazy.widget['backlight'].change_backlight(backlight.ChangeDirection.DOWN)
    # ),

    # System 
    Key([mod, "shift"], "q", lazy.spawn(home + "/.config/qtile/scripts/powermenu.sh"), desc="Open Powermenu"),
    # Key([mod], "Print", lazy.spawn(home + "/.config/qtile/scripts/screenshot.sh")),


    # Volume Control

    Key([], "Print", lazy.spawn("flameshot gui"), desc="Take a screenshot"),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("amixer sset Master 5%-"),
        desc="Lower volume",
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("amixer sset Master 5%+"),
        desc="Raise volume",
    ),
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn("amixer -D default set Master toggle"),
        desc="Mute volume",
    ),


    Key(
        [mod],
        "space",
        lazy.window.toggle_floating(),
        desc="Toggle Floating layout",
    ),

]




# --------------------------------------------------------
# Groups
# --------------------------------------------------------
#groups = [Group(i) for i in ["★", "★", "3★", "4★", "5★"]]
groups = [Group(i) for i in ["󰋜", "", "", "", "󰵮","󰝚", "󰝡",""]]
#groups = [Group(i) for i in ["","","","","","","","","",""]]
#groups = [Group(i) for i in ["零","一","二","三","四","五","六","七","八","九"]]
#groups = [Group(i) for i in "12345"]
group_hotkeys = "123456789"

for i, k in zip(groups, group_hotkeys):
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                k,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                k,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )
# Ends here


# --------------------------------------------------------
# Pywal Colors
# --------------------------------------------------------

colors = os.path.expanduser('~/.cache/wal/colors.json')
colordict = json.load(open(colors))
Color0=(colordict['colors']['color0'])
Color1=(colordict['colors']['color1'])
Color2=(colordict['colors']['color2'])
Color3=(colordict['colors']['color3'])
Color4=(colordict['colors']['color4'])
Color5=(colordict['colors']['color5'])
Color6=(colordict['colors']['color6'])
Color7=(colordict['colors']['color7'])
Color8=(colordict['colors']['color8'])
Color9=(colordict['colors']['color9'])
Color10=(colordict['colors']['color10'])
Color11=(colordict['colors']['color11'])
Color12=(colordict['colors']['color12'])
Color13=(colordict['colors']['color13'])
Color14=(colordict['colors']['color14'])
Color15=(colordict['colors']['color15'])

# --------------------------------------------------------
# Setup Layout Theme
# --------------------------------------------------------

layout_theme = { 
    "border_width": 2,
    "margin": 5,
    "border_focus": Color1,
    "border_normal": "FFFFFF",
    "single_border_width": 2
}

layout_themes = {
    "border_width": 3,
    "margin": 0,
    "border_focus": Color1,
    "border_normal": "FFFFFF",
}


# ------------------------------------------------------
# PowerLineDecoration
#-------------------------------------------------------


arrow_powerlineRight = {
    "decorations": [
        PowerLineDecoration(
            path="arrow_right",
            size=11,
        )
    ]
}
arrow_powerlineLeft = {
    "decorations": [
        PowerLineDecoration(
            path="arrow_left",
            size=11,
        )
    ]
}
rounded_powerlineRight = {
    "decorations": [
        PowerLineDecoration(
            path="rounded_right",
            size=11,
        )
    ]
}
rounded_powerlineLeft = {
    "decorations": [
        PowerLineDecoration(
            path="rouded_left",
            size=11,
        )
    ]
}
slash_powerlineRight = {
    "decorations": [
        PowerLineDecoration(
            path="forward_slash",
            size=11,
        )
    ]
}
slash_powerlineLeft = {
    "decorations": [
        PowerLineDecoration(
            path="back_slash",
            size=11,
        )
    ]
}



# ------------------------------------------------------
# Layout Configurations
#-------------------------------------------------------

layouts = [
    layout.Columns(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(),
    # **Floating Rules Down in the code.
]



widget_defaults = dict(
    font="JetBrainsMono Nerd Font Mono",
    fontsize=15,
    padding=5,
)
extension_defaults = widget_defaults.copy()


# ------------------------------------------------------
# Mouse Callbacks
#-------------------------------------------------------



# ------------------------------------------------------
# Bar Configuration
#-------------------------------------------------------
    
screens = [
    Screen(
        top=bar.Bar(
            [

                widget.GroupBox(
                    fontsize=23,
                    padding_x=3,
                    padding_y=5,
                    rounded=False,
                    center_aligned=True,
                    disable_drag=True,
                    borderwidth=3,
                    highlight_method="line",
                    active=Color1,
                    inactive=Color7,
                    highlight_color=Color6,
                    this_current_screen_border=Color4,
                    this_screen_border=Color0,
                    other_screen_border=Color11,
                    other_current_screen_border=Color6,
                    background=Color4,
                    foreground=Color3,
                    **arrow_powerlineLeft,
                ),

                 widget.Prompt(
                     prompt="run: ",
                     ignore_dups_history=True,
                 ),
                 widget.WindowName(
                    for_current_screen=True,
                    padding=18,
                    foreground=Color7,
                    background=Color3,
                ),

                widget.Spacer(
                    length=1,
                    background=Color3,
                    **rounded_powerlineRight,
                ),
                widget.CPU(
                    padding=5,
                    format="  {freq_current}GHz {load_percent}%",
                    foreground=Color7,
                    background=Color1,
                    **slash_powerlineRight,
                ),
                widget.Memory(
                    padding=5,
                    format="󰈀 {MemUsed:.0f}{mm}",
                    background=Color2,
                    foreground=Color7,
                    **slash_powerlineRight,
                ),

                widget.Clock(
                    padding=5,
                    foreground=Color7,
                    background=Color4,
                    format='  %a %d %b %I:%M %p ',
                    **slash_powerlineRight,
                ),
                
                widget.Battery(
                    padding=5,
                    full_char="󱊣",
                    not_charging_char="󰂃 Shit!",
                    charge_char= "󰂄 +",
                    discharge_char="󰁿 -",
                    empty_char="󰂎 dying!",
                    format= '{char} {percent:2.0%} {hour:d}:{min:02d} ',
                    foreground=Color7,
                    background=Color3,
                    **slash_powerlineRight,
                ),

                widget.Volume(
                    fmt="󰕾 {}",
                    foreground=Color7,
                    background=Color5,
                    padding=10,
                    **slash_powerlineRight,
                ),
                widget.Systray(
                    padding=7,
                    icon_size=15,
                ),


                widget.CurrentLayout(
                    padding=5,
                    foreground=Color0,
                    background=Color6,
                ),
                # widget.CurrentLayoutIcon(
                #scale=0.65,
                #padding=8,    
                #background=Color1
                #),
            ],
            30,
        ),
    )
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False

# ------------------------------------------------------
# **Floating Rules
#-------------------------------------------------------

floating_layout = layout.Floating(
    border_width=2,
    border_focus=Color1,
    border_normal=Color7,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="confirm"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(wm_class="pavucontrol"),
        Match(wm_class="dialog"),
        Match(wm_class="error"),
        Match(wm_class="file_progress"),
        Match(wm_class="notification"),
        Match(wm_class="splash"),
        Match(wm_class="toolbar"),
        Match(wm_class="download"),
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ],
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('/home/subhankar/.config/qtile/autostart.sh')
    subprocess.Popen([home])

@hook.subscribe.group_window_add
def switchtogroup(group, window):
    group.cmd_toscreen()
