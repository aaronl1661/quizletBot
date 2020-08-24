import py_compile as py
import subprocess

current_machine_id = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
key = '4C4C4544-0058-4410-8054-B7C04F375631'
py.compile('bot.py')