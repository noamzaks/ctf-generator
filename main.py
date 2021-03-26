from json import loads
import os
import sys

QUIET = " >/dev/null 2>&1" if sys.platform != "win32" else " >NUL 2>&1"

source = "."
if len(sys.argv) == 2:
    source = sys.argv[1]

levels = os.listdir(source)

first = 0

if f"L{first}" not in levels:
    print("Error: couldn't find the first level L0")
    exit(-1)

last = first
while f"L{last+1}" in levels:
    last += 1

levels = range(last + 1)

passwords = loads(open(os.path.join(source, "passwords.txt"), "r").read())

assert len(passwords) == len(levels)

print("Mode 1: An encrypted individual ZIP for each level")
print("Mode 2: An encrypted ZIP for each level inside the previous encrypted ZIP")
mode = int(input("Please pick a mode: "))

if mode == 1:
    for level in levels:
        if len(os.listdir(f"L{level}")) == 0:
            print(f"Warning: Not generating ZIP for level {level} because it is empty")
            continue
        os.system(f"zip -P {passwords[level]} L{level}.zip L{level}/*" + QUIET)
    print("Successfully created all ZIP archives")
elif mode == 2:
    os.system(f"zip -P {passwords[last]} L{last}.zip L{last}/*" + QUIET)
    # Invert and skip the last element
    for level in levels[-2::-1]:
        os.system(
            f"zip -P {passwords[level]} L{level}.zip L{level}/* L{level + 1}.zip"
            + QUIET
        )
        os.remove(f"L{level + 1}.zip")
    print("Successfully created L0.zip")
else:
    print("Invalid mode")
    exit(-1)
