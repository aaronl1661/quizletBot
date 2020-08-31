import py_compile as py
import subprocess
import os
key = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()

with open('bot.py', 'r') as f: # 'r' is a reading mode
    text = f.read()

if text.find("key = '") == -1:
    print('key not found')

    # with open("config.py", "a") as f:
    #     keystring = "key = " + "'" + key + "'"
    #     f.write(keystring)
    with open("bot.py",'r') as f:
        with open('newfile.txt','w') as f2: 
            keystring = "key = " + "'" + key + "'"
            f2.write(keystring + "\n")
            f2.write(f.read())
    os.system('del bot.py')
    os.rename('newfile.txt', 'bot.py')
py.compile('bot.py')
# os.system('attrib +s +h +r config.py')
# os.system('del /f .\setup.py')
# os.system('del /f .\bot.py')
os.system('README.txt')
exit()


