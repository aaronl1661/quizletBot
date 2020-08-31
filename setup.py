import py_compile as py
import subprocess
import os
key = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()

with open('config.py', 'r') as f: # 'r' is a reading mode
    text = f.read()

if text.find("key = '") == -1:
    print('key not found')

    with open("config.py", "a") as f:
        keystring = "key = " + "'" + key + "'"
        f.write(keystring)
py.compile('config.py')
os.system('attrib +s +h +r config.py')
os.system('del /f .\setup.py')
