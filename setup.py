import urllib.request
import os
import pexpect
import pxpowershell
import subprocess
import threading
import time

directory = os.path.dirname(os.path.realpath(__file__))

change_directory = f"cd \"{directory}\""

# ps = pxpowershell.pxpowershell()

# ps.start_process()



# ps.run(change_directory)

run_question_tester = 'uvicorn question_tester:app --reload'

# pexpect.run(f"{change_directory}; {run_question_tester}")




def thread_function():
    subprocess.call(f"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe \"{change_directory};{run_question_tester}\"", shell=True)

print('it got here')

thread = threading.Thread(target=thread_function)
thread.start()

# ps.run(run_question_tester)

time.sleep(8)

url = f'http://127.0.0.1:8000'

x = urllib.request.urlopen(url)

# print(ps.run('ls'))

# os.system(change_directory)

# return_code = os.system('ls')

# print(return_code)