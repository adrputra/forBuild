import subprocess
import sys

print("Installing libraries depedencies...")
subprocess.run(['pip', 'install', '-r', './requirements.txt'])