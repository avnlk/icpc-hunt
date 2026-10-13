#!/usr/bin/env python3
"""
Click wherever the mouse pointer currently is, once per second. Move the pointer yourself.

    python3 autoclick.py                 # click every 1 s until you press Ctrl+C
    python3 autoclick.py --count 50      # stop after 50 clicks
    python3 autoclick.py --interval 2    # change the gap (seconds)
    python3 autoclick.py --button right  # left (default), right or middle

It waits 3 seconds before starting so you can put the pointer where you want it.
Stop at any time with Ctrl+C in this terminal.

Backends (first one found is used):
  * ydotool  -> works on Wayland. Needs the daemon and uinput access:
        sudo apt install ydotool
        sudo usermod -aG input $USER        # then log out and back in
        (start the daemon:  ydotoold &   or  systemctl --user enable --now ydotool)
  * xdotool  -> works only for apps running under X11/XWayland:
        sudo apt install xdotool
"""
import argparse, shutil, subprocess, sys, time

p = argparse.ArgumentParser()
p.add_argument("--interval", type=float, default=1.0, help="seconds between clicks (default 1)")
p.add_argument("--count", type=int, default=0, help="stop after N clicks (default: until Ctrl+C)")
p.add_argument("--button", choices=["left", "middle", "right"], default="left")
p.add_argument("--delay", type=float, default=3.0, help="seconds to wait before the first click")
a = p.parse_args()

# ydotool button codes: 0xC0 = left click, 0xC1 = right click, 0xC2 = middle click
YD = {"left": "0xC0", "right": "0xC1", "middle": "0xC2"}
XD = {"left": "1", "middle": "2", "right": "3"}

if shutil.which("ydotool"):
    cmd = ["ydotool", "click", YD[a.button]]
    backend = "ydotool"
elif shutil.which("xdotool"):
    cmd = ["xdotool", "click", XD[a.button]]
    backend = "xdotool"
else:
    sys.exit("No click tool found. Install one:  sudo apt install ydotool   (Wayland)  or  sudo apt install xdotool")

print(f"Using {backend}. Starting in {a.delay:g}s; clicking every {a.interval:g}s. Ctrl+C to stop.", flush=True)
time.sleep(a.delay)
n = 0
try:
    while not a.count or n < a.count:
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit(f"{backend} failed: {r.stderr.strip() or r.stdout.strip() or r.returncode}")
        n += 1
        print(f"\rclicks: {n}", end="", flush=True)
        time.sleep(a.interval)
except KeyboardInterrupt:
    pass
print(f"\nStopped after {n} clicks.")
